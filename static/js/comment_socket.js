document.addEventListener('DOMContentLoaded', () => {
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const hostname = window.location.hostname;
    const port = window.location.port ? `:${window.location.port}` : '';
    const baseUrl = `${protocol}://${hostname}${port}`;
    let activeSocket = null;
    let activePostId = null;
    let commentPages = {};

    function initializeComments() {
        const commentButtons = document.querySelectorAll('.comment-btn');
        
        commentButtons.forEach((btn) => {
            btn.removeEventListener('click', btn._openModalHandler);
            const postId = btn.getAttribute('data-modal-toggle').replace('modal-', '');
            btn._openModalHandler = () => {
                const modal = document.getElementById(`modal-${postId}`);
                if (modal) {
                    modal.classList.remove('hidden');
                    if (activeSocket && activePostId !== postId) {
                        activeSocket.close();
                        activeSocket = null;
                    }
                    activePostId = postId;
                    connectWebSocket(postId);
                    if (!commentPages[postId]) commentPages[postId] = 1;
                    document.getElementById(`parent-${postId}`).value = '';
                }
            };
            btn.addEventListener('click', btn._openModalHandler);
        });

        // Close modals
        const closeButtons = document.querySelectorAll('.close-comment-modal');
        closeButtons.forEach((btn) => {
            btn.removeEventListener('click', btn._closeModalHandler);
            const postId = btn.getAttribute('data-modal-toggle').replace('modal-', '');
            btn._closeModalHandler = () => {
                const modal = document.getElementById(`modal-${postId}`);
                if (modal) {
                    modal.classList.add('hidden');
                    if (activeSocket && activePostId === postId) {
                        activeSocket.close();
                        activeSocket = null;
                        activePostId = null;
                    }
                }
            };
            btn.addEventListener('click', btn._closeModalHandler);
        });

        // Send top-level comments
        const sendButtons = document.querySelectorAll('.send-comment-btn');
        sendButtons.forEach((btn) => {
            btn.removeEventListener('click', btn._sendCommentHandler);
            const postId = btn.getAttribute('onclick').match(/'([^']+)'/)[1];
            btn._sendCommentHandler = () => sendComment(postId);
            btn.addEventListener('click', btn._sendCommentHandler);
        });

        // Reply buttons and forms
        initializeReplyButtons();
    }

    function connectWebSocket(postId) {
        if (activeSocket && activeSocket.readyState === WebSocket.OPEN && activePostId === postId) {
            return;
        }
        if (activeSocket) {
            activeSocket.close();
            activeSocket = null;
        }
        activeSocket = new WebSocket(`${baseUrl}/ws/post/comments/${postId}/`);
        const commentList = document.getElementById(`comments-${postId}`);

        // activeSocket.onopen = () => {
        // };

        activeSocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const level = data.parent ? getCommentLevel(data.parent, commentList) + 1 : 0;
            const parentUsername = data.parent ? getParentUsername(data.parent, commentList) : null;
            const commentHtml = `
            <li class="ml-${level * 4}" data-comment-id="${data.id}">
                <div class="flex justify-between items-start">
                <div class="flex">
                    <img src="${data.avatar}" alt="${data.sender}" class="w-8 h-8 rounded-full mr-2">
                    <div>
                    <p class="font-semibold">${data.sender}</p>
                    ${data.parent ? `<p class="text-xs text-gray-500">${window.replyTo} ${parentUsername}</p>` : ''}
                    <p class="text-gray-700 dark:text-gray-300">${data.comment}</p>
                    <div class="mt-1">
                        <button class="text-blue-500 text-xs hover:underline" onclick="showReplyForm(${data.id})">${window.reply}</button>
                    </div>
                    <div id="reply-form-${data.id}" class="hidden mt-2">
                        <textarea rows="1" class="w-full text-sm border rounded px-1 dark:bg-gray-800 dark:text-white" placeholder="Write a reply..."></textarea>
                        <div class="text-right mt-1">
                        <button class="reply-btn text-xs text-white bg-blue-600 px-2 py-1 rounded" onclick="sendReply('${postId}', ${data.id})">Post</button>
                        </div>
                    </div>
                    </div>
                </div>
                <span class="text-xs text-gray-400">${formatTimeSince(data.timestamp)}</span>
                </div>
                <ul class="space-y-2 mt-2"></ul>
            </li>
            `;
            const topLevelUl = commentList.querySelector('ul');
            if (!data.parent) {
                // New top-level comment: insert at the top
                topLevelUl.insertAdjacentHTML('afterbegin', commentHtml);
                commentList.scrollTop = 0; // Scroll to top for new top-level comments
            } else {
                // Reply: insert under the parent comment
                const parentLi = commentList.querySelector(`[data-comment-id="${data.parent}"]`);
                if (parentLi) {
                    let parentUl = parentLi.querySelector(':scope > ul');
                    if (!parentUl) {
                        // console.warn(`Parent ${data.parent} has no <ul>, creating one`);
                        parentLi.insertAdjacentHTML('beforeend', '<ul class="space-y-2 mt-2"></ul>');
                        parentUl = parentLi.querySelector(':scope > ul');
                    }
                    parentUl.insertAdjacentHTML('afterbegin', commentHtml);
                } else {
                    // console.warn(`Parent comment ${data.parent} not found, appending to top-level`);
                    topLevelUl.insertAdjacentHTML('afterbegin', commentHtml);
                }
            }
            initializeReplyButtons();
        };

        activeSocket.onclose = () => {
            // console.log('WebSocket closed for post:', postId);
        };

        activeSocket.onerror = (error) => {
            // console.error('WebSocket error for post:', postId, error);
        };
    }

    function getParentUsername(parentId, commentList) {
        const parentElement = commentList.querySelector(`[data-comment-id="${parentId}"]`);
        return parentElement ? parentElement.querySelector('.font-semibold').textContent : 'Unknown';
    }

    function getCommentLevel(parentId, commentList) {
        const parentElement = commentList.querySelector(`[data-comment-id="${parentId}"]`);
        if (!parentElement) return 0;
        const classList = parentElement.className.split(' ');
        const mlClass = classList.find(cls => cls.startsWith('ml-'));
        return mlClass ? parseInt(mlClass.replace('ml-', '')) / 4 : 0;
    }

    function formatTimeSince(timestamp) {
        const now = new Date();
        const commentTime = new Date(timestamp);
        const diffMs = now - commentTime;
        const diffMins = Math.round(diffMs / 60000);
        if (diffMins < 1) return 'just now';
        if (diffMins < 60) return `${diffMins}m ago`;
        const diffHours = Math.round(diffMins / 60);
        if (diffHours < 24) return `${diffHours}h ago`;
        return `${Math.round(diffHours / 24)}d ago`;
    }

    function showReplyForm(commentId) {
        const form = document.getElementById(`reply-form-${commentId}`);
        if (form) {
            form.classList.toggle('hidden');
            const textarea = form.querySelector('textarea');
            if (!form.classList.contains('hidden')) textarea.focus();
        }
    }

    function initializeReplyButtons() {
        const replyButtons = document.querySelectorAll('.reply-btn');
        replyButtons.forEach((btn) => {
            btn.removeEventListener('click', btn._handler);
            const onclick = btn.getAttribute('onclick');
            if (onclick) {
                const [postId, parentId] = onclick.match(/'([^']+)',\s*(\d+)/).slice(1);
                btn._handler = () => sendReply(postId, parentId);
                btn.addEventListener('click', btn._handler);
            }
        });
    }

    function sendComment(postId) {
        const input = document.getElementById(`comment-${postId}`);
        const parentInput = document.getElementById(`parent-${postId}`);
        const content = input.value.trim();
        const parentId = parentInput.value || null;
        if (content && activeSocket && activeSocket.readyState === WebSocket.OPEN && activePostId === postId) {
            activeSocket.send(JSON.stringify({
                comment: content,
                parent: parentId,
            }));
            input.value = '';
            parentInput.value = '';
        } else {
            console.warn('Cannot send comment: WebSocket not open, content empty, or wrong post');
        }
    }

    function sendReply(postId, parentId) {
        const form = document.getElementById(`reply-form-${parentId}`);
        const input = form.querySelector('textarea');
        const content = input.value.trim();
        if (content && activeSocket && activeSocket.readyState === WebSocket.OPEN && activePostId === postId) {
            activeSocket.send(JSON.stringify({
                comment: content,
                parent: parentId,
            }));
            input.value = '';
            form.classList.add('hidden');
        } else {
            console.warn('Cannot send reply: WebSocket not open, content empty, or wrong post');
        }
    }

    // open modal if open from notification
    const params = new URLSearchParams(window.location.search);
    const post_id = window.location.pathname.split('/').pop();
  
    const modal = document.getElementById('modal-' + post_id);
    
    if (params.get('openModal') === 'true') {
      if (modal) {
        modal.classList.remove('hidden');
        activePostId = post_id;
        if (activeSocket) {
          activeSocket.close();
          activeSocket = null;
        }
        connectWebSocket(post_id);
      }
    }
  
    document.querySelectorAll('.close-comment-modal').forEach((btn) => {
      btn.addEventListener('click', () => {
        modal.classList.add('hidden');
      });
    });

    // async function loadMoreComments(postId) {
    //     commentPages[postId] = (commentPages[postId] || 1) + 1;
    //     const baseUrls = window.location.hostname
    //     const url = `${baseUrls}/web/post/${postId}/comment/?page=${commentPages[postId]}`;
    //     try {
    //         const response = await fetch(url, {
    //             headers: {
    //                 'X-Requested-With': 'XMLHttpRequest',
    //                 'X-CSRFToken': csrfToken,
    //             },
    //         });
    //         if (!response.ok) throw new Error('Failed to load more comments');
    //         const data = await response.json();
    //         const commentList = document.getElementById(`comments-${postId}`).querySelector('ul');
    //         commentList.insertAdjacentHTML('beforeend', data.html); // Older comments at bottom
    //         if (!data.has_next) {
    //             document.querySelector(`.load-more-comments[data-post-id="${postId}"]`).style.display = 'none';
    //         }
    //         initializeReplyButtons();
    //     } catch (error) {
    //         console.error('Error loading more comments:', error);
    //     }
    // }

    // Expose globally
    window.initializeComments = initializeComments;
    window.sendComment = sendComment;
    window.sendReply = sendReply;
    // window.loadMoreComments = loadMoreComments;
    window.showReplyForm = showReplyForm;

    // Initial setup
    initializeComments();
});
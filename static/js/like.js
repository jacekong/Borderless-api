
document.addEventListener('DOMContentLoaded', () => {
    // Initialize like buttons with event delegation
    function initializeLikeButtons() {
        // Remove existing listeners to prevent duplicates
        document.body.removeEventListener('click', handleLikeButtonClick);
        document.body.removeEventListener('click', handlePublicPostLikeButtonClick);

        // Add new listeners
        document.body.addEventListener('click', handleLikeButtonClick);
        document.body.addEventListener('click', handlePublicPostLikeButtonClick);
    }

    // Handler for .like-button
    function handleLikeButtonClick(e) {
        const button = e.target.closest('.like-button');
        if (!button) return;

        e.preventDefault();
        const postId = button.getAttribute('data-post-id');
        const url = `/web/post/${postId}/like/`;
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken,
            },
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(errorData => {
                        throw new Error(errorData.message || `Server error: ${response.status}`);
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    const svg = button.querySelector('svg');
                    let textNode = null;
                    for (let node of button.childNodes) {
                        if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
                            textNode = node;
                            break;
                        }
                    }

                    // Toggle button text and color
                    if (data.action === 'liked') {
                        if (textNode) textNode.textContent = 'Unlike';
                        button.classList.remove('text-gray-500', 'hover:text-blue-600');
                        button.classList.add('text-red-500', 'hover:text-blue-700');
                        if (svg) svg.classList.add('fill-current', 'text-red-500');
                    } else {
                        if (textNode) textNode.textContent = 'Like';
                        button.classList.remove('text-red-500', 'hover:text-blue-700');
                        button.classList.add('text-gray-500', 'hover:text-blue-600');
                        if (svg) svg.classList.remove('fill-current', 'text-red-500');
                    }

                    // Update like count
                    const likeCount = button.parentElement.querySelector('.like-count');
                    if (likeCount) {
                        likeCount.textContent = `${data.like_count} likes`;
                    }
                    // Trigger notification poll (assuming this is defined elsewhere)
                    if (typeof pollNotifications === 'function') pollNotifications();
                }
            })
            .catch(error => {
                console.error('Error:', error.message);
            });
    }

    // Handler for .public-post-like-button
    function handlePublicPostLikeButtonClick(e) {
        const button = e.target.closest('.public-post-like-button');
        if (!button) return;

        e.preventDefault();
        const postId = button.getAttribute('data-post-id');
        const url = `/web/post/${postId}/like/`;
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken,
            },
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(errorData => {
                        throw new Error(errorData.message || `Server error: ${response.status}`);
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    let textNode = null;
                    for (let node of button.childNodes) {
                        if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
                            textNode = node;
                            break;
                        }
                    }

                    // Toggle button text and color
                    if (data.action === 'liked') {
                        if (textNode) textNode.textContent = 'Unlike';
                        button.classList.remove('text-gray-500', 'hover:text-blue-600');
                        button.classList.add('text-blue-600', 'hover:text-blue-700', 'bg-gray-600');
                    } else {
                        if (textNode) textNode.textContent = 'Like';
                        button.classList.remove('text-blue-600', 'hover:text-blue-700', 'bg-gray-600');
                        button.classList.add('text-gray-500', 'hover:text-blue-600');
                    }

                    // Update like count
                    const likeCount = button.parentElement.querySelector('.like-count');
                    if (likeCount) {
                        likeCount.textContent = `${data.like_count} likes`;
                    }
                    // Trigger notification poll (assuming this is defined elsewhere)
                    if (typeof pollNotifications === 'function') pollNotifications();
                }
            })
            .catch(error => {
                console.error('Error:', error.message);
            });
    }

    // Expose initialization function globally for post.js
    window.initializeLikeButtons = initializeLikeButtons;

    // Initial setup
    initializeLikeButtons();
});
import Toast from './toast.js';
import { initializeFriendRequestForms } from './friend_request.js';

document.addEventListener('DOMContentLoaded', () => {
    // State for media uploads
    let selectedVideo = null;
    const selectedFiles = new Map();
    let currentPage = 1;
    const players = [];

    // Construct base URL
    const protocol = window.location.protocol;
    const hostname = window.location.hostname;
    const port = window.location.port ? `:${window.location.port}` : '';
    const baseUrl = `${protocol}//${hostname}${port}`;

    // DOM Elements
    const getElements = () => ({
        emojiButton: document.querySelector('.emoji-picker-button'),
        emojiPickerBtn: document.querySelector('.emoji-picker-btn'),
        emojiPicker: document.querySelector('emoji-picker'),
        textarea: document.querySelector('#editor'),
        videoBtn: document.querySelector('#video-upload'),
        videoInput: document.getElementById('video-upload-input'),
        imageUploadBtn: document.getElementById('image-upload'),
        imageInput: document.getElementById('images-post'),
        createPostForm: document.querySelector('form#create-post-form'),
        postDeleteBtn: document.querySelector('.post-delete-btn'),
        deletePostForm: document.querySelector('form#delete-post'),
        postContainer: document.getElementById('posts-container'),
        loadMoreBtn: document.getElementById('load-more'),
        progressBar: document.getElementById('upload-progress'),
        progressFill: document.getElementById('progress-fill'),
        progressText: document.getElementById('progress-text'),
    });

    // Emoji Picker
    function setupEmojiPicker(elements) {
        if (!elements.emojiButton) return;

        elements.emojiButton.addEventListener('click', () => {
            elements.emojiPickerBtn.classList.remove('hidden');
            elements.emojiPickerBtn.classList.add('emoji-picker-show', 'z-99', 'fixed', 'top-60');
        });

        elements.emojiPickerBtn.addEventListener('mouseleave', () => {
            elements.emojiPickerBtn.classList.add('hidden');
        });

        elements.emojiPicker.addEventListener('emoji-click', (ev) => {
            elements.textarea.value += ev.detail.unicode;
        });

        elements.textarea.addEventListener('click', () => {
            elements.emojiPickerBtn.classList.remove('emoji-picker-show');
            elements.emojiPickerBtn.classList.add('hidden');
        });
    }

    // Video Upload
    function setupVideoUpload(elements) {
        if (!elements.videoBtn || !elements.videoInput) return;

        elements.videoBtn.addEventListener('click', () => elements.videoInput.click());

        elements.videoInput.addEventListener('change', () => {
            const file = elements.videoInput.files[0];
            if (!file || !file.type.startsWith('video/')) {
                alert('Please select a video file');
                elements.videoInput.value = '';
                return;
            }

            selectedVideo = file;
            if (selectedVideo) {
                elements.imageUploadBtn.setAttribute('disabled', 'true');
                elements.videoBtn.setAttribute('disabled', 'true');
            }

            const existingPreview = document.getElementById('video-preview');
            if (existingPreview) existingPreview.remove();

            const previewContainer = document.createElement('div');
            previewContainer.id = 'video-preview';
            document.querySelector('.post-creation').appendChild(previewContainer);

            const fileId = URL.createObjectURL(file);
            const videoWrapper = createMediaPreview(fileId, 'video', () => {
                selectedVideo = null;
                elements.videoInput.value = '';
                elements.imageUploadBtn.removeAttribute('disabled');
                elements.videoBtn.removeAttribute('disabled');
            });

            previewContainer.appendChild(videoWrapper);
        });
    }

    // Image Upload
    function setupImageUpload(elements) {
        if (!elements.imageUploadBtn) return;

        elements.imageUploadBtn.addEventListener('click', () => elements.imageInput.click());

        elements.imageInput.addEventListener('change', (event) => {
            const files = Array.from(event.target.files);
            if (files.length > 9) {
                Toast.show('You can only upload a maximum of 9 images.', 'error', 7000);
                return;
            }

            const existingPreview = document.getElementById('image-previews');
            if (existingPreview) existingPreview.remove();

            const previewContainer = document.createElement('div');
            previewContainer.id = 'image-previews';
            previewContainer.classList.add('mt-1', 'grid', 'grid-cols-4', 'gap-4');
            document.querySelector('.post-creation').appendChild(previewContainer);

            elements.videoBtn.setAttribute('disabled', 'true');

            files.forEach((file) => {
                const fileId = URL.createObjectURL(file);
                selectedFiles.set(fileId, file);

                const reader = new FileReader();
                reader.onload = (e) => {
                    const imgWrapper = createMediaPreview(fileId, 'image', () => {
                        selectedFiles.delete(fileId);
                        if (selectedFiles.size === 0) {
                            elements.videoBtn.removeAttribute('disabled');
                        }
                    }, e.target.result);
                    previewContainer.appendChild(imgWrapper);
                };
                reader.readAsDataURL(file);
            });
        });
    }

    // Helper: Create media preview (video or image)
    function createMediaPreview(fileId, type, onDelete, src = null) {
        const wrapper = document.createElement('div');
        wrapper.classList.add('relative', type === 'image' ? 'w-20' : 'w-[300px]', type === 'image' ? 'md:w-32' : 'h-[200px]');

        const media = type === 'image' ? document.createElement('img') : document.createElement('video');
        media.src = src || fileId;
        media.classList.add('w-full', 'h-full', 'object-cover', 'rounded-lg');
        if (type === 'video') media.controls = true;

        const deleteBtn = document.createElement('button');
        deleteBtn.innerHTML = '×';
        deleteBtn.classList.add('absolute', 'top-1', 'right-1', 'bg-red-500', 'text-white', 'rounded-full', 'w-6', 'h-6', 'flex', 'items-center', 'justify-center');
        deleteBtn.setAttribute('data-file-id', fileId);

        deleteBtn.addEventListener('click', (e) => {
            e.preventDefault();
            wrapper.remove();
            onDelete();
        });

        wrapper.appendChild(media);
        wrapper.appendChild(deleteBtn);
        return wrapper;
    }

    // Poll video processing status
    function pollVideoStatus(videoId) {
        const interval = setInterval(() => {
            fetch(`/video/${videoId}/`)
                .then((response) => response.json())
                .then((data) => {
                    if (data.video_url) {
                        clearInterval(interval);
                        playVideo(data.video_url);
                    } else {
                        console.log('Video still processing...');
                    }
                })
                .catch((error) => console.error('Error polling:', error));
        }, 5000);
    }

    // Play HLS video with Video.js
    function playVideo(videoUrl) {
        const videoElement = document.createElement('video');
        videoElement.id = `video-${Date.now()}`; // Unique ID
        videoElement.className = 'video-js';
        videoElement.setAttribute('controls', '');
        videoElement.setAttribute('preload', 'auto');
        videoElement.setAttribute('width', '640');
        videoElement.setAttribute('height', '360');

        const sourceElement = document.createElement('source');
        sourceElement.src = videoUrl;
        sourceElement.type = 'application/x-mpegURL';

        videoElement.appendChild(sourceElement);
        document.querySelector('.post-creation').appendChild(videoElement);

        videojs(videoElement, {}, function () {
            this.play();
        });
    }

    function setupCreatePostForm(elements) {
        if (!elements.createPostForm) return;

        elements.createPostForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value

            const isPublic = elements.createPostForm.querySelector('#is_public_post').checked ? '1' : '0';
            const content = elements.textarea.value;
            const formData = new FormData();
            formData.append('post_content', content);
            formData.append('is_public', isPublic);
            if (selectedVideo) formData.append('post_video', selectedVideo);
            selectedFiles.forEach((file) => formData.append('post_images', file));

            const xhr = new XMLHttpRequest();
            elements.progressBar.classList.remove('hidden');
            elements.progressText.textContent = 'Uploading: 0%';

            xhr.upload.addEventListener('progress', (event) => {
                if (event.lengthComputable) {
                    const percent = Math.round((event.loaded / event.total) * 100);
                    // elements.progressBar.value = percent;
                    elements.progressFill.style.width = `${percent}%`;
                    elements.progressText.textContent = `Uploading: ${percent}%`;
                    if (percent % 25 === 0) Toast.info(`Upload progress: ${percent}%`);
                }
            });

            xhr.addEventListener('load', () => {
                if (xhr.status === 201) {
                    const response = JSON.parse(xhr.responseText);

                    if (response.success) {
                        Toast.success(response.success);
                        elements.progressBar.value = 100;
                        elements.progressText.textContent = 'Upload complete!';
                        elements.createPostForm.reset();
                        elements.textarea.value = '';
                        selectedVideo = null;
                        selectedFiles.clear();
                        elements.imageUploadBtn.removeAttribute('disabled');
                        elements.videoBtn.removeAttribute('disabled');
                        document.getElementById('image-previews')?.remove();
                        document.getElementById('video-preview')?.remove();
                    } else {
                        Toast.error(response.message || 'Upload failed');
                    }
                } else {
                    Toast.error('Server error during upload');
                }
                setTimeout(() => {
                    elements.progressBar.classList.add('hidden');
                    elements.progressText.textContent = '';
                    window.location.replace('/');
                }, 2000);
            });

            xhr.addEventListener('error', () => {
                Toast.error('Network error during upload');
                elements.progressBar.classList.add('hidden');
                elements.progressText.textContent = '';
            });

            xhr.open('POST', `${baseUrl}/api/posts`, true);
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
            xhr.send(formData);
        });
    }

    // Delete Post
    function initializeDeletePost(elements) {
        if (!elements.postDeleteBtn || !elements.deletePostForm) return;

        elements.deletePostForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            if (!window.confirm('Are you sure you want to delete this post?')) return;

            const postId = elements.postDeleteBtn.getAttribute('data-post-id');
            const url = `${window.location.origin}/api/posts/${postId}`;
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

            try {
                const response = await fetch(url, {
                    method: 'DELETE',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrfToken,
                    },
                });
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.message || `Server error: ${response.status}`);
                }
                Toast.message('Successfully deleted post');
                setTimeout(() => window.location.replace('/web/account/'), 1000);
            } catch (error) {
                console.error('Error:', error.message);
            }
        });
    }

    // Video Rendering
    function initializeVideoPlayers() {
        document.querySelectorAll('.video-js').forEach((videoElement) => {
            const player = videojs(videoElement, {
                fluid: true,
                plugins: { hlsQualitySelector: { displayCurrentQuality: true } },
            }, () => player.hlsQualitySelector());

            const MAX_HEIGHT = 1080;
            player.ready(() => {
                player.el().style.maxHeight = `${MAX_HEIGHT}px`;
                player.el().style.width = '100%';
            });

            players.push(player);
            player.on('play', () => {
                players.forEach((otherPlayer) => {
                    if (otherPlayer !== player && !otherPlayer.paused()) otherPlayer.pause();
                });
            });
        });

        const checkViewport = () => {
            players.forEach((player) => {
                const rect = player.el().getBoundingClientRect();
                const isVisible = rect.top >= 0 && rect.bottom <= (window.innerHeight || document.documentElement.clientHeight);
                if (!isVisible && !player.paused()) player.pause();
            });
        };

        window.addEventListener('scroll', checkViewport);
        window.addEventListener('resize', checkViewport);
        checkViewport();
    }

    // Load Posts
    async function loadPosts(page = 1) {
        const elements = getElements();
        if (!elements.postContainer) return;

        try {
            const response = await fetch(`/?page=${page}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                },
            });
            if (!response.ok) throw new Error('Failed to load posts');
            const data = await response.json();

            if (page === 1) {
                elements.postContainer.innerHTML = data.html;
            } else {
                elements.postContainer.insertAdjacentHTML('beforeend', data.html);
            }

            currentPage = parseInt(data.page);
            if (elements.loadMoreBtn) {
                elements.loadMoreBtn.style.display = data.has_next ? 'block' : 'none';
            }

            // Reinitialize like buttons and video players
            if (window.initializeLikeButtons) window.initializeLikeButtons();
            if (window.initializeComments) window.initializeComments();
            initializeVideoPlayers();
            initializeFriendRequestForms();
        } catch (error) {
            console.log(error);

            Toast.error('Something went wrong!');
        }
    }

    // Initialization
    function initializeCreatePost() {
        const elements = getElements();
        setupEmojiPicker(elements);
        setupVideoUpload(elements);
        setupImageUpload(elements);
        setupCreatePostForm(elements);
        initializeDeletePost(elements);
        if (elements.loadMoreBtn) {
            elements.loadMoreBtn.addEventListener('click', () => loadPosts(currentPage + 1));
        }
        initializeVideoPlayers();
    }

    // Expose functions globally
    window.loadMore = () => loadPosts(currentPage + 1);
    window.initializeVideoPlayers = initializeVideoPlayers;
    window.initializeCreatePost = initializeCreatePost;

    // Initial setup
    initializeCreatePost();
    if (window.location.pathname === '/' && document.getElementById('post-container')) {
        loadPosts();
    }
});
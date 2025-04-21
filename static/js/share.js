import Toast from './toast.js';

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const elements = {
    template: document.getElementById('share-template'),
    shareBtn: document.getElementById('shareBtn'),
    modal: document.getElementById('sharePreviewModal'),
    previewImage: document.getElementById('sharePreviewImage'),
    downloadBtn: document.getElementById('downloadShareBtn'),
  };

  // Generate share image
  async function generateShareImage(post, postId, avatarUrl, username) {
    const clone = elements.template.cloneNode(true);
    clone.classList.remove('hidden');
    document.body.appendChild(clone);

    try {
      // Populate template
      clone.querySelector('#share-post-content').textContent = post;
      clone.querySelector('#share-user-avatar').src = avatarUrl || '/static/images/default-avatar.png';
      clone.querySelector('#share-username').textContent = username || 'Anonymous';

      // Generate image
      const date = new Date();
      const canvas = await html2canvas(clone, { scale: 2 });
      const dataUrl = canvas.toDataURL('image/png');
      const blob = await (await fetch(dataUrl)).blob();
      const file = new File([blob], `post-${date.getTime()}.png`, { type: 'image/png' });

      // Show preview
      elements.previewImage.src = dataUrl;
      elements.modal.classList.remove('hidden');

      // Set up download button
      elements.downloadBtn.onclick = () => {
        const link = document.createElement('a');
        link.href = dataUrl;
        link.download = `post-${date.getTime()}.png`;
        link.click();
      };

      // Store file for sharing
      window.currentShareFile = file;
    } catch (error) {
      Toast.error(`Failed to generate share image: ${error.message}`);
    } finally {
      document.body.removeChild(clone);
    }
  }

  // Share via Web Share API
  async function shareContent() {
    if (!window.currentShareFile) {
      Toast.error('No shareable content available.');
      return;
    }

    const shareData = {
      files: [window.currentShareFile],
      title: 'Check out this post!',
      text: 'Borderless Share',
      url: window.location.href,
    };

    if (navigator.share && navigator.canShare && navigator.canShare({ files: [window.currentShareFile] })) {
      try {
        await navigator.share(shareData);
        Toast.success('Shared successfully!');
      } catch (error) {
        Toast.error(`Sharing failed: ${error.message}`);
      }
    } else {
      alert('Sharing not supported on this device.');
    }
  }

  // Close preview modal
  function closeSharePreviewModal() {
    elements.modal.classList.add('hidden');
    window.currentShareFile = null;
  }

  // Initialize event listeners
  function initialize() {
    window.generateShareImage = generateShareImage;
    window.closeSharePreviewModal = closeSharePreviewModal;

    if (elements.shareBtn) {
      elements.shareBtn.onclick = shareContent;
    }
  }

  initialize();
});
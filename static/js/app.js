
// page route detection
function pageRouteDetection() {
  let route_path = window.location.pathname;
  let home_container = document.getElementById('home_container');

  if (route_path === '/account/') {
    
    home_container.classList.remove('sm:grid-cols-[7rem_1fr]');
    
    home_container.classList.add('sm:grid-cols-[16rem_1fr]');
    
  }
}
pageRouteDetection();

function openModal(postId) {
  // Find the post element by ID
  const postElement = document.querySelector(`.post[data-post-id="${postId}"]`);
  if (!postElement) return;

  // Extract post data
  const postAvatar = postElement.querySelector('.comment-avatar').src;
  const postContent = postElement.querySelector('.comment-content').innerText;

  // Populate modal with post data
  document.getElementById('author-avatar').src = postAvatar;
  document.getElementById('post-content').innerText = `Comments on ${postContent}`;

  // Extract comments
  const comments = postElement.querySelectorAll('.post-comments .comment');
  const commentsList = document.getElementById('comments-list');
  commentsList.innerHTML = '';
  comments.forEach(comment => {
    const commentAvatar = comment.querySelector('.comment-avatar').src;
    const commentUsername = comment.querySelector('.comment-username').innerText;
    const commentTimestamp = comment.querySelector('.comment-timestamp').innerText;
    const commentContent = comment.querySelector('.comment-content').innerText;

    commentsList.innerHTML += `
      <li class="w-full mb-1">
        <a href="#" class="items-center p-3 flex hover:bg-gray-100 dark:hover:bg-gray-700 hover:rounded-e-lg">
          <img class="w-10 h-10 mb-3 me-3 rounded-full sm:mb-0" src="${commentAvatar}" alt=""/>
          <div>
            <div class="text-base font-normal text-gray-600 dark:text-gray-400"><span class="font-medium text-gray-900 dark:text-white">${commentUsername}</span></div>
            <span class="text-xs text-gray-500">${commentTimestamp}</span>
          </div>
        </a>
        <div class="ml-3">
          <p class="text-black dark:text-white">${commentContent}</p>
        </div>
        <hr class="bg-gray-600 mx-5">
      </li>
    `;
  });

  // Show the modal
  document.getElementById('select-modal').classList.remove('hidden');
}

// Event listener to close the modal
document.querySelector('[data-modal-toggle="select-modal"]').addEventListener('click', function() {
  document.getElementById('select-modal').classList.add('hidden');
});
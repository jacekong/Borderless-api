import Toast from './toast.js';


document.addEventListener("DOMContentLoaded", function() {
  let currentPage = 1;

  const loadMoreBtn = document.getElementById('load-more-posts');
  const container = document.getElementById('profile-post-container');

  let mybutton = document.getElementById("topBtn");

  // When the user scrolls down 20px from the top of the document, show the button
  window.onscroll = function() {scrollFunction()};

  async function loadMorePosts(page = 1) {
      if (!container) return;

      try {
          const response = await fetch(`/web/account/?page=${page}`, {
              headers: {
                  'X-Requested-With': 'XMLHttpRequest',
                  'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                  'X-Current-Path': '/web/account/',
              },
          });
          if (!response.ok) throw new Error('Failed to load posts');
          const data = await response.json();
          console.log(data.page);
          
          if (page === 1) {
            container.innerHTML = data.html;
          } else {
            container.insertAdjacentHTML('beforeend', data.html);
          }

          currentPage = parseInt(data.page);
          if (loadMoreBtn) {
              loadMoreBtn.style.display = data.has_next ? 'block' : 'none';
          }
      } catch (error) {
          console.log(error);

          Toast.error('Something went wrong!');
      }
  }
  
  function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
      mybutton.style.display = "block";
    } else {
      mybutton.style.display = "none";
    }
  }
  
  // When the user clicks on the button, scroll to the top of the document
  function goTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
  }

    window.loadMoreAccountPosts = () => loadMorePosts(currentPage + 1);
    window.goTop = () => goTop();

});
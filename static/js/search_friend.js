document.addEventListener("DOMContentLoaded", () => {
    const protocol = window.location.protocol;
  const hostname = window.location.hostname;
  const port = window.location.port ? `:${window.location.port}` : '';
  const baseUrl = `${protocol}//${hostname}${port}`;
  const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value || '';
  
    window.initializeSearchFriends = function () {
        const form = document.getElementById('search-friend-form');
        const resultsContainer = document.getElementById('search-results');
    
        if (!form || !resultsContainer) {
          return;
        }
    
        form.addEventListener('submit', async (e) => {
          e.preventDefault();
          const query = form.querySelector('#search-friends').value;
          const url = `${baseUrl}/web/search/frined/query/?query=${encodeURIComponent(query)}`;
    
          try {
            const response = await fetch(url, {
              headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken,
              },
            });
    
            if (!response.ok) {
              const text = await response.text();
              throw new Error(`Server returned ${response.status}: ${text}`);
            }
    
            const data = await response.json();
            resultsContainer.innerHTML = data.html;
          } catch (error) {
            console.error('Error searching friends:', error.message);
          }
        });
      };
});
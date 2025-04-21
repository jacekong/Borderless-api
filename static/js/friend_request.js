import Toast, {pollNotifications}  from './toast.js';

const toast = new Toast();

function initializeFriendRequestForms() {
  // Find all forms with an ID starting with 'friend-request-form-'
  document
    .querySelectorAll('form[id^="friend-request-form-"]')
    .forEach((form) => {
      form.classList.add('initialized');
      
      form.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        const url = this.action;
        const csrfToken = formData.get("csrfmiddlewaretoken");
        fetch(url, {
          method: "POST",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrfToken,
          },
          body: formData,
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                  toast.error(errorData.message || `Server error`);
                }).catch(() => {
                  toast.error(`Server error`);
                });
            }
            // If OK, parse the JSON success response
            return response.json();
        })
        .then(data => {
            const button = form.querySelector('button');
            button.textContent = window.requestSent;
            button.disabled = true;
            button.classList.add('cursor-not-allowed');
            pollNotifications();
        })
        .catch(error => {
            toast.error('An unexpected error occurred');
            pollNotifications();
        });
      });
    });
}

// Initialize forms on page load
document.addEventListener("DOMContentLoaded", () => {
  initializeFriendRequestForms();
});

export { initializeFriendRequestForms };

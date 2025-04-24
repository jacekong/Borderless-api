export default class Toast {
  static show(message, type = 'info', duration = 7000, notificationId = null, sender = null) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.classList.add('toast', type);

    // Apply custom gradient for friend_request
    if (type === 'friend_request') {
      toast.classList.add('bg-gradient-to-r', 'from-cyan-500', 'to-blue-500');
    } else if (type === 'like') {
      toast.classList.add('bg-gradient-to-r', 'from-red-500', 'to-pink-500');
    } else if (type === 'comment') {
      toast.classList.add('bg-gradient-to-r', 'from-cyan-500', 'to-blue-500');
    }

    const icon = document.createElement('span');
    icon.classList.add('toast-icon');
    icon.innerHTML = Toast.getIcon(type);
    toast.appendChild(icon);

    // Sender avatar (if present)
    if (sender && sender.avatar) {
      const avatar = document.createElement('img');
      avatar.classList.add('w-6', 'h-6', 'rounded-full', 'mr-2');
      avatar.src = sender.avatar;
      avatar.alt = `${sender.username}'s avatar`;
      toast.appendChild(avatar);
    }

    const messageSpan = document.createElement('span');
    messageSpan.classList.add('toast-message');
    messageSpan.textContent = sender ? `${sender.username} ${message}` : message;
    toast.appendChild(messageSpan);

    const closeButton = document.createElement('button');
    closeButton.classList.add('toast-close');
    closeButton.innerHTML = '×';
    closeButton.onclick = () => {
      toast.classList.remove('show');
      setTimeout(() => container.removeChild(toast), 300);
    };
    toast.appendChild(closeButton);

    container.appendChild(toast);
    setTimeout(() => toast.classList.add('show'), 100);

    const timeoutId = setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => {
        if (container.contains(toast)) container.removeChild(toast);
        // if (notificationId) markAsRead(notificationId);
      }, 300);
    }, duration);

    closeButton.dataset.timeoutId = timeoutId;
    closeButton.addEventListener('click', () => clearTimeout(timeoutId));
  }

  static getIcon(type) {
    switch (type) {
      case 'success': return '✔';
      case 'error': return '✖';
      case 'info': return 'ℹ';
      case 'message': return '✉';
      case 'friend_request': return '👤';
      case 'like': return '❤️';
      case 'comment': return '💬';
      default: return 'ℹ';
    }
  }

  static success(message, notificationId = null, sender = null) { this.show(message, 'success', 7000, notificationId, sender); }
  static error(message, notificationId = null, sender = null) { this.show(message, 'error', 7000, notificationId, sender); }
  static info(message, notificationId = null, sender = null) { this.show(message, 'info', 7000, notificationId, sender); }
  static message(message, notificationId = null, sender = null) { this.show(message, 'message', 7000, notificationId, sender); }
  static friendRequest(message, notificationId = null, sender = null) { this.show(message, 'friend_request', 7000, notificationId, sender); }
  static like(message, notificationId = null, sender = null) { this.show(message, 'like', 7000, notificationId, sender); }
  static comment(message, notificationId = null, sender = null) { this.show(message, 'comment', 7000, notificationId, sender)}
}

// notification list
function populateDropdown(notifications) {
  const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  const list = document.getElementById('notificationList');
  list.innerHTML = '';

  if (notifications.length === 0) {
    list.innerHTML = '<div class="px-4 py-3 text-gray-500 dark:text-gray-400">No notifications</div>';
    return;
  }

  notifications.forEach(notif => {
    const item = document.createElement('a');
    if (notif.related_link) {
      item.setAttribute('href', `${notif.related_link}?openModal=true`);
    } else {
      item.href = '#';
    }
    item.classList.add('flex', 'px-4', 'py-3', 'hover:bg-gray-100', 'dark:hover:bg-gray-700');

    const iconDiv = document.createElement('div');
    iconDiv.classList.add('shrink-0', 'relative');
    const img = document.createElement('img');
    img.classList.add('rounded-full', 'w-11', 'h-11');
    img.src = notif.sender ? notif.sender.avatar : '/static/icons/borderless.png';
    img.alt = notif.sender ? `${notif.sender.username}'s avatar` : 'User image';
    const typeIconDiv = document.createElement('div');
    typeIconDiv.classList.add('absolute', 'flex', 'items-center', 'justify-center', 'w-3', 'h-3', 'ms-6', 'bottom-0', 'border', 'border-white', 'rounded-full', 'dark:border-gray-800');
    typeIconDiv.style.backgroundColor = getIconColor(notif.type);
    const typeIcon = document.createElement('svg');
    typeIcon.classList.add('w-1', 'h-1', 'text-white');
    typeIcon.setAttribute('aria-hidden', 'true');
    typeIcon.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    typeIcon.setAttribute('fill', 'currentColor');
    typeIcon.innerHTML = getSvgPath(notif.type);
    typeIconDiv.appendChild(typeIcon);
    iconDiv.appendChild(img);
    iconDiv.appendChild(typeIconDiv);
    item.appendChild(iconDiv);

    const contentDiv = document.createElement('div');
    contentDiv.classList.add('w-full', 'ps-3');
    const message = document.createElement('div');
    message.classList.add('text-gray-500', 'text-sm', 'mb-1.5', 'dark:text-gray-400', 'break-all', 'whitespace-normal');
    message.textContent = notif.sender ? `${notif.sender.username} ${notif.message}` : notif.message;
    const time = document.createElement('div');
    time.classList.add('text-xs', 'text-blue-600', 'dark:text-blue-500');
    time.textContent = timeAgo(new Date(notif.created_at));

    if (notif.type === 'friend_request') {
      const acceptButton = document.createElement('button');
      acceptButton.classList.add('bg-green-500', 'text-white', 'px-2', 'py-1', 'rounded', 'text-xs', 'mr-2');
      acceptButton.textContent = 'Accept';
      acceptButton.onclick = () => {
        fetch(`/web/accept/${notif.sender.user_id}/request/`, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
          }
        })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            pollNotifications();
            markAsRead(notif.id, csrftoken);
          } else {
            Toast.error(data.error)
          }
        })
        .catch(error => Toast.error(error.message));
      };
      contentDiv.appendChild(acceptButton);

      const declineButton = document.createElement('button');
      declineButton.classList.add('bg-red-500', 'text-white', 'px-2', 'py-1', 'rounded', 'text-xs');
      declineButton.textContent = 'Decline';
      declineButton.onclick = () => {
        fetch(`/notifications/${notif.id}/decline/`, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
          },
        }).then(() => pollNotifications());
      };
      contentDiv.appendChild(declineButton);
    }

    contentDiv.appendChild(message);
    contentDiv.appendChild(time);
    item.appendChild(contentDiv);

    list.appendChild(item);
  });

  const badge = document.getElementById('notificationBadge');
  const unreadCount = notifications.filter(n => !n.is_read).length;
  badge.classList.toggle('hidden', unreadCount === 0);
}

function getIconColor(type) {
  switch (type) {
    case 'success': return '#28a745';
    case 'error': return '#dc3545';
    case 'info': return '#17a2b8';
    case 'message': return '#6c757d';
    case 'friend_request': return '#007bff';
    case 'comment': return '#17a2b8';
    default: return '#6c757d';
  }
}

function getSvgPath(type) {
  switch (type) {
    case 'success': return '<path d="M18 0H2a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h2v4a1 1 0 0 0 1.707.707L10.414 13H18a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2Zm-5 4h2a1 1 0 1 1 0 2h-2a1 1 0 1 1 0-2ZM5 4h5a1 1 0 1 1 0 2H5a1 1 0 1 1 0-2Zm2 5H5a1 1 0 1 1 0-2h2a1 1 0 1 1 0 2Zm9 0h-6a1 1 0 1 1 0-2h6a1 1 0 1 1 0 2Z" />';
    case 'error': return '<path d="M17.947 2.053a5.209 5.209 0 0 0-3.793-1.53A6.414 6.414 0 0 0 10 2.311 6.482 6.482 0 0 0 5.824.5a5.2 5.2 0 0 0-3.8 1.521c-1.915 1.916-2.315 5.392.625 8.333l7 7a.5.5 0 0 0 .708 0l7-7a6.6 6.6 0 0 0 2.123-4.508 5.179 5.179 0 0 0-1.533-3.793Z" />';
    case 'info': return '<path d="M6.5 9a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9ZM8 10H5a5.006 5.006 0 0 0-5 5v2a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-2a5.006 5.006 0 0 0-5-5Zm11-3h-2V5a1 1 0 0 0-2 0v2h-2a1 1 0 1 0 0 2h2v2a1 1 0 0 0 2 0V9h2a1 1 0 1 0 0-2Z" />';
    case 'message': return '<path d="M18 0H2a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h2v4a1 1 0 0 0 1.707.707L10.414 13H18a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2Zm-5 4h2a1 1 0 1 1 0 2h-2a1 1 0 1 1 0-2ZM5 4h5a1 1 0 1 1 0 2H5a1 1 0 1 1 0-2Zm2 5H5a1 1 0 1 1 0-2h2a1 1 0 1 1 0 2Zm9 0h-6a1 1 0 1 1 0-2h6a1 1 0 1 1 0 2Z" />';
    case 'friend_request': return '<path d="M6.5 9a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9ZM8 10H5a5.006 5.006 0 0 0-5 5v2a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-2a5.006 5.006 0 0 0-5-5Zm11-3h-2V5a1 1 0 0 0-2 0v2h-2a1 1 0 1 0 0 2h2v2a1 1 0 0 0 2 0V9h2a1 1 0 1 0 0-2Z" />';
    default: return '<path d="M6.5 9a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9ZM8 10H5a5.006 5.006 0 0 0-5 5v2a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-2a5.006 5.006 0 0 0-5-5Zm11-3h-2V5a1 1 0 0 0-2 0v2h-2a1 1 0 1 0 0 2h2v2a1 1 0 0 0 2 0V9h2a1 1 0 1 0 0-2Z" />';
  }
}

function timeAgo(date) {
  const now = new Date();
  const seconds = Math.floor((now - date) / 1000);
  if (seconds < 60) return `${seconds} seconds ago`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
  return `${Math.floor(hours / 24)} day${hours > 24 ? 's' : ''} ago`;
}

export function pollNotifications() {
  fetch('/notifications/', {
    headers: { 'X-Requested-With': 'XMLHttpRequest' },
  })
    .then(response => response.json())
    .then(data => {
      data.toast_notifications.forEach(notif => {
        if (notif.type === 'friend_request') {
          Toast.friendRequest(notif.message, notif.id, notif.sender);
        } else if (notif.type === 'like') {
          Toast.like(notif.message, notif.id, notif.sender);
        } else if (notif.type === 'comment') {
          Toast.comment(notif.message, notif.id, notif.sender);
        } else {
          Toast[notif.type](notif.message, notif.id, notif.sender);
        }
      });
      populateDropdown(data.dropdown_notifications);
    })
    .catch(error => console.error('Error fetching notifications:', error));
}

function markAsRead(notificationId, csrftoken) {
  
  fetch(`/notifications/${notificationId}/read/`, {
    method: 'POST',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': csrftoken,
    },
  })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        console.log(`Notification ${notificationId} marked as read`);
        pollNotifications();
      }
    })
    .catch(error => console.error('Error marking notification as read:', error));
}

setInterval(pollNotifications, 10000);
pollNotifications();
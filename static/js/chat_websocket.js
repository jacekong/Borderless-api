let chatSocket = null;
let activeChatUserId = null;
let chatBackBtn = null;

// function loadChatList() {
//   // Construct the base URL dynamically
//   const protocol = window.location.protocol;
//   const hostname = window.location.hostname;
//   const port = window.location.port ? `:${window.location.port}` : '';
//   const baseUrl = `${protocol}//${hostname}${port}`;
//   fetch('/web/chat/page/', {
//     headers: {
//       'X-Requested-With': 'XMLHttpRequest',
//     },
//   })
//     .then(response => {
//       if (!response.ok) throw new Error('Failed to load chat list');
//       return response.json();
//     })
//     .then(data => {
//       document.getElementById('content-container').innerHTML = data.html;
//       document.getElementById('message-btn').classList.add('bg-gray-100', 'dark:bg-gray-700');
//       setupMessageInput();
//       window.history.pushState({ url:`${baseUrl}/web/chat/page/`}, '', '/web/chat/page/')
//     })
//     .catch(error => console.error('Error loading chat list:', error));
// }

// Open caht when tap on user's avatar
function openChat(userId, username, avatarUrl) {
  // Construct the base URL dynamically
  const protocol = window.location.protocol;
  const hostname = window.location.hostname;
  const port = window.location.port ? `:${window.location.port}` : '';
  const baseUrl = `${protocol}//${hostname}${port}`;
  
  // Fetch the chat content via AJAX
  const url = `${baseUrl}/web/chat/user/${userId}/`;
  // Remove active class from all user items
  const userItems = document.querySelectorAll('.user-item');
  userItems.forEach(item => item.classList.remove('active'));

  // Add active class to the clicked user
  const clickedItem = document.querySelector(`.user-item[data-user-id="${userId}"]`);
  if (clickedItem) {
    clickedItem.classList.add('active');
  }
  
  // Handle mobile view
  if (window.innerWidth < 768) {

    fetch(url, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
      },
    })
    .then(response => {
      if (!response.ok) throw new Error('Failed to load conten!');
      return response.json();
    })
    .then(data => {
      document.getElementById('content-container').innerHTML = data.html;
      // push state to change browser history
      showChatPage(userId, username, avatarUrl);

      const chatBackBtn = document.getElementById('chat-back-button');
      if (chatBackBtn) {
        chatBackBtn.addEventListener('click', (e) => {
          e.preventDefault();
          window.history.back();
        });
      }

      window.history.pushState({}, "", `${window.location.origin}/web/chat/user/${userId}/`);
    })
    .catch(error => console.error('Error loading chat list:', error));
  }

  if (!document.getElementById('chat-area')) {
    fetch('/web/chat/page/', {
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
      },
    })
      .then(response => {
        if (!response.ok) throw new Error('Failed to load chat list');
        return response.json();
      })
      .then(data => {
        document.getElementById('content-container').innerHTML = data.html;
        document.getElementById('message-btn').classList.add('bg-gray-100', 'dark:bg-gray-700');
        showChatArea(userId, username);
        window.history.pushState({}, '', '/web/chat/page/')
      })
      .catch(error => console.error('Error loading chat list:', error));
  } else {
    showChatArea(userId, username);
  }
}

// mobile 
// Open caht when tap on user's avatar
function openMobileChat(userId, username, avatarUrl) {
  // Construct the base URL dynamically
  const protocol = window.location.protocol;
  const hostname = window.location.hostname;
  const port = window.location.port ? `:${window.location.port}` : '';
  const baseUrl = `${protocol}//${hostname}${port}`;
  
  // Fetch the chat content via AJAX
  const url = `${baseUrl}/web/chat/user/${userId}/`;
  // Remove active class from all user items
  const userItems = document.querySelectorAll('.user-item');
  userItems.forEach(item => item.classList.remove('active'));

  // Add active class to the clicked user
  const clickedItem = document.querySelector(`.user-item[data-user-id="${userId}"]`);
  if (clickedItem) {
    clickedItem.classList.add('active');
  }
  
  // Handle mobile view
  if (window.innerWidth < 768) {

    fetch(url, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
      },
    })
    .then(response => {
      if (!response.ok) throw new Error('Failed to load conten!');
      return response.json();
    })
    .then(data => {
      document.getElementById('content-container').innerHTML = data.html;
      // push state to change browser history
      showChatPage(userId, username, avatarUrl);

      const chatBackBtn = document.getElementById('chat-back-button');
      if (chatBackBtn) {
        chatBackBtn.addEventListener('click', (e) => {
          e.preventDefault();
          window.history.back();
        });
      }

      window.history.pushState({}, "", `${window.location.origin}/web/chat/user/${userId}/`);
    })
    .catch(error => console.error('Error loading chat list:', error));
  }
  
}

function showChatArea(userId, username) {
  if (chatSocket) chatSocket.close();
  chatSocket = null;
  
  activeChatUserId = userId;
  document.getElementById('chat-area').classList.remove('hidden');
  document.getElementById('chat-header').classList.remove('hidden');
  document.getElementById('chat-input').classList.remove('hidden');
  document.getElementById('chat-username').textContent = username;
  document.getElementById('chat-avatar').src = document.querySelector(`[data-user-id="${userId}"] img`)?.src || '/media/avatars/avatar.jpg';
  const messagesDiv = document.getElementById('chat-messages');
  messagesDiv.innerHTML = '';

  fetch(`/api/chat/history/${userId}/`, {
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
    },
  })
    .then(response => {
      if (!response.ok) throw new Error('Failed to load chat history');
      return response.json();
    })
    .then(history => {
      history.forEach(msg => {
        const isSender = msg.sender.user_id === currentUserId;
        const messageHtml = `
          <div class="flex flex-col ${isSender ? 'items-end' : 'items-start'}">
            <div class="text-2xs text-gray-400 mb-1 ${isSender ? 'text-right' : 'text-left'}">${new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true }).toUpperCase()}</div>
            <div class="${isSender ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-200'} text-sm px-4 py-2 rounded-xl max-w-[75%]">
              <p>${msg.message}</p>
            </div>
          </div>
        `;
        messagesDiv.insertAdjacentHTML('beforeend', messageHtml);
      });
      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    })
    .catch(error => console.error('Error loading chat history:', error));

  connectWebSocket(userId);
  setupMessageInput();
}

function showChatPage(userId, username, avatarUrl) {
  if (chatSocket) chatSocket.close();
  chatSocket = null;

  activeChatUserId = userId;
  
  document.getElementById('chat-username').textContent = username;
  // document.getElementById('chat-avatar').src = document.querySelector(`[data-user-id="${userId}"] img`)?.src || '/media/avatars/avatar.jpg';
  document.getElementById('chat-avatar').src = avatarUrl || '/media/avatars/avatar.jpg';
  const messagesDiv = document.getElementById('chat-messages');
  messagesDiv.innerHTML = '';

  fetch(`/api/chat/history/${userId}/`, {
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
    },
  })
    .then(response => {
      if (!response.ok) throw new Error('Failed to load chat history');
      return response.json();
    })
    .then(history => {
      history.forEach(msg => {
        const isSender = msg.sender.user_id === currentUserId;
        const messageHtml = `
          <div class="flex flex-col ${isSender ? 'items-end' : 'items-start'}">
            <div class="text-xs text-gray-400 mb-1 ${isSender ? 'text-right' : 'text-left'}">${new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true }).toUpperCase()}</div>
            <div class="${isSender ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-200'} text-sm px-4 py-2 rounded-xl max-w-[75%]">
              <p>${msg.message}</p>
            </div>
          </div>
        `;
        messagesDiv.insertAdjacentHTML('beforeend', messageHtml);
      });
      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    })
    .catch(error => console.error('Error loading chat history:', error));

  connectWebSocket(userId);
  setupMessageInput();
}

function connectWebSocket(userId) {
  if (chatSocket && chatSocket.readyState === WebSocket.OPEN && activeChatUserId === userId) {
    return;
  }
  if (chatSocket) {
    chatSocket.close();
    chatSocket = null;
  }

  const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
  chatSocket = new WebSocket(`${protocol}://${window.location.host}/ws/chat/${userId}/`);

  // chatSocket.onopen = () => {
  //   console.log('WebSocket connected for user:', userId);
  // };

  chatSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    const messagesDiv = document.getElementById('chat-messages');
    if (!messagesDiv) {
      return;
    }
    const isSender = data.sender === currentUserId;
    
    const messageHtml = `
      <div class="flex flex-col ${isSender ? 'items-end' : 'items-start'}">
        <div class="text-xs text-gray-400 mb-1 ${isSender ? 'text-right' : 'text-left'}">${new Date(data.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true }).toUpperCase()}</div>
        <div class="${isSender ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-200'} text-sm px-4 py-2 rounded-xl max-w-[75%]">
          <p>${data.message}</p>
        </div>
      </div>
    `;
    messagesDiv.insertAdjacentHTML('beforeend', messageHtml);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  };

  // chatSocket.onclose = () => {
  //   console.log('WebSocket closed for user:', userId);
  // };

  // chatSocket.onerror = (error) => {
  //   console.error('WebSocket error:', error);
  // };
}

function sendMessage() {
  const input = document.getElementById('message-input');
  const message = input.value.trim();
  if (message && chatSocket && chatSocket.readyState === WebSocket.OPEN && activeChatUserId) {
    const timestamp = new Date().toISOString();
    const messageData = {
      message: message,
      sender: currentUserId,
      timestamp: timestamp,
      message_type: 'text'
    };
    chatSocket.send(JSON.stringify(messageData));
    input.value = '';
  } else {
    console.warn('Cannot send message: WebSocket not open or no active chat');
  }
}

// Add event listener for "Enter" keypress
function setupMessageInput() {
  const input = document.getElementById('message-input');
  if (input) {
    input.addEventListener('keypress', (event) => {
      if (event.key === 'Enter' && !event.shiftKey) { 
        event.preventDefault();
        sendMessage();
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  setupMessageInput();
  // loadChatList();
});

window.addEventListener('beforeunload', () => {
  if (chatSocket) chatSocket.close();
});

window.addEventListener('unload', () => {
  if (chatSocket) chatSocket.close();
});

// Handle browser back/forward navigation
window.addEventListener('popstate', (event) => {
  if (event.state && event.state.userId && event.state.username) {
    showChatArea(event.state.userId, event.state.username);
  } else {
    // loadChatList();
  }
});

// export {loadChatList};
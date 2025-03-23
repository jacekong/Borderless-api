# Borderless-api

# Blog & Real-Time Messaging API

A Django-based web application with a backend and frontend, featuring blog posting, real-time messaging, friend management, and user interactions.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Project](#running-the-project)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Real-Time Messaging](#real-time-messaging)
- [Goals](#goals)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Blog Posts**: Users can create, edit, and delete blog posts.
- **Real-Time Messaging**: Chat with friends in real-time using WebSockets.
- **Friend System**: Find and add friends, view friend lists.
- **User Authentication**: Register, log in, and log out securely.
- **Responsive Frontend**: User-friendly interface for all functionalities.

## Tech Stack
- **Backend**: Django (Python), Django REST Framework
- **Frontend**: HTML, CSS, JavaScript (optional: React/Vue if used)
- **Database**: SQLite (default) / PostgreSQL (recommended for production)
- **Real-Time**: Django Channels (WebSockets)
- **Version Control**: Git

## Project Structure
```bash
borderlessApi/
|---- api/ # App for blog post management
    |---- tempaltetags/
        |---- __init__.py
        |---- custom_filters.py
    |---- admin.py
    |---- apps.py
    |---- consumers.py
    |---- models.py
    |---- routing.py
    |---- serializers.py
    |---- tests.py
    |---- urls.py
    |---- views.py
|---- borderlessApi/ 
    |---- __init__.py
    |---- asgi.py
    |---- settings.py
    |---- urls.py
    |---- wsgi.py
|---- chat/ # App for realtime messaging
    |---- __init__.py
    |---- apps.py
    |---- channel_middleware.py
    |---- consumers.py
    |---- routing.py
    |---- models.py
    |---- serializers.py
    |---- signals.py
    |---- tests.py
    |---- token_authenication.py
    |---- urls.py
    |---- views.py
|---- friend/ # App for friend management
    |---- __init__.py
    |---- admin.py
    |---- apps.py
    |---- models.py
    |---- serializers.py
    |---- tests.py
    |---- urls.py
    |---- views.py
|---- static/ # Static files
|---- templates/ # Base tempaltes
|---- users/ # App for user management
    |---- __init__.py
    |---- admin.py
    |---- apps.py
    |---- models.py
    |---- serializers.py
    |---- signals.py
    |---- tests.py
    |---- urls.py
    |---- views.py
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Git
- Virtualenv (recommended)
- Redis (for Django Channels in production)
- Django-channels (Realtime messaging)

### Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/jacekong/Borderless-api.git
   cd borderlessApi

2. **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables: Create a .env file in the project root and add:**
    ```bash
    BASE_URL=
    SECRET_KEY=your-secret-key
    DEBUG=True
    DATABASE_URL=sqlite:///db.sqlite3 
    REDIS_URL=redis://localhost:6379/1
    <!-- Google login -->
    CLIENT_ID=
    CLIENT_SECRET=
    <!-- Send email -->
    EMAIL_HOST=
    EMAIL_PORT=
    EMAIL_HOST_PASSWORD=
    ```

5. **Apply Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **python manage.py createsuperuser:**
    ```bash
    python manage.py createsuperuser
    ```

## Running the Project
```bash
python manage.py runserver
```

## Usage
- Blog Posts: Log in, navigate to the "Posts" section, and create a new post.
- Messaging: Go to the "Messages" tab, select a friend, and start chatting.
- Friends: Use the "Find Friends" feature to search and send friend requests.

## API Endpoints
**Posts**
- GET /api/posts/ - List all posts.
- GET /api/posts/<str:pk> - Get single post
- GET api/public/posts/ - Get all public post
- GET api/posts/login/user - Get login user's post
- GET api/check/user/posts/<str:user_id> - Get specific user's posts
- POST /api/posts/ - Create a new post.
- POST api/post/comments/<str:pk> - Comment on a post
- DELETE /api/posts/<str:pk> - DELETE single post

**Real-Time Messaging**
GET /api/chat/history/<str:user_id>/ - Get chat history with current user
GET /api/chat/history/images/<str:user_id>/ - Get Iamge chat history with current user
GET /api/chat/history/voice/<str:user_id>/ -Get Audio chat history with current user
GET /api/chatlists/ - Get all chat lists
GET /api/notification/ - Send chat notification
POST /api/chatlist/create/ - Create new chat
POST /api/chat/images/ - Send iamge in chat

**Websocket**
- ws/chat/<str:user_id>/ - Chat with user
- ws/notifications/ - Reveive notifications

**Friend**
- POST /send/friend/request/ - Send fiend request
- POST /accept/friend/request/ - Accept fiend request
- POST /decline/friend/request/ - Refuse fiend request
- POST /cancel/friend/request/ - Cancel fiend sending request
- POST /remove/friend/ - Unfriend
- GET /api/user/friends/ - Get all friends
- GET /api/user/friend/request/ - Get all friends' request

**Users**
- POST /user/register/ - Register new user
- POST /user/update/ - Update user profile
- GET /current/user/ - GET current login user
- GET /api/users/search/ - Search user

## Goals
1. Complete web frontend integration
2. Extend backend features

## Contributing
- Fork the repository.
- Create a new branch (git checkout -b feature-branch).
- Commit your changes (git commit -m "Add feature").
- Push to the branch (git push origin feature-branch).
- Open a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
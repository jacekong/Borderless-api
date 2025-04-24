import { initializeFriendRequestForms } from './friend_request.js';

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const mainContainer = document.getElementById('content-container');
    const homeBtn = document.getElementById('home-page-btn');
    const accountBtn = document.getElementById('account-btn');
    const friendsBtn = document.getElementById('friends-btn');
    const searchFriendsBtn = document.getElementById('search-friend-btn');
    const createPostBtn = document.getElementById('create-post-btn');
    const messageBtn = document.getElementById('message-btn');

    const drawer = document.getElementById('logo-sidebar');
    const body = document.querySelector('body');

    // Construct base URL dynamically
    const protocol = window.location.protocol;
    const hostname = window.location.hostname;
    const port = window.location.port ? `:${window.location.port}` : '';
    const baseUrl = `${protocol}//${hostname}${port}`;

    const pages = {
        'home': { url: `${baseUrl}/`, path: '/', title: 'Home - Borderless' },
        'account': { url: `${baseUrl}/web/account/`, path: '/web/account/', title: 'My Account - Borderles' },
        'friend': { url: `${baseUrl}/web/friend/list/`, path: '/web/friend/list/', title: 'Friends - Borderless' },
        'message': { url: `${baseUrl}/web/chat/page/`, path: '/web/chat/page/', title: 'Chat List' },
        'search-friends': { url: `${baseUrl}/web/friend/search/`, path: '/web/friend/search/', title: 'Search Friends - Borderless' },
        'create-post': { url: `${baseUrl}/web/post/create/`, path: '/web/post/create/', title: 'Create Post - My Site' },
    };

    // Load home page via ajax
    async function loadHomePage(pageKey) {
        if (!mainContainer) {
            return;
        }
        // Loading animation
        const { url, path, title } = pages[pageKey];

        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                    'X-Current-Path': '/',
                },
            });

            if (!response.ok) {
                const text = await response.text();
                throw new Error(`Server returned ${response.status}: ${text}`);
            }

            const data = await response.json();
            mainContainer.innerHTML = data.html;

            history.pushState({ page: pageKey }, '', path);
            addActiveClassToButton(homeBtn);
            document.title = title;
            reinitializeDynamicContent();
            // Initialize friend request forms
            initializeFriendRequestForms();
        } catch (error) {
            homeBtn.classList.remove('bg-gray-100', 'dark:bg-gray-700');
            console.error('Error loading home page:', error.message);
        }
    }

    // Load account page via AJAX
    async function loadAccountPage() {
        if (!mainContainer) {
            return;
        }

        const url = `${baseUrl}/web/account/`;

        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                },
            });

            if (!response.ok) {
                const text = await response.text();
                throw new Error(`Server returned ${response.status}: ${text}`);
            }

            const data = await response.json();
            mainContainer.innerHTML = data.html;

            history.pushState({ page: 'account' }, '', '/web/account/');
            addActiveClassToButton(accountBtn);
        } catch (error) {
            accountBtn.classList.remove('bg-gray-100', 'dark:bg-gray-700');
            console.error('Error loading account page:', error.message);
        }
    }

    async function loadChatList(pageKey) {
        const { url, path, title } = pages[pageKey];
        if (!mainContainer) {
            return;
        }
        fetch(url, {
            headers: {
            'X-Requested-With': 'XMLHttpRequest',
            },
        })
            .then(response => {
            if (!response.ok) throw new Error('Failed to load chat list');
            return response.json();
            })
            .then(data => {
                mainContainer.innerHTML = data.html;
                //   setupMessageInput();
                history.pushState({ page: pageKey }, '', path);
                addActiveClassToButton(messageBtn);
            })
            .catch(error => console.error('Error loading chat list:', error));
    }

    // Load friends list via AJAX
    async function loadFriendsList() {
        if (!mainContainer) {
            return;
        }

        const url = `${baseUrl}/web/friend/list/`;

        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                },
            });

            if (!response.ok) {
                const text = await response.text();
                throw new Error(`Server returned ${response.status}: ${text}`);
            }

            const data = await response.json();
            mainContainer.innerHTML = data.html;

            history.pushState({ page: 'friend' }, '', '/web/friend/list/');
            addActiveClassToButton(friendsBtn);
            reinitializeDynamicContent();
        } catch (error) {
            friendsBtn.classList.remove('bg-gray-100', 'dark:bg-gray-700');
            console.error('Error loading friends list:', error.message);
        }
    }

    // Load search friends page via AJAX
    async function loadSearchFriends() {
        if (!mainContainer) {
            return;
        }

        const url = `${baseUrl}/web/search/friends/`;

        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                },
            });

            if (!response.ok) {
                const text = await response.text();
                throw new Error(`Server returned ${response.status}: ${text}`);
            }

            const data = await response.json();
            mainContainer.innerHTML = data.html;

            history.pushState({ page: 'search-friends' }, '', '/web/search/friends/');
            addActiveClassToButton(searchFriendsBtn);
        } catch (error) {
            searchFriendsBtn.classList.remove('bg-gray-100', 'dark:bg-gray-700');
            console.error('Error loading search friends page:', error.message);
        }
    }

    // Load create post page via AJAX
    async function loadCreatePost() {
        if (!mainContainer) {
            return;
        }

        const url = `${baseUrl}/web/post/create`;

        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                },
            });

            if (!response.ok) {
                const text = await response.text();
                throw new Error(`Server returned ${response.status}: ${text}`);
            }

            const data = await response.json();
            mainContainer.innerHTML = data.html;

            history.pushState({ page: 'create-post' }, '', '/web/post/create');
            addActiveClassToButton(createPostBtn);
            reinitializeDynamicContent();
        } catch (error) {
            createPostBtn.classList.remove('bg-gray-100', 'dark:bg-gray-700');
            console.error('Error loading create post page:', error.message);
        }
    }

    function addActiveClassToButton(button) {
        const buttons = [homeBtn, accountBtn, friendsBtn, searchFriendsBtn, createPostBtn, messageBtn];
        buttons.forEach(btn => {
            if (btn !== button) {
                btn.classList.remove('bg-gray-100', 'dark:bg-gray-700');
            } else {
                btn.classList.add('bg-gray-100', 'dark:bg-gray-700');
            }
        });
    }

    function reinitializeDynamicContent() {
        if (window.initializeLikeButtons) window.initializeLikeButtons();
        if (window.initializeVideoPlayers) window.initializeVideoPlayers();
        if (window.initializeCreatePost) window.initializeCreatePost();
        if (window.initializeComments) window.initializeComments();
        if (window.loadChatList) window.loadChatList();
    }

    if (homeBtn) {

        homeBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            // Loading animation
            mainContainer.innerHTML = `
                <div class="mx-auto mt-20 p-2 px-4 space-y-2 md:w-[600px] h-[75vh] bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
                    <div role="status" class="space-y-8 animate-pulse md:space-y-0 md:space-x-8 rtl:space-x-reverse md:flex md:items-center">
                        <div class="flex items-center justify-center w-full h-48 bg-gray-300 rounded-sm sm:w-96 dark:bg-gray-700">
                            <svg class="w-10 h-10 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 18">
                                <path d="M18 0H2a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2Zm-5.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm4.376 10.481A1 1 0 0 1 16 15H4a1 1 0 0 1-.895-1.447l3.5-7A1 1 0 0 1 7.468 6a.965.965 0 0 1 .9.5l2.775 4.757 1.546-1.887a1 1 0 0 1 1.618.1l2.541 4a1 1 0 0 1 .028 1.011Z"/>
                            </svg>
                        </div>
                        <div class="w-full">
                            <div class="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-48 mb-4"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[480px] mb-2.5"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 mb-2.5"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[440px] mb-2.5"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[460px] mb-2.5"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px]"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                    </div>
                      <div role="status" class="space-y-8 animate-pulse md:space-y-0 md:space-x-8 rtl:space-x-reverse md:flex md:items-center">
                    <div class="flex items-center justify-center w-full h-48 bg-gray-300 rounded-sm sm:w-96 dark:bg-gray-700">
                            <svg class="w-10 h-10 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 18">
                                <path d="M18 0H2a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2Zm-5.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm4.376 10.481A1 1 0 0 1 16 15H4a1 1 0 0 1-.895-1.447l3.5-7A1 1 0 0 1 7.468 6a.965.965 0 0 1 .9.5l2.775 4.757 1.546-1.887a1 1 0 0 1 1.618.1l2.541 4a1 1 0 0 1 .028 1.011Z"/>
                            </svg>
                        </div>
                        <div class="w-full">
                            <div class="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-48 mb-4"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[480px] mb-2.5"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 mb-2.5"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[440px] mb-2.5"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[460px] mb-2.5"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px]"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                    </div>
                      <div role="status" class="space-y-8 animate-pulse md:space-y-0 md:space-x-8 rtl:space-x-reverse md:flex md:items-center">
                    <div class="flex items-center justify-center w-full h-48 bg-gray-300 rounded-sm sm:w-96 dark:bg-gray-700">
                            <svg class="w-10 h-10 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 18">
                                <path d="M18 0H2a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2Zm-5.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm4.376 10.481A1 1 0 0 1 16 15H4a1 1 0 0 1-.895-1.447l3.5-7A1 1 0 0 1 7.468 6a.965.965 0 0 1 .9.5l2.775 4.757 1.546-1.887a1 1 0 0 1 1.618.1l2.541 4a1 1 0 0 1 .028 1.011Z"/>
                            </svg>
                        </div>
                        <div class="w-full">
                            <div class="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-48 mb-4"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[480px] mb-2.5"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 mb-2.5"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[440px] mb-2.5"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[460px] mb-2.5"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px]"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                    </div>
                      <div role="status" class="space-y-8 animate-pulse md:space-y-0 md:space-x-8 rtl:space-x-reverse md:flex md:items-center">
                    <div class="flex items-center justify-center w-full h-48 bg-gray-300 rounded-sm sm:w-96 dark:bg-gray-700">
                            <svg class="w-10 h-10 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 18">
                                <path d="M18 0H2a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2Zm-5.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm4.376 10.481A1 1 0 0 1 16 15H4a1 1 0 0 1-.895-1.447l3.5-7A1 1 0 0 1 7.468 6a.965.965 0 0 1 .9.5l2.775 4.757 1.546-1.887a1 1 0 0 1 1.618.1l2.541 4a1 1 0 0 1 .028 1.011Z"/>
                            </svg>
                        </div>
                        <div class="w-full">
                            <div class="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-48 mb-4"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[480px] mb-2.5"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 mb-2.5"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[440px] mb-2.5"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[460px] mb-2.5"></div>
                            <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px]"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                    </div>
                </div>
                `;
            await loadHomePage('home');
        });
    }

    // Event listeners for menu item clicks
    if (accountBtn) {
        accountBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            // Loading animation
            mainContainer.innerHTML = `
                <div class="mx-auto mt-20 px-4 space-y-2 md:w-[600px] h-[75vh] max-w-2xl bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
                    <div class="flex items-center justify-center mt-4">
                        <svg class="w-8 h-8 text-gray-200 dark:text-gray-700 me-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                        </svg>
                        <div class="w-20 h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 me-3"></div>
                        <div class="w-24 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                    </div>
                    <div role="status" class="animate-pulse">
                    <div class="mt-20 h-2.5 bg-gray-300 rounded-full dark:bg-gray-700 max-w-[640px] mb-2.5 mx-auto"></div>
                    <div class="mt-20 h-2.5 bg-gray-300 rounded-full dark:bg-gray-700 max-w-[640px] mb-2.5 mx-auto"></div>
                    <div class="mt-20 h-2.5 bg-gray-300 rounded-full dark:bg-gray-700 max-w-[640px] mb-2.5 mx-auto"></div>
                    <span class="sr-only">Loading...</span>
                    </div>
                </div>
            `;
            await loadAccountPage();
        });
    }

    if (messageBtn) {
        messageBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            // Loading animation
            mainContainer.innerHTML = `
                <div class="mx-auto mt-20 px-4 space-y-2 md:w-[600px] h-[75vh] max-w-2xl bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
                    <div role="status" class="animate-pulse">
                        <div class="flex items-center justify-start mt-4">
                            <svg class="w-8 h-8 text-gray-200 dark:text-gray-700 me-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                            </svg>
                            <div class="w-40 h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 me-3"></div>
                            <div class="w-40 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                        <div class="flex items-center justify-start mt-4">
                            <svg class="w-8 h-8 text-gray-200 dark:text-gray-700 me-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                            </svg>
                            <div class="w-40 h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 me-3"></div>
                            <div class="w-40 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                        <div class="flex items-center justify-start mt-4">
                            <svg class="w-8 h-8 text-gray-200 dark:text-gray-700 me-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                            </svg>
                            <div class="w-40 h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 me-3"></div>
                            <div class="w-40 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                        <div class="flex items-center justify-start mt-4">
                            <svg class="w-8 h-8 text-gray-200 dark:text-gray-700 me-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                            </svg>
                            <div class="w-40 h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 me-3"></div>
                            <div class="w-40 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                        <div class="flex items-center justify-start mt-4">
                            <svg class="w-8 h-8 text-gray-200 dark:text-gray-700 me-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                            </svg>
                            <div class="w-40 h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 me-3"></div>
                            <div class="w-40 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                        <div class="flex items-center justify-start mt-4">
                            <svg class="w-8 h-8 text-gray-200 dark:text-gray-700 me-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                            </svg>
                            <div class="w-40 h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 me-3"></div>
                            <div class="w-40 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                        <div class="flex items-center justify-start mt-4">
                            <svg class="w-8 h-8 text-gray-200 dark:text-gray-700 me-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                            </svg>
                            <div class="w-40 h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 me-3"></div>
                            <div class="w-40 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                        <div class="flex items-center justify-start mt-4">
                            <svg class="w-8 h-8 text-gray-200 dark:text-gray-700 me-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                            </svg>
                            <div class="w-40 h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 me-3"></div>
                            <div class="w-40 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                        <div class="flex items-center justify-start mt-4">
                            <svg class="w-8 h-8 text-gray-200 dark:text-gray-700 me-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                            </svg>
                            <div class="w-40 h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 me-3"></div>
                            <div class="w-40 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                        <div class="flex items-center justify-start mt-4">
                            <svg class="w-8 h-8 text-gray-200 dark:text-gray-700 me-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                            </svg>
                            <div class="w-40 h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 me-3"></div>
                            <div class="w-40 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                        <div class="flex items-center justify-start mt-4">
                            <svg class="w-8 h-8 text-gray-200 dark:text-gray-700 me-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                            </svg>
                            <div class="w-40 h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 me-3"></div>
                            <div class="w-40 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                        <div class="flex items-center justify-start mt-4">
                            <svg class="w-8 h-8 text-gray-200 dark:text-gray-700 me-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                            </svg>
                            <div class="w-40 h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 me-3"></div>
                            <div class="w-40 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                        <div class="flex items-center justify-start mt-4">
                            <svg class="w-8 h-8 text-gray-200 dark:text-gray-700 me-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                            </svg>
                            <div class="w-40 h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 me-3"></div>
                            <div class="w-40 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                        <div class="flex items-center justify-start mt-4">
                            <svg class="w-8 h-8 text-gray-200 dark:text-gray-700 me-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                            </svg>
                            <div class="w-40 h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 me-3"></div>
                            <div class="w-40 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                        <div class="flex items-center justify-start mt-4">
                            <svg class="w-8 h-8 text-gray-200 dark:text-gray-700 me-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                            </svg>
                            <div class="w-40 h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 me-3"></div>
                            <div class="w-40 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                        <div class="flex items-center justify-start mt-4">
                            <svg class="w-8 h-8 text-gray-200 dark:text-gray-700 me-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                            </svg>
                            <div class="w-40 h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 me-3"></div>
                            <div class="w-40 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <span class="sr-only">Loading...</span>
                    </div>
                </div>
            `;

            await loadChatList('message');
        }
    )}

    if (friendsBtn) {
        friendsBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            // Loading animation
            mainContainer.innerHTML = `
                <div class="mx-auto mt-20 px-4 space-y-2 md:w-[600px] h-[75vh] max-w-2xl bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
                    <div role="status" class="p-4 space-y-4 divide-y divide-gray-200 rounded-sm shadow-sm animate-pulse dark:divide-gray-700 md:p-6">
                    <div class="flex items-center justify-between">
                        <div>
                            <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-600 w-24 mb-2.5"></div>
                            <div class="w-32 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-700 w-12"></div>
                    </div>
                    <div class="flex items-center justify-between pt-4">
                        <div>
                            <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-600 w-24 mb-2.5"></div>
                            <div class="w-32 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-700 w-12"></div>
                    </div>
                    <div class="flex items-center justify-between pt-4">
                        <div>
                            <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-600 w-24 mb-2.5"></div>
                            <div class="w-32 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-700 w-12"></div>
                    </div>
                    <div class="flex items-center justify-between pt-4">
                        <div>
                            <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-600 w-24 mb-2.5"></div>
                            <div class="w-32 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-700 w-12"></div>
                    </div>
                    <div class="flex items-center justify-between pt-4">
                        <div>
                            <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-600 w-24 mb-2.5"></div>
                            <div class="w-32 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-700 w-12"></div>
                    </div>
                    <div class="flex items-center justify-between pt-4">
                        <div>
                            <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-600 w-24 mb-2.5"></div>
                            <div class="w-32 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-700 w-12"></div>
                    </div>
                    <div class="flex items-center justify-between pt-4">
                        <div>
                            <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-600 w-24 mb-2.5"></div>
                            <div class="w-32 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-700 w-12"></div>
                    </div>
                    <div class="flex items-center justify-between pt-4">
                        <div>
                            <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-600 w-24 mb-2.5"></div>
                            <div class="w-32 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-700 w-12"></div>
                    </div>
                    <div class="flex items-center justify-between pt-4">
                        <div>
                            <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-600 w-24 mb-2.5"></div>
                            <div class="w-32 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-700 w-12"></div>
                    </div>
                    <div class="flex items-center justify-between pt-4">
                        <div>
                            <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-600 w-24 mb-2.5"></div>
                            <div class="w-32 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-700 w-12"></div>
                    </div>
                    <div class="flex items-center justify-between pt-4">
                        <div>
                            <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-600 w-24 mb-2.5"></div>
                            <div class="w-32 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                        <div class="h-2.5 bg-gray-300 rounded-full dark:bg-gray-700 w-12"></div>
                    </div>
                    <span class="sr-only">Loading...</span>
                    </div>
                </div>
            `;
            await loadFriendsList();
        });
    }

    if (searchFriendsBtn) {
        searchFriendsBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            // Loading animation
            mainContainer.innerHTML = `
                <div class="mx-auto mt-20 px-4 p-2 space-y-2 md:w-[600px] h-[75vh] max-w-2xl bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
                    <div role="status" class="max-w-sm animate-pulse">
                        <div class="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-48 mb-4"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px] mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[330px] mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[300px] mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px]"></div>
                        <span class="sr-only">Loading...</span>
                    </div>
                    <div role="status" class="max-w-sm animate-pulse">
                        <div class="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-48 mb-4"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px] mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[330px] mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[300px] mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px]"></div>
                        <span class="sr-only">Loading...</span>
                    </div>
                    <div role="status" class="max-w-sm animate-pulse">
                        <div class="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-48 mb-4"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px] mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[330px] mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[300px] mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px]"></div>
                        <span class="sr-only">Loading...</span>
                    </div>
                    <div role="status" class="max-w-sm animate-pulse">
                        <div class="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-48 mb-4"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px] mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[330px] mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[300px] mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px]"></div>
                        <span class="sr-only">Loading...</span>
                    </div>
                    <div role="status" class="max-w-sm animate-pulse">
                        <div class="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-48 mb-4"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px] mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[330px] mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[300px] mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px]"></div>
                        <span class="sr-only">Loading...</span>
                    </div>
                    <div role="status" class="max-w-sm animate-pulse">
                        <div class="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-48 mb-4"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px] mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[330px] mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[300px] mb-2.5"></div>
                        <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px]"></div>
                        <span class="sr-only">Loading...</span>
                    </div>
                </div>
            `;
            await loadSearchFriends();
        });
    }

    if (createPostBtn) {
        createPostBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            // Loading animation
            mainContainer.innerHTML = `
                <div class="mx-auto mt-20 px-4 p-2 space-y-2 md:w-[600px] h-[75vh] max-w-2xl bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
                    <div role="status" class="p-4 rounded-sm shadow-sm animate-pulse md:p-6">
                    <div class="flex items-center justify-center h-48 mb-4 bg-gray-300 rounded-sm dark:bg-gray-700">
                        <svg class="w-10 h-10 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 20">
                            <path d="M14.066 0H7v5a2 2 0 0 1-2 2H0v11a1.97 1.97 0 0 0 1.934 2h12.132A1.97 1.97 0 0 0 16 18V2a1.97 1.97 0 0 0-1.934-2ZM10.5 6a1.5 1.5 0 1 1 0 2.999A1.5 1.5 0 0 1 10.5 6Zm2.221 10.515a1 1 0 0 1-.858.485h-8a1 1 0 0 1-.9-1.43L5.6 10.039a.978.978 0 0 1 .936-.57 1 1 0 0 1 .9.632l1.181 2.981.541-1a.945.945 0 0 1 .883-.522 1 1 0 0 1 .879.529l1.832 3.438a1 1 0 0 1-.031.988Z"/>
                            <path d="M5 5V.13a2.96 2.96 0 0 0-1.293.749L.879 3.707A2.98 2.98 0 0 0 .13 5H5Z"/>
                        </svg>
                    </div>
                    <div class="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-48 mb-4"></div>
                    <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 mb-2.5"></div>
                    <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 mb-2.5"></div>
                    <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                    <div class="flex items-center mt-4">
                    <svg class="w-10 h-10 me-3 text-gray-200 dark:text-gray-700" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                        </svg>
                        <div>
                            <div class="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-32 mb-2"></div>
                            <div class="w-48 h-2 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                        </div>
                    </div>
                    <span class="sr-only">Loading...</span>
                    </div>
                </div>
            `;
            await loadCreatePost('create-post');
        });
    }


});
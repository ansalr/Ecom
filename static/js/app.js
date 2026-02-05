const API_BASE = '/api';

class ApiClient {
    static getAccessToken() {
        return localStorage.getItem('access_token');
    }

    static setTokens(access, refresh) {
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
    }

    static clearTokens() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    }

    static async request(endpoint, method = 'GET', data = null) {
        const headers = {
            'Content-Type': 'application/json',
        };
        const token = this.getAccessToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            method,
            headers,
        };
        if (data) {
            config.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${API_BASE}${endpoint}`, config);
            if (response.status === 401) {
                this.clearTokens();
                window.location.href = '/login/';
                return;
            }
            return response;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }
}

// UI Helpers
const updateNav = () => {
    const token = ApiClient.getAccessToken();
    const navLinks = document.getElementById('nav-links');
    const logoutBtn = document.getElementById('logout-btn');

    if (token) {
        logoutBtn.classList.remove('hidden');
        navLinks.innerHTML = `
            <li class="nav-item"><a class="nav-link" href="/organizations/create/">organizations</a></li>
            <li class="nav-item"><a class="nav-link" href="/contacts/create/">Contact</a></li>
            <li class="nav-item"><a class="nav-link" href="/products/">Products</a></li>
            <li class="nav-item"><a class="nav-link" href="/orders/create/">New Order</a></li>
        `;
    } else {
        logoutBtn.classList.add('hidden');
        navLinks.innerHTML = `
            <li class="nav-item"><a class="nav-link" href="/login/">Login</a></li>
        `;
    }
}; 

document.addEventListener('DOMContentLoaded', () => {
    updateNav();
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            ApiClient.clearTokens();
            window.location.href = '/login/';
        });
    }
});

function showAlert(message, type = 'success') {
    const container = document.getElementById('alert-container');
    container.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
    setTimeout(() => { container.innerHTML = ''; }, 3000);
}

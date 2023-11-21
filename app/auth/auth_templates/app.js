async function register() {
    const username = document.getElementById('reg-username').value;
    const password = document.getElementById('reg-password').value;

    const response = await fetch('/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    });

    const data = await response.json();

    if (response.status === 201) {
        alert('Registration successful');
        showLoginForm();
    } else {
        alert(`Registration failed: ${data.message}`);
    }
}

async function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const response = await fetch('/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    });

    const data = await response.json();

    if (response.status === 200) {
        alert('Login successful');
        showProfileForm();
    } else {
        alert(`Login failed: ${data.message}`);
    }
}

async function updateProfile() {
    const newUsername = document.getElementById('new-username').value;
    const newPassword = document.getElementById('new-password').value;

    const response = await fetch('/auth/update-profile', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getToken()}`,
        },
        body: JSON.stringify({ new_username: newUsername, new_password: newPassword }),
    });

    const data = await response.json();

    if (response.status === 200) {
        alert('Profile updated successfully');
        showUserDetails();
    } else {
        alert(`Profile update failed: ${data.message}`);
    }
}

function getToken() {
    return document.cookie.replace(/(?:(?:^|.*;\s*)access_token\s*=\s*([^;]*).*$)|^.*$/, '$1');
}

async function showUserDetails() {
    const response = await fetch('/auth/user-details', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${getToken()}`,
        },
    });

    const data = await response.json();

    if (response.status === 200) {
        document.getElementById('user-details-content').innerHTML = JSON.stringify(data.data, null, 2);
        document.getElementById('user-details').style.display = 'block';
    } else {
        alert(`Failed to retrieve user details: ${data.message}`);
    }
}

function showLoginForm() {
    document.getElementById('register-form').style.display = 'none';
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('profile-form').style.display = 'none';
    document.getElementById('user-details').style.display = 'none';
}

function showProfileForm() {
    document.getElementById('register-form').style.display = 'none';
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('profile-form').style.display = 'block';
    document.getElementById('user-details').style.display = 'none';
    showUserDetails();
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('register-form').style.display = 'block';
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('profile-form').style.display = 'none';
    document.getElementById('user-details').style.display = 'none';
});

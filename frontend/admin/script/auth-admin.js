// Handle Sign In
document.getElementById("loginFormAdmin").addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const error = document.getElementById("error");

    try {
        const response = await fetch("http://localhost:5000/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
        });

        const result = await response.json();

        if (response.ok) {
            localStorage.setItem("adminToken", result.token);
            error.textContent = "";
            window.location.href = "admin.html"; // Redirect to admin dashboard
        } else {
            error.textContent = result.message || "Login failed.";
        }
    } catch (err) {
        error.textContent = "Error connecting to server.";
    }
});

// Handle Sign Up
document.getElementById("signupFormAdmin").addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("newName").value.trim();
    const email = document.getElementById("newEmail").value.trim();
    const password = document.getElementById("newPassword").value.trim();
    const error = document.getElementById("signupError");

    try {
        const response = await fetch("http://localhost:5000/api/auth/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name, email, password }),
        });

        const result = await response.json();

        if (response.ok) {
            error.textContent = "";
            alert("Admin account created! Please log in.");
            showSignIn();
        } else {
            error.textContent = result.message || "Signup failed.";
        }
    } catch (err) {
        error.textContent = "Error connecting to server.";
    }
});

// Toggle functions (already in login.html)
function showSignIn() {
    document.getElementById('signInForm').classList.remove('hidden');
    document.getElementById('signUpForm').classList.add('hidden');
}

function showSignUp() {
    document.getElementById('signInForm').classList.add('hidden');
    document.getElementById('signUpForm').classList.remove('hidden');
}
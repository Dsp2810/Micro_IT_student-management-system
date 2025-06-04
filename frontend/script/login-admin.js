document.getElementById("adminLoginForm").addEventListener("submit", async function (e) {
            e.preventDefault();
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            const response = await fetch("http://localhost:5000/admin/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, password })
            });

            const result = await response.json();

            if (response.ok) {
                localStorage.setItem("adminToken", result.token);
                document.getElementById("status").innerText = "Login successful!";
                window.location.href = "admin.html"; // Redirect to admin dashboard
            } else {
                document.getElementById("status").innerText = result.message || "Login failed.";
            }
        });
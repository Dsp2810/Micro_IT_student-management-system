// login.js
document.getElementById("loginForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const role = localStorage.getItem("selectedRole");

  const response = await fetch("http://127.0.0.1:5000/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, role }),
  });

  const data = await response.json();
  const errorText = document.getElementById("error");

  if (response.ok) {
    localStorage.setItem("token", data.token);
    localStorage.setItem("email", data.email);
    localStorage.setItem("role", data.role);

    if (data.role === "admin") {
      window.location.href = "admin/dashboard.html";
    } else if (data.role === "client") {
      window.location.href = "client/dashboard.html";
    }
  } else {
    errorText.textContent = data.message || "Login failed.";
  }
});

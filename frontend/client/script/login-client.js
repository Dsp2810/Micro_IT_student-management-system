document.getElementById("loginFormClient").addEventListener("submit", async function (e) {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const errorText = document.getElementById("error");

  try {
    const response = await fetch("http://127.0.0.1:5000/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (response.ok && data.role === "client") {
      localStorage.setItem("token", data.token);
      localStorage.setItem("email", data.email);
      localStorage.setItem("role", data.role);
      localStorage.setItem("studentName", data.name || "Student");
      // ✅ Use forward slashes for URLs
      window.location.href = "client/dashboard.html";
    } else {
      errorText.textContent = data.message || "Access denied.";
    }
  } catch (err) {
    errorText.textContent = "Server error. Try again.";
  }
});

document.getElementById("setPasswordForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();
  const status = document.getElementById("status");

  try {
    const res = await fetch("http://localhost:5000/api/auth/set-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const result = await res.json();

    if (res.ok) {
      status.style.color = "green";
      status.textContent = "Password set successfully! You can now login.";
    } else {
      status.textContent = result.message || "Unable to set password.";
    }
  } catch (err) {
    status.textContent = "Server error.";
  }
});

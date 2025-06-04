document.getElementById("settingsForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const token = localStorage.getItem("adminToken");
  const status = document.getElementById("status");

  const email = document.getElementById("newEmail").value.trim();
  const password = document.getElementById("newPassword").value.trim();

  if (!email && !password) {
    status.textContent = "Please provide email or password to update.";
    return;
  }

  const updates = {};
  if (email) updates.email = email;
  if (password) updates.password = password;

  try {
    const res = await fetch("http://localhost:5000/api/auth/settings", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(updates)
    });

    const result = await res.json();
    if (res.ok) {
      status.textContent = result.message;
    } else {
      status.textContent = result.message || "Update failed.";
    }
  } catch (err) {
    status.textContent = "Server error.";
  }
});

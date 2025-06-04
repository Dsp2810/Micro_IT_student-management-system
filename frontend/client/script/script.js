document.addEventListener("DOMContentLoaded", async function () {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Unauthorized access. Please login first.");
    window.location.href = "login.html";
    return;
  }

  try {
    const response = await fetch("http://localhost:5000/api/client/dashboard", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const data = await response.json();

    if (response.ok) {
      document.getElementById("student-name").textContent = data.studentName;
      document.querySelector(".bg-info .display-6").textContent = data.attendance;
      document.querySelector(".bg-success .display-6").textContent = data.grades;
      document.querySelector(".bg-warning .display-6").textContent = data.next_class;
    } else {
      alert(data.message || "Failed to load dashboard data.");
    }
  } catch (err) {
    console.error("Error loading dashboard:", err);
    alert("Server error. Please try again later.");
  }
});

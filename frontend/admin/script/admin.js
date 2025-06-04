document.addEventListener("DOMContentLoaded", () => {
  // Token check for all admin pages
  const token = localStorage.getItem("adminToken");
  if (!token) {
    alert("Unauthorized access. Please log in first.");
    window.location.href = "login.html";
    return;
  }

  // Highlight active nav link
  const navLinks = document.querySelectorAll(".nav-link");
  const currentPage = window.location.pathname.split("/").pop();

  navLinks.forEach(link => {
    if (link.getAttribute("href") === currentPage) {
      link.classList.add("active", "fw-bold");
    } else {
      link.classList.remove("active", "fw-bold");
    }
  });

  // Logout handling
  const logoutLink = document.querySelector(".nav-link[href='#logout']");
  if (logoutLink) {
    logoutLink.addEventListener("click", (e) => {
      e.preventDefault();
      localStorage.removeItem("adminToken");
      alert("Logged out successfully!");
      window.location.href = "login.html";
    });
  }
});

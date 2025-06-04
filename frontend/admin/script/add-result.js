document.getElementById("addResultForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const student_id = document.getElementById("studentId").value.trim();
  const subject = document.getElementById("subject").value;
  const marks = document.getElementById("marks").value.trim();
  const status = document.getElementById("status");

  const token = localStorage.getItem("adminToken");

  if (!token) {
    status.textContent = "Unauthorized. Please log in.";
    status.style.color = "red";
    return;
  }

  try {
    const response = await fetch("http://localhost:5000/api/results/add-result", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ student_id, subject, marks })
    });

    const result = await response.json();

    if (response.ok) {
      status.textContent = result.message;
      status.style.color = "green";
      document.getElementById("addResultForm").reset();
    } else {
      status.textContent = result.message || "Failed to add result.";
      status.style.color = "red";
    }
  } catch (err) {
    console.error(err);
    status.textContent = "Server error.";
    status.style.color = "red";
  }
});

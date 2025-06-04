document.getElementById("addStudentForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const token = localStorage.getItem("adminToken");
  const status = document.getElementById("status");

  const student = {
    student_id: document.getElementById("studentId").value.trim(),
    name: document.getElementById("name").value.trim(),
    email: document.getElementById("email").value.trim(),
    semester: document.getElementById("semester").value.trim(),
    division: document.getElementById("division").value.trim(),
  };

  try {
    const res = await fetch("http://localhost:5000/api/students/add-student", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(student),
    });
    const result = await res.json();
    if (res.ok) {
      status.textContent = "Student added successfully!";
      e.target.reset();
    } else {
      status.textContent = result.message || "Failed to add student.";
    }
  } catch (err) {
    status.textContent = "Server error.";
  }
});

document.getElementById("markAttendanceForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const token = localStorage.getItem("adminToken");
  const status = document.getElementById("status");

  const attendanceData = {
    studentId: document.getElementById("studentId").value.trim(),
    date: document.getElementById("date").value,
    present: document.getElementById("present").checked
  };

  try {
    const res = await fetch("http://localhost:5000/api/attendance/mark-attendance", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(attendanceData),
    });
    const result = await res.json();
    if (res.ok) {
      status.textContent = "Attendance recorded.";
      e.target.reset();
    } else {
      status.textContent = result.message || "Failed to mark attendance.";
    }
  } catch (err) {
    status.textContent = "Server error.";
  }
});

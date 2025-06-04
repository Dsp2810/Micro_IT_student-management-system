document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem("adminToken");
  if (!token) {
    alert("Unauthorized access.");
    window.location.href = "login.html";
    return;
  }

  try {
    const res = await fetch("http://localhost:5000/api/dashboard/summary", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const data = await res.json();
    if (res.ok) {
      document.getElementById("totalStudents").textContent = data.total_students;
      document.getElementById("activeStudents").textContent = data.active_students;
      document.getElementById("lowAttendance").textContent = data.low_attendance;
    } else {
      console.error("Failed to load dashboard:", data.message);
    }

    // Fetch attendance alerts
    const alertsRes = await fetch("http://localhost:5000/api/attendance/summary", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const alertsData = await alertsRes.json();
    const alertBody = document.getElementById("alertTableBody");
    if (alertsRes.ok && alertsData.summary) {
      alertsData.summary
        .filter(s => s.alert)
        .forEach(a => {
          const row = document.createElement("tr");
          row.innerHTML = `<td>${a._id}</td><td>${a.attendance_percent.toFixed(2)}%</td>`;
          alertBody.appendChild(row);
        });
    }
  } catch (err) {
    console.error("Error loading dashboard data", err);
  }
});

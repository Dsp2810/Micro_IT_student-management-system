document.addEventListener("DOMContentLoaded", async () => {
  const ctx = document.getElementById("attendanceChart").getContext("2d");
  const token = localStorage.getItem("adminToken");

  try {
    const res = await fetch("http://localhost:5000/api/attendance/summary", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const data = await res.json();

    if (res.ok && data.summary) {
      const labels = data.summary.map((entry) => entry._id);
      const percentages = data.summary.map((entry) => parseFloat(entry.attendance_percent.toFixed(2)));

      new Chart(ctx, {
        type: "bar",
        data: {
          labels,
          datasets: [{
            label: "Attendance %",
            data: percentages,
            backgroundColor: percentages.map(p => p >= 75 ? "rgba(75, 192, 192, 0.6)" : "rgba(255, 99, 132, 0.6)"),
            borderColor: "rgba(0, 0, 0, 0.1)",
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
              title: {
                display: true,
                text: "Attendance Percentage"
              }
            }
          },
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: context => ` ${context.parsed.y}%`
              }
            }
          }
        }
      });
    } else {
      alert("Failed to fetch summary");
    }
  } catch (err) {
    console.error("Error fetching attendance data:", err);
    alert("Server error");
  }
});

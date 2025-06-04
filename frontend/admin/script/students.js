document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem("adminToken");
  const table = document.getElementById("studentsTable");

  if (!token || !table) return;

  try {
    const res = await fetch("http://localhost:5000/api/students/list", {
      headers: { Authorization: `Bearer ${token}` }
    });

    const result = await res.json();

    console.log("Fetched students:", result);

    if (res.ok && Array.isArray(result) && result.length > 0) {
      result.forEach((student, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td class="text-center">${index + 1}</td>
          <td>${student.student_id}</td>
          <td>${student.name}</td>
          <td>${student.email}</td>
          <td class="text-center">${student.semester}</td>
          <td class="text-center">${student.division}</td>
          <td class="text-center">${student.attendance || 0}%</td>
        `;
        table.appendChild(row);
      });
    } else if (res.ok) {
      table.innerHTML = `<tr><td colspan="6" class="text-center">No students found.</td></tr>`;
    } else {
      table.innerHTML = `<tr><td colspan="6" class="text-center text-danger">Failed to load students</td></tr>`;
    }
  } catch (err) {
    console.error("Error loading students:", err);
    table.innerHTML = `<tr><td colspan="6" class="text-center text-danger">Server error</td></tr>`;
  }
});


function filterTable() {
  const searchInput = document.getElementById("searchBar").value.toLowerCase();
  const rows = document.querySelectorAll("#studentsTable tr");

  rows.forEach(row => {
    const text = row.innerText.toLowerCase();
    row.style.display = text.includes(searchInput) ? "" : "none";
  });
}
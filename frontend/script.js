const API_URL = 'http://127.0.0.1:5000/api/entries';

document.getElementById('entryForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const station = document.getElementById('station').value;
  const delay_reason = document.getElementById('reason').value;
  const duration = parseFloat(document.getElementById('duration').value);

  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ station, delay_reason, duration }),
  });

  if (response.ok) {
    document.getElementById('entryForm').reset();
    loadEntries();
  } else {
    const errorData = await response.json();
    alert(`Failed to add entry: ${errorData.error || 'Unknown error'}`);
    console.error("Server response:", errorData);
  }
});

async function loadEntries() {
  const res = await fetch(API_URL);
  const entries = await res.json();

  const tbody = document.querySelector('#entriesTable tbody');
  tbody.innerHTML = '';

  entries.forEach(entry => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${new Date(entry.timestamp).toLocaleString()}</td>
      <td>${entry.station}</td>
      <td>${entry.delay_reason}</td>
      <td>${entry.duration}</td>
    `;
    tbody.appendChild(row);
  });
}

loadEntries();
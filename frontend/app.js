const calendarBody = document.querySelector("#calendar-table tbody");
const briefEmpty = document.getElementById("brief-empty");
const briefOutput = document.getElementById("brief-output");
const briefText = document.getElementById("brief-text");
const briefNeedsInput = document.getElementById("brief-needs-input");
const gapsOutput = document.getElementById("gaps-output");
const performanceBody = document.querySelector("#performance-table tbody");
const recommendationEl = document.getElementById("recommendation");
const performanceError = document.getElementById("performance-error");

async function loadCalendar() {
  const res = await fetch("/api/calendar");
  const rows = await res.json();
  calendarBody.innerHTML = "";
  for (const row of rows) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.id}</td>
      <td>${row.target_date}</td>
      <td>${row.content_type}</td>
      <td>${row.platform || "<em>missing</em>"}</td>
      <td>${row.title}</td>
      <td>${row.owner}</td>
      <td class="status-${row.status}">${row.status}</td>
      <td><button data-id="${row.id}" class="brief-btn">Generate brief</button></td>
    `;
    calendarBody.appendChild(tr);
  }
  document.querySelectorAll(".brief-btn").forEach((btn) => {
    btn.addEventListener("click", () => generateBrief(btn.dataset.id));
  });
}

async function generateBrief(rowId) {
  const res = await fetch(`/api/briefs/${rowId}`, { method: "POST" });
  const data = await res.json();
  briefEmpty.hidden = true;
  briefOutput.hidden = false;
  if (!res.ok) {
    briefText.textContent = `Error: ${data.error}`;
    briefNeedsInput.hidden = true;
    return;
  }
  briefText.textContent = data.brief;
  if (data.needs_input.length) {
    briefNeedsInput.hidden = false;
    briefNeedsInput.textContent = `Needs input before this brief is usable: ${data.needs_input.join(", ")}`;
  } else {
    briefNeedsInput.hidden = true;
  }
}

async function checkGaps() {
  const daysAhead = document.getElementById("days-ahead").value || 14;
  const res = await fetch(`/api/gaps?days_ahead=${daysAhead}`);
  const data = await res.json();
  const section = (title, items) => `
    <h3>${title}</h3>
    ${items.length ? `<ul>${items.map((i) => `<li>${i}</li>`).join("")}</ul>` : `<p class="muted">none</p>`}
  `;
  gapsOutput.innerHTML =
    `<p class="muted">As of ${data.as_of}</p>` +
    section("Missing required fields", data.missing_fields) +
    section("Past-due, not marked posted", data.past_due) +
    section(`Scheduling gaps of ${daysAhead}+ days`, data.gaps);
}

async function loadPerformance() {
  const res = await fetch("/api/performance");
  const data = await res.json();
  performanceBody.innerHTML = "";
  for (const row of data.entries) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.date}</td>
      <td>${row.content_type}</td>
      <td>${row.platform}</td>
      <td>${row.engagement_score}</td>
      <td>${row.notes || ""}</td>
    `;
    performanceBody.appendChild(tr);
  }
  recommendationEl.textContent = data.recommendation;
}

document.getElementById("check-gaps-btn").addEventListener("click", checkGaps);

document.getElementById("performance-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  performanceError.hidden = true;
  const form = e.target;
  const payload = {
    date: form.date.value,
    content_type: form.content_type.value,
    platform: form.platform.value,
    engagement_score: form.engagement_score.value,
    notes: form.notes.value,
  };
  const res = await fetch("/api/performance", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  if (!res.ok) {
    performanceError.hidden = false;
    performanceError.textContent = data.error;
    return;
  }
  form.reset();
  await loadPerformance();
});

loadCalendar();
checkGaps();
loadPerformance();

(function () {
  const data = JSON.parse(document.getElementById("dashboard-data").textContent);
  const csrf = document.body.dataset.csrf;
  const S = data.summary;
  const LEVELS = ["High", "Moderate", "Low"];
  const COLORS = { High: "#16a34a", Moderate: "#f59e0b", Low: "#dc2626" };

  // ---- Summary charts ----
  new Chart(document.getElementById("distChart"), {
    type: "doughnut",
    data: {
      labels: LEVELS,
      datasets: [{ data: LEVELS.map(l => S.counts[l]), backgroundColor: LEVELS.map(l => COLORS[l]) }],
    },
    options: { maintainAspectRatio: false },
  });

  new Chart(document.getElementById("levelChart"), {
    type: "bar",
    data: {
      labels: S.metrics.map(m => m.replace(/_/g, " ")),
      datasets: LEVELS.filter(l => S.by_level[l]).map(l => ({
        label: l,
        data: S.metrics.map(m => S.by_level[l][m]),
        backgroundColor: COLORS[l],
      })),
    },
    options: { maintainAspectRatio: false, scales: { y: { beginAtZero: true } } },
  });

  // ---- Digital twin ----
  const select = document.getElementById("employeeSelect");
  const slidersEl = document.getElementById("sliders");
  const profileEl = document.getElementById("profileTable");
  const SIM_FIELDS = ["Working_Hours", "Training_Hours", "Meeting_Hours", "Task_Delay_Count",
                      "Tasks_Completed", "Attendance", "Job_Satisfaction", "Project_Count"];
  const labelOf = Object.fromEntries(data.fields.map(f => [f.name, f.label]));
  const stepOf = Object.fromEntries(data.fields.map(f => [f.name, f.step]));

  let current = null;   // actual employee values
  let sim = null;       // simulated values

  data.employees.forEach(e => {
    const o = document.createElement("option");
    o.value = e.Employee_ID;
    o.textContent = e.Employee_ID;
    select.appendChild(o);
  });

  function probChart(canvasId) {
    return new Chart(document.getElementById(canvasId), {
      type: "bar",
      data: { labels: LEVELS, datasets: [{ data: [0, 0, 0], backgroundColor: LEVELS.map(l => COLORS[l]) }] },
      options: {
        maintainAspectRatio: false, plugins: { legend: { display: false } },
        scales: { y: { min: 0, max: 100, title: { display: true, text: "Probability (%)" } } },
      },
    });
  }
  const baseChart = probChart("baseChart");
  const simChart = probChart("simChart");

  async function predict(values) {
    const res = await fetch("/api/predict/", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
      body: JSON.stringify(values),
    });
    return res.json();
  }

  function show(result, chart, badgeId) {
    const b = document.getElementById(badgeId);
    b.textContent = result.level;
    b.className = "badge " + result.level.toLowerCase();
    chart.data.datasets[0].data = LEVELS.map(l => Math.round((result.probabilities[l] || 0) * 1000) / 10);
    chart.update();
  }

  function renderProfile() {
    const rows = [["Employee ID", current.Employee_ID]];
    data.fields.forEach(f => rows.push([f.label, current[f.name]]));
    if (current.Productivity_Level) rows.push(["Recorded level", current.Productivity_Level]);
    profileEl.innerHTML = rows.map(r => `<tr><th>${r[0]}</th><td>${r[1]}</td></tr>`).join("");
  }

  function renderSliders() {
    slidersEl.innerHTML = "";
    SIM_FIELDS.forEach(name => {
      const r = S.ranges[name];
      if (!r) return;
      const row = document.createElement("div");
      row.className = "slider-row";
      row.innerHTML = `<label><span>${labelOf[name]}</span><strong id="v_${name}">${sim[name]}</strong></label>
        <input type="range" id="s_${name}" min="${r.min}" max="${r.max}" step="${stepOf[name]}" value="${sim[name]}">`;
      slidersEl.appendChild(row);
      row.querySelector("input").addEventListener("input", ev => {
        sim[name] = parseFloat(ev.target.value);
        document.getElementById("v_" + name).textContent = sim[name];
        debounceSim();
      });
    });
  }

  let timer = null;
  function debounceSim() {
    clearTimeout(timer);
    timer = setTimeout(async () => show(await predict(sim), simChart, "simLevel"), 150);
  }

  async function loadEmployee(id) {
    current = data.employees.find(e => String(e.Employee_ID) === String(id));
    sim = Object.assign({}, current);
    renderProfile();
    renderSliders();
    const base = await predict(current);
    show(base, baseChart, "baseLevel");
    show(base, simChart, "simLevel");
  }

  select.addEventListener("change", () => loadEmployee(select.value));
  document.getElementById("resetBtn").addEventListener("click", () => loadEmployee(select.value));

  if (data.employees.length) loadEmployee(data.employees[0].Employee_ID);
})();

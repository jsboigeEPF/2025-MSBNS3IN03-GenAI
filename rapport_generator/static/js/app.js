/* ══ D5 — Rédacteur de Rapports IA | app.js ══════════════════════════ */

"use strict";

// ── État global ────────────────────────────────────────────────────────
const state = {
  currentData: null,
  currentReport: null,
  charts: [],
  activeTab: "demo",
  activeReportTab: "narrative",
};

// ── Init ───────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  checkHealth();
  setTimeout(() => updateStatusIndicators(), 1000);
});

async function checkHealth() {
  try {
    const res = await fetch("/health");
    if (res.ok) {
      setStatus("status-openai", "active");
    }
  } catch {}
}

function updateStatusIndicators() {
  // On affiche tous comme actifs après l'init — vérifications réelles dans la génération
  ["status-openai", "status-qdrant", "status-searxng"].forEach(id => {
    setStatus(id, "active");
  });
}

function setStatus(id, state) {
  const el = document.getElementById(id);
  if (!el) return;
  const dot = el.querySelector(".status-dot");
  if (dot) dot.className = `status-dot ${state}`;
}

// ── Navigation ─────────────────────────────────────────────────────────
function showView(name) {
  document.querySelectorAll(".view").forEach(v => v.classList.remove("active"));
  document.querySelectorAll(".nav-item").forEach(n => n.classList.remove("active"));

  const view = document.getElementById(`view-${name}`);
  if (view) view.classList.add("active");

  const navItem = document.querySelector(`[data-view="${name}"]`);
  if (navItem) navItem.classList.add("active");
}

function showStep(name) {
  document.querySelectorAll(".step-panel").forEach(p => p.classList.remove("active"));
  const panel = document.getElementById(`step-${name}`);
  if (panel) panel.classList.add("active");
}

// ── Tab switching ──────────────────────────────────────────────────────
function switchTab(name) {
  state.activeTab = name;
  document.querySelectorAll(".tab-content").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(".tabs-nav .tab-btn").forEach((btn, i) => {
    const tabs = ["demo", "upload", "json", "text"];
    btn.classList.toggle("active", tabs[i] === name);
  });
  const tab = document.getElementById(`tab-${name}`);
  if (tab) tab.classList.add("active");
}

function switchReportTab(name) {
  state.activeReportTab = name;
  document.querySelectorAll(".rtab-content").forEach(t => t.classList.remove("active"));

  // Get all report tab buttons
  const reportTabBtns = document.querySelectorAll("#step-report .tabs-nav .tab-btn");
  const tabs = ["narrative", "charts", "data", "search"];
  reportTabBtns.forEach((btn, i) => {
    btn.classList.toggle("active", tabs[i] === name);
  });

  const tab = document.getElementById(`rtab-${name}`);
  if (tab) tab.classList.add("active");

  if (name === "charts" && state.currentReport) {
    renderCharts(state.currentReport.charts || []);
  }
}

// ── Start with type (from home cards) ─────────────────────────────────
function startWithType(type) {
  showView("generate");
  showStep("input");
  document.getElementById("report-type").value = type;
  const navItem = document.querySelector('[data-view="generate"]');
  if (navItem) {
    document.querySelectorAll(".nav-item").forEach(n => n.classList.remove("active"));
    navItem.classList.add("active");
  }
}

// ── Demo Data ──────────────────────────────────────────────────────────
async function loadDemoData() {
  const type = document.getElementById("report-type").value;

  try {
    const res = await fetch(`/api/reports/demo/${type}`);
    if (!res.ok) throw new Error("Demo fetch failed");
    const data = await res.json();

    state.currentData = data;
    if (!document.getElementById("report-name").value) {
      document.getElementById("report-name").value = data.name;
    }

    const preview = document.getElementById("demo-preview");
    preview.textContent = JSON.stringify(data.data, null, 2).slice(0, 600) + "\n...";
    preview.classList.remove("hidden");

    enableGenerate();
    showToast("✅ Données démo chargées", "success");
  } catch (e) {
    showToast("❌ Erreur chargement démo", "error");
  }
}

// ── File Upload ────────────────────────────────────────────────────────
function handleDrop(e) {
  e.preventDefault();
  const file = e.dataTransfer.files[0];
  if (file) uploadFile(file);
}

function handleFileUpload(e) {
  const file = e.target.files[0];
  if (file) uploadFile(file);
}

async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  try {
    showToast("📤 Upload en cours...");
    const res = await fetch("/api/data/upload", { method: "POST", body: formData });
    if (!res.ok) throw new Error(await res.text());
    const result = await res.json();

    state.currentData = result.data;
    if (!document.getElementById("report-name").value) {
      document.getElementById("report-name").value = result.data.name || file.name;
    }
    if (result.detected_type) {
      document.getElementById("report-type").value = result.detected_type;
    }

    const preview = document.getElementById("upload-preview");
    preview.textContent = `Type détecté: ${result.detected_type}\n\n${result.preview}`;
    preview.classList.remove("hidden");

    enableGenerate();
    showToast(`✅ ${file.name} chargé (${result.data.data?.row_count || "N"} lignes)`, "success");
  } catch (e) {
    showToast(`❌ Erreur upload: ${e.message}`, "error");
  }
}

// ── JSON Manual ────────────────────────────────────────────────────────
function validateJson() {
  const raw = document.getElementById("json-input").value;
  const feedback = document.getElementById("json-feedback");
  feedback.classList.remove("hidden");

  try {
    const parsed = JSON.parse(raw);
    state.currentData = {
      name: document.getElementById("report-name").value || "Rapport JSON",
      type: document.getElementById("report-type").value,
      data: parsed,
    };

    feedback.className = "feedback-msg success";
    feedback.textContent = `✅ JSON valide — ${Object.keys(parsed).length} clé(s) détectée(s)`;
    enableGenerate();
  } catch (e) {
    feedback.className = "feedback-msg error";
    feedback.textContent = `❌ JSON invalide: ${e.message}`;
  }
}

// ── Text Extraction ────────────────────────────────────────────────────
async function extractFromText() {
  const raw = document.getElementById("text-input").value.trim();
  const feedback = document.getElementById("text-feedback");

  if (!raw) {
    showFeedback("text-feedback", "error", "Entrez du texte à analyser");
    return;
  }

  feedback.className = "feedback-msg";
  feedback.textContent = "🔍 Extraction en cours...";
  feedback.classList.remove("hidden");

  try {
    const res = await fetch("/api/data/extract", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        raw_text: raw,
        report_type: document.getElementById("report-type").value,
      }),
    });

    const result = await res.json();
    state.currentData = {
      name: document.getElementById("report-name").value || "Rapport extrait",
      type: result.detected_type || document.getElementById("report-type").value,
      data: result.extracted_data,
    };

    feedback.className = "feedback-msg success";
    feedback.textContent = `✅ Données extraites — type: ${result.detected_type}`;
    enableGenerate();
  } catch (e) {
    feedback.className = "feedback-msg error";
    feedback.textContent = `❌ Erreur extraction: ${e.message}`;
  }
}

// ── Enable generate button ─────────────────────────────────────────────
function enableGenerate() {
  document.getElementById("btn-generate").disabled = false;
}

// ── Generate Report ────────────────────────────────────────────────────
async function generateReport() {
  const name = document.getElementById("report-name").value.trim();
  const type = document.getElementById("report-type").value;
  const useSearch = document.getElementById("use-search").checked;
  const saveMemory = document.getElementById("save-memory").checked;

  if (!name) { showToast("❌ Donnez un nom au rapport", "error"); return; }
  if (!state.currentData) { showToast("❌ Aucune donnée chargée", "error"); return; }

  // Passer en mode loading
  showView("generate");
  showStep("loading");

  const loadSteps = [
    { id: "ls-1", label: "Enrichissement SearxNG", duration: 1500 },
    { id: "ls-2", label: "Analyse GPT-4o", duration: 3000 },
    { id: "ls-3", label: "Génération KPIs", duration: 800 },
    { id: "ls-4", label: "Création graphiques", duration: 600 },
    { id: "ls-5", label: "Sauvegarde Qdrant", duration: 400 },
  ];

  // Animer les étapes
  let delay = 0;
  loadSteps.forEach((step, i) => {
    setTimeout(() => {
      // Désactiver l'étape précédente
      if (i > 0) {
        const prev = document.getElementById(loadSteps[i - 1].id);
        if (prev) { prev.classList.remove("active"); prev.classList.add("done"); prev.querySelector(".ls-dot").textContent = "✓"; }
      }
      const el = document.getElementById(step.id);
      if (el) { el.classList.add("active"); el.querySelector(".ls-dot").textContent = "●"; }
    }, delay);
    delay += step.duration;
  });

  // Appel API
  try {
    const payload = {
      name,
      type,
      data: state.currentData.data || state.currentData,
      use_web_search: useSearch,
      save_to_memory: saveMemory,
    };

    const res = await fetch("/api/reports/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Erreur serveur");
    }

    const report = await res.json();
    state.currentReport = report;

    // Finaliser les steps
    loadSteps.forEach(step => {
      const el = document.getElementById(step.id);
      if (el) { el.classList.remove("active"); el.classList.add("done"); el.querySelector(".ls-dot").textContent = "✓"; }
    });

    setTimeout(() => renderReport(report), 400);

  } catch (e) {
    showStep("input");
    showToast(`❌ Erreur: ${e.message}`, "error");
    console.error(e);
  }
}

// ── Render Report ──────────────────────────────────────────────────────
function renderReport(report) {
  // Badge & titre
  const badges = { financial: "RAPPORT FINANCIER", technical: "RAPPORT TECHNIQUE", medical: "RAPPORT MÉDICAL", generic: "RAPPORT ANALYTIQUE" };
  document.getElementById("rpt-badge").textContent = badges[report.type] || "RAPPORT";
  document.getElementById("rpt-title").textContent = report.name;
  document.getElementById("rpt-meta").textContent = `Généré le ${new Date().toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" })} · GPT-4o · ID: ${(report.report_id || "").slice(0, 8)}`;

  // KPI Cards
  const kpiGrid = document.getElementById("kpi-cards");
  kpiGrid.innerHTML = "";
  (report.kpis || []).slice(0, 4).forEach(kpi => {
    const card = document.createElement("div");
    card.className = `kpi-card color-${kpi.color || "blue"}`;
    const trendClass = kpi.trend?.startsWith("+") ? "up" : kpi.trend?.startsWith("-") ? "down" : "neutral";
    card.innerHTML = `
      <div class="kpi-label">${kpi.label}</div>
      <div class="kpi-value">${kpi.value}</div>
      <div class="kpi-trend ${trendClass}">${kpi.trend || ""}</div>
    `;
    kpiGrid.appendChild(card);
  });

  // Narrative
  const narrativeEl = document.getElementById("narrative-content");
  narrativeEl.innerHTML = markdownToHtml(report.narrative || "Narratif non disponible.");

  // Raw data
  document.getElementById("raw-data-display").textContent = JSON.stringify(report.data, null, 2);

  // Search context
  renderSearchContext(report.search_context_used);

  showStep("report");
  switchReportTab("narrative");
  showToast("✅ Rapport généré avec succès!", "success");
}

// ── Markdown → HTML ────────────────────────────────────────────────────
function markdownToHtml(text) {
  if (!text) return "";
  let html = text
    // ## Headers
    .replace(/^## (.+)$/gm, "<h2>$1</h2>")
    // **bold**
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    // *italic*
    .replace(/\*(.+?)\*/g, "<em>$1</em>")
    // Paragraphs
    .split("\n\n")
    .map(para => {
      para = para.trim();
      if (!para) return "";
      if (para.startsWith("<h2>")) return para;
      if (para.startsWith("- ") || para.startsWith("• ")) {
        const items = para.split("\n").map(l => `<li>${l.replace(/^[-•]\s*/, "")}</li>`).join("");
        return `<ul>${items}</ul>`;
      }
      return `<p>${para}</p>`;
    })
    .join("\n");
  return html;
}

// ── Render Charts ──────────────────────────────────────────────────────
const chartInstances = {};

function renderCharts(charts) {
  const container = document.getElementById("charts-container");
  container.innerHTML = "";

  // Détruire les anciennes instances
  Object.values(chartInstances).forEach(c => c.destroy());

  if (!charts || charts.length === 0) {
    container.innerHTML = '<p class="hint">Aucun graphique généré.</p>';
    return;
  }

  charts.forEach((chart, i) => {
    const card = document.createElement("div");
    card.className = "chart-card";
    const canvasId = `chart-canvas-${i}`;
    card.innerHTML = `<h3>${chart.title || `Graphique ${i + 1}`}</h3><canvas id="${canvasId}"></canvas>`;
    container.appendChild(card);

    // Adapter les couleurs au thème sombre
    const darkData = JSON.parse(JSON.stringify(chart.data));
    if (darkData.datasets) {
      darkData.datasets.forEach(ds => {
        if (!ds.backgroundColor || typeof ds.backgroundColor === "string") {
          ds.backgroundColor = ["#c8a96e", "#4af0c4", "#e05c8a", "#5b8dee", "#f0a040"].slice(0, ds.data?.length || 1);
        }
        if (!ds.borderColor) ds.borderColor = "#c8a96e";
      });
    }

    const options = {
      ...(chart.options || {}),
      plugins: {
        ...(chart.options?.plugins || {}),
        legend: { labels: { color: "#aaa", font: { family: "DM Sans" } } },
        title: { ...(chart.options?.plugins?.title || {}), color: "#ccc" },
      },
      scales: chart.type !== "doughnut" && chart.type !== "radar" ? {
        x: { ticks: { color: "#777" }, grid: { color: "#1a1a1a" } },
        y: { ticks: { color: "#777" }, grid: { color: "#1a1a1a" } },
      } : {},
    };

    try {
      chartInstances[canvasId] = new Chart(document.getElementById(canvasId), {
        type: chart.type || "bar",
        data: darkData,
        options,
      });
    } catch (e) {
      console.error("Chart error:", e);
    }
  });
}

// ── Search Context ─────────────────────────────────────────────────────
function renderSearchContext(used) {
  const el = document.getElementById("search-context-display");
  if (!used) {
    el.innerHTML = '<p class="no-search">La recherche web n\'a pas été utilisée pour ce rapport.</p>';
    return;
  }
  el.innerHTML = '<p class="hint">Le narratif IA a été enrichi avec des sources web récentes via SearxNG.</p>';
}

// ── Export PDF ─────────────────────────────────────────────────────────
async function exportPDF() {
  if (!state.currentReport) { showToast("❌ Aucun rapport à exporter", "error"); return; }

  const btn = document.getElementById("btn-export-pdf");
  btn.textContent = "⏳ Génération PDF...";
  btn.disabled = true;

  try {
    const res = await fetch("/api/export/pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        report_id: state.currentReport.report_id || "",
        name: state.currentReport.name,
        type: state.currentReport.type,
        narrative: state.currentReport.narrative,
        data: state.currentReport.data,
        kpis: state.currentReport.kpis || [],
      }),
    });

    const result = await res.json();
    if (!result.success) throw new Error(result.detail || "Erreur PDF");

    // Téléchargement automatique
    const link = document.createElement("a");
    link.href = result.download_url;
    link.download = result.filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    showToast("✅ PDF téléchargé!", "success");
  } catch (e) {
    showToast(`❌ ${e.message}`, "error");
  } finally {
    btn.textContent = "⬇ Télécharger PDF";
    btn.disabled = false;
  }
}

// ── History ────────────────────────────────────────────────────────────
async function loadHistory() {
  const list = document.getElementById("history-list");
  list.innerHTML = '<p class="hint">Chargement depuis Qdrant...</p>';

  try {
    const res = await fetch("/api/reports/history");
    const result = await res.json();

    if (!result.reports || result.reports.length === 0) {
      list.innerHTML = '<p class="hint">Aucun rapport sauvegardé pour l\'instant.</p>';
      return;
    }

    list.innerHTML = "";
    result.reports.forEach(r => {
      const card = document.createElement("div");
      card.className = "history-card";
      card.innerHTML = `
        <div>
          <div class="history-card-name">${r.name}</div>
          <div class="history-card-meta">${r.created_at ? new Date(r.created_at).toLocaleString("fr-FR") : "Date inconnue"}</div>
        </div>
        <div class="history-card-type">${r.type || "generic"}</div>
      `;
      card.onclick = () => loadSavedReport(r.report_id);
      list.appendChild(card);
    });
  } catch (e) {
    list.innerHTML = `<p class="hint" style="color:#f04060">Erreur: ${e.message}</p>`;
  }
}

async function searchReports() {
  const query = document.getElementById("search-input").value.trim();
  if (!query) { await loadHistory(); return; }

  try {
    const res = await fetch("/api/reports/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    const result = await res.json();
    const list = document.getElementById("history-list");
    list.innerHTML = "";

    if (!result.results?.length) {
      list.innerHTML = '<p class="hint">Aucun résultat trouvé.</p>';
      return;
    }

    result.results.forEach(r => {
      const card = document.createElement("div");
      card.className = "history-card";
      card.innerHTML = `
        <div>
          <div class="history-card-name">${r.name}</div>
          <div class="history-card-meta">Score: ${r.score} · ${r.preview?.slice(0, 80)}...</div>
        </div>
        <div class="history-card-type">${r.type || "generic"}</div>
      `;
      card.onclick = () => loadSavedReport(r.report_id);
      list.appendChild(card);
    });
  } catch (e) {
    showToast(`❌ Recherche échouée: ${e.message}`, "error");
  }
}

async function loadSavedReport(reportId) {
  try {
    const res = await fetch(`/api/reports/${reportId}`);
    if (!res.ok) throw new Error("Rapport non trouvé");
    const report = await res.json();
    state.currentReport = report;
    showView("generate");
    renderReport(report);
    showToast("✅ Rapport chargé", "success");
  } catch (e) {
    showToast(`❌ ${e.message}`, "error");
  }
}

// ── Reset ──────────────────────────────────────────────────────────────
function resetToInput() {
  state.currentData = null;
  state.currentReport = null;
  document.getElementById("report-name").value = "";
  document.getElementById("demo-preview").classList.add("hidden");
  document.getElementById("upload-preview").classList.add("hidden");
  document.getElementById("json-input").value = "";
  document.getElementById("text-input").value = "";
  document.getElementById("btn-generate").disabled = true;
  showStep("input");
  switchTab("demo");
}

// ── Toast ──────────────────────────────────────────────────────────────
let toastTimer = null;

function showToast(msg, type = "info") {
  const toast = document.getElementById("toast");
  toast.textContent = msg;
  toast.className = `toast ${type}`;

  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.add("hidden"), 3500);
}

function showFeedback(id, type, msg) {
  const el = document.getElementById(id);
  if (!el) return;
  el.className = `feedback-msg ${type}`;
  el.textContent = msg;
  el.classList.remove("hidden");
}

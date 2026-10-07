// Pre-filled samples matching report screenshots
const SAMPLES = {
    real: "ISRO successfully launches PSLV-C51, placing multiple satellites into orbit.",
    fake: "Joseph Vijay is the Chief Minister of Tamil Nadu."
};

function fillSample(type) {
    if (SAMPLES[type]) {
        document.getElementById('news-input').value = SAMPLES[type];
    }
}

// Tab Switching
function showTab(tabName) {
    document.getElementById('page-home').classList.add('d-none');
    document.getElementById('page-history').classList.add('d-none');
    document.getElementById('page-about').classList.add('d-none');

    document.getElementById('nav-home').classList.remove('active');
    document.getElementById('nav-history').classList.remove('active');
    document.getElementById('nav-about').classList.remove('active');

    document.getElementById('page-' + tabName).classList.remove('d-none');
    document.getElementById('nav-' + tabName).classList.add('active');

    if (tabName === 'history') {
        renderHistoryTable();
    }
}

// Prediction Form Submission
document.getElementById('news-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const text = document.getElementById('news-input').value.trim();
    if (!text) {
        alert("Please enter a news headline or article.");
        return;
    }

    const btn = document.getElementById('submit-btn');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Verifying Evidence...';

    try {
        const res = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });
        const data = await res.json();

        if (data.error) {
            alert(data.error);
        } else {
            renderVerificationCard(text, data);
            saveToHistory(text, data);
        }
    } catch (err) {
        alert("Error connecting to verification server: " + err.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-search me-2"></i>Check News';
    }
});

// Render Multi-Source Evidence Verification Result Card (Requirement #20)
function renderVerificationCard(text, data) {
    const container = document.getElementById('result-container');
    const verdict = data.verdict || data.label || 'UNVERIFIED';
    const conf = (data.confidence || 0).toFixed(1);

    let cardClass = "result-card-unverified";
    let badgeClass = "badge-unverified";
    let iconClass = "bi-question-lg";
    let verdictTitle = "UNVERIFIED";

    if (verdict === 'TRUE') {
        cardClass = "result-card-real";
        badgeClass = "bg-success";
        iconClass = "bi-check-lg";
        verdictTitle = "VERDICT: TRUE";
    } else if (verdict === 'FALSE') {
        cardClass = "result-card-fake";
        badgeClass = "bg-danger";
        iconClass = "bi-x-lg";
        verdictTitle = "VERDICT: FALSE";
    } else if (verdict === 'PARTIALLY TRUE') {
        cardClass = "result-card-warning";
        badgeClass = "bg-warning text-dark";
        iconClass = "bi-exclamation-triangle-fill";
        verdictTitle = "VERDICT: PARTIALLY TRUE";
    } else if (verdict === 'MISLEADING') {
        cardClass = "result-card-warning";
        badgeClass = "bg-warning text-dark";
        iconClass = "bi-exclamation-circle-fill";
        verdictTitle = "VERDICT: MISLEADING";
    } else if (verdict === 'QUESTION_ANSWER' || verdict === 'ANSWER') {
        cardClass = "result-card-info";
        badgeClass = "bg-info text-dark";
        iconClass = "bi-lightbulb-fill";
        verdictTitle = "QUESTION ANSWER";
    } else if (verdict === 'OPINION' || verdict === 'STATEMENT') {
        cardClass = "result-card-info";
        badgeClass = "bg-secondary";
        iconClass = "bi-chat-quote-fill";
        verdictTitle = "VERDICT: OPINION STATEMENT";
    }

    // Render Evidence Items
    let evidenceHTML = '';
    if (data.evidence && data.evidence.length > 0) {
        data.evidence.forEach((ev, idx) => {
            const urlLink = ev.url ? `<a href="${ev.url}" target="_blank" class="small text-primary me-2"><i class="bi bi-link-45deg"></i>View Source</a>` : '';
            evidenceHTML += `
            <div class="evidence-item mb-2 p-2 rounded bg-white border">
                <div class="d-flex justify-content-between align-items-center mb-1">
                    <strong class="small text-dark">[Source ${idx + 1}] ${ev.source || 'Verified Archive'}</strong>
                    <span class="badge bg-primary-subtle text-primary border border-primary-subtle small">${ev.credibility || 'High'} Credibility</span>
                </div>
                <p class="small text-secondary mb-1">${ev.snippet || ''}</p>
                ${urlLink}
            </div>
            `;
        });
    } else {
        evidenceHTML = '<p class="small text-muted mb-0">No external source links available.</p>';
    }

    // Render Entities Badges
    let entitiesHTML = '';
    if (data.entities && Object.keys(data.entities).length > 0) {
        for (const [k, v] of Object.entries(data.entities)) {
            entitiesHTML += `<span class="badge bg-secondary me-1 mb-1">${k}: ${v}</span> `;
        }
    }

    const html = `
    <div class="${cardClass} shadow-sm">
        <div class="d-flex align-items-center justify-content-between mb-3">
            <div class="d-flex align-items-center gap-3">
                <div class="${verdict === 'TRUE' ? 'result-icon-real' : (verdict === 'FALSE' ? 'result-icon-fake' : 'result-icon-info')}">
                    <i class="bi ${iconClass}"></i>
                </div>
                <div>
                    <h3 class="${verdict === 'TRUE' ? 'result-title-real' : (verdict === 'FALSE' ? 'result-title-fake' : 'text-primary')} mb-0">${verdictTitle}</h3>
                    <div class="text-muted small">Confidence Score: <strong>${conf}%</strong></div>
                </div>
            </div>
            <span class="badge ${badgeClass} fs-6 px-3 py-2 rounded-pill">${verdict}</span>
        </div>

        <div class="quote-box">
            <strong>Claim Analyzed:</strong> "${text}"
        </div>

        <div class="explanation-box p-3 rounded bg-white border mb-3">
            <h6 class="fw-bold mb-1 text-dark"><i class="bi bi-patch-question-fill text-primary me-2"></i>Explanation & Reasoning:</h6>
            <p class="mb-0 text-secondary small">${data.explanation || 'Analyzed against factual evidence.'}</p>
            ${entitiesHTML ? `<div class="mt-2"><small class="fw-semibold text-muted d-block mb-1">Extracted Entities:</small>${entitiesHTML}</div>` : ''}
        </div>

        <div class="details-box">
            <h6 class="fw-bold mb-2"><i class="bi bi-shield-check text-success me-2"></i>Evidence Sources (${data.source_credibility || 'High'} Credibility)</h6>
            ${evidenceHTML}
            <div class="text-end text-muted small mt-2">Verified at: ${data.verification_time || new Date().toLocaleString()}</div>
        </div>
    </div>
    `;

    container.innerHTML = html;
    container.classList.remove('d-none');
    container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Save Prediction to History (localStorage)
function saveToHistory(text, data) {
    let history = JSON.parse(localStorage.getItem('fake_news_history') || '[]');
    const now = new Date();
    const timeStr = now.toISOString().split('T')[0] + ' ' + now.toTimeString().split(' ')[0].substring(0, 5);
    const verdict = data.verdict || data.label || 'UNVERIFIED';

    history.unshift({
        text: text,
        prediction: verdict,
        confidence: (data.confidence || 0).toFixed(1) + '%',
        datetime: timeStr
    });

    if (history.length > 30) history.pop();
    localStorage.setItem('fake_news_history', JSON.stringify(history));
}

// Render History Table
function renderHistoryTable() {
    const tbody = document.getElementById('history-body');
    let history = JSON.parse(localStorage.getItem('fake_news_history') || '[]');

    if (history.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="text-center py-4 text-muted">No prediction history recorded yet. Test some news on the Home tab!</td></tr>`;
        return;
    }

    let rows = '';
    history.forEach((item, index) => {
        let badgeClass = 'badge-unverified';
        if (item.prediction === 'TRUE' || item.prediction === 'REAL') badgeClass = 'badge-real';
        else if (item.prediction === 'FALSE' || item.prediction === 'FAKE') badgeClass = 'badge-fake';
        else if (item.prediction === 'PARTIALLY TRUE' || item.prediction === 'MISLEADING') badgeClass = 'badge-warning';

        rows += `
        <tr>
            <td>${index + 1}</td>
            <td class="text-truncate" style="max-width: 380px;">${item.text}</td>
            <td><span class="${badgeClass}">${item.prediction}</span></td>
            <td><strong>${item.confidence}</strong></td>
            <td class="text-muted small">${item.datetime}</td>
        </tr>
        `;
    });
    tbody.innerHTML = rows;
}

function clearHistory() {
    if (confirm("Are you sure you want to clear prediction history?")) {
        localStorage.removeItem('fake_news_history');
        renderHistoryTable();
    }
}

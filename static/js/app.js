// Pre-filled samples matching report screenshots
const SAMPLES = {
    real: "ISRO successfully launches PSLV-C51, placing multiple satellites into orbit.",
    fake: "Government to give free laptops to all students across the country next month."
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
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Checking...';

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
            renderResultCard(text, data);
            saveToHistory(text, data);
        }
    } catch (err) {
        alert("Error connecting to prediction server: " + err.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-search me-2"></i>Check News';
    }
});

// Render Result Card matching report screenshot design
function renderResultCard(text, data) {
    const container = document.getElementById('result-container');
    const isReal = data.label === 'REAL';
    const conf = data.confidence.toFixed(1);

    let html = '';

    if (isReal) {
        html = `
        <div class="result-card-real shadow-sm">
            <div class="d-flex align-items-center gap-3 mb-2">
                <div class="result-icon-real">
                    <i class="bi bi-check-lg"></i>
                </div>
                <div>
                    <h3 class="result-title-real">Real News</h3>
                    <div class="text-muted small">Confidence: <strong>${conf}%</strong></div>
                </div>
            </div>

            <div class="quote-box">
                "${text}"
            </div>

            <div class="details-box">
                <h6 class="fw-bold mb-2">Prediction Details</h6>
                <div class="detail-row">
                    <span class="detail-label">Prediction</span>
                    <span class="detail-val text-success">Real</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Confidence Score</span>
                    <span class="detail-val">${conf}%</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Model Used</span>
                    <span class="detail-val">Passive-Aggressive (TF-IDF)</span>
                </div>
            </div>
        </div>
        `;
    } else {
        html = `
        <div class="result-card-fake shadow-sm">
            <div class="d-flex align-items-center gap-3 mb-2">
                <div class="result-icon-fake">
                    <i class="bi bi-x-lg"></i>
                </div>
                <div>
                    <h3 class="result-title-fake">Fake News</h3>
                    <div class="text-muted small">Confidence: <strong>${conf}%</strong></div>
                </div>
            </div>

            <div class="quote-box">
                "${text}"
            </div>

            <div class="details-box">
                <h6 class="fw-bold mb-2">Prediction Details</h6>
                <div class="detail-row">
                    <span class="detail-label">Prediction</span>
                    <span class="detail-val text-danger">Fake</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Confidence Score</span>
                    <span class="detail-val">${conf}%</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Model Used</span>
                    <span class="detail-val">Passive-Aggressive (TF-IDF)</span>
                </div>
            </div>
        </div>
        `;
    }

    container.innerHTML = html;
    container.classList.remove('d-none');
    container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Save Prediction to History (localStorage)
function saveToHistory(text, data) {
    let history = JSON.parse(localStorage.getItem('fake_news_history') || '[]');
    const now = new Date();
    const timeStr = now.toISOString().split('T')[0] + ' ' + now.toTimeString().split(' ')[0].substring(0, 5);

    history.unshift({
        text: text,
        prediction: data.label,
        confidence: data.confidence.toFixed(1) + '%',
        datetime: timeStr
    });

    // Keep max 20 entries
    if (history.length > 20) history.pop();
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
        const badgeClass = item.prediction === 'REAL' ? 'badge-real' : 'badge-fake';
        const predText = item.prediction === 'REAL' ? 'Real' : 'Fake';

        rows += `
        <tr>
            <td>${index + 1}</td>
            <td class="text-truncate" style="max-width: 380px;">${item.text}</td>
            <td><span class="${badgeClass}">${predText}</span></td>
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

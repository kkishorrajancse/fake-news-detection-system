const SAMPLES = {
    real: {
        title: "NASA James Webb Space Telescope discovers oldest known galaxy",
        text: "Astronomers using the James Webb Space Telescope have identified a galaxy that formed just 300 million years after the Big Bang. Peer-reviewed findings published in Nature confirm spectral measurements consistent with early cosmic expansion."
    },
    fake: {
        title: "Secret miracle root cures all forms of cancer in 48 hours big pharma does not want you to know",
        text: "Doctors are stunned! This ancient mountain herb destroys every cancer cell in two days. Government scientists are hiding the miracle remedy to protect pharmaceutical trillion-dollar profits. Order now before it is banned worldwide!"
    }
};

function loadSample(type) {
    if (SAMPLES[type]) {
        document.getElementById('newsTitle').value = SAMPLES[type].title;
        document.getElementById('newsText').value = SAMPLES[type].text;
        hideResults();
    }
}

function hideResults() {
    document.getElementById('resultCard').classList.add('d-none');
    document.getElementById('errorAlert').classList.add('d-none');
}

// Form submission handler
document.getElementById('detectForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    hideResults();

    const title = document.getElementById('newsTitle').value.trim();
    const text = document.getElementById('newsText').value.trim();

    if (!text && !title) {
        showError("Please enter a headline or article content to analyze.");
        return;
    }

    const analyzeBtn = document.getElementById('analyzeBtn');
    const analyzeSpinner = document.getElementById('analyzeSpinner');
    const analyzeIcon = document.getElementById('analyzeIcon');

    // UI Loading state
    analyzeBtn.disabled = true;
    analyzeSpinner.classList.remove('d-none');
    analyzeIcon.classList.add('d-none');

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, text })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to analyze article.");
        }

        displayResult(data);
    } catch (err) {
        showError(err.message);
    } finally {
        analyzeBtn.disabled = false;
        analyzeSpinner.classList.add('d-none');
        analyzeIcon.classList.remove('d-none');
    }
});

function displayResult(data) {
    const card = document.getElementById('resultCard');
    const badge = document.getElementById('verdictBadge');
    const title = document.getElementById('verdictTitle');
    const desc = document.getElementById('verdictDesc');
    const conf = document.getElementById('confidenceText');
    const probRealVal = document.getElementById('probRealVal');
    const probRealBar = document.getElementById('probRealBar');
    const probFakeVal = document.getElementById('probFakeVal');
    const probFakeBar = document.getElementById('probFakeBar');
    const keywordsBadges = document.getElementById('keywordsBadges');

    const isReal = data.label === 'REAL';

    card.className = "mt-4 p-4 rounded-3 " + (isReal ? "bg-real" : "bg-fake");
    card.classList.remove('d-none');

    if (isReal) {
        badge.className = "badge bg-success fs-5 px-3 py-2 rounded-pill";
        badge.innerHTML = '<i class="bi bi-check-circle-fill me-1"></i> VERIFIED REAL NEWS';
        title.className = "fw-bold mb-2 text-success";
        title.innerText = "Likely Authentic & Verified";
        desc.innerText = "Linguistic syntax, source markers, and lexical distribution indicate authentic news reporting.";
    } else {
        badge.className = "badge bg-danger fs-5 px-3 py-2 rounded-pill";
        badge.innerHTML = '<i class="bi bi-exclamation-octagon-fill me-1"></i> FLAGGED AS FAKE NEWS';
        title.className = "fw-bold mb-2 text-danger";
        title.innerText = "Sensationalist or Misleading Content";
        desc.innerText = "Contains emotional triggers, exaggerations, or phrasing patterns characteristic of unreliable or fabricated stories.";
    }

    conf.innerText = `Confidence: ${data.confidence}%`;
    probRealVal.innerText = `${data.probability_real}%`;
    probRealBar.style.width = `${data.probability_real}%`;
    probFakeVal.innerText = `${data.probability_fake}%`;
    probFakeBar.style.width = `${data.probability_fake}%`;

    // Render keyword badges
    keywordsBadges.innerHTML = "";
    if (data.key_tokens && data.key_tokens.length > 0) {
        data.key_tokens.forEach(tok => {
            const span = document.createElement('span');
            span.className = "badge-keyword";
            span.innerText = tok;
            keywordsBadges.appendChild(span);
        });
    } else {
        keywordsBadges.innerHTML = '<span class="text-muted small">No specific keyword bias detected.</span>';
    }

    // Scroll smoothly to results
    card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showError(msg) {
    const alert = document.getElementById('errorAlert');
    alert.innerText = msg;
    alert.classList.remove('d-none');
}

async function triggerTrain() {
    const icon = document.getElementById('trainIcon');
    if (icon) icon.classList.add('spin-animation');

    if (!confirm("Start model training now? This will train on the dataset and update metrics.")) {
        if (icon) icon.classList.remove('spin-animation');
        return;
    }

    try {
        const res = await fetch('/train', { method: 'POST' });
        const data = await res.json();
        if (data.success && data.metrics) {
            alert(`🎉 Training Completed Successfully! Model accuracy: ${data.metrics.accuracy}%`);
            window.location.reload();
        } else {
            alert("Training Error: " + (data.error || "Unknown issue"));
        }
    } catch (e) {
        alert("Failed to connect to training server: " + e.message);
    } finally {
        if (icon) icon.classList.remove('spin-animation');
    }
}

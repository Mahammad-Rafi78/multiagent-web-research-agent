const questionInput = document.getElementById('question');
const submitBtn = document.getElementById('submitBtn');
const demoBtn = document.getElementById('demoBtn');
const loading = document.getElementById('loading');
const resultContent = document.getElementById('resultContent');
const errorBox = document.getElementById('errorBox');
const resultState = document.querySelector('.result-state');
const suggestions = document.querySelectorAll('.suggestion');
const themeToggle = document.getElementById('themeToggle');
const themeIcon = themeToggle.querySelector('.theme-icon');

const demoQuestion = 'What are the main advantages and limitations of retrieval-augmented generation compared with fine-tuning for enterprise AI applications?';
const isStaticDeployment = window.location.hostname.endsWith('github.io');

const staticDemoResult = (question) => ({
  demo_mode: true,
  question,
  answer: 'This free static deployment provides a demo response. A live deployment uses the FastAPI service to search multiple providers, compare evidence, and synthesize a cited answer.',
  supporting_claims: [
    'Using independent providers reduces dependence on a single search ecosystem.',
    'Evidence-aware synthesis is more reliable than a one-shot search-to-answer chain.',
    'Conflict and uncertainty reporting improves trustworthiness.'
  ],
  references: [
    { id: 'S1', title: 'Demo evidence note', url: 'https://example.com/demo' },
    { id: 'S2', title: 'Research design overview', url: 'https://example.com/design' }
  ],
  conflicts: [{ details: 'No conflicting evidence detected in this demo run.' }],
  missing_evidence: ['Live provider data is unavailable in the static deployment.'],
  research_run: { queries: [question], providers_attempted: ['demo'], sources_fetched: 0 }
});

function setTheme(theme) {
  const isLight = theme === 'light';
  document.body.classList.toggle('theme-light', isLight);
  themeIcon.textContent = isLight ? '☾' : '☼';
  themeToggle.setAttribute('aria-label', isLight ? 'Switch to dark mode' : 'Switch to light mode');
  localStorage.setItem('zephra-theme', isLight ? 'light' : 'dark');
}

setTheme(localStorage.getItem('zephra-theme') || 'dark');
themeToggle.addEventListener('click', () => {
  setTheme(document.body.classList.contains('theme-light') ? 'dark' : 'light');
});

function setLoadingState(isLoading) {
  loading.classList.toggle('hidden', !isLoading);
  submitBtn.disabled = isLoading;
  submitBtn.textContent = isLoading ? 'Researching...' : 'Run research';
  resultState.textContent = isLoading ? 'Investigating...' : resultState.textContent;
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.remove('hidden');
}

function clearError() {
  errorBox.textContent = '';
  errorBox.classList.add('hidden');
}

function renderResult(data) {
  const refs = (data.references || []).map((ref) => `
    <li>
      <strong>[${ref.id}]</strong> ${ref.title}<span class="reference-provider">${ref.provider || 'source'}</span><br />
      <a href="${ref.url}" target="_blank" rel="noreferrer">${ref.url}</a>
    </li>
  `).join('');

  const claims = (data.supporting_claims || []).map((claim) => `<li>${claim}</li>`).join('');
  const conflicts = (data.conflicts || []).map((item) => `<li>${item.details}</li>`).join('') || '<li>No conflicts detected.</li>';
  const missing = (data.missing_evidence || []).map((item) => `<li>${item}</li>`).join('') || '<li>No obvious missing evidence flagged.</li>';

  resultContent.innerHTML = `
    <div class="answer-card">
      <span class="badge ${data.demo_mode ? 'demo' : 'live'}">${data.demo_mode ? 'demo mode' : 'live evidence'}</span>
      <h3>Answer</h3>
      <p>${(data.answer || '').replace(/\n/g, '<br />')}</p>
    </div>

    <div class="meta-card">
      <h3>Research run</h3>
      <p><strong>Queries:</strong> ${data.research_run?.queries?.length || 0}</p>
      <p><strong>Providers:</strong> ${(data.research_run?.providers_attempted || []).join(', ') || 'N/A'}</p>
      <p><strong>Sources fetched:</strong> ${data.research_run?.sources_fetched || 0}</p>
    </div>

    <div class="answer-card">
      <h3>Supporting claims</h3>
      <ul class="supporting-list">${claims || '<li>No supporting claims returned.</li>'}</ul>
    </div>

    <div class="reference-card">
      <h3>References</h3>
      <ul class="reference-list">${refs || '<li>No references available.</li>'}</ul>
    </div>

    <div class="conflict-card">
      <h3>Conflicts</h3>
      <ul class="conflict-list">${conflicts}</ul>
    </div>

    <div class="conflict-card">
      <h3>Uncertainty / missing evidence</h3>
      <p class="uncertainty-text">${data.uncertainty || 'No uncertainty statement returned.'}</p>
      <ul class="conflict-list">${missing}</ul>
    </div>
  `;
}

async function runResearch(question) {
  clearError();
  setLoadingState(true);

  try {
    if (isStaticDeployment) {
      renderResult(staticDemoResult(question));
      resultState.textContent = 'Static demo response';
      return;
    }

    const response = await fetch('./api/research', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    });

    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || 'Research failed.');
    }

    renderResult(payload);
    resultState.textContent = payload.demo_mode ? 'Demo response' : 'Live response';
  } catch (error) {
    const payload = staticDemoResult(question);
    renderResult(payload);
    resultState.textContent = 'Static demo response';
  } finally {
    setLoadingState(false);
  }
}

submitBtn.addEventListener('click', () => {
  const question = questionInput.value.trim();
  if (!question) {
    showError('Please enter a research question first.');
    return;
  }
  runResearch(question);
});

demoBtn.addEventListener('click', () => {
  questionInput.value = demoQuestion;
  runResearch(demoQuestion);
});

suggestions.forEach((suggestion) => {
  suggestion.addEventListener('click', () => {
    questionInput.value = suggestion.dataset.question || '';
    questionInput.focus();
  });
});

/* diagnostico.js — lógica de steps, validação, resultado e integração com I18N */

const TOTAL_STEPS = 4;
let currentStep = 1;
const respostas = {};

// Armazena o último resultado para re-renderização em troca de idioma
let ultimoResultado = null;

/* ── Utilitários ── */

function getStep(n) {
  return document.querySelector(`.diag-step[data-step="${n}"]`);
}

function updateProgress(step) {
  const pct = Math.round((step / TOTAL_STEPS) * 100);
  const bar = document.getElementById('progressBar');
  const label = document.getElementById('progressLabel');

  if (bar) bar.style.setProperty('--progress', pct + '%');

  if (label && window.I18N && window.I18N.translations) {
    if (step < TOTAL_STEPS) {
      const template = I18N.t('diagnostic.progressQuestion') || 'Pergunta {step} de {total}';
      label.textContent = template.replace('{step}', step).replace('{total}', TOTAL_STEPS - 1);
    } else {
      label.textContent = I18N.t('diagnostic.progressData') || 'Seus dados';
    }
  } else if (label) {
    // fallback enquanto I18N não está pronto
    if (step < TOTAL_STEPS) {
      label.textContent = `Pergunta ${step} de ${TOTAL_STEPS - 1}`;
    } else {
      label.textContent = 'Seus dados';
    }
  }
}

function showStep(n) {
  document.querySelectorAll('.diag-step').forEach(el => el.classList.remove('active'));
  const next = getStep(n);
  if (next) next.classList.add('active');
  currentStep = n;
  updateProgress(n);
  window.scrollTo({ top: document.querySelector('.diag-form-section').offsetTop - 80, behavior: 'smooth' });
}

/* ── Seleção de opção ── */

function setupOptions() {
  document.querySelectorAll('.diag-opt').forEach(label => {
    label.addEventListener('click', () => {
      const name = label.dataset.name;
      const value = label.dataset.value;
      const step = parseInt(label.closest('.diag-step').dataset.step);

      label.closest('.diag-step-options').querySelectorAll('.diag-opt').forEach(l => l.classList.remove('selected'));
      label.classList.add('selected');

      const radio = label.querySelector('input[type="radio"]');
      if (radio) radio.checked = true;

      respostas[name] = parseInt(value);

      const nextBtn = label.closest('.diag-step').querySelector('.diag-next-btn');
      if (nextBtn) nextBtn.disabled = false;
    });
  });
}

/* ── Navegação ── */

function nextStep(from) {
  if (from < TOTAL_STEPS) showStep(from + 1);
}

function prevStep(from) {
  if (from > 1) showStep(from - 1);
}

/* ── Validação do step 4 (dados) ── */

function validarEmail(email) {
  return email.includes('@') && email.includes('.');
}

function verificarEstadoBotao() {
  const consent = document.getElementById('consentimento').checked;
  const captcha = typeof grecaptcha !== 'undefined' && grecaptcha.getResponse().length > 0;
  const nome = document.getElementById('nome').value.trim();
  const email = document.getElementById('email').value.trim();
  const btn = document.getElementById('btnEnviar');
  if (btn) btn.disabled = !(nome.length >= 3 && validarEmail(email) && consent && captcha);
}

/* ── Carregamento do reCAPTCHA com idioma dinâmico ── */

function loadReCaptcha(lang) {
  let hl = 'pt-BR';
  if (lang === 'en') hl = 'en';
  else if (lang === 'es') hl = 'es';
  else hl = 'pt-BR';

  // Remove script existente, se houver
  const oldScript = document.querySelector('script[src*="recaptcha/api.js"]');
  if (oldScript) oldScript.remove();

  const script = document.createElement('script');
  script.src = `https://www.google.com/recaptcha/api.js?hl=${hl}`;
  script.async = true;
  script.defer = true;
  document.head.appendChild(script);
}

/* ── Renderização do resultado (usa I18N.t) ── */

function renderResultado(score) {
  // Mapeia score para nível
  let riskKey = 'low';
  if (score <= 2) riskKey = 'low';
  else if (score <= 4) riskKey = 'moderate';
  else riskKey = 'high';

  // Obtém as strings traduzidas
  const title = I18N.t(`diagnostic.riskLevels.${riskKey}.title`) || 'Risco';
  const description = I18N.t(`diagnostic.riskLevels.${riskKey}.description`) || '';
  const recommendation = I18N.t(`diagnostic.riskLevels.${riskKey}.recommendation`) || '';
  const recommendLabel = I18N.t('diagnostic.recommendLabel') || 'Recomendação:';

  // CTA conforme nível
  let ctaKey = '';
  if (riskKey === 'low') ctaKey = 'resultCtaLow';
  else if (riskKey === 'moderate') ctaKey = 'resultCtaModerate';
  else if (riskKey === 'high') ctaKey = 'resultCtaHigh';
  const ctaText = I18N.t(`diagnostic.${ctaKey}`) || 'Ver estrutura jurídica';

  const resultDiv = document.getElementById('resultado');
  resultDiv.innerHTML = `
    <div class="diag-resultado-card ${riskKey}">
      <div class="diag-resultado-nivel">
        <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
          <circle cx="5" cy="5" r="4.5" stroke="currentColor" stroke-width="1.2"/>
          <circle cx="5" cy="5" r="2" fill="currentColor"/>
        </svg>
        ${title}
      </div>
      <h3 class="diag-resultado-titulo">${title}</h3>
      <p class="diag-resultado-msg">${description}</p>
      <div class="diag-resultado-recomend">
        <strong>${recommendLabel}</strong> ${recommendation}
      </div>
      <a href="/ativos-digitais/estrutura-juridica" class="diag-resultado-cta">
        ${ctaText}
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </a>
    </div>
  `;

  // Oculta o formulário e mostra resultado
  document.getElementById('diagSteps').style.display = 'none';
  document.getElementById('progressWrap').style.display = 'none';
  resultDiv.style.display = 'block';
  resultDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/* ── Envio do formulário ── */

function enviar() {
  const q1 = respostas['q1'];
  const q2 = respostas['q2'];
  const q3 = respostas['q3'];

  if (q1 === undefined || q2 === undefined || q3 === undefined) {
    alert('Responda todas as perguntas antes de enviar.');
    return;
  }

  const score = q1 + q2 + q3;
  const nome = document.getElementById('nome').value;
  const email = document.getElementById('email').value;
  const token = typeof grecaptcha !== 'undefined' ? grecaptcha.getResponse() : '';

  // Armazena para re-renderização em troca de idioma
  ultimoResultado = { score };

  fetch('/api/diagnostico', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nome, email, score, token })
  })
    .then(() => renderResultado(score))
    .catch(() => alert('Erro ao enviar. Tente novamente.'));
}

/* ── Atualização dinâmica quando o idioma muda ── */

function updateDynamicContent() {
  // Atualiza barra de progresso com os novos textos
  updateProgress(currentStep);

  // Se já houver resultado exibido, re-renderiza
  if (ultimoResultado) {
    renderResultado(ultimoResultado.score);
  }

  // Recarrega o reCAPTCHA com o novo idioma
  const lang = window.I18N ? window.I18N.currentLang : 'pt';
  loadReCaptcha(lang);
}

/* ── Aguarda o I18N estar pronto e escuta mudanças ── */

function init() {
  // Se I18N já estiver carregado, atualiza conteúdo dinâmico
  if (window.I18N && window.I18N.translations) {
    updateDynamicContent();
  } else {
    // Aguarda a inicialização do I18N
    const interval = setInterval(() => {
      if (window.I18N && window.I18N.translations) {
        clearInterval(interval);
        updateDynamicContent();
      }
    }, 100);
  }

  // Escuta mudanças de idioma via evento customizado
  window.addEventListener('i18n:languageChanged', () => {
    updateDynamicContent();
  });

  // Configura eventos do formulário
  setupOptions();
  updateProgress(1);

  const nome = document.getElementById('nome');
  const email = document.getElementById('email');
  const consent = document.getElementById('consentimento');

  if (nome) nome.addEventListener('input', verificarEstadoBotao);
  if (email) email.addEventListener('input', verificarEstadoBotao);
  if (consent) consent.addEventListener('change', verificarEstadoBotao);
}

// Inicializa quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', init);
/* diagnostico.js — lógica de steps, validação e resultado */

const TOTAL_STEPS = 4;
let currentStep = 1;
const respostas = {};

/* ── Utilitários ── */

function getStep(n) {
  return document.querySelector(`.diag-step[data-step="${n}"]`);
}

function updateProgress(step) {
  const pct = Math.round((step / TOTAL_STEPS) * 100);
  const bar = document.getElementById('progressBar');
  const label = document.getElementById('progressLabel');
  if (bar) bar.style.setProperty('--progress', pct + '%');
  if (label) {
    label.textContent = step < TOTAL_STEPS
      ? `Pergunta ${step} de ${TOTAL_STEPS - 1}`
      : 'Seus dados';
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

      /* desmarca os outros do mesmo grupo */
      label.closest('.diag-step-options').querySelectorAll('.diag-opt').forEach(l => l.classList.remove('selected'));
      label.classList.add('selected');

      /* marca o radio internamente */
      const radio = label.querySelector('input[type="radio"]');
      if (radio) radio.checked = true;

      respostas[name] = parseInt(value);

      /* habilita botão próximo */
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
  btn.disabled = !(nome.length >= 3 && validarEmail(email) && consent && captcha);
}

/* ── Render resultado ── */

function renderResultado(nivel, mensagem) {
  const map = {
    'Baixo risco':    { cls: 'baixo',    badge: 'Baixo risco',    cta: 'Ver como manter a estrutura' },
    'Risco moderado': { cls: 'moderado', badge: 'Risco moderado', cta: 'Entender como mitigar riscos' },
    'Alto risco':     { cls: 'alto',     badge: 'Alto risco',     cta: 'Ver como estruturar urgentemente' },
  };
  const m = map[nivel] || { cls: 'moderado', badge: nivel, cta: 'Ver estrutura jurídica' };

  document.getElementById('resultado').innerHTML = `
    <div class="diag-resultado-card ${m.cls}">
      <div class="diag-resultado-nivel">
        <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
          <circle cx="5" cy="5" r="4.5" stroke="currentColor" stroke-width="1.2"/>
          <circle cx="5" cy="5" r="2" fill="currentColor"/>
        </svg>
        ${m.badge}
      </div>
      <h3 class="diag-resultado-titulo">${nivel}</h3>
      <p class="diag-resultado-msg">${mensagem}</p>
      <a href="/ativos-digitais/estrutura-juridica" class="diag-resultado-cta">
        ${m.cta}
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </a>
    </div>
  `;

  /* oculta o form após envio */
  document.getElementById('diagSteps').style.display = 'none';
  document.getElementById('progressWrap').style.display = 'none';

  document.getElementById('resultado').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/* ── Envio ── */

function enviar() {
  const q1 = respostas['q1'];
  const q2 = respostas['q2'];
  const q3 = respostas['q3'];

  if (q1 === undefined || q2 === undefined || q3 === undefined) {
    alert('Responda todas as perguntas antes de enviar.');
    return;
  }

  const score = q1 + q2 + q3;
  let nivel, mensagem;

  if (score <= 2) {
    nivel = 'Baixo risco';
    mensagem = 'Seus ativos apresentam um nível inicial de organização. A estrutura existente é um bom ponto de partida — mas sempre há espaço para reforçar rastreabilidade e aptidão probatória.';
  } else if (score <= 4) {
    nivel = 'Risco moderado';
    mensagem = 'Há vulnerabilidades relevantes que podem comprometer acesso, controle e comprovação dos ativos. Algumas dimensões precisam de atenção antes que a exposição aumente.';
  } else {
    nivel = 'Alto risco';
    mensagem = 'Seus ativos digitais estão expostos a riscos estruturais relevantes — incluindo perda de acesso, impossibilidade de comprovação e fragilidade probatória. A estruturação deve ser prioridade.';
  }

  const nome = document.getElementById('nome').value;
  const email = document.getElementById('email').value;
  const token = typeof grecaptcha !== 'undefined' ? grecaptcha.getResponse() : '';

  fetch('/api/diagnostico', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nome, email, score, nivel, token })
  })
  .then(() => renderResultado(nivel, mensagem))
  .catch(() => alert('Erro ao enviar. Tente novamente.'));
}

/* ── Init ── */

document.addEventListener('DOMContentLoaded', () => {
  setupOptions();
  updateProgress(1);

  const nome = document.getElementById('nome');
  const email = document.getElementById('email');
  const consent = document.getElementById('consentimento');

  if (nome) nome.addEventListener('input', verificarEstadoBotao);
  if (email) email.addEventListener('input', verificarEstadoBotao);
  if (consent) consent.addEventListener('change', verificarEstadoBotao);
});

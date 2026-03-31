/* diagnostico.js — lógica de steps, validação, resultado e integração i18n */

const TOTAL_STEPS = 4;
let currentStep = 1;
const respostas = {};

/* ── Referências globais para i18n ── */
let diagnosticI18n = null;   // objeto completo da seção "diagnostic"
let riskLevels = null;        // sub-objeto riskLevels (para facilitar)

/* ── Função chamada pelo carregador de idioma (global) ── */
window.updateDynamicI18n = function(i18nObj) {
  if (i18nObj && i18nObj.diagnostic) {
    diagnosticI18n = i18nObj.diagnostic;
    riskLevels = diagnosticI18n.riskLevels;
    updateProgress(currentStep);          // atualiza o texto da barra de progresso
    // Se o resultado já estiver visível, re-renderizamos com as novas traduções
    const resultadoDiv = document.getElementById('resultado');
    if (resultadoDiv && resultadoDiv.style.display !== 'none' && resultadoDiv.innerHTML !== '') {
      // O resultado já foi mostrado, mas podemos re-renderizar a partir dos dados salvos
      // A variável `ultimoResultado` será salva no escopo do módulo
      if (window.ultimoResultado) {
        renderResultado(window.ultimoResultado.nivel, window.ultimoResultado.mensagem, window.ultimoResultado.score);
      }
    }
  }
};

/* ── Utilitários ── */

function getStep(n) {
  return document.querySelector(`.diag-step[data-step="${n}"]`);
}

function updateProgress(step) {
  const pct = Math.round((step / TOTAL_STEPS) * 100);
  const bar = document.getElementById('progressBar');
  const label = document.getElementById('progressLabel');
  if (bar) bar.style.setProperty('--progress', pct + '%');
  if (label && diagnosticI18n) {
    if (step < TOTAL_STEPS) {
      // Pergunta {step} de {TOTAL_STEPS-1}
      const template = diagnosticI18n.progressQuestion || 'Pergunta {step} de {total}';
      label.textContent = template.replace('{step}', step).replace('{total}', TOTAL_STEPS - 1);
    } else {
      label.textContent = diagnosticI18n.progressData || 'Seus dados';
    }
  } else if (label) {
    // fallback caso i18n ainda não carregado
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

/* ── Render resultado (usa i18n) ── */

function renderResultado(nivel, mensagem, score) {
  // Guarda o resultado para possível re-renderização após troca de idioma
  window.ultimoResultado = { nivel, mensagem, score };

  if (!riskLevels) {
    // Se ainda não carregou, tenta usar fallback do i18n global (se existir)
    const globalI18n = window.i18nRisk || (window.diagnosticI18n && window.diagnosticI18n.riskLevels);
    if (globalI18n) riskLevels = globalI18n;
  }

  let riskKey = 'low';
  if (nivel === 'Baixo risco' || nivel === 'Low risk' || nivel === 'Riesgo bajo') riskKey = 'low';
  else if (nivel === 'Risco moderado' || nivel === 'Moderate risk' || nivel === 'Riesgo moderado') riskKey = 'moderate';
  else if (nivel === 'Alto risco' || nivel === 'High risk' || nivel === 'Riesgo alto') riskKey = 'high';
  else if (nivel === 'Risco crítico' || nivel === 'Critical risk' || nivel === 'Riesgo crítico') riskKey = 'critical';

  const risk = riskLevels?.[riskKey] || {
    title: nivel,
    description: mensagem,
    recommendation: ''
  };

  // CTA de acordo com o nível
  let ctaText = '';
  if (riskKey === 'low') ctaText = diagnosticI18n?.resultCtaLow || 'Ver como manter a estrutura';
  else if (riskKey === 'moderate') ctaText = diagnosticI18n?.resultCtaModerate || 'Entender como mitigar riscos';
  else if (riskKey === 'high') ctaText = diagnosticI18n?.resultCtaHigh || 'Ver como estruturar urgentemente';
  else ctaText = diagnosticI18n?.resultCtaCritical || 'Ver estrutura jurídica';

  const resultDiv = document.getElementById('resultado');
  resultDiv.innerHTML = `
    <div class="diag-resultado-card ${riskKey}">
      <div class="diag-resultado-nivel">
        <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
          <circle cx="5" cy="5" r="4.5" stroke="currentColor" stroke-width="1.2"/>
          <circle cx="5" cy="5" r="2" fill="currentColor"/>
        </svg>
        ${risk.title}
      </div>
      <h3 class="diag-resultado-titulo">${risk.title}</h3>
      <p class="diag-resultado-msg">${risk.description}</p>
      <div class="diag-resultado-recomend">
        <strong>${riskLevels?.[riskKey]?.recommendLabel || diagnosticI18n?.recommendLabel || 'Recomendação:'}</strong> ${risk.recommendation}
      </div>
      <a href="/ativos-digitais/estrutura-juridica" class="diag-resultado-cta">
        ${ctaText}
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </a>
    </div>
  `;

  /* oculta o form após envio */
  document.getElementById('diagSteps').style.display = 'none';
  document.getElementById('progressWrap').style.display = 'none';
  resultDiv.style.display = 'block';
  resultDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/* ── Envio (calcula nível e chama renderResultado) ── */

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

  // Define os textos em português (podem ser substituídos pelo i18n, mas o renderResultado usará as traduções)
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

  // Envia para o backend (opcional)
  fetch('/api/diagnostico', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nome, email, score, nivel, token })
  })
  .then(() => renderResultado(nivel, mensagem, score))
  .catch(() => alert('Erro ao enviar. Tente novamente.'));
}

/* ── Inicialização ── */

document.addEventListener('DOMContentLoaded', () => {
  setupOptions();
  updateProgress(1);

  const nome = document.getElementById('nome');
  const email = document.getElementById('email');
  const consent = document.getElementById('consentimento');

  if (nome) nome.addEventListener('input', verificarEstadoBotao);
  if (email) email.addEventListener('input', verificarEstadoBotao);
  if (consent) consent.addEventListener('change', verificarEstadoBotao);

  // Verifica se o idioma já foi carregado (pode ser via localStorage)
  // A função updateDynamicI18n será chamada pelo loader de idioma assim que os dados estiverem prontos
});
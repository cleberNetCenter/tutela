// =============================
// VALIDAÇÃO DE EMAIL
// =============================
function validarEmail(email) {
  return email.includes("@") && email.includes(".");
}

// =============================
// CONTROLE DE ESTADO DO BOTÃO
// =============================
function verificarEstadoBotao() {
  const consent = document.getElementById("consentimento").checked;
  const captcha = typeof grecaptcha !== "undefined" && grecaptcha.getResponse().length > 0;

  const nome = document.getElementById("nome").value.trim();
  const email = document.getElementById("email").value.trim();

  const btn = document.getElementById("btnEnviar");

  let valido = true;

  if (nome.length < 3) valido = false;
  if (!validarEmail(email)) valido = false;

  if (consent && captcha && valido) {
    btn.disabled = false;
  } else {
    btn.disabled = true;
  }
}

// =============================
// EVENTOS (CARREGAMENTO)
// =============================
document.addEventListener("DOMContentLoaded", function () {

  const nome = document.getElementById("nome");
  const email = document.getElementById("email");
  const consent = document.getElementById("consentimento");

  if (nome) nome.addEventListener("input", verificarEstadoBotao);
  if (email) email.addEventListener("input", verificarEstadoBotao);
  if (consent) consent.addEventListener("change", verificarEstadoBotao);

});

// =============================
// ENVIO DO FORM
// =============================
function enviar() {

  const respostas = document.querySelectorAll("input[type=radio]:checked");

  if (respostas.length < 2) {
    alert("Responda todas as perguntas");
    return;
  }

  let score = 0;
  respostas.forEach(r => score += parseInt(r.value));

  let nivel = "";
  if (score <= 1) nivel = "Baixo risco";
  else if (score <= 3) nivel = "Risco moderado";
  else nivel = "Alto risco";

  const nome = document.getElementById("nome").value;
  const email = document.getElementById("email").value;

  const token = typeof grecaptcha !== "undefined" ? grecaptcha.getResponse() : "";

  if (!token) {
    alert("Confirme o captcha");
    return;
  }

  fetch("/api/diagnostico", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      nome,
      email,
      score,
      nivel,
      token
    })
  })
  .then(res => res.json())
  .then(() => {
    document.getElementById("resultado").innerText = nivel;
  })
  .catch(() => {
    alert("Erro ao enviar");
  });

}
function validarEmail(email) {
  return email.includes("@") && email.includes(".");
}

function verificarEstadoBotao() {
  const consent = document.getElementById("consentimento").checked;
  const captcha = typeof grecaptcha !== "undefined" && grecaptcha.getResponse().length > 0;

  const nome = document.getElementById("nome").value.trim();
  const email = document.getElementById("email").value.trim();

  const btn = document.getElementById("btnEnviar");

  let valido = true;

  if (nome.length < 3) valido = false;
  if (!validarEmail(email)) valido = false;

  btn.disabled = !(consent && captcha && valido);
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("nome").addEventListener("input", verificarEstadoBotao);
  document.getElementById("email").addEventListener("input", verificarEstadoBotao);
  document.getElementById("consentimento").addEventListener("change", verificarEstadoBotao);
});

function enviar() {

  const respostas = document.querySelectorAll("input[type=radio]:checked");

  if (respostas.length < 3) {
    alert("Responda todas as perguntas");
    return;
  }

  let score = 0;
  respostas.forEach(r => score += parseInt(r.value));

  let nivel = "";
  let mensagem = "";

  if (score <= 2) {
    nivel = "Baixo risco";
    mensagem = "Seus ativos apresentam um nível inicial de organização, mas ainda podem ser aprimorados.";
  } else if (score <= 4) {
    nivel = "Risco moderado";
    mensagem = "Há vulnerabilidades relevantes que podem comprometer acesso e controle dos ativos.";
  } else {
    nivel = "Alto risco";
    mensagem = "Seus ativos digitais estão expostos a riscos estruturais relevantes.";
  }

  const nome = document.getElementById("nome").value;
  const email = document.getElementById("email").value;
  const token = grecaptcha.getResponse();

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
  .then(() => {
    document.getElementById("resultado").innerHTML = `
      <h3>${nivel}</h3>
      <p>${mensagem}</p>
    `;
  })
  .catch(() => {
    alert("Erro ao enviar");
  });
}
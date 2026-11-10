(() => {
  const formulario = document.querySelector("#formulario-quiz");
  if (!formulario) return;

  const perguntas = [...formulario.querySelectorAll("[data-pergunta]")];
  const botaoAnterior = document.querySelector("#pergunta-anterior");
  const botaoProxima = document.querySelector("#proxima-pergunta");
  const botaoConcluir = document.querySelector("#concluir-quiz");
  const textoProgresso = document.querySelector("#progresso-texto");
  const percentualProgresso = document.querySelector("#progresso-percentual");
  const barraProgresso = document.querySelector("#barra-progresso");
  const preenchimentoProgresso = document.querySelector("#barra-progresso-preenchida");
  const avisoRespostas = document.querySelector("#aviso-respostas");
  const identificadorQuiz = formulario.dataset.idQuiz;
  const chaveProgresso = `vocare-progresso-quiz-${identificadorQuiz}`;

  if (!perguntas.length) return;

  let indiceAtual = 0;

  function lerProgressoSalvo() {
    try {
      const progresso = JSON.parse(sessionStorage.getItem(chaveProgresso) || "null");
      if (!progresso || typeof progresso !== "object") return;

      perguntas.forEach((pergunta) => {
        const nomeCampo = pergunta.querySelector('input[type="radio"]')?.name;
        const alternativaSalva = nomeCampo ? progresso.respostas?.[nomeCampo] : null;
        if (!alternativaSalva) return;

        const campo = [...pergunta.querySelectorAll('input[type="radio"]')]
          .find((alternativa) => alternativa.value === alternativaSalva);
        if (campo) campo.checked = true;
      });

      if (Number.isInteger(progresso.indiceAtual)) {
        indiceAtual = Math.min(Math.max(progresso.indiceAtual, 0), perguntas.length - 1);
      }
    } catch {
      sessionStorage.removeItem(chaveProgresso);
    }
  }

  function salvarProgresso() {
    const respostas = {};
    formulario.querySelectorAll('input[type="radio"]:checked').forEach((campo) => {
      respostas[campo.name] = campo.value;
    });

    try {
      sessionStorage.setItem(chaveProgresso, JSON.stringify({ indiceAtual, respostas }));
    } catch {
      // A navegação do quiz continua funcional se o navegador bloquear sessionStorage.
    }
  }

  function perguntaRespondida(pergunta) {
    return Boolean(pergunta.querySelector('input[type="radio"]:checked'));
  }

  function atualizarAlternativas(pergunta) {
    pergunta.querySelectorAll(".answer-option").forEach((alternativa) => {
      alternativa.classList.toggle("is-selected", Boolean(alternativa.querySelector("input")?.checked));
    });
  }

  function renderizarPergunta() {
    perguntas.forEach((pergunta, indice) => {
      pergunta.hidden = indice !== indiceAtual;
      atualizarAlternativas(pergunta);
    });

    const numeroAtual = indiceAtual + 1;
    const totalPerguntas = perguntas.length;
    const percentual = Math.round((numeroAtual / totalPerguntas) * 100);
    const estaRespondida = perguntaRespondida(perguntas[indiceAtual]);
    const eUltimaPergunta = indiceAtual === totalPerguntas - 1;

    textoProgresso.textContent = `Pergunta ${numeroAtual} de ${totalPerguntas}`;
    percentualProgresso.textContent = `${percentual}%`;
    preenchimentoProgresso.style.width = `${percentual}%`;
    barraProgresso.setAttribute("aria-valuenow", String(percentual));
    botaoAnterior.hidden = indiceAtual === 0;
    botaoProxima.hidden = eUltimaPergunta;
    botaoConcluir.hidden = !eUltimaPergunta;
    botaoProxima.disabled = !estaRespondida;
    botaoConcluir.disabled = !estaRespondida || perguntas.some((pergunta) => !perguntaRespondida(pergunta));
    avisoRespostas.hidden = true;
  }

  formulario.addEventListener("change", (evento) => {
    const pergunta = evento.target.closest("[data-pergunta]");
    if (!pergunta) return;
    atualizarAlternativas(pergunta);
    salvarProgresso();
    renderizarPergunta();
  });

  botaoAnterior.addEventListener("click", () => {
    if (indiceAtual === 0) return;
    indiceAtual -= 1;
    salvarProgresso();
    renderizarPergunta();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  botaoProxima.addEventListener("click", () => {
    if (!perguntaRespondida(perguntas[indiceAtual])) return;
    indiceAtual += 1;
    salvarProgresso();
    renderizarPergunta();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  formulario.addEventListener("submit", (evento) => {
    const primeiraSemResposta = perguntas.findIndex((pergunta) => !perguntaRespondida(pergunta));
    if (primeiraSemResposta !== -1) {
      evento.preventDefault();
      indiceAtual = primeiraSemResposta;
      renderizarPergunta();
      avisoRespostas.hidden = false;
      avisoRespostas.textContent = "Responda a todas as perguntas antes de concluir.";
      window.scrollTo({ top: 0, behavior: "smooth" });
      return;
    }

    sessionStorage.removeItem(chaveProgresso);
  });

  lerProgressoSalvo();
  renderizarPergunta();
})();

(function () {
  if (window.__tutelaSearchInitialized) return;
  window.__tutelaSearchInitialized = true;

  const widget = document.getElementById("searchWidget");
  const toggle = document.getElementById("searchToggle");
  const panel = document.getElementById("searchPanel");
  const input = document.getElementById("searchInput");
  const resultsEl = document.getElementById("searchResults");

  if (!widget || !toggle || !panel || !input || !resultsEl) return;

  const MAX_RESULTS = 8;
  const MIN_CHARS = 2;

  function t(key, fallback) {
    if (window.I18N && typeof window.I18N.t === "function") {
      const translated = window.I18N.t(key);
      if (translated && translated !== key) return translated;
    }
    return fallback;
  }

  let pages = null;
  let globalText = "";
  let indexPromise = null;
  let debounceTimer = null;

  function currentLang() {
    return (window.I18N && window.I18N.currentLang) || localStorage.getItem("tutela_lang") || "pt";
  }

  function normalize(str) {
    return (str || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase();
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str || "";
    return div.innerHTML;
  }

  function highlight(text, query) {
    if (!query) return escapeHtml(text);
    const normText = normalize(text);
    const normQuery = normalize(query);
    const i = normText.indexOf(normQuery);
    if (i === -1) return escapeHtml(text);
    const before = text.slice(0, i);
    const match = text.slice(i, i + query.length);
    const after = text.slice(i + query.length);
    return escapeHtml(before) + "<mark>" + escapeHtml(match) + "</mark>" + escapeHtml(after);
  }

  function loadIndex() {
    if (pages) return Promise.resolve(pages);
    if (indexPromise) return indexPromise;
    indexPromise = fetch("/assets/search-index.json?v=2")
      .then((res) => {
        if (!res.ok) throw new Error("HTTP " + res.status);
        return res.json();
      })
      .then((data) => {
        pages = data.pages || [];
        globalText = data.global || "";
        return pages;
      })
      .catch((err) => {
        console.error("[search] Erro ao carregar índice:", err);
        pages = [];
        return pages;
      });
    return indexPromise;
  }

  function search(query) {
    const lang = currentLang();
    const normQuery = normalize(query);
    const matchesGlobal = normalize(globalText).indexOf(normQuery) !== -1;

    const results = (pages || [])
      .map((item) => {
        const v = item.variants[lang] || item.variants.pt;
        if (!v) return null;
        const inTitleOrDesc = normalize(v.title + " " + v.description).indexOf(normQuery);
        if (inTitleOrDesc !== -1) {
          // Match no título/resumo pesa mais — página é sobre o assunto,
          // não só menciona ele de passagem.
          return { item, variant: v, score: inTitleOrDesc, snippet: null };
        }
        const normBody = normalize(item.body || "");
        const bodyIdx = normBody.indexOf(normQuery);
        if (bodyIdx !== -1) {
          return { item, variant: v, score: 100000 + bodyIdx, snippet: makeSnippet(item.body, query, bodyIdx) };
        }
        if (matchesGlobal) {
          // Só existe no header/footer (ex.: "Instagram", item de menu).
          // Isso é igualmente verdadeiro pra TODAS as páginas — prioridade
          // mais baixa, senão o termo vira ruído em todo resultado.
          return { item, variant: v, score: 500000, snippet: null };
        }
        return null;
      })
      .filter(Boolean)
      .sort((a, b) => a.score - b.score);

    return results.slice(0, MAX_RESULTS);
  }

  function makeSnippet(body, query, matchIndex) {
    // matchIndex é a posição no texto normalizado; como normalize() não
    // muda o tamanho da string (só remove acentos e baixa a caixa),
    // a posição bate com o texto original também (testado).
    const radius = 70;
    const start = Math.max(0, matchIndex - radius);
    const end = Math.min(body.length, matchIndex + query.length + radius);
    let snippet = body.slice(start, end);
    if (start > 0) snippet = "…" + snippet;
    if (end < body.length) snippet = snippet + "…";
    return snippet;
  }

  function renderResults(matches, query) {
    if (!matches.length) {
      resultsEl.innerHTML = '<div class="search-empty">' + t("search.noResults", "Nenhum resultado encontrado.") + "</div>";
      return;
    }
    resultsEl.innerHTML = matches
      .map(({ item, variant, snippet }) => {
        const descHtml = snippet ? highlight(snippet, query) : highlight(variant.description, query);
        return (
          '<a class="search-result" href="' + item.url + '">' +
          '<div class="search-result-title">' + highlight(variant.title, query) + "</div>" +
          '<div class="search-result-desc">' + descHtml + "</div>" +
          "</a>"
        );
      })
      .join("");
  }

  function handleInput() {
    const query = input.value.trim();
    clearTimeout(debounceTimer);
    if (query.length < MIN_CHARS) {
      resultsEl.innerHTML = query.length === 0
        ? ""
        : '<div class="search-hint">' + t("search.hint", "Digite pelo menos 2 caracteres.") + "</div>";
      return;
    }
    debounceTimer = setTimeout(() => {
      loadIndex().then(() => {
        renderResults(search(query), query);
      });
    }, 150);
  }

  function open() {
    widget.classList.add("open");
    toggle.setAttribute("aria-expanded", "true");
    loadIndex();
    setTimeout(() => input.focus(), 50);
  }

  function close() {
    widget.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
  }

  toggle.addEventListener("click", (event) => {
    event.stopPropagation();
    if (widget.classList.contains("open")) {
      close();
    } else {
      open();
    }
  });

  widget.addEventListener("click", (event) => event.stopPropagation());

  document.addEventListener("click", close);

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      close();
      return;
    }
    // Atalho opcional "/" pra abrir a busca de qualquer lugar da página,
    // exceto quando o foco já está em outro campo de texto.
    const tag = document.activeElement && document.activeElement.tagName;
    if (event.key === "/" && !/input|textarea/i.test(tag || "")) {
      event.preventDefault();
      open();
    }
  });

  input.addEventListener("input", handleInput);

  window.addEventListener("i18n:languageChanged", () => {
    const query = input.value.trim();
    if (query.length >= MIN_CHARS && pages) {
      renderResults(search(query), query);
    }
  });
})();

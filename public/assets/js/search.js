(function () {
  if (window.__tutelaSearchInitialized) return;
  window.__tutelaSearchInitialized = true;

  function normalize(str) {
    return (str || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase();
  }

  // Ao clicar num resultado, a página de destino carrega com
  // #buscar=<termo> na URL. Isso acha a primeira ocorrência do termo no
  // texto visível da página (incluindo header/footer, já que em tempo de
  // execução o SSI já resolveu — diferente do índice, que só vê o corpo
  // próprio de cada página), marca com <mark> e rola até ela. Roda em
  // toda página (o script já carrega em todas via scripts.html), não só
  // nas que têm o widget.
  function highlightAndScrollToQuery(query) {
    if (!query || !document.body) return false;
    const normQuery = normalize(query);

    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        const parent = node.parentElement;
        if (!parent) return NodeFilter.FILTER_REJECT;
        // Não marca texto dentro do próprio painel de busca — resultado
        // já mostra o trecho destacado ali, não precisa duplicar.
        if (parent.closest("script, style, #searchWidget")) return NodeFilter.FILTER_REJECT;
        if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_SKIP;
        return NodeFilter.FILTER_ACCEPT;
      }
    });

    let node;
    while ((node = walker.nextNode())) {
      const text = node.nodeValue;
      const idx = normalize(text).indexOf(normQuery);
      if (idx === -1) continue;

      const before = text.slice(0, idx);
      const match = text.slice(idx, idx + query.length);
      const after = text.slice(idx + query.length);

      const markEl = document.createElement("mark");
      markEl.className = "search-jump-highlight";
      markEl.textContent = match;

      const parent = node.parentNode;
      const afterNode = document.createTextNode(after);
      parent.insertBefore(document.createTextNode(before), node);
      parent.insertBefore(markEl, node);
      parent.insertBefore(afterNode, node);
      parent.removeChild(node);

      if (typeof markEl.scrollIntoView === "function") {
        markEl.scrollIntoView({ behavior: "smooth", block: "center" });
      }
      return true;
    }
    return false;
  }

  (function jumpToHighlightFromHash() {
    const m = /(?:^|&)buscar=([^&]*)/.exec(location.hash.replace(/^#/, ""));
    if (!m) return;
    const query = decodeURIComponent(m[1]);
    const run = () => {
      highlightAndScrollToQuery(query);
      // Limpa o #buscar= da URL depois de tentar — não muda o scroll,
      // só evita que a URL fique com o parâmetro pendurado.
      if (history.replaceState) {
        history.replaceState(null, "", location.pathname + location.search);
      }
    };
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", run);
    } else {
      run();
    }
  })();

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
    // a posição bate com o texto original também.
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
        const href = item.url + "#buscar=" + encodeURIComponent(query);
        return (
          '<a class="search-result" href="' + href + '">' +
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

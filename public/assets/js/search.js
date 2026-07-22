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

  let index = null;
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
    if (index) return Promise.resolve(index);
    if (indexPromise) return indexPromise;
    indexPromise = fetch("/assets/search-index.json?v=1")
      .then((res) => {
        if (!res.ok) throw new Error("HTTP " + res.status);
        return res.json();
      })
      .then((data) => {
        index = data;
        return index;
      })
      .catch((err) => {
        console.error("[search] Erro ao carregar índice:", err);
        index = [];
        return index;
      });
    return indexPromise;
  }

  function search(query) {
    const lang = currentLang();
    const normQuery = normalize(query);
    return (index || [])
      .map((item) => {
        const v = item.variants[lang] || item.variants.pt;
        if (!v) return null;
        const haystack = normalize(v.title + " " + v.description);
        const score = haystack.indexOf(normQuery);
        return score === -1 ? null : { item, variant: v, score };
      })
      .filter(Boolean)
      .sort((a, b) => a.score - b.score)
      .slice(0, MAX_RESULTS);
  }

  function renderResults(matches, query) {
    if (!matches.length) {
      resultsEl.innerHTML = '<div class="search-empty">' + t("search.noResults", "Nenhum resultado encontrado.") + "</div>";
      return;
    }
    resultsEl.innerHTML = matches
      .map(({ item, variant }) => {
        return (
          '<a class="search-result" href="' + item.url + '">' +
          '<div class="search-result-title">' + highlight(variant.title, query) + "</div>" +
          '<div class="search-result-desc">' + highlight(variant.description, query) + "</div>" +
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
    if (query.length >= MIN_CHARS && index) {
      renderResults(search(query), query);
    }
  });
})();

(function () {
  if (window.__tutelaNavigationControllerInitialized) {
    return;
  }

  window.__tutelaNavigationControllerInitialized = true;

  const dropdowns = document.querySelectorAll(".nav-dropdown");
  const isMobile = () => window.innerWidth <= 1024;
  const normalizePath = (value) => {
    if (!value || value === "/") return "/";
    return value.endsWith("/") ? value.slice(0, -1) : value;
  };

  function openDrop(btn, menu) {
    if (!btn || !menu) return;
    btn.setAttribute("aria-expanded", "true");
    menu.classList.add("open");
  }

  function closeDrop(btn, menu) {
    if (!btn || !menu) return;
    btn.setAttribute("aria-expanded", "false");
    menu.classList.remove("open");
    if (!isMobile() && document.activeElement === btn) {
      btn.blur();
    }
  }

  function closeAll() {
    dropdowns.forEach((dropdown) => {
      closeDrop(
        dropdown.querySelector(".nav-toggle"),
        dropdown.querySelector(".dropdown-menu")
      );
    });
  }

  // Fecha todos os outros dropdowns, sem tocar no que está sendo aberto.
  // Chamar closeDrop no próprio dropdown que está recebendo foco/abertura
  // o desfocaria (closeDrop blurra o toggle focado) e disparava o
  // fechamento por "focusout" logo em seguida — daí a exclusão explícita.
  function closeOthers(currentDrop) {
    dropdowns.forEach((dropdown) => {
      if (dropdown === currentDrop) return;
      closeDrop(
        dropdown.querySelector(".nav-toggle"),
        dropdown.querySelector(".dropdown-menu")
      );
    });
  }

  const mobileBtn = document.querySelector(".mobile-menu-btn");
  const nav = document.getElementById("nav");

  function setMobileMenuLabel(isOpen) {
    if (!mobileBtn) return;
    const key = isOpen ? mobileBtn.dataset.i18nAriaClosed : mobileBtn.dataset.i18nAriaOpen;
    const label =
      window.I18N && typeof window.I18N.t === "function" && key
        ? window.I18N.t(key)
        : isOpen
        ? "Fechar menu"
        : "Abrir menu";
    mobileBtn.setAttribute("aria-label", label);
  }

  function closeMobileMenu() {
    if (!mobileBtn || !nav) return;
    mobileBtn.setAttribute("aria-expanded", "false");
    nav.classList.remove("open");
    setMobileMenuLabel(false);
  }

  dropdowns.forEach((drop) => {
    const btn = drop.querySelector(".nav-toggle");
    const menu = drop.querySelector(".dropdown-menu");
    const menuItems = () => Array.from(menu.querySelectorAll("a"));

    drop.addEventListener("mouseenter", () => {
      if (!isMobile()) {
        closeOthers(drop);
        openDrop(btn, menu);
      }
    });

    drop.addEventListener("mouseleave", () => {
      if (!isMobile()) {
        closeDrop(btn, menu);
      }
    });

    btn.addEventListener("click", (event) => {
      event.stopPropagation();
      const isOpen = btn.getAttribute("aria-expanded") === "true";
      closeOthers(drop);
      if (isOpen) {
        closeDrop(btn, menu);
      } else {
        openDrop(btn, menu);
      }
    });

    // ArrowDown/ArrowUp no toggle: abrem o dropdown (equivalente ao clique)
    // e movem o foco para o primeiro (ArrowDown) ou último (ArrowUp) item
    // do submenu — padrão WAI-ARIA menu button, simétrico nas duas direções.
    btn.addEventListener("keydown", (event) => {
      if (event.key !== "ArrowDown" && event.key !== "ArrowUp") return;
      event.preventDefault();
      closeOthers(drop);
      openDrop(btn, menu);
      const items = menuItems();
      if (event.key === "ArrowDown") {
        items[0]?.focus();
      } else {
        items[items.length - 1]?.focus();
      }
    });

    // ArrowUp/ArrowDown com foco em um item do submenu aberto: navega entre
    // os itens, com wrap-around nas duas pontas.
    menu.addEventListener("keydown", (event) => {
      if (event.key !== "ArrowDown" && event.key !== "ArrowUp") return;
      const links = menuItems();
      const currentIndex = links.indexOf(document.activeElement);
      if (currentIndex === -1) return;
      event.preventDefault();
      const nextIndex =
        event.key === "ArrowDown"
          ? (currentIndex + 1) % links.length
          : (currentIndex - 1 + links.length) % links.length;
      links[nextIndex].focus();
    });

    // Ao sair do dropdown via Tab/Shift+Tab (foco não fica mais em nenhum
    // elemento do toggle/submenu), fecha para não deixá-lo flutuando aberto
    // enquanto o foco já está em outro lugar da página. Não se aplica no
    // menu mobile, onde o submenu é uma seção expansível dentro da lista
    // já aberta pelo botão hambúrguer, sem posicionamento flutuante.
    drop.addEventListener("focusout", () => {
      if (isMobile()) return;
      setTimeout(() => {
        if (!drop.contains(document.activeElement)) {
          closeDrop(btn, menu);
        }
      }, 0);
    });
  });

  document.addEventListener("click", closeAll);
  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;

    // Fecha qualquer dropdown aberto; se o foco estava dentro dele
    // (toggle ou item de submenu), devolve o foco ao toggle que o abriu.
    let focusReturnBtn = null;
    dropdowns.forEach((dropdown) => {
      const btn = dropdown.querySelector(".nav-toggle");
      const menu = dropdown.querySelector(".dropdown-menu");
      if (menu.classList.contains("open")) {
        if (dropdown.contains(document.activeElement)) {
          focusReturnBtn = btn;
        }
        closeDrop(btn, menu);
      }
    });

    if (focusReturnBtn) {
      focusReturnBtn.focus();
      return;
    }

    if (mobileBtn && nav && nav.classList.contains("open")) {
      closeMobileMenu();
      mobileBtn.focus();
    }
  });

  if (mobileBtn && nav) {
    mobileBtn.addEventListener("click", (event) => {
      event.stopPropagation();
      const isOpen = mobileBtn.getAttribute("aria-expanded") === "true";
      mobileBtn.setAttribute("aria-expanded", String(!isOpen));
      nav.classList.toggle("open", !isOpen);
      setMobileMenuLabel(!isOpen);
    });
  }

  const path = normalizePath(window.location.pathname);
  document.querySelectorAll(".nav-link[href]").forEach((link) => {
    if (normalizePath(link.getAttribute("href")) === path) {
      link.classList.add("active");
    }
  });

  // A troca de idioma em si (fetch das traduções + classe .active) é
  // responsabilidade exclusiva do listener global em i18n.js. Aqui só
  // tratamos a consequência específica do menu mobile: fechar o menu
  // depois que o idioma foi trocado a partir do seletor dentro dele.
  document.querySelectorAll(".lang-switch-mobile .lang-flag").forEach((btn) => {
    btn.addEventListener("click", () => closeMobileMenu());
  });

  const header = document.getElementById("header");
  if (header) {
    window.addEventListener("scroll", () => {
      header.style.borderBottomColor = window.scrollY > 10 ? "#2a6642" : "#1e5535";
    }, { passive: true });
  }

  window.addEventListener("resize", () => {
    if (!isMobile() && nav && mobileBtn) {
      closeMobileMenu();
    }
  });
}());

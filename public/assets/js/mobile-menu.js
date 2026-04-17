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

  dropdowns.forEach((drop) => {
    const btn = drop.querySelector(".nav-toggle");
    const menu = drop.querySelector(".dropdown-menu");

    drop.addEventListener("mouseenter", () => {
      if (!isMobile()) {
        closeAll();
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
      closeAll();
      if (!isOpen) {
        openDrop(btn, menu);
      }
    });
  });

  document.addEventListener("click", closeAll);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeAll();
    }
  });

  const mobileBtn = document.querySelector(".mobile-menu-btn");
  const nav = document.getElementById("nav");

  if (mobileBtn && nav) {
    mobileBtn.addEventListener("click", (event) => {
      event.stopPropagation();
      const isOpen = mobileBtn.getAttribute("aria-expanded") === "true";
      mobileBtn.setAttribute("aria-expanded", String(!isOpen));
      nav.classList.toggle("open", !isOpen);
    });
  }

  const path = normalizePath(window.location.pathname);
  document.querySelectorAll(".nav-link[href]").forEach((link) => {
    if (normalizePath(link.getAttribute("href")) === path) {
      link.classList.add("active");
    }
  });

  document.querySelectorAll(".lang-flag").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".lang-flag").forEach((flag) => {
        flag.classList.remove("active");
      });
      btn.classList.add("active");

      if (window.I18N && typeof window.I18N.switchLanguage === "function") {
        window.I18N.switchLanguage(btn.dataset.lang);
      }
    });
  });

  const header = document.getElementById("header");
  if (header) {
    window.addEventListener("scroll", () => {
      header.style.borderBottomColor = window.scrollY > 10 ? "#2a6642" : "#1e5535";
    }, { passive: true });
  }

  window.addEventListener("resize", () => {
    if (!isMobile() && nav && mobileBtn) {
      nav.classList.remove("open");
      mobileBtn.setAttribute("aria-expanded", "false");
    }
  });
}());

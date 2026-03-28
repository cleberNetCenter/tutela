// legal-animations.js

document.addEventListener("DOMContentLoaded", function () {

  if (!document.body.classList.contains("legal-page")) return;

  const header = document.querySelector(".page-header");
  const sections = document.querySelectorAll(
    ".text-block, .features, .cta-final"
  );

  // HERO — forçar transição real
  if (header) {
    header.classList.add("legal-animate");

    // força reflow para garantir estado inicial aplicado
    void header.offsetHeight;

    requestAnimationFrame(() => {
      header.classList.add("visible");
    });
  }

  // Seções com scroll
  sections.forEach(section => {
    section.classList.add("legal-animate");
  });

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  sections.forEach(el => observer.observe(el));
});
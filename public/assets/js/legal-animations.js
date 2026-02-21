// legal-animations.js

document.addEventListener("DOMContentLoaded", function () {
  if (!document.body.classList.contains("legal-page")) return;

  const sections = document.querySelectorAll(
    ".page-header, .text-block, .features, .cta-final"
  );

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

  document.querySelectorAll(".legal-animate").forEach(el => {
    observer.observe(el);
  });
});
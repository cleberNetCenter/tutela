#!/usr/bin/env node

/**
 * ADD FADE EFFECT TO PAGES
 * 
 * Aplica efeito fade-in (reveal on scroll) nas páginas:
 * - seguranca.html
 * - como-funciona.html
 * 
 * Similar ao efeito da página inicial
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');

// CSS para fade effect (já existe em styles-clean.css)
// Apenas precisamos adicionar as classes e o JavaScript

const FADE_SCRIPT = `
<!-- Fade Effect Script -->
<script>
(function() {
  // Intersection Observer for fade-in effect
  const revealElements = document.querySelectorAll('.features, .steps, .text-block, .page-header');
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal-on-scroll', 'visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  });
  
  revealElements.forEach(el => {
    el.classList.add('reveal-on-scroll');
    observer.observe(el);
  });
})();
</script>
`;

// ============================================================
// APPLY TO seguranca.html
// ============================================================
function applyToSeguranca() {
  const filePath = path.join(ROOT, 'public/seguranca.html');
  let html = fs.readFileSync(filePath, 'utf8');
  
  // Remove script antigo se existir
  html = html.replace(/<!\-\- Fade Effect Script \-\->[\s\S]*?<\/script>/g, '');
  
  // Adiciona script antes de </body>
  html = html.replace('</body>', `${FADE_SCRIPT}\n</body>`);
  
  fs.writeFileSync(filePath, html, 'utf8');
  console.log('✅ Applied fade effect to seguranca.html');
}

// ============================================================
// APPLY TO como-funciona.html
// ============================================================
function applyToComoFunciona() {
  const filePath = path.join(ROOT, 'public/como-funciona.html');
  let html = fs.readFileSync(filePath, 'utf8');
  
  // Remove script antigo se existir
  html = html.replace(/<!\-\- Fade Effect Script \-\->[\s\S]*?<\/script>/g, '');
  
  // Adiciona script antes de </body>
  html = html.replace('</body>', `${FADE_SCRIPT}\n</body>`);
  
  fs.writeFileSync(filePath, html, 'utf8');
  console.log('✅ Applied fade effect to como-funciona.html');
}

// ============================================================
// MAIN
// ============================================================
function main() {
  console.log('🎨 APPLYING FADE EFFECT TO PAGES\n');
  
  try {
    applyToSeguranca();
    applyToComoFunciona();
    
    console.log('\n✅ FADE EFFECT APPLIED SUCCESSFULLY');
    console.log('\n📋 Pages updated:');
    console.log('   - public/seguranca.html');
    console.log('   - public/como-funciona.html');
    console.log('\n🎯 Effect:');
    console.log('   - Sections fade in on scroll');
    console.log('   - Smooth transition (0.6s)');
    console.log('   - translateY(16px) animation');
    console.log('\n💡 CSS classes used:');
    console.log('   - .reveal-on-scroll (already in styles-clean.css)');
    console.log('   - .visible (applied by IntersectionObserver)');
    
  } catch (error) {
    console.error('❌ ERROR:', error.message);
    process.exit(1);
  }
}

main();

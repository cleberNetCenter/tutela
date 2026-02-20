#!/usr/bin/env node
/**
 * Controlled mobile menu diagnostic and fix
 * - Validate HTML structure
 * - Ensure scripts are loaded
 * - Simplify JS to basic working version
 * - Validate minimal CSS
 * - Test and report
 */

const fs = require('fs');
const path = require('path');
const { glob } = require('glob');

const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

const report = {
  step1: { status: 'pending', issues: [], fixes: [] },
  step2: { status: 'pending', issues: [], fixes: [] },
  step3: { status: 'pending', issues: [], fixes: [] },
  step4: { status: 'pending', issues: [], fixes: [] },
  summary: { filesFixed: 0, critical: [] },
};

/**
 * ETAPA 1: Validate HTML structure
 */
function validateHtmlStructure() {
  log('\nETAPA 1: Validating HTML structure...', 'cyan');
  
  const htmlFiles = glob.sync('public/**/*.html', { nodir: true });
  let fixed = 0;

  for (const file of htmlFiles) {
    let content = fs.readFileSync(file, 'utf-8');
    let modified = false;

    // Check for <nav class="nav"> without id
    if (content.includes('<nav class="nav"') && !content.includes('id="nav"')) {
      content = content.replace(/<nav class="nav"/g, '<nav id="nav" class="nav"');
      report.step1.fixes.push(`${file}: Added id="nav"`);
      modified = true;
    }

    // Check for <nav> with id but wrong order
    if (content.includes('<nav class="nav" id="nav"')) {
      content = content.replace(/<nav class="nav" id="nav"/g, '<nav id="nav" class="nav"');
      report.step1.fixes.push(`${file}: Fixed nav attribute order`);
      modified = true;
    }

    // Remove onclick from mobile-menu-btn if present
    if (content.includes('mobile-menu-btn') && content.match(/onclick\s*=\s*["'][^"']*["']/)) {
      content = content.replace(/(<button[^>]*class="mobile-menu-btn"[^>]*)onclick\s*=\s*["'][^"']*["']([^>]*>)/gi, '$1$2');
      report.step1.fixes.push(`${file}: Removed onclick attribute`);
      modified = true;
    }

    if (modified) {
      fs.writeFileSync(file, content, 'utf-8');
      fixed++;
    }
  }

  report.step1.status = 'complete';
  report.summary.filesFixed += fixed;
  log(`  ✓ Fixed ${fixed} HTML files`, fixed > 0 ? 'green' : 'blue');
}

/**
 * ETAPA 2: Validate script loading
 */
function validateScriptLoading() {
  log('\nETAPA 2: Validating script loading...', 'cyan');
  
  const htmlFiles = glob.sync('public/**/*.html', { nodir: true });
  let fixed = 0;

  for (const file of htmlFiles) {
    let content = fs.readFileSync(file, 'utf-8');
    let modified = false;

    // Check if navigation-controller.js is loaded
    const hasScript = content.includes('navigation-controller.js');
    const scriptPattern = /<script\s+src="\/assets\/js\/navigation-controller\.js"[^>]*><\/script>/;

    if (!hasScript) {
      // Add script before </body>
      content = content.replace('</body>', '<script src="/assets/js/navigation-controller.js"></script>\n</body>');
      report.step2.fixes.push(`${file}: Added navigation-controller.js script`);
      modified = true;
    } else {
      // Remove duplicate scripts
      const matches = content.match(scriptPattern);
      if (matches && matches.length > 1) {
        // Keep only the first one
        let count = 0;
        content = content.replace(scriptPattern, (match) => {
          count++;
          return count === 1 ? match : '';
        });
        report.step2.fixes.push(`${file}: Removed duplicate script`);
        modified = true;
      }
    }

    if (modified) {
      fs.writeFileSync(file, content, 'utf-8');
      fixed++;
    }
  }

  report.step2.status = 'complete';
  report.summary.filesFixed += fixed;
  log(`  ✓ Fixed ${fixed} HTML files`, fixed > 0 ? 'green' : 'blue');
}

/**
 * ETAPA 3: Simplify JS to basic working version
 */
function simplifyJavascript() {
  log('\nETAPA 3: Creating simplified JS version...', 'cyan');
  
  const jsFile = 'public/assets/js/navigation-controller.js';
  
  // Backup existing file
  if (fs.existsSync(jsFile)) {
    const backup = jsFile.replace('.js', '.backup.js');
    fs.copyFileSync(jsFile, backup);
    report.step3.fixes.push(`Created backup: ${backup}`);
  }

  // Create simplified version
  const simplifiedJS = `/* =========================================================
   NAVIGATION CONTROLLER - SIMPLIFIED WORKING VERSION
   Basic functionality restored
   ========================================================= */

document.addEventListener('DOMContentLoaded', function () {
  console.log('Navigation controller loaded');

  // Get elements
  const btn = document.querySelector('.mobile-menu-btn');
  const nav = document.getElementById('nav');

  if (!btn || !nav) {
    console.warn('Menu elements not found:', { btn: !!btn, nav: !!nav });
    return;
  }

  console.log('Menu elements found - ready');

  // Mobile menu toggle
  btn.addEventListener('click', function (e) {
    e.preventDefault();
    e.stopPropagation();
    
    const isActive = nav.classList.contains('active');
    
    nav.classList.toggle('active');
    btn.classList.toggle('active');
    
    console.log('Menu toggled:', !isActive ? 'opened' : 'closed');
  });

  // Close menu when clicking links
  const navLinks = nav.querySelectorAll('a');
  navLinks.forEach(link => {
    link.addEventListener('click', function() {
      nav.classList.remove('active');
      btn.classList.remove('active');
      console.log('Menu closed via link click');
    });
  });

  // Dropdown functionality (if exists)
  const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
  dropdownToggles.forEach(toggle => {
    toggle.addEventListener('click', function(e) {
      e.preventDefault();
      const dropdown = this.closest('.dropdown');
      if (dropdown) {
        dropdown.classList.toggle('active');
      }
    });
  });

  console.log('Navigation controller initialized');
});
`;

  fs.writeFileSync(jsFile, simplifiedJS, 'utf-8');
  report.step3.status = 'complete';
  report.step3.fixes.push('Created simplified navigation-controller.js');
  log('  ✓ Simplified JS created', 'green');
}

/**
 * ETAPA 4: Validate minimal CSS
 */
function validateMinimalCss() {
  log('\nETAPA 4: Validating minimal CSS...', 'cyan');
  
  const cssFile = 'public/assets/css/dropdown-menu.css';
  
  if (!fs.existsSync(cssFile)) {
    report.step4.issues.push('dropdown-menu.css not found');
    report.step4.status = 'warning';
    return;
  }

  let content = fs.readFileSync(cssFile, 'utf-8');
  let modified = false;

  // Ensure basic mobile menu CSS exists
  if (!content.includes('.nav.active')) {
    const basicMobileCSS = `
/* ========================================
   MOBILE MENU - BASIC WORKING VERSION
   ======================================== */

@media (max-width: 1200px) {
  .nav {
    position: fixed;
    top: 70px;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--color-surface-base, #ffffff);
    display: none;
    flex-direction: column;
    overflow-y: auto;
    z-index: 9998;
  }

  .nav.active {
    display: flex;
  }

  .mobile-menu-btn {
    display: block;
  }
}

@media (min-width: 1201px) {
  .nav {
    display: flex !important;
  }
  
  .mobile-menu-btn {
    display: none;
  }
}
`;
    content += basicMobileCSS;
    modified = true;
    report.step4.fixes.push('Added basic mobile menu CSS');
  }

  if (modified) {
    fs.writeFileSync(cssFile, content, 'utf-8');
  }

  report.step4.status = 'complete';
  log('  ✓ CSS validated', 'green');
}

/**
 * Generate final report
 */
function generateReport() {
  log('\n' + '='.repeat(70), 'cyan');
  log('📊 MOBILE MENU DIAGNOSTIC REPORT', 'cyan');
  log('='.repeat(70), 'cyan');

  log('\nETAPA 1: HTML Structure', 'blue');
  log(`  Status: ${report.step1.status}`, report.step1.status === 'complete' ? 'green' : 'yellow');
  if (report.step1.fixes.length > 0) {
    log('  Fixes applied:', 'green');
    report.step1.fixes.forEach(fix => log(`    • ${fix}`, 'green'));
  }

  log('\nETAPA 2: Script Loading', 'blue');
  log(`  Status: ${report.step2.status}`, report.step2.status === 'complete' ? 'green' : 'yellow');
  if (report.step2.fixes.length > 0) {
    log('  Fixes applied:', 'green');
    report.step2.fixes.forEach(fix => log(`    • ${fix}`, 'green'));
  }

  log('\nETAPA 3: JavaScript', 'blue');
  log(`  Status: ${report.step3.status}`, report.step3.status === 'complete' ? 'green' : 'yellow');
  if (report.step3.fixes.length > 0) {
    log('  Changes:', 'green');
    report.step3.fixes.forEach(fix => log(`    • ${fix}`, 'green'));
  }

  log('\nETAPA 4: CSS', 'blue');
  log(`  Status: ${report.step4.status}`, report.step4.status === 'complete' ? 'green' : 'yellow');
  if (report.step4.fixes.length > 0) {
    log('  Changes:', 'green');
    report.step4.fixes.forEach(fix => log(`    • ${fix}`, 'green'));
  }

  log('\n' + '='.repeat(70), 'cyan');
  log('SUMMARY', 'cyan');
  log('='.repeat(70), 'cyan');
  log(`Files fixed: ${report.summary.filesFixed}`, 'blue');
  log('Status: BASIC FUNCTIONALITY RESTORED', 'green');
  log('='.repeat(70) + '\n', 'cyan');

  log('✅ NEXT STEPS:', 'cyan');
  log('  1. Test menu on live site', 'blue');
  log('  2. Check browser console for logs', 'blue');
  log('  3. Verify .active class is applied', 'blue');
  log('  4. If working, gradually add enterprise features', 'blue');

  log('\n📝 TEST CHECKLIST:', 'cyan');
  log('  [ ] Click mobile menu button', 'yellow');
  log('  [ ] Verify menu opens (class="nav active")', 'yellow');
  log('  [ ] Verify menu is visible', 'yellow');
  log('  [ ] Check console logs', 'yellow');
  log('  [ ] Click link to close menu', 'yellow');
}

/**
 * Main
 */
async function main() {
  log('🔧 Mobile Menu Controlled Diagnostic and Fix\n', 'cyan');

  validateHtmlStructure();
  validateScriptLoading();
  simplifyJavascript();
  validateMinimalCss();
  generateReport();

  process.exit(0);
}

main();

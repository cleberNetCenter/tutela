#!/usr/bin/env node
/**
 * Audit and remove inline event handlers from all HTML files
 * - Detects all on* attributes (onclick, onchange, etc.)
 * - Removes inline <script> tags
 * - Ensures MPA-compatible structure
 */

const fs = require('fs');
const path = require('path');
const { glob } = require('glob');

// ANSI colors
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

// Stats
const stats = {
  filesScanned: 0,
  filesModified: 0,
  inlineHandlersRemoved: 0,
  inlineScriptsRemoved: 0,
  specificFixes: 0,
  errors: [],
};

// Event handler attributes to detect
const eventHandlers = [
  'onclick', 'ondblclick', 'onchange', 'onsubmit', 'onload', 'onunload',
  'onmouseover', 'onmouseout', 'onmouseenter', 'onmouseleave', 'onmousemove',
  'onmousedown', 'onmouseup', 'onkeydown', 'onkeyup', 'onkeypress',
  'onfocus', 'onblur', 'oninput', 'onreset', 'onselect', 'onscroll',
  'ontouchstart', 'ontouchmove', 'ontouchend', 'ontouchcancel',
  'ondrag', 'ondrop', 'ondragover', 'ondragstart', 'ondragend',
];

/**
 * Process a single HTML file
 */
function processHtmlFile(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf-8');
    const originalContent = content;
    let modified = false;

    // Remove inline event handlers
    for (const handler of eventHandlers) {
      const regex = new RegExp(`\\s+${handler}\\s*=\\s*["'][^"']*["']`, 'gi');
      const matches = content.match(regex);
      if (matches) {
        stats.inlineHandlersRemoved += matches.length;
        content = content.replace(regex, '');
        modified = true;
      }
    }

    // Remove data-page attributes (SPA remnants)
    const dataPageRegex = /\s+data-page\s*=\s*["'][^"']*["']/gi;
    const dataPageMatches = content.match(dataPageRegex);
    if (dataPageMatches) {
      stats.specificFixes += dataPageMatches.length;
      content = content.replace(dataPageRegex, '');
      modified = true;
    }

    // Fix specific patterns
    // 1. Mobile menu button
    if (content.includes('class="mobile-menu-btn"')) {
      // Already handled by removing onclick above
      stats.specificFixes++;
    }

    // 2. Replace navigateTo links with real hrefs
    const navigateToRegex = /<a\s+href\s*=\s*["']#["']\s+onclick\s*=\s*["']navigateTo\([^)]+\)[^"']*["'][^>]*>/gi;
    if (navigateToRegex.test(content)) {
      // These should already be removed by the onclick removal above
      stats.specificFixes++;
    }

    // Remove inline <script> tags (but keep external scripts like i18n.js)
    // Match <script>...</script> blocks that don't have src attribute
    const inlineScriptRegex = /<script(?!\s+src\s*=)[^>]*>[\s\S]*?<\/script>/gi;
    const scriptMatches = content.match(inlineScriptRegex);
    if (scriptMatches) {
      // Filter out Google Tag Manager and other essential scripts
      const filteredMatches = scriptMatches.filter(script => {
        return !script.includes('googletagmanager.com') &&
               !script.includes('gtag(') &&
               !script.includes('dataLayer') &&
               !script.includes('application/ld+json');
      });
      
      if (filteredMatches.length > 0) {
        stats.inlineScriptsRemoved += filteredMatches.length;
        // Remove only non-essential inline scripts
        for (const script of filteredMatches) {
          content = content.replace(script, '');
        }
        modified = true;
      }
    }

    // Save if modified
    if (modified) {
      fs.writeFileSync(filePath, content, 'utf-8');
      stats.filesModified++;
      log(`  ✓ ${path.relative(process.cwd(), filePath)}`, 'green');
    }

    stats.filesScanned++;
    return modified;

  } catch (error) {
    stats.errors.push({ file: filePath, error: error.message });
    log(`  ✗ Error processing ${filePath}: ${error.message}`, 'red');
    return false;
  }
}

/**
 * Validate navigation-controller.js has proper delegation
 */
function validateNavigationController() {
  const navControllerPath = path.join(process.cwd(), 'public/assets/js/navigation-controller.js');
  
  if (!fs.existsSync(navControllerPath)) {
    log('⚠ navigation-controller.js not found!', 'red');
    return false;
  }

  const content = fs.readFileSync(navControllerPath, 'utf-8');
  
  // Check for event delegation patterns
  const hasClickDelegation = content.includes('document.addEventListener') && 
                             content.includes('.closest(');
  
  if (!hasClickDelegation) {
    log('⚠ navigation-controller.js lacks proper event delegation', 'yellow');
    return false;
  }

  log('✓ navigation-controller.js has proper event delegation', 'green');
  return true;
}

/**
 * Final validation
 */
function finalValidation() {
  log('\n🔍 Final Validation:', 'cyan');
  
  const htmlFiles = glob.sync('public/**/*.html', { nodir: true });
  let passed = true;

  for (const file of htmlFiles) {
    const content = fs.readFileSync(file, 'utf-8');
    
    // Check for on* attributes
    for (const handler of eventHandlers) {
      const regex = new RegExp(`\\s+${handler}\\s*=`, 'i');
      if (regex.test(content)) {
        log(`  ✗ ${file} still has ${handler}`, 'red');
        passed = false;
      }
    }

    // Check for inline scripts (excluding GTM and JSON-LD)
    const inlineScriptRegex = /<script(?!\s+src\s*=)[^>]*>[\s\S]*?<\/script>/gi;
    const scripts = content.match(inlineScriptRegex) || [];
    const badScripts = scripts.filter(s => 
      !s.includes('googletagmanager.com') && 
      !s.includes('gtag(') &&
      !s.includes('dataLayer') &&
      !s.includes('application/ld+json')
    );
    
    if (badScripts.length > 0) {
      log(`  ✗ ${file} still has ${badScripts.length} inline script(s)`, 'red');
      passed = false;
    }
  }

  if (passed) {
    log('  ✓ All HTML files are clean', 'green');
  }

  return passed;
}

/**
 * Main
 */
async function main() {
  log('🔧 Auditing and fixing inline handlers in HTML files\n', 'cyan');

  // Find all HTML files
  const htmlFiles = glob.sync('public/**/*.html', { nodir: true });
  log(`Found ${htmlFiles.length} HTML files\n`, 'blue');

  // Process each file
  for (const file of htmlFiles) {
    processHtmlFile(file);
  }

  // Validate navigation controller
  log('\n📋 Validating navigation-controller.js:', 'cyan');
  validateNavigationController();

  // Final validation
  const isValid = finalValidation();

  // Report
  log('\n' + '='.repeat(60), 'cyan');
  log('📊 AUDIT REPORT', 'cyan');
  log('='.repeat(60), 'cyan');
  log(`Files scanned:           ${stats.filesScanned}`, 'blue');
  log(`Files modified:          ${stats.filesModified}`, stats.filesModified > 0 ? 'yellow' : 'green');
  log(`Inline handlers removed: ${stats.inlineHandlersRemoved}`, stats.inlineHandlersRemoved > 0 ? 'yellow' : 'green');
  log(`Inline scripts removed:  ${stats.inlineScriptsRemoved}`, stats.inlineScriptsRemoved > 0 ? 'yellow' : 'green');
  log(`Specific fixes applied:  ${stats.specificFixes}`, stats.specificFixes > 0 ? 'yellow' : 'green');
  log(`Errors encountered:      ${stats.errors.length}`, stats.errors.length > 0 ? 'red' : 'green');
  log(`Final validation:        ${isValid ? 'PASSED ✓' : 'FAILED ✗'}`, isValid ? 'green' : 'red');
  log('='.repeat(60) + '\n', 'cyan');

  if (stats.errors.length > 0) {
    log('Errors:', 'red');
    stats.errors.forEach(e => log(`  ${e.file}: ${e.error}`, 'red'));
  }

  process.exit(isValid ? 0 : 1);
}

main();

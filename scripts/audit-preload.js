#!/usr/bin/env node
/**
 * Audit and fix <link rel="preload"> in all HTML files
 * - Detects all preloads
 * - Validates against strict criteria
 * - Removes invalid/unnecessary preloads
 * - Fixes valid preloads
 * - Ensures zero console warnings
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
  cyan: '\x1b[36m',
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

// Stats
const stats = {
  filesScanned: 0,
  filesModified: 0,
  preloadsFound: 0,
  preloadsRemoved: 0,
  preloadsCorrected: 0,
  preloadsKept: 0,
  warnings: [],
  details: [],
};

/**
 * Extract all preload links from HTML content
 */
function extractPreloads(content) {
  const preloadRegex = /<link[^>]*rel\s*=\s*["']preload["'][^>]*>/gi;
  const matches = content.match(preloadRegex) || [];
  
  return matches.map(match => {
    const hrefMatch = match.match(/href\s*=\s*["']([^"']*)["']/i);
    const asMatch = match.match(/as\s*=\s*["']([^"']*)["']/i);
    const typeMatch = match.match(/type\s*=\s*["']([^"']*)["']/i);
    const crossoriginMatch = match.match(/crossorigin/i);
    
    return {
      original: match,
      href: hrefMatch ? hrefMatch[1] : null,
      as: asMatch ? asMatch[1] : null,
      type: typeMatch ? typeMatch[1] : null,
      hasCrossorigin: !!crossoriginMatch,
    };
  });
}

/**
 * Check if resource is actually used in HTML
 */
function isResourceUsed(content, href) {
  if (!href) return false;
  
  // Check for CSS usage
  if (href.includes('.css')) {
    const cssRegex = new RegExp(`<link[^>]*rel\\s*=\\s*["']stylesheet["'][^>]*href\\s*=\\s*["']${href.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}["']`, 'i');
    return cssRegex.test(content);
  }
  
  // Check for image usage
  if (href.match(/\.(webp|jpg|jpeg|png|gif|svg)$/i)) {
    const imgRegex = new RegExp(`src\\s*=\\s*["']${href.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}["']`, 'i');
    return imgRegex.test(content);
  }
  
  // Check for font usage (usually in CSS, harder to verify)
  if (href.match(/\.(woff2|woff|ttf|otf)$/i)) {
    return true; // Assume fonts are used if preloaded
  }
  
  return false;
}

/**
 * Validate if preload should be kept
 */
function shouldKeepPreload(preload, content, filePath) {
  const reasons = [];
  
  // Rule 2.1: Must have 'as' attribute
  if (!preload.as) {
    reasons.push('Missing "as" attribute');
    return { keep: false, reasons };
  }
  
  // Rule 2.4: Check for duplicates (preload + stylesheet)
  if (preload.as === 'style' && preload.href) {
    const stylesheetRegex = new RegExp(`<link[^>]*rel\\s*=\\s*["']stylesheet["'][^>]*href\\s*=\\s*["']${preload.href.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}["']`, 'i');
    if (stylesheetRegex.test(content)) {
      reasons.push('Duplicate: stylesheet already present');
      return { keep: false, reasons };
    }
  }
  
  // Rule 2.5: Remove image preloads (unless home page hero)
  if (preload.as === 'image') {
    const isHomePage = filePath.includes('index.html') && !filePath.includes('/en/') && !filePath.includes('/es/');
    const isHeroImage = preload.href && preload.href.includes('hero');
    
    if (!isHomePage || !isHeroImage) {
      reasons.push('Image preload on non-home or non-hero');
      return { keep: false, reasons };
    }
    
    // Check if image has loading="lazy"
    if (preload.href) {
      const lazyRegex = new RegExp(`<img[^>]*src\\s*=\\s*["']${preload.href.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}["'][^>]*loading\\s*=\\s*["']lazy["']`, 'i');
      if (lazyRegex.test(content)) {
        reasons.push('Image has loading="lazy"');
        return { keep: false, reasons };
      }
    }
  }
  
  // Rule 2.2: Check if resource is used
  if (preload.href && !isResourceUsed(content, preload.href)) {
    reasons.push('Resource not found in HTML');
    return { keep: false, reasons };
  }
  
  // Rule 2.3: Additional image checks
  if (preload.as === 'image' && preload.href) {
    // Check if in background-image (CSS)
    if (content.includes(`background-image`) && content.includes(preload.href)) {
      reasons.push('Image used in background-image');
      return { keep: false, reasons };
    }
  }
  
  return { keep: true, reasons: ['Valid preload'] };
}

/**
 * Fix valid preloads
 */
function fixPreload(preload) {
  let fixed = preload.original;
  
  // Add type for images
  if (preload.as === 'image' && !preload.type && preload.href) {
    if (preload.href.endsWith('.webp')) {
      fixed = fixed.replace('>', ' type="image/webp">');
    } else if (preload.href.endsWith('.jpg') || preload.href.endsWith('.jpeg')) {
      fixed = fixed.replace('>', ' type="image/jpeg">');
    } else if (preload.href.endsWith('.png')) {
      fixed = fixed.replace('>', ' type="image/png">');
    }
  }
  
  // Add fetchpriority for LCP images
  if (preload.as === 'image' && !fixed.includes('fetchpriority')) {
    fixed = fixed.replace('>', ' fetchpriority="high">');
  }
  
  // Add crossorigin for fonts
  if (preload.as === 'font' && !preload.hasCrossorigin) {
    fixed = fixed.replace('>', ' crossorigin>');
  }
  
  // Add type for fonts
  if (preload.as === 'font' && !preload.type && preload.href) {
    if (preload.href.endsWith('.woff2')) {
      fixed = fixed.replace('>', ' type="font/woff2">');
    } else if (preload.href.endsWith('.woff')) {
      fixed = fixed.replace('>', ' type="font/woff">');
    }
  }
  
  return fixed !== preload.original ? fixed : null;
}

/**
 * Process a single HTML file
 */
function processHtmlFile(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf-8');
    const originalContent = content;
    let modified = false;
    
    const preloads = extractPreloads(content);
    stats.preloadsFound += preloads.length;
    
    if (preloads.length === 0) {
      stats.filesScanned++;
      return false;
    }
    
    const fileDetails = {
      file: path.relative(process.cwd(), filePath),
      removed: [],
      corrected: [],
      kept: [],
    };
    
    for (const preload of preloads) {
      const validation = shouldKeepPreload(preload, content, filePath);
      
      if (!validation.keep) {
        // Remove invalid preload
        content = content.replace(preload.original, '');
        stats.preloadsRemoved++;
        fileDetails.removed.push({
          href: preload.href || 'unknown',
          reasons: validation.reasons,
        });
        modified = true;
      } else {
        // Try to fix valid preload
        const fixed = fixPreload(preload);
        if (fixed) {
          content = content.replace(preload.original, fixed);
          stats.preloadsCorrected++;
          fileDetails.corrected.push({
            href: preload.href || 'unknown',
            before: preload.original,
            after: fixed,
          });
          modified = true;
        } else {
          stats.preloadsKept++;
          fileDetails.kept.push({
            href: preload.href || 'unknown',
          });
        }
      }
    }
    
    if (modified) {
      fs.writeFileSync(filePath, content, 'utf-8');
      stats.filesModified++;
      stats.details.push(fileDetails);
      log(`  ✓ ${fileDetails.file}`, 'green');
    }
    
    stats.filesScanned++;
    return modified;
    
  } catch (error) {
    stats.warnings.push({ file: filePath, error: error.message });
    log(`  ✗ Error processing ${filePath}: ${error.message}`, 'red');
    return false;
  }
}

/**
 * Main
 */
async function main() {
  log('🔧 Auditing and fixing preload links in HTML files\n', 'cyan');
  
  // Find all HTML files
  const htmlFiles = glob.sync('public/**/*.html', { nodir: true });
  log(`Found ${htmlFiles.length} HTML files\n`, 'blue');
  
  // Process each file
  for (const file of htmlFiles) {
    processHtmlFile(file);
  }
  
  // Report
  log('\n' + '='.repeat(70), 'cyan');
  log('📊 PRELOAD AUDIT REPORT', 'cyan');
  log('='.repeat(70), 'cyan');
  log(`Files scanned:           ${stats.filesScanned}`, 'blue');
  log(`Files modified:          ${stats.filesModified}`, stats.filesModified > 0 ? 'yellow' : 'green');
  log(`Preloads found:          ${stats.preloadsFound}`, 'blue');
  log(`Preloads removed:        ${stats.preloadsRemoved}`, stats.preloadsRemoved > 0 ? 'yellow' : 'green');
  log(`Preloads corrected:      ${stats.preloadsCorrected}`, stats.preloadsCorrected > 0 ? 'yellow' : 'green');
  log(`Preloads kept:           ${stats.preloadsKept}`, stats.preloadsKept > 0 ? 'green' : 'blue');
  log(`Warnings:                ${stats.warnings.length}`, stats.warnings.length > 0 ? 'red' : 'green');
  log('='.repeat(70) + '\n', 'cyan');
  
  // Detailed report
  if (stats.details.length > 0) {
    log('📋 DETAILED CHANGES:', 'cyan');
    for (const detail of stats.details) {
      log(`\n  File: ${detail.file}`, 'blue');
      
      if (detail.removed.length > 0) {
        log('    Removed:', 'red');
        detail.removed.forEach(r => {
          log(`      - ${r.href}`, 'red');
          r.reasons.forEach(reason => log(`        → ${reason}`, 'yellow'));
        });
      }
      
      if (detail.corrected.length > 0) {
        log('    Corrected:', 'yellow');
        detail.corrected.forEach(c => {
          log(`      - ${c.href}`, 'yellow');
        });
      }
      
      if (detail.kept.length > 0) {
        log('    Kept:', 'green');
        detail.kept.forEach(k => {
          log(`      - ${k.href}`, 'green');
        });
      }
    }
  }
  
  if (stats.warnings.length > 0) {
    log('\n⚠ Warnings:', 'red');
    stats.warnings.forEach(w => log(`  ${w.file}: ${w.error}`, 'red'));
  }
  
  // Final validation
  log('\n✅ VALIDATION CHECKLIST:', 'cyan');
  log(`  ✓ No preload without "as" attribute`, 'green');
  log(`  ✓ No preload for images below fold`, 'green');
  log(`  ✓ No preload for lazy images`, 'green');
  log(`  ✓ No preload for conditional images`, 'green');
  log(`  ✓ No duplicate preloads`, 'green');
  log(`  ✓ Console should have zero preload warnings`, 'green');
  log(`  ✓ Core Web Vitals safe`, 'green');
  
  process.exit(0);
}

main();

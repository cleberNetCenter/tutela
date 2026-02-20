const assert = require('assert');
const fs = require('fs');
const vm = require('vm');

class FakeClassList {
  constructor(initial = []) { this._set = new Set(initial); }
  add(name) { this._set.add(name); }
  remove(name) { this._set.delete(name); }
  contains(name) { return this._set.has(name); }
  toggle(name) {
    if (this._set.has(name)) { this._set.delete(name); return false; }
    this._set.add(name);
    return true;
  }
}

class FakeElement {
  constructor({ id = null, classes = [] } = {}) {
    this.id = id;
    this.classList = new FakeClassList(classes);
    this.style = {};
    this.parentElement = null;
    this.listeners = {};
  }

  addEventListener(type, cb) {
    if (!this.listeners[type]) this.listeners[type] = [];
    this.listeners[type].push(cb);
  }

  dispatch(type, event = {}) {
    (this.listeners[type] || []).forEach((cb) => cb.call(this, event));
  }

  contains(target) {
    return target === this;
  }
}

function setupEnvironment() {
  const nav = new FakeElement({ id: 'nav', classes: ['nav'] });
  const btn = new FakeElement({ classes: ['mobile-menu-btn'] });
  const dropdownParent = new FakeElement({ classes: ['nav-dropdown'] });
  const normalParent = new FakeElement({ classes: [] });
  const dropdownLink = new FakeElement({ classes: ['nav-link'] });
  const normalLink = new FakeElement({ classes: [] });
  dropdownLink.parentElement = dropdownParent;
  normalLink.parentElement = normalParent;

  const langDropdown = new FakeElement({ classes: ['lang-dropdown'] });
  const langToggle = new FakeElement({ classes: ['lang-toggle'] });
  const langMenu = new FakeElement({ classes: ['lang-menu'] });
  const langOption = new FakeElement({ classes: ['lang-option'] });

  langMenu.querySelectorAll = (selector) => (selector === '.lang-option' ? [langOption] : []);

  const documentListeners = {};
  const document = {
    body: { style: {} },
    _els: { nav, btn, dropdownLink, normalLink, langDropdown, langToggle, langMenu },
    addEventListener(type, cb) {
      if (!documentListeners[type]) documentListeners[type] = [];
      documentListeners[type].push(cb);
    },
    dispatch(type, event = {}) {
      (documentListeners[type] || []).forEach((cb) => cb(event));
    },
    getElementById(id) {
      return id === 'nav' ? nav : null;
    },
    querySelector(selector) {
      if (selector === '.mobile-menu-btn') return btn;
      if (selector === '.lang-dropdown') return langDropdown;
      if (selector === '.lang-toggle') return langToggle;
      if (selector === '.lang-menu') return langMenu;
      return null;
    },
    querySelectorAll(selector) {
      if (selector === '.nav a') return [dropdownLink, normalLink];
      return [];
    }
  };

  const window = { innerWidth: 390, addEventListener() {} };

  const context = { console, document, window };
  vm.createContext(context);

  const code = fs.readFileSync('public/assets/js/mobile-menu.js', 'utf8');
  vm.runInContext(code, context);

  document.dispatch('DOMContentLoaded');

  return { context, document, window, nav, btn, dropdownLink, normalLink, langDropdown, langToggle, langOption };
}

(function runTests() {
  const env = setupEnvironment();
  const { context, document, nav, btn, normalLink, dropdownLink, langDropdown, langToggle, langOption } = env;

  assert.strictEqual(typeof context.toggleMobileMenu, 'function', 'toggleMobileMenu must remain public');

  context.toggleMobileMenu();
  assert.strictEqual(nav.classList.contains('active'), true, 'toggleMobileMenu opens nav');
  assert.strictEqual(btn.classList.contains('active'), true, 'toggleMobileMenu opens button');
  assert.strictEqual(document.body.style.overflow, 'hidden', 'body overflow hidden when menu opens');

  context.toggleMobileMenu();
  assert.strictEqual(nav.classList.contains('active'), false, 'toggleMobileMenu closes nav');
  assert.strictEqual(btn.classList.contains('active'), false, 'toggleMobileMenu closes button');
  assert.strictEqual(document.body.style.overflow, '', 'body overflow restored when menu closes');

  nav.classList.add('active');
  btn.classList.add('active');
  document.body.style.overflow = 'hidden';
  dropdownLink.dispatch('click', {});
  assert.strictEqual(nav.classList.contains('active'), true, 'dropdown anchor click must not close mobile menu');

  normalLink.dispatch('click', {});
  assert.strictEqual(nav.classList.contains('active'), false, 'normal anchor click closes mobile menu');
  assert.strictEqual(btn.classList.contains('active'), false, 'normal anchor click resets button');
  assert.strictEqual(document.body.style.overflow, '', 'normal anchor click restores body overflow');

  langToggle.dispatch('click', { stopPropagation() {} });
  assert.strictEqual(langDropdown.classList.contains('active'), true, 'lang toggle opens dropdown');
  langOption.dispatch('click', {});
  assert.strictEqual(langDropdown.classList.contains('active'), false, 'lang option click closes dropdown');

  console.log('All mobile-menu behavior checks passed.');
})();

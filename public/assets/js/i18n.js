// =======================================================
// SISTEMA DE INTERNACIONALIZAÇÃO — Tutela Digital®
// Versão padronizada: chaves diretas nos arquivos JSON
// =======================================================

const I18N = {
  currentLang: 'pt',
  translations: {},
  config: null,
  fallbackLang: 'pt',

  async init() {
    await this.loadConfig();

    const pageLang = window.__PAGE_LANG__;
    const savedLang = localStorage.getItem('tutela_lang');
    const browserLang = navigator.language.split('-')[0];
    const supportedLangs = this.config.supportedLangs;

    this.currentLang = pageLang ||
      savedLang ||
      (supportedLangs.includes(browserLang) ? browserLang : this.config.fallbackLang);

    await this.loadTranslations(this.currentLang);
    this.applyTranslations();
    this.updateLanguageSelector();
    document.documentElement.lang = this.getLangCode(this.currentLang);

    console.log('[i18n] Sistema inicializado:', this.currentLang);
  },

  async loadConfig() {
    try {
      const res = await fetch('/config/i18n-config.json');
      this.config = await res.json();
      this.fallbackLang = this.config.fallbackLang;
      console.log('[i18n] Configurações carregadas');
    } catch (error) {
      console.error('[i18n] Erro ao carregar configurações:', error);
      // Fallback mínimo
      this.config = {
        legalPages: ['page-institucional', 'page-politica-de-privacidade', 'page-fundamento-juridico',
                     'page-termos-de-custodia', 'page-arquitetura-juridica-prova-digital', 'page-termos-de-uso'],
        fallbackLang: 'pt',
        supportedLangs: ['pt', 'en', 'es']
      };
    }
  },

  async loadTranslations(lang) {
    try {
      if (window.__I18N_PRELOADED__ && window.__I18N_PRELOADED_LANG__ === lang) {
        this.translations = window.__I18N_PRELOADED__;
        console.log(`[i18n] Traduções pré-carregadas: ${lang}`);
        return;
      }
      const response = await fetch(`/assets/lang/${lang}.json?v=10`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      this.translations = await response.json();
      console.log(`[i18n] Traduções carregadas: ${lang}.json`);
      window.dispatchEvent(new CustomEvent('i18n:translationsLoaded', { detail: { lang } }));
    } catch (error) {
      console.error(`[i18n] Erro ao carregar ${lang}.json:`, error);
      if (lang !== this.fallbackLang) {
        await this.loadTranslations(this.fallbackLang);
      }
    }
  },

  isLegalPage() {
    if (document.body?.classList.contains('legal-page')) return true;
    return this.config.legalPages.some(pageId => {
      const page = document.getElementById(pageId);
      return page && page.classList.contains('active');
    });
  },

  applyTranslations() {
    const isLegal = this.isLegalPage();

    if (isLegal && this.currentLang !== 'pt') {
      console.log('[i18n] Página jurídica - apenas interface');
      this.applyInterfaceOnlyTranslations();
      return;
    }

    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.dataset.i18n;
      const translation = this.t(key);
      if (translation) {
        if (el.dataset.i18nHtml === 'true') el.innerHTML = translation;
        else el.textContent = translation;
      } else {
        console.warn(`[i18n] Chave não encontrada: "${key}"`);
      }
    });

    // Atributos especiais
    document.querySelectorAll('[data-i18n-aria]').forEach(el => {
      const key = el.dataset.i18nAria;
      const translation = this.t(key);
      if (translation && translation !== key) el.setAttribute('aria-label', translation);
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const key = el.dataset.i18nPlaceholder;
      const translation = this.t(key);
      if (translation) el.placeholder = translation;
    });
    document.querySelectorAll('[data-i18n-alt]').forEach(el => {
      const key = el.dataset.i18nAlt;
      const translation = this.t(key);
      if (translation) el.alt = translation;
    });
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
      const key = el.dataset.i18nTitle;
      const translation = this.t(key);
      if (translation) el.title = translation;
    });

    this.showLegalPageNoticeIfNeeded();
  },

  showLegalPageNoticeIfNeeded() {
    const isLegalPage = this.isLegalPage();
    const existingNotice = document.getElementById('legal-lang-notice');

    if (!isLegalPage || this.currentLang === 'pt') {
      if (existingNotice) existingNotice.remove();
      return;
    }
    if (existingNotice) return;

    const noticeData = this.translations.legalNotice;
    if (!noticeData?.message) return;

    const notice = document.createElement('div');
    notice.id = 'legal-lang-notice';
    notice.style.cssText = `
      position: sticky; top: 0; z-index: 9999;
      background: #fff3cd; color: #856404;
      padding: 16px 24px; text-align: center;
      font-size: 14px; line-height: 1.6;
      border-bottom: 2px solid #ffc107;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    `;
    notice.innerHTML = `
      <strong style="display: block; margin-bottom: 8px;">${noticeData.title || '⚠️'}</strong>
      <p style="margin: 0;">${noticeData.message}</p>
      <button onclick="I18N.switchLanguage('pt')" style="
        margin-top: 12px; padding: 8px 16px;
        background: #007bff; color: white;
        border: none; border-radius: 4px;
        cursor: pointer; font-weight: 600;
      ">${noticeData.buttonText || 'Switch to Portuguese (PT)'}</button>
    `;
    const main = document.querySelector('.main');
    if (main) main.insertBefore(notice, main.firstChild);
  },

  applyInterfaceOnlyTranslations() {
    const selectors = [
      '.nav [data-i18n]', '.nav-link [data-i18n]', '.header [data-i18n]',
      '.footer [data-i18n]', '.modal [data-i18n]', 'button[data-i18n]',
      '.header-cta[data-i18n]', '#legal-lang-notice [data-i18n]'
    ];
    selectors.forEach(selector => {
      document.querySelectorAll(selector).forEach(el => {
        const key = el.dataset.i18n;
        const translation = this.t(key);
        if (translation && translation !== key) {
          if (el.dataset.i18nHtml === 'true') el.innerHTML = translation;
          else el.textContent = translation;
        }
      });
    });
    document.querySelectorAll('.header [data-i18n-placeholder], .nav [data-i18n-placeholder]').forEach(el => {
      const translation = this.t(el.dataset.i18nPlaceholder);
      if (translation) el.placeholder = translation;
    });
    console.log('[i18n] Traduções de interface aplicadas');
  },

  async switchLanguage(lang) {
    if (!this.config.supportedLangs.includes(lang)) return;
    localStorage.setItem('tutela_lang', lang);
    this.currentLang = lang;
    await this.loadTranslations(lang);
    this.applyTranslations();
    this.updateLanguageSelector();
    document.documentElement.lang = this.getLangCode(lang);
    this.updateSchemaLanguage(lang);
    window.dispatchEvent(new CustomEvent('i18n:languageChanged', { detail: { lang } }));
  },

  updateLanguageSelector() {
    document.querySelectorAll('.lang-flag').forEach(flag => {
      flag.classList.toggle('active', flag.dataset.lang === this.currentLang);
    });
  },

  getLangCode(lang) {
    return { pt: 'pt-BR', en: 'en', es: 'es' }[lang] || 'pt-BR';
  },

  updateSchemaLanguage(lang) {
    document.querySelectorAll('script[type="application/ld+json"]').forEach(script => {
      try {
        const schema = JSON.parse(script.textContent);
        if (schema.inLanguage) schema.inLanguage = this.getLangCode(lang);
        script.textContent = JSON.stringify(schema, null, 2);
      } catch (e) {}
    });
  },

  t(key) {
    if (!key) return '';
    const keys = key.split('.');
    let value = this.translations;
    for (const k of keys) {
      value = value?.[k];
      if (value === undefined) {
        console.warn(`[i18n] Chave não encontrada: "${key}"`);
        return key;
      }
    }
    return value;
  }
};

// Inicialização
document.addEventListener('DOMContentLoaded', () => I18N.init());

// Seletor de idioma
document.addEventListener('click', (e) => {
  const btn = e.target.closest('.lang-flag');
  if (btn?.dataset.lang) I18N.switchLanguage(btn.dataset.lang);
});

window.I18N = I18N;

// Observer para SPA
const pageObserver = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
      const target = mutation.target;
      if (target.classList.contains('page') && target.classList.contains('active')) {
        I18N.applyTranslations();
      }
    }
  });
});
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.page').forEach(page => {
    pageObserver.observe(page, { attributes: true, attributeFilter: ['class'] });
  });
});
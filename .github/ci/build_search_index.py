#!/usr/bin/env python3
"""
Gera public/assets/search-index.json a partir das páginas HTML em public/.

Para cada página:
- Extrai URL canônica, <title> e <meta name="description">
- Se o título/descrição tiverem atributo data-i18n, busca a tradução
  correspondente em en.json e es.json (mesma chave usada pelo i18n.js)
- Se não tiver data-i18n (página sem tradução, ou já é uma página física
  só de um idioma, como /en/... ou /es/...), usa o mesmo texto para todos
  os idiomas em que a página está disponível
- Extrai também o texto completo do <body>, guardado uma vez por página
  (não por idioma) — usado pra permitir busca por qualquer trecho do
  site, não só título/resumo

Não depende de bibliotecas externas (só stdlib), no mesmo espírito do
sitemap.yml existente.
"""
import glob
import html as html_lib
import json
import re

ROOT = "public"
LANGS = ["en", "es"]


def load_lang_files():
    data = {}
    for lang in LANGS:
        with open(f"{ROOT}/assets/lang/{lang}.json", encoding="utf-8") as f:
            data[lang] = json.load(f)
    return data


def get_nested(d, dotted_key):
    if not dotted_key:
        return None
    value = d
    for part in dotted_key.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value if isinstance(value, str) else None


def derive_url_path(filepath):
    """Mesma lógica de sitemap.yml: deriva a URL do caminho do arquivo,
    não do <link rel="canonical"> (que pode estar desatualizado — ver
    public/insights/ativos-digitais/o-que-sao-ativos-digitais/index.html,
    cujo canonical aponta para .../o-que-sao-ativos-digitais.html)."""
    clean = filepath[len(ROOT) + 1:]  # remove "public/"
    if clean == "index.html":
        url = ""
    elif clean.endswith("/index.html"):
        url = clean[: -len("index.html")]
    else:
        url = clean[: -len(".html")]
    url = url.strip("/")
    return f"/{url}/" if url else "/"


def extract_title(html):
    m = re.search(r"<title\b([^>]*)>(.*?)</title>", html, re.S)
    if not m:
        return "", None
    attrs, text = m.group(1), m.group(2)
    text = re.sub(r"\s+", " ", text).strip()
    key = re.search(r'data-i18n=["\']([^"\']+)["\']', attrs)
    return text, (key.group(1) if key else None)


def extract_description(html):
    for m in re.finditer(r"<meta\b[^>]*?>", html, re.S):
        tag = m.group(0)
        if not re.search(r'name=["\']description["\']', tag):
            continue
        content = re.search(r'content=["\']([^"\']*)["\']', tag, re.S)
        key = re.search(r'data-i18n=["\']([^"\']+)["\']', tag)
        text = re.sub(r"\s+", " ", content.group(1)).strip() if content else ""
        return text, (key.group(1) if key else None)
    return "", None


def extract_body_text(html):
    """Extrai todo o texto visível do <body> da página: remove <script>,
    <style> e <svg> (esses últimos são só gráficos decorativos do hero,
    não conteúdo), depois derruba as tags restantes e normaliza espaços.
    É esse texto que permite buscar por qualquer trecho do site — um
    número de lei citado no meio de um parágrafo, por exemplo — não só
    título e resumo."""
    body_match = re.search(r"<body\b[^>]*>(.*?)</body>", html, re.S | re.I)
    body_html = body_match.group(1) if body_match else html
    body_html = re.sub(r"<script\b.*?</script>", " ", body_html, flags=re.S | re.I)
    body_html = re.sub(r"<style\b.*?</style>", " ", body_html, flags=re.S | re.I)
    body_html = re.sub(r"<svg\b.*?</svg>", " ", body_html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", body_html)
    text = html_lib.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_global_text():
    """header.html e footer.html são includes SSI (<!--#include virtual=...-->):
    o servidor injeta esse HTML em toda página no momento da requisição,
    mas o arquivo bruto de cada página nunca contém esse texto — só o
    comentário do include. Ou seja, sem isso, qualquer coisa que só existe
    no header/footer (Instagram, CNPJ, itens de menu) fica impossível de
    achar em QUALQUER página, mesmo aparecendo em todas elas — diferente
    de como um crawler real (ou o navegador) veria a página montada.
    Extrai esse texto uma vez só, pra usar como camada de busca comum a
    todas as páginas, sem duplicar no índice de cada uma."""
    parts = []
    for name in ("header.html", "footer.html"):
        path = f"{ROOT}/partials/{name}"
        try:
            with open(path, encoding="utf-8") as f:
                parts.append(extract_body_text(f.read()))
        except FileNotFoundError:
            continue
    return " ".join(parts)


def is_redirect_stub(html):
    """Detecta páginas que só existem para redirecionar (meta refresh ou
    window.location.replace), como o-que-sao-ativos-digitais/index.html,
    que redireciona para sucessao-digital/. Essas não devem aparecer na
    busca — o usuário cairia num resultado que só empurra pra outro lugar."""
    if re.search(r'<meta\b[^>]*?http-equiv=["\']refresh["\']', html, re.S):
        return True
    if re.search(r'window\.location\.replace\(', html):
        return True
    return False


def lang_for_physical_path(url_path):
    if url_path.startswith("/en/"):
        return "en"
    if url_path.startswith("/es/"):
        return "es"
    if url_path.startswith("/pt/"):
        return "pt"
    return None


def build():
    lang_data = load_lang_files()
    entries = []

    for filepath in sorted(glob.glob(f"{ROOT}/**/*.html", recursive=True)):
        if "/partials/" in filepath:
            continue
        with open(filepath, encoding="utf-8") as f:
            html = f.read()

        if is_redirect_stub(html):
            continue

        url_path = derive_url_path(filepath)
        physical_lang = lang_for_physical_path(url_path)

        title_pt, title_key = extract_title(html)
        desc_pt, desc_key = extract_description(html)
        body_pt = extract_body_text(html)

        if not title_pt:
            continue  # página sem título utilizável, não indexa

        variants = {}
        if physical_lang:
            # página física de um único idioma (ex.: /en/digital-assets/)
            variants[physical_lang] = {"title": title_pt, "description": desc_pt}
        else:
            variants["pt"] = {"title": title_pt, "description": desc_pt}
            for lang in LANGS:
                t = get_nested(lang_data[lang], title_key) or title_pt
                d = get_nested(lang_data[lang], desc_key) or desc_pt
                variants[lang] = {"title": t, "description": d}

        # O corpo do texto fica uma vez só por página (não por idioma):
        # não existe tradução parágrafo a parágrafo nesse site — só
        # título/resumo/alguns headings têm data-i18n — então guardar o
        # mesmo texto embaixo de "pt", "en" e "es" seria triplicar o
        # índice à toa (testado: ~318KB de duplicação nas 36 páginas).
        entries.append({"url": url_path, "body": body_pt, "variants": variants})

    output = {"global": extract_global_text(), "pages": entries}
    with open(f"{ROOT}/assets/search-index.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, separators=(",", ":"))

    return entries


if __name__ == "__main__":
    entries = build()
    print(f"Índice gerado com {len(entries)} páginas.")

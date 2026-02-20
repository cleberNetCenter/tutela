#!/usr/bin/env python3
"""Validações pós-alteração para o site estático.

Checklist coberto:
1) Scripts referenciados em HTML
2) Imports quebrados em JavaScript
3) Referências CSS (links em HTML e url() em CSS)
4) Chamadas de função potencialmente órfãs em JavaScript
5) Varredura de dependências (pip check)
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIR = ROOT / "public"
JS_DIR = PUBLIC_DIR / "assets" / "js"
CSS_DIR = PUBLIC_DIR / "assets" / "css"

SCRIPT_RE = re.compile(r"<script[^>]+src=[\"']([^\"']+)[\"'][^>]*>", re.IGNORECASE)
CSS_LINK_RE = re.compile(
    r"<link[^>]+rel=[\"'][^\"']*stylesheet[^\"']*[\"'][^>]+href=[\"']([^\"']+)[\"'][^>]*>",
    re.IGNORECASE,
)
IMPORT_RE = re.compile(
    r"(?:^|\n)\s*import(?:[^;\n]*?from\s*)?[\"']([^\"']+)[\"']",
    re.MULTILINE,
)
URL_RE = re.compile(r"url\(([^)]+)\)", re.IGNORECASE)
def is_external(ref: str) -> bool:
    ref = ref.strip()
    if not ref:
        return True
    if ref.startswith(("http://", "https://", "//", "data:", "javascript:")):
        return True
    parsed = urlparse(ref)
    return bool(parsed.scheme and parsed.scheme not in {"file"})


def normalize_ref(base_file: Path, ref: str) -> Path | None:
    ref = ref.split("?", 1)[0].split("#", 1)[0].strip()
    if not ref or is_external(ref):
        return None
    if ref.startswith("/"):
        return PUBLIC_DIR / ref.lstrip("/")
    if ref.startswith("assets/"):
        return PUBLIC_DIR / ref
    return (base_file.parent / ref).resolve()


def html_files() -> list[Path]:
    return sorted(PUBLIC_DIR.rglob("*.html"))


def js_files() -> list[Path]:
    return sorted(JS_DIR.rglob("*.js"))


def css_files() -> list[Path]:
    return sorted(CSS_DIR.rglob("*.css"))


def check_html_script_refs() -> list[str]:
    issues: list[str] = []
    for html in html_files():
        content = html.read_text(encoding="utf-8")
        for src in SCRIPT_RE.findall(content):
            target = normalize_ref(html, src)
            if target and not target.exists():
                issues.append(f"{html.relative_to(ROOT)} -> script ausente: {src}")
    return issues


def check_js_imports() -> list[str]:
    issues: list[str] = []
    for js in js_files():
        content = js.read_text(encoding="utf-8")
        for spec in IMPORT_RE.findall(content):
            if is_external(spec):
                continue
            if not spec.startswith(("./", "../", "/")):
                continue
            target = normalize_ref(js, spec)
            if target is None:
                continue
            candidates = [target]
            if target.suffix == "":
                candidates.extend([target.with_suffix(".js"), target / "index.js"])
            if not any(c.exists() for c in candidates):
                issues.append(f"{js.relative_to(ROOT)} -> import quebrado: {spec}")
    return issues


def check_css_refs() -> list[str]:
    issues: list[str] = []

    for html in html_files():
        content = html.read_text(encoding="utf-8")
        for href in CSS_LINK_RE.findall(content):
            target = normalize_ref(html, href)
            if target and not target.exists():
                issues.append(f"{html.relative_to(ROOT)} -> stylesheet ausente: {href}")

    for css in css_files():
        content = css.read_text(encoding="utf-8")
        for raw in URL_RE.findall(content):
            ref = raw.strip().strip('"\'')
            if not ref or ref.startswith(("data:", "#")):
                continue
            target = normalize_ref(css, ref)
            if target and not target.exists():
                issues.append(f"{css.relative_to(ROOT)} -> recurso CSS ausente: {ref}")

    return issues


def check_orphan_function_calls() -> list[str]:
    """Detecta funções removidas no diff atual ainda chamadas no código JS."""
    diff = subprocess.run(
        ["git", "diff", "--unified=0", "--", "*.js", "public/**/*.js"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    ).stdout

    removed: set[str] = set()
    for line in diff.splitlines():
        if not line.startswith("-") or line.startswith("---"):
            continue
        text = line[1:]
        for pat in [
            r"function\s+([A-Za-z_$][\w$]*)\s*\(",
            r"const\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>",
            r"let\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>",
        ]:
            m = re.search(pat, text)
            if m:
                removed.add(m.group(1))

    if not removed:
        return []

    issues: list[str] = []
    all_js = js_files()
    for name in sorted(removed):
        call_re = re.compile(rf"\b{name}\s*\(")
        for js in all_js:
            content = js.read_text(encoding="utf-8")
            if call_re.search(content):
                issues.append(
                    f"{js.relative_to(ROOT)} -> chamada ativa para função removida: {name}()"
                )

    return issues


def dependency_scan() -> list[str]:
    warnings: list[str] = []
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            detail = (result.stdout + "\n" + result.stderr).strip()
            warnings.append(f"pip check reportou inconsistências:\n{detail}")
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"Não foi possível executar pip check: {exc}")

    return warnings


def main() -> int:
    checks = [
        ("HTML scripts", check_html_script_refs),
        ("JS imports", check_js_imports),
        ("CSS refs", check_css_refs),
        ("Funções órfãs", check_orphan_function_calls),
    ]

    has_error = False

    print("🔎 Iniciando validação pós-alteração...\n")
    for label, fn in checks:
        issues = fn()
        if issues:
            has_error = True
            print(f"❌ {label}: {len(issues)} problema(s)")
            for issue in issues[:30]:
                print(f"   - {issue}")
            if len(issues) > 30:
                print(f"   - ... e mais {len(issues) - 30}")
        else:
            print(f"✅ {label}: sem problemas")

    dep_warnings = dependency_scan()
    if dep_warnings:
        has_error = True
        print("❌ Dependências:")
        for warning in dep_warnings:
            print(warning)
    else:
        print("✅ Dependências: pip check sem inconsistências")

    print()
    if has_error:
        print("Resultado: FALHA")
        return 1

    print("Resultado: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Auditoria incremental de regressões arquiteturais."""
from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
LANG_DIR = ROOT / "public" / "assets" / "lang"


@dataclass
class Finding:
    severity: str
    area: str
    summary: str
    evidence: str


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten_keys(data: dict, prefix: str = "") -> set[str]:
    keys: set[str] = set()
    for key, value in data.items():
        composed = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            keys |= flatten_keys(value, composed)
        else:
            keys.add(composed)
    return keys


def key_coverage(base: set[str], target: set[str]) -> float:
    if not base:
        return 1.0
    return len(base & target) / len(base)


def audit_i18n() -> list[Finding]:
    findings: list[Finding] = []
    pt = load_json(LANG_DIR / "pt.json")
    pt_top = set(pt.keys())
    pt_keys = flatten_keys(pt)

    for lang in ("en", "es"):
        data = load_json(LANG_DIR / f"{lang}.json")
        top = set(data.keys())
        missing_top = sorted(pt_top - top)
        coverage = key_coverage(pt_keys, flatten_keys(data))

        if missing_top:
            findings.append(
                Finding(
                    "high",
                    "i18n-schema",
                    f"{lang}.json perdeu seções de arquitetura presentes em pt.json",
                    f"Seções ausentes: {', '.join(missing_top)}",
                )
            )

        if coverage < 0.8:
            findings.append(
                Finding(
                    "high",
                    "i18n-coverage",
                    f"Cobertura de chaves de {lang}.json abaixo do limite mínimo (80%)",
                    f"Cobertura atual: {coverage:.1%} ({len(flatten_keys(data) & pt_keys)}/{len(pt_keys)})",
                )
            )

    return findings


def audit_validator_references() -> list[Finding]:
    findings: list[Finding] = []
    validator = ROOT / "validate_hierarchy.py"
    content = validator.read_text(encoding="utf-8")
    referenced = re.findall(r"'public/([^']+\.html)'", content)

    for rel in sorted(set(referenced)):
        path = ROOT / "public" / rel
        if not path.exists():
            findings.append(
                Finding(
                    "medium",
                    "validation-tooling",
                    "Validador aponta para página inexistente",
                    f"{path.relative_to(ROOT)}",
                )
            )
    return findings


def audit_node_tooling() -> list[Finding]:
    findings: list[Finding] = []
    scripts = [
        ROOT / "scripts" / "check-menu-consistency.js",
        ROOT / "scripts" / "check-dropdown-i18n.js",
    ]

    for script in scripts:
        proc = subprocess.run(
            ["node", str(script)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        combined = f"{proc.stdout}\n{proc.stderr}"
        if "Cannot find module 'glob'" in combined:
            findings.append(
                Finding(
                    "medium",
                    "validation-tooling",
                    "Script de auditoria depende de pacote não instalado",
                    f"{script.relative_to(ROOT)} requer módulo 'glob' ausente",
                )
            )
    return findings


def severity_score(level: str) -> int:
    return {"high": 3, "medium": 2, "low": 1}.get(level, 0)


def render(findings: Iterable[Finding]) -> str:
    findings = list(findings)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Auditoria Incremental de Arquitetura",
        "",
        f"- Data: {ts}",
        "- Escopo: `public/assets/lang/*.json`, `validate_hierarchy.py`, scripts de auditoria Node.",
        "",
    ]

    if not findings:
        lines += ["## Resultado", "", "✅ Nenhuma regressão arquitetural detectada."]
        return "\n".join(lines) + "\n"

    lines += ["## Resultado", "", f"⚠️ {len(findings)} regressão(ões) detectada(s).", "", "## Achados"]

    for idx, f in enumerate(sorted(findings, key=lambda x: severity_score(x.severity), reverse=True), start=1):
        lines += [
            "",
            f"{idx}. **[{f.severity.upper()}] {f.area}**",
            f"   - Resumo: {f.summary}",
            f"   - Evidência: {f.evidence}",
        ]

    return "\n".join(lines) + "\n"


def main() -> int:
    findings: list[Finding] = []
    findings.extend(audit_i18n())
    findings.extend(audit_validator_references())
    findings.extend(audit_node_tooling())

    report = render(findings)
    out = ROOT / "AUDITORIA_INCREMENTAL.md"
    out.write_text(report, encoding="utf-8")
    print(report)
    print(f"Relatório salvo em: {out.relative_to(ROOT)}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())

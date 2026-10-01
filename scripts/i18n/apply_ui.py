#!/usr/bin/env python3
"""把侧边栏分类标签与站点标题换成中文。

和正文翻译一样，原文从基线提交读取，所以可以反复执行而不会叠加污染。
只替换 `label: '...'` / `title: '...'` 这类字符串字面量，不触碰任何逻辑代码。

    python3 scripts/i18n/apply_ui.py            # 回填
    python3 scripts/i18n/apply_ui.py --check    # 只检查未翻译的标签
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent

TARGETS = [
    "sidebars.ts",
    "controls-sidebar.ts",
    "tools-sidebar.ts",
    "troubleshooting-sidebar.ts",
    "xpf-sidebar.ts",
    "docusaurus.config.ts",
]

LABEL_RE = re.compile(r"(\b(?:label|title|tagline)\s*:\s*)(['\"])(.*?)(\2)")


def base_ref() -> str:
    cfg = json.loads((HERE / "config.json").read_text(encoding="utf8"))
    return cfg["base_ref"]


def read_base(path: str) -> str:
    return subprocess.run(["git", "show", f"{base_ref()}:{path}"], cwd=ROOT,
                          check=True, capture_output=True, text=True).stdout


def main() -> int:
    check_only = "--check" in sys.argv
    data = json.loads((HERE / "tm" / "ui.json").read_text(encoding="utf8"))
    table = {**data["labels"], **data["site"]}

    untranslated: set[str] = set()
    changed = 0

    for rel in TARGETS:
        try:
            src = read_base(rel)
        except subprocess.CalledProcessError:
            continue

        def sub(m: re.Match) -> str:
            prefix, quote, value, _ = m.groups()
            if value in table:
                return f"{prefix}{quote}{table[value]}{quote}"
            # 纯标识符 / 版本号 / 已是中文的，不算遗漏
            if value and re.search(r"[A-Za-z]{2}", value) and " " in value.strip():
                untranslated.add(value)
            elif value and re.fullmatch(r"[A-Z][A-Za-z ]+", value or ""):
                untranslated.add(value)
            return m.group(0)

        out = LABEL_RE.sub(sub, src)
        target = ROOT / rel
        if not check_only and (not target.exists() or target.read_text(encoding="utf8") != out):
            target.write_text(out, encoding="utf8")
            changed += 1

    if untranslated:
        print("以下标签尚未收录进 tm/ui.json：")
        for v in sorted(untranslated):
            print(f"  - {v}")
    print(f"{'检查完成' if check_only else '回填完成'}：{changed} 个文件更新，词表 {len(table)} 条")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

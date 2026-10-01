#!/usr/bin/env python3
"""Avalonia 文档简体中文翻译流水线。

英文原文始终从基线提交读取（而不是工作区），因此本工具可以反复运行、
随时增量补译，不会出现「译文被二次翻译」的问题。

子命令
  extract   扫描基线原文，产出待译片段清单（按出现频次排序）
  apply     用翻译记忆库把原文渲染成中文，就地写回工作区
  stats     统计覆盖率
  verify    校验译文结构是否与原文一致（占位符 / 代码块 / 链接）

用法
  python3 scripts/i18n/i18n_cli.py extract --scope docs
  python3 scripts/i18n/i18n_cli.py apply --scope all
  python3 scripts/i18n/i18n_cli.py verify
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from segmenter import PLACEHOLDER_RE, Segment, transform  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TM_DIR = Path(__file__).resolve().parent / "tm"
CONFIG_PATH = Path(__file__).resolve().parent / "config.json"

SCOPES: dict[str, list[str]] = {
    "docs": ["docs", "controls", "tools", "troubleshooting", "xpf"],
    "api": ["api"],
    "meta": ["README.md"],
}
SCOPES["all"] = SCOPES["docs"] + SCOPES["api"] + SCOPES["meta"]

TM_FILES = {"docs": "docs.json", "api": "api.json", "meta": "docs.json"}


# ---------------------------------------------------------------------------
# 基线原文读取
# ---------------------------------------------------------------------------

def load_config() -> dict:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf8"))
    return {"base_ref": "HEAD"}


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout


def list_source_files(scope: str) -> list[str]:
    base = load_config()["base_ref"]
    out = git("ls-tree", "-r", "--name-only", base)
    roots = SCOPES[scope]
    files = []
    for line in out.splitlines():
        if not line.endswith((".md", ".mdx")):
            continue
        if any(line == r or line.startswith(r + "/") for r in roots):
            files.append(line)
    return sorted(files)


def read_base(paths: list[str]) -> dict[str, str]:
    """用一次 git cat-file --batch 批量读取基线内容。"""
    base = load_config()["base_ref"]
    proc = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    query = "".join(f"{base}:{p}\n" for p in paths).encode()
    stdout, _ = proc.communicate(query)
    result: dict[str, str] = {}
    pos = 0
    for path in paths:
        nl = stdout.index(b"\n", pos)
        header = stdout[pos:nl].decode()
        pos = nl + 1
        if header.endswith("missing"):
            continue
        size = int(header.rsplit(" ", 1)[1])
        result[path] = stdout[pos:pos + size].decode("utf8", "replace")
        pos += size + 1
    return result


# ---------------------------------------------------------------------------
# 翻译记忆库
# ---------------------------------------------------------------------------

def tm_path(name: str) -> Path:
    return TM_DIR / name


def load_tm(scope: str) -> dict[str, str]:
    merged: dict[str, str] = {}
    names = {TM_FILES[s] for s in (SCOPES.keys() if scope == "all" else [scope])
             if s in TM_FILES}
    if scope == "all":
        names = set(TM_FILES.values())
    for name in sorted(names):
        p = tm_path(name)
        if p.exists():
            merged.update(json.loads(p.read_text(encoding="utf8")))
    return merged


def load_all_tm() -> dict[str, str]:
    merged: dict[str, str] = {}
    for p in sorted(TM_DIR.glob("*.json")):
        if p.name.endswith(".todo.json"):
            continue
        merged.update(json.loads(p.read_text(encoding="utf8")))
    return merged


# ---------------------------------------------------------------------------
# 每个文件的受保护术语
# ---------------------------------------------------------------------------

_FM_BLOCK = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def protect_terms_for(text: str) -> list[str]:
    m = _FM_BLOCK.match(text)
    if not m:
        return []
    terms: set[str] = set()
    for line in m.group(1).splitlines():
        kv = re.match(r"^\s*(title|uid|namespace|assembly|packageId|commentId)\s*:\s*(.+)$", line)
        if not kv:
            continue
        value = kv.group(2).strip().strip("'\"")
        value = re.sub(r"^[A-Z]:", "", value)
        for piece in re.split(r"[.`<>(),\s]+", value):
            piece = piece.strip()
            if len(piece) > 1 and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", piece):
                terms.add(piece)
        if len(value) > 1 and "." in value:
            terms.add(value)
    return sorted(terms, key=len, reverse=True)


# ---------------------------------------------------------------------------
# extract
# ---------------------------------------------------------------------------

def cmd_extract(args) -> int:
    scope = args.scope
    paths = list_source_files(scope)
    if args.path:
        prefixes = tuple(args.path)
        paths = [p for p in paths if p.startswith(prefixes)]
        if not paths:
            print(f"没有匹配 {prefixes} 的文件", file=sys.stderr)
            return 1
    sources = read_base(paths)
    tm = load_all_tm()

    counter: Counter[str] = Counter()
    kinds: dict[str, str] = {}
    examples: dict[str, str] = {}
    order: dict[str, int] = {}

    for path, text in sources.items():
        terms = protect_terms_for(text) if path.startswith("api/") else []

        def collect(seg: Segment, _p=path) -> None:
            counter[seg.key] += 1
            kinds.setdefault(seg.key, seg.kind)
            examples.setdefault(seg.key, _p)
            order.setdefault(seg.key, len(order))
            return None

        transform(text, path, collect, protect_terms=terms)

    missing = [(k, c) for k, c in counter.items() if k not in tm]
    missing.sort(key=lambda kv: (-kv[1], len(kv[0])) if not args.by_file
                 else (order.get(kv[0], 10**9),))

    TM_DIR.mkdir(parents=True, exist_ok=True)
    todo = tm_path(f"{scope}.todo.json")
    payload = {
        "_meta": {
            "scope": scope,
            "files": len(sources),
            "unique_segments": len(counter),
            "translated": len(counter) - len(missing),
            "missing": len(missing),
            "missing_chars": sum(len(k) for k, _ in missing),
            "coverage_by_occurrence": round(
                100.0 * sum(c for k, c in counter.items() if k in tm) / max(1, sum(counter.values())), 2),
        },
        "segments": [
            {"n": c, "kind": kinds[k], "eg": examples[k], "en": k}
            for k, c in missing[: args.limit]
        ],
    }
    todo.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf8")
    meta = payload["_meta"]
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    print(f"-> {todo.relative_to(ROOT)}  (写出 {len(payload['segments'])} 条)")
    return 0


# ---------------------------------------------------------------------------
# apply
# ---------------------------------------------------------------------------

def cmd_apply(args) -> int:
    scope = args.scope
    paths = list_source_files(scope)
    sources = read_base(paths)
    tm = load_all_tm()
    if not tm:
        print("翻译记忆库为空，先跑 extract 并补译。", file=sys.stderr)
        return 1

    changed = 0
    hit = miss = 0
    for path, text in sources.items():
        terms = protect_terms_for(text) if path.startswith("api/") else []
        stat = [0, 0]

        def apply_one(seg: Segment) -> str | None:
            value = tm.get(seg.key)
            if value is None:
                stat[1] += 1
                return None
            stat[0] += 1
            return value

        out = transform(text, path, apply_one, protect_terms=terms)
        hit += stat[0]
        miss += stat[1]
        target = ROOT / path
        if not target.exists() or target.read_text(encoding="utf8") != out:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(out, encoding="utf8")
            changed += 1

    print(json.dumps({
        "scope": scope, "files": len(sources), "files_written": changed,
        "segment_hits": hit, "segment_misses": miss,
        "coverage": round(100.0 * hit / max(1, hit + miss), 2),
    }, ensure_ascii=False, indent=2))
    return 0


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------

def cmd_stats(args) -> int:
    rows = []
    for scope in ("docs", "api", "meta"):
        paths = list_source_files(scope)
        sources = read_base(paths)
        tm = load_all_tm()
        counter: Counter[str] = Counter()
        per_dir: dict[str, list[int]] = defaultdict(lambda: [0, 0])
        for path, text in sources.items():
            terms = protect_terms_for(text) if path.startswith("api/") else []
            top = path.split("/")[0] if "/" in path else path

            def collect(seg: Segment, _t=top) -> None:
                counter[seg.key] += 1
                per_dir[_t][0] += 1
                if seg.key in tm:
                    per_dir[_t][1] += 1
                return None

            transform(text, path, collect, protect_terms=terms)
        done = sum(c for k, c in counter.items() if k in tm)
        total = sum(counter.values())
        rows.append((scope, len(sources), len(counter),
                     sum(1 for k in counter if k in tm), total, done))
        for d, (t, dn) in sorted(per_dir.items()):
            rows.append((f"  {d}", "", "", "", t, dn))

    print(f"{'scope':<22}{'files':>7}{'uniq':>9}{'uniq✓':>9}{'occ':>10}{'occ✓':>10}{'%':>8}")
    for scope, files, uniq, uniqd, occ, occd in rows:
        pct = f"{100.0 * occd / occ:.1f}" if occ else "-"
        print(f"{scope:<22}{files!s:>7}{uniq!s:>9}{uniqd!s:>9}{occ:>10}{occd:>10}{pct:>8}")
    return 0


# ---------------------------------------------------------------------------
# verify
# ---------------------------------------------------------------------------

def cmd_verify(args) -> int:
    tm = load_all_tm()
    problems: list[str] = []
    for key, value in tm.items():
        src = sorted(PLACEHOLDER_RE.findall(key))
        dst = sorted(PLACEHOLDER_RE.findall(value))
        if src != dst:
            problems.append(f"占位符不匹配: {key[:90]!r} -> {value[:90]!r}")
        if value.count("`") % 2 != key.count("`") % 2:
            problems.append(f"反引号奇偶不一致: {key[:90]!r}")
        for ch_open, ch_close in (("[", "]"),):
            if value.count(ch_open) != key.count(ch_open) or value.count(ch_close) != key.count(ch_close):
                problems.append(f"方括号数量变化: {key[:90]!r} -> {value[:90]!r}")

    # 工作区文件与基线的结构对比
    paths = list_source_files("all")
    sources = read_base(paths)
    for path, text in sources.items():
        target = ROOT / path
        if not target.exists():
            continue
        cur = target.read_text(encoding="utf8")
        if text.count("```") != cur.count("```"):
            problems.append(f"{path}: 代码围栏数量变化 {text.count('```')} -> {cur.count('```')}")
        if PLACEHOLDER_RE.search(cur):
            problems.append(f"{path}: 残留未还原的占位符")
        for tag in ("<ApiRefPage>", "</ApiRefPage>"):
            if text.count(tag) != cur.count(tag):
                problems.append(f"{path}: {tag} 数量变化")

    if problems:
        for p in problems[:200]:
            print("✗", p)
        print(f"\n共 {len(problems)} 处问题")
        return 1
    print("✓ 校验通过：占位符、代码围栏、JSX 包裹标签均与原文一致")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("extract", help="产出待译清单")
    e.add_argument("--scope", default="docs", choices=list(SCOPES))
    e.add_argument("--limit", type=int, default=4000)
    e.add_argument("--path", nargs="*", default=None, help="只处理这些路径前缀")
    e.add_argument("--by-file", action="store_true", help="按文中出现顺序排序，便于整篇连贯翻译")
    e.set_defaults(func=cmd_extract)

    a = sub.add_parser("apply", help="回填译文")
    a.add_argument("--scope", default="all", choices=list(SCOPES))
    a.set_defaults(func=cmd_apply)

    s = sub.add_parser("stats", help="覆盖率统计")
    s.set_defaults(func=cmd_stats)

    v = sub.add_parser("verify", help="结构校验")
    v.set_defaults(func=cmd_verify)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

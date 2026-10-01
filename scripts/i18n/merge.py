#!/usr/bin/env python3
"""把一批译文按「待译清单里的序号」合并进翻译记忆库。

译文批次文件形如：
    {"0": "定义 ⟦2⟧⟦0⟧ 事件。继承自 ⟦1⟧。", "1": "暂无摘要。"}

序号对应 <scope>.todo.json 里 segments 数组的下标，这样写译文时不必重复
抄一遍英文 key，也就不会抄错。合并前会校验占位符集合是否一致。

    python3 scripts/i18n/merge.py api batch.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TM_DIR = HERE / "tm"
PLACEHOLDER_RE = re.compile(r"\u27e6(\d+)\u27e7")

TARGET = {"docs": "docs.json", "api": "api.json", "meta": "docs.json"}


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    scope, batch_path = sys.argv[1], sys.argv[2]
    todo = json.loads((TM_DIR / f"{scope}.todo.json").read_text(encoding="utf8"))
    segments = todo["segments"]
    batch = json.loads(Path(batch_path).read_text(encoding="utf8"))

    tm_file = TM_DIR / TARGET[scope]
    tm = json.loads(tm_file.read_text(encoding="utf8")) if tm_file.exists() else {}

    added = skipped = 0
    errors: list[str] = []
    for idx_str, value in batch.items():
        idx = int(idx_str)
        if idx >= len(segments):
            errors.append(f"序号 {idx} 越界")
            continue
        key = segments[idx]["en"]
        if not isinstance(value, str) or not value.strip():
            skipped += 1
            continue
        src = sorted(PLACEHOLDER_RE.findall(key))
        dst = sorted(PLACEHOLDER_RE.findall(value))
        if src != dst:
            errors.append(f"[{idx}] 占位符不一致 {src} != {dst}\n     EN: {key[:110]}\n     ZH: {value[:110]}")
            continue
        if key.count("[") != value.count("[") or key.count("]") != value.count("]"):
            errors.append(f"[{idx}] 方括号数量不一致\n     EN: {key[:110]}\n     ZH: {value[:110]}")
            continue
        tm[key] = value
        added += 1

    if errors:
        for e in errors:
            print("✗", e)
        print(f"\n{len(errors)} 条未合并（其余 {added} 条已写入）")

    tm_file.write_text(json.dumps(tm, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf8")
    print(f"✓ {scope}: 新增/更新 {added} 条，跳过 {skipped} 条，记忆库共 {len(tm)} 条 -> {tm_file.name}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

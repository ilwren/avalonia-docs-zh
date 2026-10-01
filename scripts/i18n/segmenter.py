"""Markdown / MDX 分段器。

设计目标：
  1. 把文档拆成「可翻译片段」，代码、JSX 标签、链接地址、API 标识符一律屏蔽成占位符，
     保证译文回填后结构与原文完全一致。
  2. 同一个 walk() 既用于「抽取」也用于「回填」，两边逻辑天然一致，不会跑偏。
  3. 片段 key 使用屏蔽后的文本，于是 `Namespace: Avalonia.Controls` 与
     `Namespace: Avalonia.Media` 归一化成同一条，自动生成的 API 文档去重率极高。

占位符写作 ⟦n⟧，译文必须原样保留。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable, Iterable, Optional

PLACEHOLDER = "\u27e6{}\u27e7"
PLACEHOLDER_RE = re.compile(r"\u27e6(\d+)\u27e7")

# ---------------------------------------------------------------------------
# 行内屏蔽规则（顺序敏感：先行内代码，再标签，最后裸标识符）
# ---------------------------------------------------------------------------

_INLINE_RULES: list[re.Pattern] = [
    re.compile(r"`{1,3}[^`\n]*?`{1,3}"),            # `inline code`
    re.compile(r"<[^<>\n]{1,500}?>"),                 # <div ...> / </div> / <br/>
    re.compile(r"\{[^{}\n]{0,500}\}"),               # {mdxExpression}
    re.compile(r"\]\(<?[^)\n]*?>?\)"),               # ](url "title")
    re.compile(r"\]\[[^\]\n]{0,120}\]"),             # ][ref]
    re.compile(r"&[a-zA-Z#0-9]{1,10};"),             # &gt; &amp; &#8203;
    re.compile(r"https?://[^\s)\]<>\"']+"),          # 裸 URL
    re.compile(r"(?<![\w/])[~./]{0,3}[\w./-]*\.(?:cs|xaml|axaml|csproj|fsproj|sln|json|md|mdx|ts|tsx|js|jsx|yml|yaml|props|targets|dll|exe|png|svg|jpg|gif|sh|ps1|xml|config|plist|razor)\b"),
]

# 形如 Avalonia.Controls.Button / System.IDisposable 的点分标识符
_DOTTED_ID = re.compile(
    r"\b[A-Za-z_][A-Za-z0-9_]+(?:\.[A-Za-z_][A-Za-z0-9_]+)+(?:<[^<>\n]{0,80}>)?(?:\(\))?"
)

# 看起来像「纯标识符」的片段，不值得翻译
_IDENTIFIER_ONLY = re.compile(r"^[A-Za-z0-9_.<>,\[\]()&;:\-+*/\\|\s\u27e6\u27e7]*$")
_HAS_LETTER = re.compile(r"[A-Za-z]")
_WORD = re.compile(r"[A-Za-z][A-Za-z'-]*")

# 这些单 token 词即便独立成段也值得翻译
_STANDALONE_WORDS = {
    # API 参考页的固定小节
    "namespace", "assembly", "package", "source", "inheritance", "implements",
    "remarks", "returns", "parameters", "exceptions", "examples", "definition",
    "constructors", "methods", "properties", "events", "fields", "operators",
    "attributes", "overloads", "summary", "description", "name", "value", "type",
    "note", "warning", "tip", "caution", "danger", "info", "important",
    # 手写文档常见的单词小节标题
    "welcome", "overview", "introduction", "usage", "reference", "requirements",
    "prerequisites", "installation", "troubleshooting", "limitations", "notes",
    "glossary", "resources", "conclusion", "tips", "caveats", "syntax", "output",
    "input", "result", "results", "setup", "configuration", "platforms",
    "features", "benefits", "alternatives", "migration", "compatibility",
    "performance", "security", "testing", "debugging", "deployment", "packaging",
    "publishing", "logging", "accessibility", "recommendations", "background",
    "basics", "concepts", "options", "parameters", "steps", "capability",
}


def _looks_like_identifier(word: str) -> bool:
    return bool(re.fullmatch(r"[A-Z][a-z0-9]*(?:[A-Z][A-Za-z0-9]*)+|[a-z]+[A-Z][A-Za-z0-9]*", word))


def _is_translatable(text: str, force: bool = False) -> bool:
    """判断去掉占位符后是否还剩下值得翻译的英文内容。

    force=True 用于 front matter 与表头这类「一定是人读的文字」的位置，
    此时放宽单词数限制，但仍然拦掉明显是标识符的内容。
    """
    bare = PLACEHOLDER_RE.sub(" ", text).strip()
    if not bare or not _HAS_LETTER.search(bare):
        return False
    words = _WORD.findall(bare)
    if not words:
        return False
    lowered = [w.lower() for w in words]
    # 单个词：只有在白名单里、带冒号、或处于 force 位置时才翻
    if len(words) == 1:
        if force:
            return not _looks_like_identifier(words[0])
        return lowered[0] in _STANDALONE_WORDS or bare.rstrip().endswith(":")
    # 全是驼峰 / 点分标识符风格，且没有常见英文虚词 -> 判定为代码而非散文
    if _IDENTIFIER_ONLY.match(bare) and not any(
        w in {"the", "a", "an", "of", "to", "is", "are", "and", "or", "for",
              "in", "on", "with", "this", "that", "be", "not", "if", "when",
              "from", "by", "as", "it", "its", "can", "will", "has", "have"}
        for w in lowered
    ):
        if all(re.fullmatch(r"[A-Z][A-Za-z0-9]*|[a-z]+[A-Z][A-Za-z0-9]*", w) for w in words):
            return False
    return True


@dataclass
class Protector:
    """把受保护的内容换成占位符，翻译完再换回来。"""

    extra_terms: tuple[str, ...] = ()
    _extra_re: Optional[re.Pattern] = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        terms = sorted({t for t in self.extra_terms if t and len(t) > 1}, key=len, reverse=True)
        if terms:
            self._extra_re = re.compile(r"\b(?:%s)\b" % "|".join(re.escape(t) for t in terms))

    def mask(self, text: str, use_extra: bool = False) -> tuple[str, list[str]]:
        tokens: list[str] = []

        def take(match: re.Match) -> str:
            tokens.append(match.group(0))
            return PLACEHOLDER.format(len(tokens) - 1)

        for rule in _INLINE_RULES:
            text = rule.sub(take, text)

        def take_dotted(match: re.Match) -> str:
            raw = match.group(0)
            if not any(c.isupper() for c in raw) or len(raw) < 5:
                return raw
            tokens.append(raw)
            return PLACEHOLDER.format(len(tokens) - 1)

        text = _DOTTED_ID.sub(take_dotted, text)

        if use_extra and self._extra_re is not None:
            text = self._extra_re.sub(take, text)

        return text, tokens

    @staticmethod
    def unmask(text: str, tokens: list[str]) -> str:
        def put(match: re.Match) -> str:
            idx = int(match.group(1))
            return tokens[idx] if idx < len(tokens) else match.group(0)

        return PLACEHOLDER_RE.sub(put, text)


@dataclass
class Segment:
    """一个待翻译片段。"""

    key: str           # 屏蔽后的源文本，同时作为翻译记忆库的键
    kind: str          # prose / heading / table-cell / frontmatter / jsx-text / admonition
    path: str
    line: int
    tokens: list[str] = field(default_factory=list)


Handler = Callable[[Segment], Optional[str]]

# ---------------------------------------------------------------------------
# 块级识别
# ---------------------------------------------------------------------------

_FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
_HEADING_RE = re.compile(r"^(\s{0,3}#{1,6}\s+)(.*?)(\s*\{#[^}]+\})?\s*$")
_SETEXT_RE = re.compile(r"^\s{0,3}(=+|-{2,})\s*$")
_LIST_RE = re.compile(r"^(\s*(?:[-*+]|\d{1,3}[.)])\s+(?:\[[ xX]\]\s+)?)(.*)$")
_QUOTE_RE = re.compile(r"^(\s*>+\s?)(.*)$")
_TABLE_SEP_RE = re.compile(r"^\s*\|?[\s:|-]+\|[\s:|-]*$")
_IMPORT_RE = re.compile(r"^\s*(?:import|export)\s")
_ADMONITION_RE = re.compile(r"^(\s*:::+\s*[a-zA-Z-]+\s*)(.*?)\s*$")
_HTML_COMMENT_RE = re.compile(r"^\s*<!--")

# API 成员标题：`### Content Property` -> 屏蔽掉 `Content`
_MEMBER_HEADING_RE = re.compile(
    r"^(\S+?)\s+(Constructor|Constructors|Property|Method|Event|Field|Operator|Class|Struct|Interface|Enum|Delegate|Namespace)$"
)

_FM_TRANSLATABLE_KEYS = {"title", "description", "sidebar_label", "label", "tagline"}


def _slugify(text: str) -> str:
    """近似 github-slugger，用于在翻译标题时锁定原始锚点。"""
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[*_~]", "", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\u4e00-\u9fff\- ]+", "", text)
    text = text.replace(" ", "-")
    return re.sub(r"-{2,}", "-", text).strip("-")


class Walker:
    """逐块遍历文档；handler 返回译文则替换，返回 None 则保持原样。"""

    def __init__(self, path: str, handler: Handler, *, protect_terms: Iterable[str] = (),
                 keep_api_title: bool = True, anchor_pin: bool = True) -> None:
        self.path = path
        self.handler = handler
        self.protector = Protector(tuple(protect_terms))
        self.keep_api_title = keep_api_title
        self.anchor_pin = anchor_pin
        # 复现 github-slugger 的重复标题编号（第二个同名标题 -> slug-1）
        self._slug_seen: dict[str, int] = {}

    # -- 单段处理 ---------------------------------------------------------
    def _render(self, raw: str, kind: str, lineno: int, *, use_extra: bool = False,
                force: bool = False) -> str:
        masked, tokens = self.protector.mask(raw, use_extra=use_extra)
        if not _is_translatable(masked, force=force):
            return raw
        seg = Segment(key=masked.strip(), kind=kind, path=self.path, line=lineno, tokens=tokens)
        result = self.handler(seg)
        if result is None:
            return raw
        # 还原原文首尾空白，避免破坏缩进
        lead = raw[: len(raw) - len(raw.lstrip())]
        trail = raw[len(raw.rstrip()):]
        return lead + self.protector.unmask(result.strip(), tokens) + trail

    # -- JSX 结构行：只翻标签之间的文本 ------------------------------------
    def _render_jsx_line(self, line: str, lineno: int) -> str:
        if self.keep_api_title and "apiref-page__title" in line:
            return line
        parts = re.split(r"(<[^<>\n]{1,500}?>)", line)
        for i, part in enumerate(parts):
            if part.startswith("<") and part.endswith(">"):
                continue
            if not part.strip():
                continue
            parts[i] = self._render(part, "jsx-text", lineno, use_extra=True)
        return "".join(parts)

    # -- 表格行 -----------------------------------------------------------
    def _render_table_row(self, line: str, lineno: int, header: bool = False) -> str:
        lead = line[: len(line) - len(line.lstrip())]
        cells = line.strip().split("|")
        for i, cell in enumerate(cells):
            if not cell.strip():
                continue
            cells[i] = self._render(cell, "table-header" if header else "table-cell",
                                    lineno, force=header)
        return lead + "|".join(cells)

    # -- 标题 -------------------------------------------------------------
    def _render_heading(self, line: str, lineno: int) -> str:
        m = _HEADING_RE.match(line)
        if not m:
            return line
        prefix, body, explicit_anchor = m.group(1), m.group(2), m.group(3) or ""
        if not body.strip():
            return line

        base_slug = _slugify(body)
        member = _MEMBER_HEADING_RE.match(body.strip())
        use_extra = True
        if member:
            # 把成员名当作受保护术语临时注入
            ident, suffix = member.group(1), member.group(2)
            tokens = [ident]
            masked = PLACEHOLDER.format(0) + " " + suffix
            seg = Segment(key=masked, kind="heading", path=self.path, line=lineno, tokens=tokens)
            result = self.handler(seg)
            if result is None:
                self._claim_slug(base_slug)
                return line
            new_body = Protector.unmask(result.strip(), tokens)
        else:
            rendered = self._render(body, "heading", lineno, use_extra=use_extra)
            if rendered == body:
                self._claim_slug(base_slug)
                return line
            new_body = rendered.strip()

        anchor = explicit_anchor
        if explicit_anchor:
            self._claim_slug(base_slug)
        if self.anchor_pin and not explicit_anchor:
            slug = self._claim_slug(_slugify(body))
            if slug and slug != _slugify(new_body):
                anchor = " {#%s}" % slug
        return prefix + new_body + anchor

    def _claim_slug(self, slug: str) -> str:
        """按出现顺序分配锚点，重复标题追加 -1、-2 …（与 github-slugger 一致）。"""
        if not slug:
            return slug
        n = self._slug_seen.get(slug, 0)
        self._slug_seen[slug] = n + 1
        return slug if n == 0 else f"{slug}-{n}"

    # -- 主循环 -----------------------------------------------------------
    @staticmethod
    def _opens_tag(line: str) -> bool:
        """这一行是否起了一个跨行的 JSX/HTML 标签（`<Foo` 后面没有 `>`）。

        只认 `<` 紧跟字母或 `/` 的情况，避免把散文里的 `a < b` 误判成标签。
        """
        rest = re.sub(r"`[^`\n]*`", "", line)          # 行内代码不算
        rest = re.sub(r"<[^<>\n]*?>", "", rest)        # 去掉本行闭合的完整标签
        m = re.search(r"<[A-Za-z/!]", rest)
        return bool(m) and ">" not in rest[m.start():]

    @staticmethod
    def _closes_tag(line: str) -> bool:
        rest = re.sub(r"<[^<>\n]*?>", "", line)
        return ">" in rest

    def run(self, text: str) -> str:
        lines = text.split("\n")
        out: list[str] = []
        i = 0
        n = len(lines)
        open_tag = 0

        # front matter
        if lines and lines[0].strip() == "---":
            out.append(lines[0])
            i = 1
            while i < n and lines[i].strip() != "---":
                out.append(self._render_frontmatter_line(lines[i], i + 1))
                i += 1
            if i < n:
                out.append(lines[i])
                i += 1

        while i < n:
            line = lines[i]
            stripped = line.strip()

            # 位于一个尚未闭合的多行 JSX 标签内部：原样保留
            if open_tag > 0:
                out.append(line)
                open_tag = 0 if self._closes_tag(line) else open_tag - 1
                i += 1
                continue
            if self._opens_tag(line):
                out.append(line)
                open_tag = 30          # 最多跨 30 行，避免误判吞掉整篇
                i += 1
                continue

            fence = _FENCE_RE.match(line)
            if fence:
                marker = fence.group(2)
                out.append(line)
                i += 1
                while i < n:
                    out.append(lines[i])
                    if lines[i].strip().startswith(marker[0] * 3):
                        i += 1
                        break
                    i += 1
                continue

            if not stripped:
                out.append(line)
                i += 1
                continue

            if _IMPORT_RE.match(line) or _HTML_COMMENT_RE.match(line):
                out.append(line)
                i += 1
                continue

            adm = _ADMONITION_RE.match(line)
            if adm and stripped.startswith(":::"):
                out.append(adm.group(1) + self._render(adm.group(2), "admonition", i + 1)
                           if adm.group(2).strip() else line)
                i += 1
                continue

            if _HEADING_RE.match(line) and stripped.startswith("#"):
                out.append(self._render_heading(line, i + 1))
                i += 1
                continue

            if stripped.startswith("|"):
                if _TABLE_SEP_RE.match(line):
                    out.append(line)
                else:
                    is_header = i + 1 < n and bool(_TABLE_SEP_RE.match(lines[i + 1]))
                    out.append(self._render_table_row(line, i + 1, header=is_header))
                i += 1
                continue

            if stripped.startswith("<"):
                out.append(self._render_jsx_line(line, i + 1))
                i += 1
                continue

            quote = _QUOTE_RE.match(line)
            if quote and stripped.startswith(">"):
                out.append(quote.group(1) + self._render(quote.group(2), "prose", i + 1))
                i += 1
                continue

            lst = _LIST_RE.match(line)
            if lst:
                out.append(lst.group(1) + self._render(lst.group(2), "prose", i + 1))
                i += 1
                continue

            # 普通散文：合并软换行的连续行
            block: list[str] = [line]
            j = i + 1
            while j < n:
                nxt = lines[j]
                if (not nxt.strip() or nxt.strip().startswith(("|", "<", ">", "#", ":::", "```", "~~~"))
                        or _LIST_RE.match(nxt) or _IMPORT_RE.match(nxt)
                        or block[-1].endswith("  ") or block[-1].endswith("\\")):
                    break
                block.append(nxt)
                j += 1
            if _SETEXT_RE.match(lines[j]) if j < n else False:
                out.extend(block)
                i = j
                continue
            merged = "\n".join(block)
            out.append(self._render(merged, "prose", i + 1))
            i = j

        return "\n".join(out)

    def _render_frontmatter_line(self, line: str, lineno: int) -> str:
        m = re.match(r"^(\s*)([A-Za-z_][\w-]*)(\s*:\s*)(.*)$", line)
        if not m:
            return line
        indent, key, sep, value = m.groups()
        if key not in _FM_TRANSLATABLE_KEYS or not value.strip():
            return line
        quote = ""
        body = value.strip()
        if len(body) >= 2 and body[0] in "\"'" and body[-1] == body[0]:
            quote = body[0]
            body = body[1:-1]
        rendered = self._render(body, "frontmatter", lineno, force=True)
        if rendered == body:
            return line
        if not quote and (":" in rendered or rendered.strip().startswith(("#", "&", "*", "{", "["))):
            quote = "'"
        if quote == "'":
            rendered = rendered.replace("'", "''")
        return f"{indent}{key}{sep}{quote}{rendered}{quote}"


def transform(text: str, path: str, handler: Handler, **kw) -> str:
    return Walker(path, handler, **kw).run(text)

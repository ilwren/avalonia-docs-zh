/**
 * 用 Docusaurus 同款的 MDX 编译器逐篇校验文档。
 *
 * 整站 build 要做 SSR，吃内存又耗时；而翻译真正可能引入的风险只有 MDX 语法本身
 * （标签被截断、花括号被破坏、表格列数变化等）。这里只做编译，速度快几十倍，
 * 足以在提交前兜住回归。
 *
 *   node scripts/i18n/check_mdx.mjs docs controls tools troubleshooting xpf api
 */
import { compile } from '@mdx-js/mdx';
import remarkFrontmatter from 'remark-frontmatter';
import remarkGfm from 'remark-gfm';
import remarkDirective from 'remark-directive';
import { readFile, readdir, stat } from 'node:fs/promises';
import path from 'node:path';

const roots = process.argv.slice(2);
if (roots.length === 0) {
  console.error('用法: node scripts/i18n/check_mdx.mjs <目录...>');
  process.exit(2);
}

async function* walk(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) yield* walk(full);
    else if (/\.mdx?$/.test(entry.name)) yield full;
  }
}

/**
 * 复刻 Docusaurus 交给 MDX 编译器之前的预处理（见 @docusaurus/utils 的
 * escapeMarkdownHeadingIds）：只有「行首（无缩进）」的 ATX 标题，其中的 `{#`
 * 才会被转义成 `\\{#`。带缩进的标题不在此列 —— 它的 `{#id}` 会被 MDX 当作
 * JS 表达式，直接报 "Could not parse expression with acorn"。
 * 这里一比一照搬该正则，使校验结果与真实构建完全一致。
 */
function escapeMarkdownHeadingIds(content) {
  const markdownHeadingRegexp = /(?:^|\n)#{1,6}(?!#).*/g;
  return content.replaceAll(markdownHeadingRegexp, (substring) =>
    substring.replace('{#', '\\{#').replace('\\\\{#', '\\{#'));
}

const options = {
  format: 'mdx',
  remarkPlugins: [remarkFrontmatter, remarkGfm, remarkDirective],
  development: false,
};

let checked = 0;
const failures = [];

for (const root of roots) {
  try {
    await stat(root);
  } catch {
    continue;
  }
  for await (const file of walk(root)) {
    checked++;
    const source = escapeMarkdownHeadingIds(await readFile(file, 'utf8'));
    try {
      // docusaurus.config.ts 未设置 markdown.format，默认即 'mdx'：
      // .md 与 .mdx 一律按 MDX 编译，这里保持一致。
      await compile(source, options);
    } catch (error) {
      failures.push({ file, message: error.message?.split('\n')[0] ?? String(error) });
    }
    if (checked % 500 === 0) process.stderr.write(`  ...已校验 ${checked} 篇\n`);
  }
}

if (failures.length) {
  console.error(`\n✗ ${failures.length} / ${checked} 篇编译失败：\n`);
  for (const f of failures.slice(0, 50)) console.error(`  ${f.file}\n    ${f.message}`);
  if (failures.length > 50) console.error(`  ...另有 ${failures.length - 50} 篇`);
  process.exit(1);
}

console.log(`✓ ${checked} 篇文档全部通过 MDX 编译校验`);

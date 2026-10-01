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
 * Docusaurus 在交给 MDX 编译器之前，会先把标题行末尾的显式锚点 `{#id}` 摘掉
 * （见 parseMarkdownHeadingId）。独立调用 @mdx-js/mdx 时没有这一步，`{#id}`
 * 会被当成 JS 表达式而报 "Could not parse expression with acorn"。
 * 这里复刻该预处理，让校验结果与真实构建保持一致。
 */
function stripExplicitHeadingIds(source) {
  return source.replace(/^(\s{0,3}#{1,6}\s.*?)\s*\{#[\w-]+\}\s*$/gm, '$1');
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
    const source = stripExplicitHeadingIds(await readFile(file, 'utf8'));
    try {
      // Docusaurus 对 .md 走的是更宽松的 CommonMark 解析，这里统一按 mdx 严格校验
      await compile(source, { ...options, format: file.endsWith('.mdx') ? 'mdx' : 'md' });
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

/**
 * 把文档正文里「泛指社区讨论区」的链接改指向本仓库的 GitHub Discussions。
 *
 * 为什么用 remark 插件而不是直接改 markdown：
 * 翻译流水线（scripts/i18n/i18n_cli.py apply）每次都会从英文基线提交重新渲染
 * docs/controls/tools/troubleshooting/xpf 下的文件，手改的 URL 会被覆盖掉。
 * 在构建期改写既不碰源文件，也不会被流水线回滚。
 *
 * 只改写「不带具体帖子编号」的通用入口；指向上游某一条具体讨论的链接
 * （例如 .../discussions/19721）保持原样，因为那是内容引用，不是社区入口。
 */

const UPSTREAM_DISCUSSIONS = 'https://github.com/AvaloniaUI/Avalonia/discussions';
const LOCAL_DISCUSSIONS = 'https://github.com/ilwren/avalonia-docs-zh/discussions';

/** @param {string} url */
function rewrite(url) {
  if (!url) return url;
  const normalized = url.replace(/\/+$/, '');
  return normalized === UPSTREAM_DISCUSSIONS ? LOCAL_DISCUSSIONS : url;
}

module.exports = function communityLinksPlugin() {
  return async (tree) => {
    const { visit } = await import('unist-util-visit');

    visit(tree, (node) => {
      // 普通 markdown 链接：[文字](url)
      if (node.type === 'link' && typeof node.url === 'string') {
        node.url = rewrite(node.url);
        return;
      }
      // MDX / HTML 里的 <a href="...">
      if (
        (node.type === 'mdxJsxTextElement' || node.type === 'mdxJsxFlowElement') &&
        node.name === 'a' &&
        Array.isArray(node.attributes)
      ) {
        for (const attr of node.attributes) {
          if (attr.type === 'mdxJsxAttribute' && attr.name === 'href' && typeof attr.value === 'string') {
            attr.value = rewrite(attr.value);
          }
        }
        return;
      }
      if (node.type === 'html' && typeof node.value === 'string' && node.value.includes(UPSTREAM_DISCUSSIONS)) {
        node.value = node.value.split(`${UPSTREAM_DISCUSSIONS}"`).join(`${LOCAL_DISCUSSIONS}"`);
      }
    });
  };
};

module.exports.UPSTREAM_DISCUSSIONS = UPSTREAM_DISCUSSIONS;
module.exports.LOCAL_DISCUSSIONS = LOCAL_DISCUSSIONS;

/**
 * DocItemContent renders the doc's markdown body, plus the "synthetic" page
 * title when the title comes from front matter rather than the content.
 *
 * Original source:
 * @link https://github.com/facebook/docusaurus/blob/main/packages/docusaurus-theme-classic/src/theme/DocItem/Content/index.tsx
 *
 * Reason for overriding:
 * - Render a page's companion video as a pill button directly below the page
 *   title. It lives here rather than in DocItem/Layout because the <h1> is
 *   rendered here, and the button has to follow it.
 * - 在中文站首页文档（docs/welcome）顶部插入 AI 翻译免责说明。
 */

import React, {type ReactNode} from 'react';
import clsx from 'clsx';
import {ThemeClassNames} from '@docusaurus/theme-common';
import {useDoc} from '@docusaurus/plugin-content-docs/client';
import Heading from '@theme/Heading';
import MDXContent from '@theme/MDXContent';
import Admonition from '@theme/Admonition';
import Link from '@docusaurus/Link';
import type {Props} from '@theme/DocItem/Content';
import {
  CompanionVideoButton,
  useCompanionVideo,
} from '@site/src/components/global/CompanionVideo';
import companionVideoStyles from './companionVideo.module.css';

/**
 Title can be declared inside md content or declared through
 front matter and added manually. To make both cases consistent,
 the added title is added under the same div.markdown block
 See https://github.com/facebook/docusaurus/pull/4882#issuecomment-853021120

 We render a "synthetic title" if:
 - user doesn't ask to hide it with front matter
 - the markdown content does not already contain a top-level h1 heading
*/
function useSyntheticTitle(): string | null {
  const {metadata, frontMatter, contentTitle} = useDoc();
  const shouldRender =
    !frontMatter.hide_title && typeof contentTitle === 'undefined';
  if (!shouldRender) {
    return null;
  }
  return metadata.title;
}

// 需要展示 AI 翻译免责说明的页面（按 permalink 结尾匹配，不受 baseUrl 影响）。
const DISCLAIMER_PAGES = ['/docs/welcome'];

const UPSTREAM_REPO = 'https://github.com/AvaloniaUI/avalonia-docs';
const UPSTREAM_DOCS = 'https://docs.avaloniaui.net';
const DISCUSSIONS = 'https://github.com/ilwren/avalonia-docs-zh/discussions';

function AiDisclaimer(): ReactNode {
  return (
    <Admonition type="caution" title="关于这份中文文档（AI 翻译免责说明）">
      <p>
        本站内容由 <strong>AI 自动翻译</strong>自 Avalonia 官方英文文档（
        <Link to={UPSTREAM_REPO}>AvaloniaUI/avalonia-docs</Link>
        ），仅经过有限的人工校对，<strong>可能存在错译、漏译或与上游版本不同步</strong>的情况。
      </p>
      <p>
        涉及 API 行为、许可条款、安全与部署等关键决策时，请以{' '}
        <Link to={UPSTREAM_DOCS}>官方英文文档</Link>{' '}
        为准；代码示例、类型名与 API 标识符均保留英文原文。
      </p>
      <p>
        本项目与 Avalonia 官方团队无关，不提供任何担保。发现翻译问题，欢迎到{' '}
        <Link to={DISCUSSIONS}>本仓库的 GitHub 讨论区</Link> 反馈。
      </p>
    </Admonition>
  );
}

export default function DocItemContent({children}: Props): ReactNode {
  const syntheticTitle = useSyntheticTitle();
  const companionVideo = useCompanionVideo();
  const {frontMatter, toc, metadata} = useDoc();
  const permalink = metadata?.permalink ?? '';
  const showDisclaimer = DISCLAIMER_PAGES.some(
    (page) => permalink === page || permalink.endsWith(page) || permalink.endsWith(`${page}/`),
  );

  // Whether this page gets a TOC column at all. The width half is left to the
  // `hiddenOnDesktop` media query, which is what actually hides the button
  // where the TOC panel's thumbnail card takes over.
  const hasTOCColumn = !frontMatter.hide_table_of_contents && toc.length > 0;

  return (
    <div className={clsx(ThemeClassNames.docs.docMarkdown, 'markdown')}>
      {syntheticTitle && (
        <header>
          <Heading as="h1">{syntheticTitle}</Heading>
        </header>
      )}
      {/* Placed after the synthetic title so it reads as part of the page
          header. A page that writes its own `# H1` in the body gets no
          synthetic title, so the button would sit above it. For that reason,
          every page with a companion video should take its title from front matter. */}
      {companionVideo && (
        <CompanionVideoButton
          video={companionVideo}
          className={clsx(hasTOCColumn && companionVideoStyles.hiddenOnDesktop)}
        />
      )}
      {showDisclaimer && <AiDisclaimer />}
      <MDXContent>{children}</MDXContent>
    </div>
  );
}

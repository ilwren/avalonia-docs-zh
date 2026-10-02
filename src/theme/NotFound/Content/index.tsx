import React, {type ReactNode} from 'react';
import clsx from 'clsx';
import {useBaseUrlUtils} from '@docusaurus/useBaseUrl';
import type {Props} from '@theme/NotFound/Content';

const NAV_SECTIONS = [
  {label: '指南', href: '/docs/welcome', description: '概念、教程与操作指引'},
  {label: '控件', href: '/controls', description: '内置控件参考'},
  {label: '工具', href: '/tools', description: '开发工具与扩展'},
  {label: 'API 参考', href: '/api', description: '完整 API 参考'},
  {label: 'Avalonia XPF', href: '/xpf', description: 'WPF 兼容层'},
  {label: '疑难排查', href: '/troubleshooting', description: '常见问题与解决办法'},
];

export default function NotFoundContent({className}: Props): ReactNode {
  // withBaseUrl 保证部署到 GitHub Pages 这类子路径站点时链接依然正确。
  const {withBaseUrl} = useBaseUrlUtils();
  return (
    <main className={clsx('container margin-vert--xl', className)}>
      <div className="row">
        <div className="col col--6 col--offset-3">
          <h1>页面不存在</h1>
          <p>没有找到你要访问的内容。</p>
          <img src='https://media.giphy.com/media/PibODdY9C5xiKzmRhW/giphy.gif'/>
          <h2 style={{
            fontSize: '0.625rem',
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            color: 'var(--ifm-color-secondary-darkest)',
            marginTop: '2rem',
            marginBottom: '1rem',
          }}>
            浏览文档
          </h2>
          <ul style={{listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.5rem'}}>
            {NAV_SECTIONS.map(({label, href, description}) => (
              <li key={href}>
                <a
                  href={withBaseUrl(href)}
                  style={{textDecoration: 'none', display: 'block', padding: '0.5rem 0.75rem', borderRadius: '6px', border: '1px solid var(--ifm-toc-border-color)', transition: 'border-color 0.15s ease, background 0.15s ease'}}
                  onMouseEnter={e => {
                    e.currentTarget.style.borderColor = 'var(--ifm-link-color)';
                    e.currentTarget.style.background = 'var(--ifm-hover-overlay)';
                  }}
                  onMouseLeave={e => {
                    e.currentTarget.style.borderColor = 'var(--ifm-toc-border-color)';
                    e.currentTarget.style.background = 'transparent';
                  }}
                >
                  <span style={{display: 'block', fontWeight: 600, fontSize: '0.875rem', color: 'var(--ifm-heading-color)'}}>{label}</span>
                  <span style={{display: 'block', fontSize: '0.75rem', color: 'var(--ifm-color-secondary-darkest)', marginTop: '2px'}}>{description}</span>
                </a>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </main>
  );
}

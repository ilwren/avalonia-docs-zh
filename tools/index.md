---
id: index
title: Avalonia Tools
sidebar_label: Avalonia Tools
doc-type: overview
---

import DocsCard from '@site/src/components/global/DocsCard';
import DocsCards from '@site/src/components/global/DocsCards';

<head>
  <title>Avalonia Tools</title>
  <meta
    name="description"
    content="Professional developer tools for Avalonia. Debug visually, package effortlessly, and build faster."
  />
  <style>{`
    :root {
      --doc-item-container-width: 60rem;
    }
  `}</style>
</head>

Avalonia 是一个免费开源的 UI 框架。你可以零成本地开发并发布跨平台 .NET 应用。框架采用 MIT 许可证，由一支不断壮大的团队维护。

开发工具链管的是框架之外的那些活儿：诊断布局问题、为多种操作系统打包应用，以及边写边预览 XAML。

## Avalonia Plus

Avalonia Plus 是一套专为 Avalonia 开发打造的专业工具。

<DocsCards>
<DocsCard header="Dev Tools" href="/tools/developer-tools/installation" img="/icons/feature-devtools-icon.png">
  <p>可视化地检视和诊断你的 Avalonia 应用：实时改属性、分析性能、调试布局，不必再靠猜。</p>
</DocsCard>

<DocsCard header="Parcel" href="/tools/parcel/setup" img="/icons/feature-parcel-icon.png">
  <p>一个工具搞定 Windows、macOS 和 Linux 的打包，代码签名、公证和安装包都替你办妥。</p>
</DocsCard>

<DocsCard header="Avalonia for Visual Studio" href="/tools/visual-studio-extension" img="/icons/feature-vs-ext-icon.png">
  <p>专门打造的 Visual Studio 扩展，带 XAML 预览、代码补全和拖放式设计器。</p>
</DocsCard>
</DocsCards>

## Avalonia Pro

Avalonia Pro 涵盖 Avalonia Plus 中的全部专业工具，另外还包含 [Charts](/controls/data-display/charts/)、[TreeDataGrid](/controls/data-display/structured-data/treedatagrid/)、[RichTextEditor](/controls/input/text-input/richtexteditor/)、[PdfViewer](/controls/data-display/pdfviewer/)、[VirtualKeyboard](/controls/input/text-input/virtualkeyboard) 等高级 UI 控件。从展示层级数据到不捆绑 Chromium 就能嵌入原生网页内容，这些组件都能应付。

## 谁可以用 {#who-gets-access}

用于非商业用途时，[Community 许可证](https://avaloniaui.net/pricing)让你免费使用 Avalonia Plus 的工具和组件，没有试用期，也不锁功能。

面向更大的团队和组织，我们提供付费订阅，详见[价格页](https://avaloniaui.net/pricing)。

订阅收入用于支撑这个开源框架的持续开发。

<br />
<div style={{ display: 'flex', justifyContent: 'center', gap: '10px' }}>
  <Button label="Purchase Avalonia Enterprise" link="https://avaloniaui.net/pricing" variant="secondary" outline />
</div>

## 另请参阅 {#see-also}

- [AI Tools](/tools/ai-tools/)
- [IDE Support](/tools/ide/)
- [FAQ](/tools/faq)

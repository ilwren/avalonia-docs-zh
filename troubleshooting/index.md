---
id: index
title: 排查问题
sidebar_label: 首页
---

import DocsCard from '@site/src/components/global/DocsCard';
import DocsCards from '@site/src/components/global/DocsCards';

<head>
  <title>Avalonia 文档：排查问题</title>
  <meta
    name="description"
    content="Find guidance on diagnosing and resolving common issues in Avalonia apps, including installation, performance, platform-specific behaviour, and UI development."
  />
  <style>{`
    :root {
      --doc-item-container-width: 60rem;
    }
  `}</style>
</head>

这里汇集了开发 Avalonia 应用时常见问题的诊断与解决办法。无论你是卡在安装环节、遇上性能瓶颈，还是被样式与主题折腾得够呛，都能在这些页面里找到对症的指引，让应用重回正轨。

## General

<DocsCards>
  <DocsCard header="Installation" href="/troubleshooting/installation">
    <p>配置 .NET 和 Avalonia 时常见的问题。</p>
  </DocsCard>
  <DocsCard header="App performance issues" href="/troubleshooting/app-performance-issues">
    <p>提升 Avalonia 应用运行时性能的若干办法。</p>
  </DocsCard>
</DocsCards>

## Controls

<DocsCards>
  <DocsCard header="MediaPlayer" href="/troubleshooting/controls/mediaplayer">
    <p>Avalonia Pro MediaPlayer 控件的常见问题。</p>
  </DocsCard>
  <DocsCard header="MessageBox" href="/troubleshooting/controls/messagebox">
    <p>显示消息对话框的几种选择，含第三方替代方案。</p>
  </DocsCard>
  <DocsCard header="NumericUpDown" href="/troubleshooting/controls/numericupdown">
    <p>如何解决 NumericUpDown 控件的问题。</p>
  </DocsCard>
  <DocsCard header="RichTextEditor" href="/troubleshooting/controls/richtexteditor">
    <p>Avalonia Pro RichTextEditor 控件的常见问题与调试方法。</p>
  </DocsCard>
</DocsCards>

## 平台专属问题 {#platform-specific-issues}

<DocsCards>
  <DocsCard header="macOS" href="/troubleshooting/platform-specific-issues/macos">
    <p>macOS 专属问题，包括应用菜单与系统集成。</p>
  </DocsCard>
  <DocsCard header="WebAssembly" href="/troubleshooting/platform-specific-issues/webassembly">
    <p>在浏览器中运行 Avalonia 应用时的常见问题，包括原生库缺失。</p>
  </DocsCard>
  <DocsCard header="Windows" href="/troubleshooting/platform-specific-issues/windows">
    <p>Windows 专属问题，包括打包、签名和 SmartScreen 警告。</p>
  </DocsCard>
</DocsCards>

## Tools

<DocsCards>
  <DocsCard header="Developer tools" href="/troubleshooting/tools/developer-tools">
    <p>用 Avalonia DevTools 检视和调试应用时的常见问题。</p>
  </DocsCard>
</DocsCards>

## 界面开发 {#ui-development}

<DocsCards>
  <DocsCard header="Styles" href="/troubleshooting/ui-development/styles">
    <p>样式选择器的常见问题，包括悄无声息的失效和匹配不到目标。</p>
  </DocsCard>
  <DocsCard header="Themes" href="/troubleshooting/ui-development/themes">
    <p>控件主题的常见问题，包括主题查找和意料之外的连带影响。</p>
  </DocsCard>
</DocsCards>

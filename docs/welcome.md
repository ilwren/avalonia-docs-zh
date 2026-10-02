---
id: welcome
title: 欢迎
description: 开始使用跨平台 .NET UI 框架 Avalonia。这里有安装指南、教程、迁移路线和 API 参考。
doc-type: overview
---

<head>
  <title>Avalonia 文档</title>
  <meta
    name="description"
    content="Documentation for Avalonia, the cross-platform .NET UI framework. Build apps for Windows, macOS, Linux, iOS, Android, and WebAssembly from a single codebase."
  />
</head>

欢迎阅读 Avalonia 文档。无论你是在写第一个应用，还是在迁移现有项目，这里都涵盖了从安装到部署的全部内容。

:::info

本文档对应 Avalonia 12。Avalonia 11 的文档请访问 [v11.docs.avaloniaui.net](https://v11.docs.avaloniaui.net/)。

:::

## Avalonia 是什么？ {#what-is-avalonia}

Avalonia 是一个开源的 .NET 跨平台 UI 框架。它使用自研渲染引擎绘制控件，因此你的应用在每个平台上的外观和行为都完全一致。用 C# 或 F# 配合 XAML 写一次界面，即可发布到：

- **Windows** (10, 11)
- **macOS**（Apple Silicon 与 Intel）
- **桌面版 Linux**（X11 与 Wayland）
- **嵌入式 Linux**（树莓派等设备上的 framebuffer）
- **iOS** 与 **Android**
- **WebAssembly**

确切的版本与架构支持情况，请见[支持的平台](/docs/supported-platforms)。

## 核心能力 {#key-capabilities}

| 能力 | 说明 |
|---|---|
| **跨平台渲染** | Avalonia 自研的渲染引擎能在每个平台上输出像素级一致的画面。默认后端是 Skia，同时团队正与 Google 的 Flutter 团队合作，把 [Impeller](https://avaloniaui.net/blog/avalonia-partners-with-google-s-flutter-t-eam-to-bring-impeller-rendering-to-net) 渲染引擎引入 .NET。没有原生控件的包装层，也没有各平台各自为政的怪脾气。 |
| **XAML 与代码隐藏** | 既可以用 XAML 声明式地描述界面，也可以完全用代码构建。如果你用过 WPF 或 UWP，会觉得 Avalonia XAML 相当眼熟。 |
| **样式系统** | 一套借鉴 CSS 的样式系统，支持选择器、样式类、伪类和控件主题。详见[样式](/docs/styling/styles)。 |
| **数据绑定** | 编译期即完成校验的编译绑定、完整的 MVVM 支持，并可与 CommunityToolkit.Mvvm 集成。详见[数据绑定](/docs/data-binding/introduction-to-data-binding)。 |
| **丰富的控件库** | 内置 60 多个控件，涵盖 DataGrid、TreeView、TabControl、Calendar 等，且全部支持自定义样式与模板。 |
| **无障碍访问** | 跨平台内置支持屏幕阅读器与键盘导航。 |
| **DevTools** | 运行时按 <kbd>F12</kbd> 即可检视视觉树、属性、样式和布局。 |

## 选一条适合你的路线 {#choose-your-path}

### 初次接触 Avalonia？ {#new-to-avalonia}

1. [安装 Avalonia](/docs/get-started/install-avalonia) 并[配置你的 IDE](/docs/get-started/set-up-your-ide)
2. [创建你的第一个项目](/docs/get-started/create-your-first-project)
3. [跟着入门教程](/docs/get-started/starter-tutorial)做一个温度换算器
4. [掌握核心概念](/docs/fundamentals/avalonia-xaml)：XAML、控件、布局与视觉树

### 从 WPF 转过来？ {#coming-from-wpf}

Avalonia 的 API 刻意向 WPF 看齐，但在样式、模板和属性系统上仍有一些重要差异。

- [WPF 迁移指南](/docs/migration/wpf)：逐节对照说明
- [WPF 速查表](/docs/migration/wpf/cheat-sheet)：WPF 概念到 Avalonia 对应物的快速映射

如果你需要让现有 WPF 应用在不重写的前提下跨平台运行，[Avalonia XPF](/xpf) 在 Avalonia 渲染引擎之上提供了二进制兼容的 WPF 支持。

### 从 Avalonia 11 升级？ {#upgrading-from-avalonia-11}

Avalonia 12 默认启用编译绑定，并带来了全新的剪贴板 API、更新后的窗口装饰等改动。

- [Avalonia 12 的破坏性变更](/docs/avalonia12-breaking-changes)：完整清单，每项都附有迁移指引

### 想找示例？ {#looking-for-samples}

- [示例与教程](/docs/samples-tutorials)：入门应用、实战案例和视频讲解

## 需要帮助？ {#need-help}

如果卡住了，可以翻翻[疑难排查](/troubleshooting)页面，或者到 [GitHub Discussions](https://github.com/AvaloniaUI/Avalonia/discussions) 上与社区交流。

要报告缺陷，请在 [GitHub](https://github.com/AvaloniaUI/Avalonia) 上提交 issue。

## 另请参阅 {#see-also}

- [支持的平台](/docs/supported-platforms)
- [示例与教程](/docs/samples-tutorials)
- [Avalonia GitHub 仓库](https://github.com/AvaloniaUI/Avalonia)

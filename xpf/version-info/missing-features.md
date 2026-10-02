---
id: missing-features
title: 尚未支持的特性
description: 汇总 Avalonia XPF 中尚不可用、有所限制或计划日后支持的 WPF 特性。
doc-type: reference
---

## 概述 {#overview}

XPF 尽力实现 WPF 的全部 API，但受跨平台约束和底层架构差异所限，有些特性难以支持乃至无从支持。本页列出目前缺失、部分实现或多半不会补上的特性，方便你据此规划迁移。

## 有限制的特性 {#features-with-limitations}

下列特性虽然可用，但有已知的限制：

- **`WebBrowser`**：XPF 以另一套机制提供网页内容嵌入，细节请见 [WebView 文档](/docs/app-development/embedding-web-content)。
- **`FlowDocument`**：支持基本的流式文档渲染，但有以下限制：
  - 不支持分页文档。
  - 不支持 `PageHeader` 和 `PageFooter`。
  - 不支持 `Floater`。
  - 部分表格功能（比如跨行与跨列）不受支持。

## 计划在后续版本中支持的特性 {#features-planned-for-future-releases}

下列特性工程量不小，会在日后的版本中提供：

- `Viewport3D` 及相关的 3D API
- `MediaElement` and `MediaPlayer`
- `InkCanvas`

若你的应用离不开其中某项特性，请常去[发行说明](/xpf/version-info/release-notes)看看进展。

## 多半不会支持的特性 {#features-unlikely-to-be-supported}

受平台所限，下列特性多半不会支持：

- **多个 UI 线程**（多个 `Dispatcher` 实例）：macOS 只允许一个 UI 线程，Windows 和 Linux 上的支持也相当有限。更多细节请见[与 WPF 的已知差异](/xpf/migration/known-differences#multiple-ui-threads)。
- **`HwndHost` / `HwndSource`**：这两个类型与 Win32 窗口句柄绑得太死，没有跨平台的对应物。
- **`XPS`**：XPS 文档支持依赖 Windows 的某个系统组件，其他平台上没有。

## Workarounds

若你的应用依赖某项缺失或受限的特性，不妨考虑这几条路子：

- **条件编译**：用 `#if` 指令为 XPF 构建和 WPF 构建分别提供不同的实现。
- **运行时特性检测**：用之前先查一查该特性是否可用，不可用时给个体面的回退方案。
- **联系 XPF 团队**：若某个缺失的特性对你的应用至关重要，欢迎联系 Avalonia 团队——客户的呼声往往能左右特性的优先级。

## 另请参阅 {#see-also}

- [与 WPF 的已知差异](/xpf/migration/known-differences)
- [发行说明](/xpf/version-info/release-notes)
- [Versioning](/xpf/version-info/versioning)

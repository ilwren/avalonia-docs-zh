---
id: index
title: IDE Support
doc-type: overview
---

Avalonia 与你惯用的 .NET IDE 都合得来。无论你偏爱 Visual Studio、VS Code 还是 Rider，开箱即可开发 Avalonia 应用，IntelliSense、调试和项目支持一应俱全。真正有差别的是 XAML 的编辑体验，具体说就是预览、代码补全和设计器工具。

## Visual Studio

[Avalonia for Visual Studio](/tools/visual-studio-extension) 扩展是 Avalonia Plus 的一部分，提供全功能的 XAML 编辑体验：实时预览器、能自动导入命名空间的智能代码补全、带修复建议的错误高亮、拖放式设计器，以及完整的 XAML 着色。

若你在 Windows 上开发，这个扩展提供的 XAML 编辑与预览支持最为完备。

## Visual Studio Code

Avalonia for Visual Studio Code 扩展与 Visual Studio 扩展建立在同一套 XAML 解析器之上，也就是说两边的底层引擎是同一个。Visual Studio 里每一项代码编辑增强都会直接流向 VS Code。

该扩展提供带上下文感知的丰富 IntelliSense、可顺着绑定查看数据上下文的完整 `x:DataType` 快速信息、XAML 的转到定义、自动导入命名空间、生成事件处理程序，以及清晰可操作的诊断信息。它还带有一个靠谱的 XAML 预览器，DPI 处理得当，并支持缩放以适应窗口。

## JetBrains Rider

Rider 为 Avalonia 开发提供了出色的 .NET 支持，项目管理、调试和代码导航都很顺手。它没有内置 Avalonia XAML 预览器，但社区维护的 [AvalonRider](https://plugins.jetbrains.com/plugin/14839-avalonrider) 插件把预览功能直接带进了 IDE。

## 另请参阅 {#see-also}

- [Avalonia for Visual Studio](/tools/visual-studio-extension)
- [AI Tools](/tools/ai-tools/)
- [Avalonia 工具概述](/tools/)

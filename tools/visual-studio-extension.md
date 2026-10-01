---
id: visual-studio-extension
title: Avalonia for Visual Studio 扩展
description: 用 Avalonia Visual Studio 扩展获得更好的 XAML 编辑体验：IntelliSense、错误高亮，还内置 UI 预览器。
sidebar_label: Visual Studio 扩展
doc-type: reference
---

import TestXamlPreviewer from '/img/guides/ui-development/xaml-preview-and-design-settings/test-xaml-previewer.png';
import VSOptions from '/img/vs-extension/visual-studio-avalonia-options.png';

## 功能一览 {#features}

Avalonia for Visual Studio 扩展让你处理 Avalonia XAML 文件时更加顺手，它提供了：

- 一个深度集成的增强型编辑器，编辑体验相当丰富。
- 一个预览器，不运行应用也能看到界面长什么样。

## 安装 {#installation}

安装说明请见[配置你的 IDE](/docs/get-started/set-up-your-ide)。

### Enhanced Editor

Avalonia XAML 编辑器具备以下能力：

- 输入时给出更聪明、更有用的 Intellisense。
- 错误高亮并给出修复建议。
- 自动导入 XAML 命名空间。
- 完整的 XAML 着色。
- “转到定义”导航。
- 智能悬停提示。
- 自动格式化文档。
- 文档大纲，可折叠元素。

### Previewer

预览器让你不运行应用就能看到当前文档的界面效果。

更多信息请见[预览你的界面设计](/docs/app-development/xaml-preview-and-design-settings)。

<Image light={TestXamlPreviewer} alt="A screenshot demonstrating a test of the Avalonia XAML previewer." maxWidth={400} cornerRadius="true"/>

## Settings

编辑器和预览器的行为提供了多个可配置选项。

在 Visual Studio 中依次选择**工具**菜单下的**选项**即可访问这些设置。

<Image light={VSOptions} alt="A screenshot showing the options dialog." maxWidth={400} cornerRadius="true"/>
<br />

|  设置项              | 说明 | 选项       |
|-----------------------|-------------|---------------|
| Color Scheme          | 控制 AXAML 文件内容的着色方式。更改此项需付费账户。 | <ul><li>**Roslyn（默认）：**按等价的 C# 分类着色。</li><li>**XML：**按普通 XML 文档的方式着色。</li></ul> |
| Default Document View | 打开文档时显示什么。 | <ul><li>**Split（默认）：**代码和预览器都显示。</li><li>**Design：**只显示预览器</li><li>**Source：**只显示源代码。</li></ul> |
| Split Orientation     | 拆分方向是水平还是垂直。 | <ul><li>**Horizontal（默认）：**编辑器与预览器并排显示。</li><li>**Vertical：**编辑器与预览器上下排列。</li></ul> |
| Swapped               | 在 Split 模式下对调编辑器与预览器的位置。 | **勾选：**两者位置对调。 |
| Default Zoom Level    | 窗口内容如何缩放。  | <ul><li>50%、75%、**100%（默认）**、125%、150%、200%</li><li>**Fit to Width：**把预览缩放到可用宽度。</li><li>**Fit All：**填满整个预览器。</li></ul> |
| Minimum Log Verbosity | 扩展输出日志所需的最低 `LogLevel`。 | Trace, Debug, **Information (Default)**, Warning, Error, Critical, None |
| Telemetry Enabled     | 是否上报基础使用情况遥测。更改此项需付费账户。 | <ul><li>**勾选（默认）：**上报遥测。</li><li>**不勾选：**不上报遥测。</li></ul> |
| Experimental Previewer | 使用新版预览器，适合绝大多数用户。 | <ul><li>**勾选（默认）：**新版预览器</li><li>**不勾选：**旧版预览器</li></ul> |
| 登录状态      | 已登录时显示账户名称。 | 登录或退出的链接。 |

## 另请参阅 {#see-also}

- [IDE Support](/tools/ide/)
- [Avalonia 工具概述](/tools/)

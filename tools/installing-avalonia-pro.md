---
id: installing-avalonia-pro
title: Installing Avalonia Pro
description: 配置你的项目以使用 Avalonia Pro NuGet 包，并填入许可证密钥。
doc-type: how-to
tags:
  - avalonia pro
  - avalonia enterprise
---

本指南讲解如何配置项目以使用 Avalonia Pro 包。这些包是 [Avalonia Pro 或 Enterprise](https://avaloniaui.net/pricing)的一部分。

## 前置条件 {#prerequisites}

动手之前，请确认你具备：

- 一个面向 .NET 8 或更高版本的 Avalonia 项目。
- 一个有效的 Avalonia 许可证密钥，可在 [Avalonia 门户](https://portal.avaloniaui.net)获取。

## NuGet 包源 {#nuget-package-source}

Avalonia Pro 包经由 [nuget.org](https://www.nuget.org/) 分发，不需要额外配置 NuGet 源。

:::note
2025 年 10 月 13 日之前，安装 Avalonia Pro 组件需要配置专用的 NuGet 源。那个源现已不再需要，改用 [nuget.org](https://www.nuget.org/) 即可。
:::

## 添加 NuGet 包 {#add-the-nuget-package}

运行 `dotnet add package` 命令安装你需要的 Avalonia Pro 包。比如要添加媒体播放控件：

```bash
dotnet add package Avalonia.Controls.MediaPlayer
```

把包名换成你需要的那个。下列 Avalonia Pro 包可供选用：

| NuGet 包 | 说明 |
|---------|-------------|
| [`Avalonia.Controls.Charts`](/controls/data-display/charts/#getting-started) | 图表、仪表板与分析组件库 |
| [`Avalonia.Controls.Markdown`](/controls/data-display/text-display/markdown/#getting-started) | Markdown 文本渲染 |
| [`Avalonia.Controls.MediaPlayer`](/controls/media/mediaplayer/#getting-started) | 音频与视频播放控件 |
| [`Avalonia.Controls.PdfViewer`](/controls/data-display/pdfviewer/#getting-started) | PDF 查看、搜索、批注与打印 |
| [`Avalonia.Controls.RichTextEditor`](/controls/input/text-input/richtexteditor/#getting-started) | 文档编辑与处理 |
| [`Avalonia.Controls.TreeDataGrid`](/controls/data-display/structured-data/treedatagrid/#getting-started) | 层级式与平铺式数据网格 |
| [`Avalonia.Controls.VirtualKeyboard`](/controls/input/text-input/virtualkeyboard/#getting-started) | 屏幕键盘 |

## 填入你的许可证密钥 {#add-your-license-key}

把 Avalonia 许可证密钥写进可执行项目文件（`.csproj`）：

```xml
<ItemGroup>
  <AvaloniaUILicenseKey Include="YOUR_LICENSE_KEY" />
</ItemGroup>
```

把 `YOUR_LICENSE_KEY` 换成你 [Avalonia 门户](https://portal.avaloniaui.net)账号中的密钥。

不要把许可证密钥留空。留空的话，项目可能既构建不了也打不开。

:::tip
若要在多个项目之间共用一个许可证密钥，可以借助[环境变量](https://learn.microsoft.com/en-us/visualstudio/msbuild/how-to-use-environment-variables-in-a-build)或[共享 props 文件](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory?view=vs-2022#directorybuildprops-example)。

用共享 `Directory.Build.props` 文件的具体做法，可参考 [Avalonia Pro 示例仓库](https://github.com/AvaloniaUI/AvaloniaPro.Samples/blob/main/Directory.Build.props)。
:::

## 验证安装 {#verify-the-installation}

构建项目，确认包能还原、许可证密钥被认可：

```bash
dotnet build
```

若密钥缺失或无效，构建时会出现警告。请检查 `<AvaloniaUILicenseKey>` 元素是否写在了正确的项目文件里，以及密钥值是否与门户账号中显示的一致。

## 另请参阅 {#see-also}

- [Avalonia 工具概述](/tools/)
- [FAQ](/tools/faq)

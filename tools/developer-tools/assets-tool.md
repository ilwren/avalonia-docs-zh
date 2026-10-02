---
id: assets-tool
title: 资产工具
description: 用开发者工具的资产面板浏览、搜索、预览运行中应用里的所有嵌入式 Avalonia 资源，并复制它们的 URI。
doc-type: reference
---

资产工具会列出运行中进程里嵌入的所有 Avalonia 资源。

这也包括来自依赖项的嵌入资产，比如第三方主题或图标库——它们同样以 Avalonia 资源的形式存在。

![资产页面](/img/tools/dev-tools/assets-page.png)

## 浏览资产列表 {#navigating-the-asset-list}

资产工具以网格视图呈现所有嵌入资源，每行显示资产名称及其所属程序集。你可以用顶部的搜索框按名称或路径筛选。

资产 URI 采用 `avares://` 方案。例如 `avares://MyApp/Assets/logo.png` 指的是 `MyApp` 程序集中 `Assets` 文件夹下名为 `logo.png` 的文件。

## 资产右键菜单 {#asset-context-menu}

右键点击任意资产即可打开上下文菜单，从中可以复制资产的绝对 URI，或把资产导出到文件系统。

复制出的 URI 可以直接用在你的 XAML 里。比如复制了一个图片资产的 URI 之后：

```xml
<Image Source="avares://MyApp/Assets/logo.png" />
```

![资产右键菜单](/img/tools/dev-tools/assets-context-menu.png)

## 资产预览 {#asset-preview}

网格列表只显示每个资源的有限信息，以免无谓地把它们读进内存。

要预览某个资产，双击它或在右键菜单中选择 **Preview**。工具会从应用进程中取回该资产并显示出来。支持预览的格式包括：

- **位图图像**（PNG、JPEG、BMP 及其他位图格式）
- **字体**（TrueType 和 OpenType）
- **文本文件**（XAML、XML、JSON 和纯文本）

对于图片资产，预览还会显示位图格式和解码后的像素尺寸。

:::note
超过 100mb 的资产无法预览，目前这一上限还不可配置。
:::

![图片资产预览示例](/img/tools/dev-tools/assets-image.png)

![字体资产预览示例](/img/tools/dev-tools/assets-font.png)

## 另请参阅 {#see-also}

- [资产基础](/docs/fundamentals/including-assets)
- [资源工具](/tools/developer-tools/resources-tool)
- [元素工具](/tools/developer-tools/elements-tool)

---
id: attaching-to-the-previewer
title: 把 DevTools 挂接到预览器
sidebar_label: 挂接到预览器
description: 了解如何把 Avalonia 开发者工具挂接到 XAML 预览器进程上，以便检视视觉树、做诊断。
doc-type: how-to
tags:
  - avalonia plus
  - avalonia pro
  - avalonia enterprise
---

:::caution
此功能尚属实验性，日后版本中可能变动。
:::

[AvaloniaVS](https://marketplace.visualstudio.com/items?itemName=AvaloniaTeam.AvaloniaVS) 和 [AvaloniaRider](https://plugins.jetbrains.com/plugin/14839-avaloniarider) 扩展把预览窗口跑在一个完整的应用进程里，但没有真正的窗口子系统。这限制了你能用的诊断功能，分析视觉树、查看控件的实际摆放也就更费劲。

由于开发者工具可以在进程外运行，你可以把它挂接到预览器进程上，从而获得完整的诊断能力：检视视觉树、编辑属性、分析布局。

![DevTools 应用挂接到预览器进程的示例](/img/tools/dev-tools/attaching-to-previewer.png)

## 配置 {#configuration}

预览扩展不支持键盘输入，因此眼下 `AutoConnectFromDesignMode` 是你唯一的连接方式。请把下列内容加进应用的启动代码：

```csharp title="App.axaml.cs"
this.AttachDeveloperTools(o =>
{
    o.AutoConnectFromDesignMode = true;
});
```

当 `IsDesignMode` 为 `true` 时，`DeveloperToolsOptions.Runner` 默认是禁用的。这样你每次在 IDE 里打开 XAML 文件时就不会凭空多出一堆进程。

既然 runner 被禁用了，你就需要单独打开开发者工具应用（和浏览器、移动端目标的做法一样）。

## 排查问题 {#troubleshooting}

### 快捷键没反应 {#shortcuts-are-ignored}

如上所述，预览器扩展不监听键盘输入，你没法在预览器里用快捷键唤起开发者工具。请改用开发者工具应用窗口里的操作按钮或快捷键。

### 开发者工具开出了太多窗口 {#developer-tools-opens-too-many-windows}

开发者工具会为每个连接的进程开一个工具窗口。若你在 IDE 里开着多个 XAML 预览器标签页，每个都会对应一个独立的工具窗口。想少些杂乱，就把当下不看的预览器标签页关掉。

## 另请参阅 {#see-also}

- [挂接应用](/tools/developer-tools/attaching-applications)
- [挂接到远程工具](/tools/developer-tools/attaching-to-the-remote-tool)
- [开发者工具选项](/tools/developer-tools/options)
- [开发者工具快捷键](/tools/developer-tools/shortcuts)

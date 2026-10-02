---
id: events-tool
title: 事件工具
doc-type: reference
---

事件工具为 Avalonia 的路由事件系统提供实时监视与调试能力。Avalonia 中的路由事件走的是一套颇为精巧的处理机制，事件可以沿视觉树向上或向下传递。借助这个工具，开发者可以追踪事件的传播路径、认出事件处理程序，排查应用中与事件相关的问题。

更多基础知识请见 Avalonia 文档中的[路由事件](https://docs.avaloniaui.net/docs/concepts/input/routed-events)。

![已触发事件列表](/img/tools/dev-tools/events-raised-events-list.png)

## 启用事件侦听 {#enabling-event-listeners}

默认启用的事件有 `Button.Click`、`KeyDown`、`KeyUp`、`TextInput`、`PointerReleased` 和 `PointerPressed`。这组默认值可通过 `Default Routed Events` 设置项调整，详见[开发者工具设置](/tools/developer-tools/settings)页。

用 **Event Listeners** 浮出按钮可以启用或禁用某个路由事件或某组事件。

![侦听器筛选浮出菜单](/img/tools/dev-tools/events-listeners-filter.png)

这份列表是在该选项卡首次打开时，从静态注册的路由事件中收集而来的。
若某个事件不在列表里，多半是因为应用里从未引用过它。

## 浏览事件处理程序列表 {#navigating-list-of-event-handlers}

Avalonia 的路由事件有三种路由策略：
- `Tunnel` 策略从根部（通常是窗口）向源元素（通常是被点击或获得焦点的元素）传递。
- `Bubble` 策略正好相反，从源元素一路传回窗口。
- `Direct` 策略只在事件直接在源元素上触发时发生，不会路由到任何其他元素。

`Bubble` 是 XAML 和 C# 事件处理程序中默认采用的策略。`Tunnel` 策略常被称作 `Preview`，因为它让你赶在标准的 `Bubble` 之前先行处理事件。

一次触发的事件可能经过多个元素的处理程序，但真正把事件标记为已处理、从而中断路由的只有一个。

在 `Developer Tools` 中，三种策略各有配色。
处理了该事件的那个元素在视觉上与众不同，标明路由就此止步。

`Developer Tools` 仍会把后面的元素处理程序列出来——它们本可能收到已被处理过的事件参数。

![已触发事件的处理程序链](/img/tools/dev-tools/events-chain-list.png)

## 检视处理事件的控件 {#inspecting-event-handler-control}

每个元素处理程序都可点击，点击后会跳到元素树中对应的节点。

注意：若点击某个元素后毫无反应，多半是它已经从元素树中移除了。

![检视处理程序](/img/tools/dev-tools/events-inspect-handler.gif)

## 另请参阅 {#see-also}

- [元素工具](/tools/developer-tools/elements-tool)
- [断点工具](/tools/developer-tools/breakpoints-tool)

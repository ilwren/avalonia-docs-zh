---
id: shortcuts
title: Developer Tools Shortcuts
sidebar_label: 快捷键
description: Avalonia 开发者工具的键盘快捷键参考，涵盖检视、搜索、导航、布局和工具切换等命令。
doc-type: reference
---

本页列出 Avalonia 开发者工具中的所有键盘快捷键。标注为 **Unassigned** 的，你可以在[开发者工具设置](/tools/developer-tools/settings)中自行绑定。

## Inspection

排查布局问题、追踪焦点顺序或测量元素间距时，这些快捷键都用得上。

| 显示名称 | 说明 | 适用场景 | Windows / Linux | macOS |
|---|---|---|---|---|
| Focus Tracking | 高亮应用中当前获得焦点的元素。在开发者工具和目标应用中都可用。 | 调试 tab 顺序或焦点相关的毛病时用它，能清楚看到焦点究竟落在哪个控件上。 | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>K</kbd> | <kbd>⌘</kbd> <kbd>⇧</kbd> <kbd>K</kbd> |
| Inspect Element | 在应用中点击即可选中并检视 UI 元素。在开发者工具和目标应用中都可用。 | 想迅速跳到元素树中某个控件、又不想一层层手动展开时用它。 | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>C</kbd> | <kbd>⌘</kbd> <kbd>⇧</kbd> <kbd>C</kbd> |
| Highlight Elements | 开关 UI 元素的实时高亮。在开发者工具和目标应用中都可用。 | 用它把元素边界和内边距可视化，布局问题一眼便知。 | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>H</kbd> | <kbd>⌘</kbd> <kbd>⇧</kbd> <kbd>H</kbd> |
| Show Overlay Rulers | 在叠加层中显示或隐藏度量标尺。在开发者工具和目标应用中都可用。 | 当你需要精确到像素地测量元素间距，或想核对对齐情况时用它。 | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd> | <kbd>⌘</kbd> <kbd>⇧</kbd> <kbd>R</kbd> |
| Show Overlay Info | 在叠加层中显示或隐藏详细信息。在开发者工具和目标应用中都可用。 | 用它直接在元素叠加层上查看 `Width`、`Height`、`Margin` 等属性值，不必切到属性面板。 | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>D</kbd> | <kbd>⌘</kbd> <kbd>⇧</kbd> <kbd>D</kbd> |
| Toggle TopMost | 开关开发者工具的置顶模式。在开发者工具和目标应用中都可用。 | 用它把开发者工具窗口压在应用之上，检视时不必来回 alt-tab。 | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>T</kbd> | <kbd>⌘</kbd> <kbd>⇧</kbd> <kbd>T</kbd> |
| Set Breakpoint | 在属性或事件上下断点。 | 当某个属性变化或某个事件触发时暂停执行，追查意料之外的状态变更时很好使。 | <kbd>F9</kbd> | <kbd>F9</kbd> |

## 搜索与导航 {#search-and-navigation}

这些快捷键帮你在开发者工具中查找元素、属性或资源。

| 显示名称 | 说明 | 适用场景 | Windows / Linux | macOS |
|---|---|---|---|---|
| Search Current List | 在当前工具中启用搜索。 | 用它把冗长的元素树或属性列表筛到你要找的那一项。 | <kbd>Ctrl</kbd>+<kbd>F</kbd> | <kbd>⌘</kbd> <kbd>F</kbd> |
| Next Search Result | 跳到当前视图中的下一个搜索结果。 | 输入搜索词后，用它向后逐个翻看匹配项。 | <kbd>F3</kbd> | <kbd>⌘</kbd> <kbd>G</kbd> |
| Previous Search Result | 跳到当前视图中的上一个搜索结果。 | 用它向前逐个翻看匹配项。 | <kbd>Shift</kbd>+<kbd>F3</kbd> | <kbd>⌘</kbd> <kbd>⇧</kbd> <kbd>G</kbd> |
| Next Tool | 切换到下一个开发者工具选项卡。 | 用它在各工具之间切换（比如从元素跳到事件），全程不碰鼠标。 | <kbd>Ctrl</kbd>+<kbd>]</kbd> | <kbd>⌘</kbd> <kbd>]</kbd> |
| Previous Tool | 切换到上一个开发者工具选项卡。 | 用它退回到你刚才用的那个工具。 | <kbd>Ctrl</kbd>+<kbd>[</kbd> | <kbd>⌘</kbd> <kbd>[</kbd> |

## 布局与视图 {#layout-and-views}

这些快捷键控制开发者工具的窗口布局和面板显隐。

| 显示名称 | 说明 | 适用场景 | Windows / Linux | macOS |
|---|---|---|---|---|
| Refresh Current View | 刷新当前视图。 | 改完代码后用它重新加载元素树或资源列表。 | <kbd>F5</kbd> | <kbd>⌘</kbd> <kbd>⇧</kbd> <kbd>R</kbd> |
| Remove Item | 从当前列表或视图中移除选中项。 | 用它删掉某个不再需要的断点或日志条目。 | <kbd>Delete</kbd> | <kbd>Delete</kbd> |
| Clear Current List | 清空当前列表或视图中的所有项。 | 用它重置事件或日志工具，好开始一轮干净的采集。 | <kbd>Ctrl</kbd>+<kbd>L</kbd> | <kbd>⌘</kbd> <kbd>L</kbd> |
| Show Navigation | 显示或隐藏导航面板。 | 用不上侧边栏时用它把主内容区让到最大。 | <kbd>Alt</kbd>+<kbd>1</kbd> | <kbd>⌥</kbd> <kbd>1</kbd> |
| Show Tools | 显示或隐藏工具面板。 | 用它收起底部工具面板，腾出更多纵向空间。 | <kbd>Alt</kbd>+<kbd>2</kbd> | <kbd>⌥</kbd> <kbd>2</kbd> |
| Reset Layout | 把开发者工具的窗口布局恢复为默认。 | 面板调乱了想回到初始布局时用它。 | Unassigned | Unassigned |

## Tools

这些快捷键直接打开特定的开发者工具面板。

| 显示名称 | 说明 | 适用场景 | Windows / Linux | macOS |
|---|---|---|---|---|
| Open Elements | 打开元素检视工具。 | 用它查看并浏览应用的视觉树。 | Unassigned | Unassigned |
| Open Assets | 打开资产浏览器。 | 用它浏览随应用打包的嵌入式资产，比如图片和字体。 | Unassigned | Unassigned |
| Open Resources | 打开资源浏览器。 | 用它在运行时查看 `StaticResource` 和 `DynamicResource` 的取值。 | Unassigned | Unassigned |
| Open Settings | 打开开发者工具设置。 | 用它配置主题、按键绑定和连接选项。 | Unassigned | <kbd>⌘</kbd> <kbd>.</kbd> |
| Open Logs | 打开应用日志查看器。 | 用它查看绑定错误、布局警告和其他诊断消息。 | Unassigned | Unassigned |
| Open Events | 打开事件监视工具。 | 用它观察路由事件在视觉树中隧道和冒泡的全过程。 | Unassigned | Unassigned |
| Open Breakpoints | 打开断点管理工具。 | 用它在一处查看、启用、禁用或移除所有属性断点和事件断点。 | Unassigned | Unassigned |
| Open Metrics | 打开性能指标查看器。 | 分析应用性能时，用它监控帧率、渲染耗时等性能计数器。 | Unassigned | Unassigned |
| Open Protocol | 打开开发者工具的协议监视工具。 | 用它查看开发者工具与你的应用之间往来的底层消息。 | Unassigned | Unassigned |
| Open Documentation | 打开开发者工具文档。 | 用它不离开开发者工具就能快速翻阅在线文档。 | <kbd>Ctrl</kbd>+<kbd>F1</kbd> | <kbd>⌘</kbd> <kbd>?</kbd> |

## 另请参阅 {#see-also}

- [开发者工具设置](/tools/developer-tools/settings)
- [元素工具](/tools/developer-tools/elements-tool)
- [事件工具](/tools/developer-tools/events-tool)
- [断点工具](/tools/developer-tools/breakpoints-tool)
- [日志工具](/tools/developer-tools/logs-tool)
- [指标工具](/tools/developer-tools/metrics-tool)
- [资产工具](/tools/developer-tools/assets-tool)
- [资源工具](/tools/developer-tools/resources-tool)

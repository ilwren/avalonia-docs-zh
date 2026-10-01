---
id: settings
title: 开发者工具设置
sidebar_label: 设置
doc-type: reference
---

设置页可从**托盘图标**菜单（Windows 和 Linux）或 **macOS 全局菜单**进入。
若应用已经连上，也可以在**左侧导航栏**里找到设置页。

| 类别 | 设置项 | 说明 | Default Value |
|----------|---------|-------------|---------------|
| **Appearance** |
| | Theme Variant | 控制应用的配色主题 | Dark |
| | 关闭最后一个窗口时退出 | 决定关掉最后一个窗口时应用是否随之退出 | true |
| | Skip Welcome Window | 启动应用时跳过欢迎页 | false |
| | Enable Protocol Monitor | 显示诊断通信协议的监视窗口 | false |
| **Elements Tree** |
| | Aggregate Templates | 把模板的视觉子级合并成单个树节点，视图更清爽，默认折叠 | true |
| | InlinePseudoclasses | 默认只有可见元素的伪类会在树中右对齐显示，其余的收在叠加按钮里。开启此项后，无论是否可见，所有伪类都内联显示。 | false |
| | Contextual Properties | 只显示与所选元素当前上下文/状态相关的属性。比如 `Grid.Row` 属性只在 `Grid` 的直接子级上才可见 | true |
| | Include CLR Properties | 除 Avalonia 专有属性外，还显示 .NET CLR 属性（重复项除外） | false |
| **Overlay** |
| | Show ToolTip Info | 鼠标悬停时以提示框显示控件信息 | true |
| | Visualize Margin & Padding | 高亮显示悬停元素的外边距、内边距和边框区域 | true |
| | Show Rulers | 显示度量标尺，便于精确定位元素 | true |
| | Show Extension Lines | 在悬停元素与标尺之间显示参考线 | true |
| **事件** |
| | Default Routed Events | 事件工具中默认跟踪的事件列表 | `Button.ClickEvent`, `InputElement.KeyDownEvent`, `InputElement.KeyUpEvent`, `InputElement.TextInputEvent`, `InputElement.PointerReleasedEvent`, `InputElement.PointerPressedEvent` |
| **Metrics** |
| | 可观察 meter 的轮询间隔（毫秒） | 多久轮询一次可观察 meter 以取得新值。值越小刷新越勤，但可能拖累所连接应用的性能。 | 1000ms |
| | 度量帧间隔（毫秒） | 多久采集一次度量并刷新到可视化图表中。 | 250ms |
| | 合并同一帧内的度量 | 启用后会把同一帧内的多次度量合并：基于时间的指标取平均，计数器和 gauge 取最新值。禁用时则保留全部原始度量。 | true |
| | 度量历史保留时长（秒） | 定义往前多久的度量会被保留并显示。 | 60s |
| **Protocol** |
| | HTTP 端口 | 定义用来侦听应用连接的 HTTP 端口。改动后需重启。要与目标应用中配置的 `DeveloperToolsOptions.Protocol` 保持一致。 | 29414 |

## 另请参阅 {#see-also}

- [开发者工具选项](/tools/developer-tools/options)
- [开发者工具快捷键](/tools/developer-tools/shortcuts)

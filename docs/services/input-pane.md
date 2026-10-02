---
id: input-pane
title: Input Pane
description: "在 Avalonia 应用中监测平台输入面板（软键盘）的状态、边界和动画。"
doc-type: reference
---

`InputPane` 让开发者能够监听平台输入面板（比如软键盘或屏幕键盘）的当前状态和边界。

`InputPane` 可通过 `TopLevel` 或 `Window` 的实例取得；关于如何访问 `TopLevel`，更多细节请看 [TopLevel](/docs/fundamentals/top-level) 页。

```csharp
var inputPane = TopLevel.GetTopLevel(control).InputPane;
```

:::note
目前 Avalonia 不会根据输入面板的状态自动调整根视图和滚动位置，建议开发者使用 IInputPane API 自行调整应用。

自动调整已列入日后 11.* 版本的计划。
:::

## 属性 {#properties}

### State
输入面板的当前状态。
可能的取值：
- `InputPaneState.Closed`
- `InputPaneState.Opened`

```csharp
InputPaneState State { get; }
```

### OccludedRect
输入面板的当前边界。

```csharp
Rect OccludedRect { get; }
```

:::note
返回值采用相对于当前顶层的客户区坐标。
若输入面板是浮动/分离的、悬在视图之上，则返回空矩形。
:::

## 事件 {#events}

### StateChanged
输入面板状态发生变化时触发。

```csharp
event EventHandler<InputPaneStateEventArgs>? StateChanged;
```

值得一提的是，事件参数里有几个很有用的字段：
- `InputPaneStateEventArgs.NewState`——输入面板的新状态。
- `InputPaneStateEventArgs.StartRect`——输入面板的初始边界。
- `InputPaneStateEventArgs.EndRect`——输入面板的最终边界。
- `InputPaneStateEventArgs.AnimationDuration`——输入面板状态变化动画的时长。
- `InputPaneStateEventArgs.Easing`——输入面板状态变化动画的缓动。

有了 `AnimationDuration` 和 `Easing`，开发者就能在两个状态之间做出过渡效果。

## 平台兼容性 {#platform-compatibility}

| 特性        | Windows | macOS | Linux | 浏览器 | Android |  iOS |
|---------------|-------|-------|-------|-------|-------|-------|
| `State` | ✓ | ✗ | ✗ | ✓* | ✓ | ✓ |
| `OccludedRect` | ✓ | ✗ | ✗ | ✓*  | ✓ | ✓ |
| `StateChanged` | ✓ | ✗ | ✗ | ✓* | ✓ | ✓ |
| `StateChanged.StartRect` | ✗ | ✗ | ✗ | ✓* | ✓ | ✓ |
| `StateChanged.AnimationDuration` | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| `StateChanged.Easing` | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |

\* —— 只有移动端的 Chromium 浏览器支持 IInputPane API。

## 另请参阅 {#see-also}

- [Insets Manager](/docs/services/insets-manager)：系统栏可见性与安全区管理。
- [TopLevel](/docs/fundamentals/top-level)：从控件访问平台服务。
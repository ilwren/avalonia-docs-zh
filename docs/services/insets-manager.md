---
id: insets-manager
title: Insets Manager
description: "在 Avalonia 中管理移动端和浏览器平台上的系统栏可见性、安全区内边距以及全屏贴边显示。"
doc-type: reference
---

`InsetsManager` 让你能与平台的系统栏打交道，并处理移动端窗口安全区的变化。 

`InsetsManager` 可通过 `TopLevel` 或 `Window` 的实例取得；关于如何访问 `TopLevel`，更多细节请看 [TopLevel](/docs/fundamentals/top-level) 页。

```csharp
var insetsManager = TopLevel.GetTopLevel(control).InsetsManager;
```

:::note
该服务在移动端和浏览器后端上有实现。桌面端的窗口装饰定制请用 `Window.ExtendClientAreaToDecorationsHint` 配合 `WindowDrawnDecorations`，细节见[窗口管理](/docs/app-development/window-management#custom-title-bar)。
:::

:::note
从 Avalonia 11.1 起，任何 Avalonia 应用都会自动按 inset 值调整其根视图。若要关掉这一行为，请在根视图上设置 `TopLevel.AutoSafeAreaPadding="False"` 附加属性。
:::

## 属性 {#properties}

### IsSystemBarVisible
获取或设置一个值，指示系统栏是否可见。若平台不支持显示或隐藏系统栏，则返回 null。

```csharp
bool? IsSystemBarVisible { get; set; }
```

### DisplayEdgeToEdge
获取或设置一个值，指示窗口是否应当贴边绘制到可见系统栏的后面。

```csharp
bool DisplayEdgeToEdge { get; set; }
```

### SafeAreaPadding
获取当前的安全区内边距。安全区指的是窗口中不被系统栏遮挡的那部分。

```csharp
Thickness SafeAreaPadding { get; }
```

### SystemBarColor
获取或设置平台系统栏的颜色。若平台不支持设置系统栏颜色，则返回 null。

```csharp
Color? SystemBarColor { get; set; }
```

## 事件 {#events}

### SafeAreaChanged
当前窗口的安全区发生变化时触发。系统栏显示或隐藏、窗口尺寸或方向改变时，都可能引发它。

```csharp
event EventHandler<SafeAreaChangedArgs>? SafeAreaChanged;
```

#### SafeAreaChangedArgs

SafeAreaChangedArgs 类为 SafeAreaChanged 事件提供数据。

#### SafeAreaPadding
获取新的安全区内边距。

```csharp
public Thickness SafeAreaPadding { get; }
```

## SystemBarTheme

SystemBarTheme 是一个枚举，其取值表示系统栏的浅色与深色主题。

### Light
系统栏为浅色背景、深色前景。

### Dark
系统栏为深色背景、浅色前景。


## 平台兼容性 {#platform-compatibility}

| 特性        | Windows | macOS | Linux | 浏览器 | Android |  iOS |
|---------------|-------|-------|-------|-------|-------|-------|
| `IsSystemBarVisible` | ✗ | ✗ | ✗ | ✓* | ✓ | ✓ |
| `DisplayEdgeToEdge` | ✗ | ✗ | ✗ | ✗  | ✓ | ✓ |
| `SafeAreaPadding` | ✗ | ✗ | ✗ | ✓* | ✓ | ✓ |
| `SystemBarColor` | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ |
| `SafeAreaChanged` | ✗ | ✗ | ✗ | ✓* | ✓ | ✓ |

\* —— 只有移动端的 Chromium 浏览器支持 IInsetsManager API。

## 另请参阅 {#see-also}

- [输入面板](/docs/services/input-pane)：软键盘的状态与边界。
- [TopLevel](/docs/fundamentals/top-level)：从控件访问平台服务。
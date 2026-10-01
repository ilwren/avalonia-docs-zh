---
id: focus-manager
title: Focus Manager
description: 用 FocusManager 服务管理 Avalonia 应用中的键盘焦点：跟踪、设置和清除当前获得焦点的元素。
doc-type: reference
---

[`FocusManager`](/api/avalonia/input/focusmanager) 服务负责管理应用中的键盘焦点，它会记录当前获得焦点的元素和当前的焦点范围。

你可以通过 [`TopLevel`](/api/avalonia/controls/toplevel) 或 `Window` 的实例取得 `FocusManager`。关于如何访问 `TopLevel`，更多细节请看 [TopLevel](/docs/fundamentals/top-level) 页。

```csharp
var focusManager = window.FocusManager;
```

## 方法 {#methods}

### `GetFocusedElement()`

返回当前获得焦点的 `IInputElement`；若没有元素获得焦点，则返回 `null`。

```csharp
IInputElement? GetFocusedElement()
```

你可以用这个方法查看当前是哪个控件握着键盘焦点：

```csharp
var focused = focusManager.GetFocusedElement();
if (focused is TextBox textBox)
{
    // The user is currently editing a text box
}
```

### `ClearFocus()`

把键盘焦点从当前元素上摘掉。调用之后，在别的元素获得焦点之前，`GetFocusedElement()` 都会返回 `null`。

```csharp
void ClearFocus()
```

## 小贴士 {#tips}

### 让某个控件获得焦点 {#focusing-a-control}

要让控件获得焦点，通常用不着 `FocusManager` 服务，直接在控件上调用 `Focus` 方法即可：

```csharp
bool hasFocused = button.Focus();
```

若控件不可见，或其 `Focusable` 属性为 `false`，`Focus` 方法会返回 `false`。

### 监听全局的焦点变化 {#listening-for-global-focus-changes}

`FocusManager.GetFocusedElement` 方法返回的是某一时刻获得焦点的控件，因此并不适合用来响应焦点的实时变化。要跨所有顶层监听全局焦点变化，请订阅那个路由事件：

```csharp
InputElement.GotFocusEvent.Raised.Subscribe(args =>
{
    var (sender, e) = args;
    // Handle focus change
});
```

### Tab 导航顺序 {#tab-navigation-order}

默认情况下，控件按它们在视觉树中出现的顺序接受导航。要改变 Tab 顺序，请在控件上设置 `TabIndex` 属性：

```xml
<StackPanel>
    <TextBox TabIndex="2" PlaceholderText="Second" />
    <TextBox TabIndex="1" PlaceholderText="First" />
    <TextBox TabIndex="3" PlaceholderText="Third" />
</StackPanel>
```

### 让控件不接受焦点 {#preventing-a-control-from-receiving-focus}

把 `Focusable` 设为 `False`，即可把控件排除在键盘导航之外：

```xml
<Button Content="Not focusable" Focusable="False" />
```

### 加载时设定焦点 {#focus-on-load}

若想在视图加载时让某个控件获得焦点，请重写 `OnLoaded`，并对目标控件调用 `Focus`：

```csharp
protected override void OnLoaded(RoutedEventArgs e)
{
    base.OnLoaded(e);
    myTextBox.Focus();
}
```

## 另请参阅 {#see-also}

- [焦点](/docs/input-interaction/focus)：焦点体系概览与焦点事件。
- [TopLevel](/docs/fundamentals/top-level)：从 `TopLevel` 访问平台服务。

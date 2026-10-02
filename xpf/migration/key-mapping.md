---
id: key-mapping
title: 映射按键
description: 如何在 XPF 应用中重新映射键盘快捷键，让各平台专属的组合键在 macOS 和 Linux 上用起来更地道。
---

WPF 内置控件用的某些快捷键，在 Windows 上天经地义，换到别的操作系统上就显得格格不入。若源码在你手上，还能加点逻辑按操作系统切换快捷键；可换成第三方控件，这条路就走不通了。

为此，XPF 提供了按键映射功能，可以在运行时自动把按键映射过去。这项功能在 macOS 上最常用到，在其他操作系统上也派得上用场。

:::tip
专门针对 macOS 的相关内容，请见 [macOS](/xpf/platforms/macos#key-mapping) 一节。
:::

## 添加自定义按键映射处理程序 {#adding-a-custom-key-map-handler}

```csharp
using System.Windows;
using Atlantis;

namespace XpfKeyboardMappingExample;

/// <summary>
/// Interaction logic for App.xaml
/// </summary>
public partial class App : Application
{
    public App()
    {
        XpfKeyboard.AddMapKeyHandler(OnMapKey);
    }

    private void OnMapKey(object? sender, XpfMapKeyEventArgs e)
    {
    }
}
```

每次按键都会调用 `OnMapKey` 处理程序，它的职责是把 Avalonia 的按键和修饰键映射成 WPF 的按键。你可以添加多个映射处理程序，它们会按注册顺序依次被调用。

## 映射一个按键 {#map-a-key}

下面的例子把 Alt+Q（macOS 上是 Option+Q）映射成 Ctrl+A（“全选”）。

```csharp
private void OnMapKey(object? sender, XpfMapKeyEventArgs e)
{
    // If another handler has already handled this key then do nothing.
    if (e.Handled)
        return;

    // Maps Alt+Q (Option+Q on macOS) to Ctrl+A
    if (e.Modifiers == Avalonia.Input.KeyModifiers.Alt && e.Key == Avalonia.Input.Key.Q)
    {
        e.MappedKey = System.Windows.Input.Key.A;
        e.MappedModifiers = System.Windows.Input.ModifierKeys.Control;
        e.Handled = true;
    }
}
```

## 映射修饰键 {#mapping-modifier-keys}

修饰键有两种映射方式：

第一种是处理最初那次修饰键按下。比如收到 `e.Key == System.Windows.Input.Key.LeftCtrl` 后随即设置 `e.MappedKey = System.Windows.Input.Key.LeftAlt`。这样一来，应用会收到针对 `LeftAlt` 的一对 `KeyDown`/`KeyUp` 事件，并且在按键持续期间 `Keyboard.Modifiers` 都会是 `Alt`。这种做法不需要碰 `e.MappedModifiers`。

这种做法的麻烦在于，往往要等第二个键按下来才知道修饰键该映射成什么。这时就该等第二次按键再设置 `e.MappedModifiers`。用这种办法时请记住：抛出的 `KeyDown` 事件与当时的 `Keyboard.Modifiers` 值并不一致——不会为修饰键伪造 `KeyDown` 事件，映射结果只体现在 `Keyboard.Modifiers` 和 `Keyboard.IsKeyDown` 上。

## 按条件映射 {#conditional-mapping}

当前获得焦点的控件会通过 `XpfMapKeyEventArgs.Source` 属性传给处理程序。借助它，你可以根据当前焦点所在的控件有条件地映射按键。

## 另请参阅 {#see-also}

- [macOS 上的 Avalonia](/docs/deployment/macos)
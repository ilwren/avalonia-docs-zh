---
id: repeatbutton
title: RepeatButton
description: A button that repeatedly raises its click event while the user holds it down.
doc-type: reference
---

The `RepeatButton` is a control that has the added feature of regularly generating click events while the button is being pressed down.

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性 | 说明                                                                              |
| -------- | ---------------------------------------------------------------------------------------- |
| `Delay`    | The time (milliseconds) to wait before repeated click generation begins. Default is 300. |
| `Interval` | The time (milliseconds) between clicks being generated. Default is 100.                  |

## Example

This example shows a repeat button generating click events with the default interval and delay.

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             Padding="20">
  <RepeatButton Click="OnClick"
                HorizontalAlignment="Center"
                VerticalAlignment="Center">
    Press and hold down
  </RepeatButton>
</UserControl>
```

```csharp
public partial class MainView : UserControl
{
    private int _clickCount = 0;

    public void OnClick(object sender, RoutedEventArgs args)
    {
        var btn = (RepeatButton)sender;
        btn.Content = $"Clicked: {++_clickCount} times";
    }
}
```

</XamlPreview>

## Customizing delay and interval

You can configure the `Delay` and `Interval` properties directly in XAML to control how quickly repeated clicks begin and how frequently they fire. The following example waits 500 milliseconds before the first repeat, then fires every 50 milliseconds:

```xml
<RepeatButton Delay="500" Interval="50" Click="OnClick">
    Fast repeat after half-second delay
</RepeatButton>
```

## 常见用法 {#common-use-cases}

The `RepeatButton` is useful in any scenario where you need continuous action while the user holds down a button. Common examples include volume controls, scroll buttons, numeric steppers, and zoom controls. In each of these cases, the repeat behavior lets your users make incremental adjustments without clicking repeatedly.

## 另请参阅 {#see-also}

- [Button](/controls/input/buttons/button)
- [ButtonSpinner](/controls/input/buttons/buttonspinner)
- [RepeatButton API reference](/api/avalonia/controls/repeatbutton)
- [GitHub 上的 `RepeatButton.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/RepeatButton.cs)

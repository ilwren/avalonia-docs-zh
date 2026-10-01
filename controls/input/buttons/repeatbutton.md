---
id: repeatbutton
title: RepeatButton
description: 一个按钮：用户按住不放时，它会反复引发点击事件。
doc-type: reference
---

`RepeatButton` 这个控件多了一项本事：按住它不放时会定期生成点击事件。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性 | 说明                                                                              |
| -------- | ---------------------------------------------------------------------------------------- |
| `Delay`    | 开始连续生成点击之前的等待时间（毫秒），默认值 300。 |
| `Interval` | 两次生成点击之间的间隔（毫秒），默认值 100。                  |

## Example

这个例子展示一个按默认间隔和延迟生成点击事件的 repeat button。

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

## 定制延迟与间隔 {#customizing-delay-and-interval}

在 XAML 中直接配置 `Delay` 和 `Interval` 属性，即可控制连点多久开始、多密集。下面的例子等 500 毫秒才开始重复，之后每 50 毫秒触发一次：

```xml
<RepeatButton Delay="500" Interval="50" Click="OnClick">
    Fast repeat after half-second delay
</RepeatButton>
```

## 常见用法 {#common-use-cases}

凡是需要「按住不放就持续动作」的场合，`RepeatButton` 都能派上用场。常见的例子有音量控制、滚动按钮、数值步进器和缩放控制。在这些场景里，重复行为让用户不必反复点击就能微调。

## 另请参阅 {#see-also}

- [Button](/controls/input/buttons/button)
- [ButtonSpinner](/controls/input/buttons/buttonspinner)
- [RepeatButton API 参考](/api/avalonia/controls/repeatbutton)
- [GitHub 上的 `RepeatButton.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/RepeatButton.cs)

---
id: button
title: Button
description: 一个可点击的控件：响应指针输入，引发 Click 事件，也可以调用 ICommand。
doc-type: reference
---

import ButtonClickScreenshot from '/img/controls/buttons/button/button-click.gif';

[`Button`](/api/avalonia/controls/button) 控件响应指针操作，并在指针按下时以「凹陷」状态给出视觉反馈。从按下到抬起的一整套动作会被解读为一次点击，这一行为可以通过 [`ClickMode`](/api/avalonia/controls/clickmode) 属性配置。

处理点击有两种方式：在代码隐藏中订阅 `Click` 事件，或者把一个 `ICommand` 实例绑定到 `Command` 属性。绑定命令的具体做法请参阅[添加交互](/docs/input-interaction/adding-interactivity)。

## 常用属性 {#common-properties}

| 属性           | 说明                                                         |
| ------------------ | ------------------------------------------------------------------- |
| `ClickMode`        | 描述按钮应如何响应点击。                    |
| `Command`          | 按钮被点击时要调用的 `ICommand` 实例。 |
| `CommandParameter` | 调用命令时传给它的参数。             |
| `Content`          | 按钮内显示的内容，可以是文字，也可以是任意控件。 |
| [`Flyout`](/api/avalonia/controls/flyout)           | 点击按钮时打开的 `Flyout`。                   |
| `IsPressed`        | 按钮当前是否处于按下状态（只读）。     |
| `IsDefault`        | 为 `true` 时，用户按 Enter 即可触发该按钮。   |
| `IsCancel`         | 为 `true` 时，用户按 Esc 即可触发该按钮。  |

## Example

这个例子展示一个简单的按钮，以及用 C# 代码隐藏写的点击事件处理程序。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             Padding="20">
  <Button Click="OnClick"
          HorizontalAlignment="Center"
          VerticalAlignment="Center">
    Press Me!
  </Button>
</UserControl>
```

```csharp
public partial class MainView : UserControl
{
    private int _clickCount = 0;

    public void OnClick(object sender, RoutedEventArgs args)
    {
        var btn = (Button)sender;
        btn.Content = $"Clicked: {++_clickCount} times";
    }
}
```

</XamlPreview>

## 绑定到命令 {#binding-to-a-command}

MVVM 中更推荐的做法，是把 `Command` 属性绑定到视图模型中的 `ICommand`：

```xml
<Button Content="Save" Command="{Binding SaveCommand}" />
```

```csharp
[RelayCommand]
private void Save()
{
    _repository.Save(CurrentItem);
}
```

### 带参数的命令 {#command-with-a-parameter}

```xml
<Button Content="Delete"
        Command="{Binding DeleteCommand}"
        CommandParameter="{Binding SelectedItem}" />
```

### 用 `CanExecute` 禁用按钮 {#disabling-the-button-with-canexecute}

当命令的 `CanExecute` 返回 `false` 时，按钮会自动变为不可用：

```csharp
[ObservableProperty]
[NotifyCanExecuteChangedFor(nameof(SaveCommand))]
private string _name = "";

[RelayCommand(CanExecute = nameof(CanSave))]
private void Save() { /* ... */ }

private bool CanSave() => !string.IsNullOrWhiteSpace(Name);
```

## 带图标的按钮 {#button-with-icon}

```xml
<Button>
    <StackPanel Orientation="Horizontal" Spacing="6">
        <PathIcon Data="{StaticResource save_regular}" Width="16" />
        <TextBlock Text="Save" VerticalAlignment="Center" />
    </StackPanel>
</Button>
```

## `ClickMode`

`ClickMode` 属性决定 `Click` 事件何时触发：

| 值 | 说明 |
|---|---|
| `Release` | 指针抬起时触发点击（默认）。 |
| `Press` | 指针按下时触发点击。 |
| `Hover` | 指针移入按钮时触发点击。 |

## `IsDefault` and `IsCancel`

你可以把某个按钮指定为窗口或对话框的默认操作或取消操作。把 `IsDefault` 设为 `true` 后，用户按 **Enter** 即可触发该按钮；把 `IsCancel` 设为 `true` 后，用户按 **Esc** 即可触发。

```xml
<StackPanel Orientation="Horizontal" Spacing="8">
  <Button Content="OK" IsDefault="True" Command="{Binding ConfirmCommand}" />
  <Button Content="Cancel" IsCancel="True" Command="{Binding CancelCommand}" />
</StackPanel>
```

## 带 flyout 的按钮 {#button-with-a-flyout}

可以给按钮挂一个 `Flyout`，这样点击按钮就会弹出一个浮层：

```xml
<Button Content="Options">
  <Button.Flyout>
    <MenuFlyout>
      <MenuItem Header="Cut" />
      <MenuItem Header="Copy" />
      <MenuItem Header="Paste" />
    </MenuFlyout>
  </Button.Flyout>
</Button>
```

## `Click` vs. `PointerPressed`

判断用户是否按下了按钮，请一律用 `Click` 事件，而不是 `PointerPressed`。`Click` 是 `Button` 专有的高层事件，而 `PointerPressed` 是低层输入事件，`Button` 内部已经把它处理掉了（会把 `IsHandled` 置为 `true`）。正因为该事件被标记为已处理，你的应用不会像从其他控件那样收到来自 `Button` 的 `PointerPressed`。

按钮事件的完整列表请参阅 [Button 事件 API 参考](/api/avalonia/controls/button)。

## 键盘与无障碍 {#keyboard-and-accessibility}

`Button` 默认可获得焦点，并参与 Tab 导航。按钮获得键盘焦点后，用户按 **空格** 或 **Enter** 即可触发它。屏幕阅读器会把按钮的 `Content` 当作它的无障碍名称来播报，所以请提供有意义的文字。如果按钮里只有一个图标，请设置 `AutomationProperties.Name` 附加属性，好让辅助技术认出它：

```xml
<Button Command="{Binding SaveCommand}"
        AutomationProperties.Name="Save">
  <PathIcon Data="{StaticResource save_regular}" Width="16" />
</Button>
```

## Styling

`Button` 提供了几个可在样式中定位的伪类：

| 伪类   | 生效时机                          |
|----------------|---------------------------------------|
| `:pointerover` | 指针悬停在按钮上。 |
| `:pressed`     | 按钮正被按下。          |
| `:disabled`    | 按钮的 `IsEnabled` 为 `false`。  |
| `:focus`       | 按钮拥有键盘焦点。        |

```xml
<Style Selector="Button.accent:pointerover">
  <Setter Property="Background" Value="{DynamicResource SystemAccentColorDark1}" />
</Style>
```

## 另请参阅 {#see-also}

- [Button API 参考](/api/avalonia/controls/button)
- [GitHub 上的 `Button.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Button.cs)
- [RepeatButton](/controls/input/buttons/repeatbutton)
- [ToggleButton](/controls/input/buttons/togglebutton)
- [SplitButton](/controls/input/buttons/splitbutton)
- [HyperlinkButton](/controls/input/buttons/hyperlinkbutton)
- [添加交互](/docs/input-interaction/adding-interactivity)

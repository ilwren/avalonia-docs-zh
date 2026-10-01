---
id: buttonspinner
title: ButtonSpinner
description: 一个内容控件，带有「加」「减」两个微调按钮，用于在一组值之间来回切换。
doc-type: reference
---

[`ButtonSpinner`](/api/avalonia/controls/buttonspinner) 提供一个带有上调、下调按钮的控件。按钮的内容可以很灵活，但相应的行为得你自己写不少代码。

## 何时使用 `ButtonSpinner` {#when-to-use-buttonspinner}

当你需要完全掌控微调行为时就用 `ButtonSpinner`，比如在一组非数值的取值之间循环，或者在每次加减时跑一段自定义逻辑。由于该控件不内置取值处理，响应微调事件、更新所显示的内容都得你自己来。

若只是标准的数值输入、还想要内置的校验和格式化，请改用 [`NumericUpDown`](/controls/input/selectors/numericupdown)。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性 | 说明 |
|---|---|
| `ButtonSpinnerLocation` | 微调按钮的位置：`Left` 或 `Right`（默认）。 |
| `ValidSpinDirection` | 限制微调方向：`Increase`、`Decrease` 或 `None`。 |
| `AllowSpin` | 是否允许微调，默认值为 `true`。 |

## Example

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             Padding="20">
  <ButtonSpinner Spin="OnSpin"
                 HorizontalAlignment="Center"
                 VerticalAlignment="Center">
    Press the spinner
  </ButtonSpinner>
</UserControl>
```

```csharp
public partial class MainView : UserControl
{
    private int _currentValue = 0;

    public void OnSpin(object sender, SpinEventArgs args)
    {
        if (args.Direction == SpinDirection.Increase)
            _currentValue++;
        else
            _currentValue--;

        var btn = (ButtonSpinner)sender;
        btn.Content = $"Value: {_currentValue}";
    }
}
```

</XamlPreview>

## 搭配 MVVM 使用 {#using-with-mvvm}

可以把 `Spin` 事件绑定到视图模型中的命令。把要显示的内容放进 `ButtonSpinner`，再绑定到视图模型的某个属性即可。

```xml
<ButtonSpinner Spin="{Binding SpinCommand}">
    <TextBlock Text="{Binding CurrentValue}" />
</ButtonSpinner>
```

```csharp
public partial class MyViewModel : ObservableObject
{
    [ObservableProperty]
    private string _currentValue = "0";

    [RelayCommand]
    private void Spin(SpinEventArgs args)
    {
        var value = int.Parse(CurrentValue);

        if (args.Direction == SpinDirection.Increase)
            value++;
        else
            value--;

        CurrentValue = value.ToString();
    }
}
```

## 另请参阅 {#see-also}

- [ButtonSpinner API 参考](/api/avalonia/controls/buttonspinner)
- [GitHub 上的 `ButtonSpinner.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/ButtonSpinner.cs)
- [`NumericUpDown`](/controls/input/selectors/numericupdown)
- [`Button`](/controls/input/buttons/button)

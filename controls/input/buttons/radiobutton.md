---
id: radiobutton
title: RadioButton
description: 一个互斥的选项控件，让用户从一组选项中只选其一。
doc-type: reference
---

`RadioButton` 控件给出一组选项，一次只能选中其中一个。选中的选项画成实心圆，未选中的画成空心圆。每个单选按钮的内容作为标签显示在圆圈旁边。

一组选项可以全都不选中。但一旦选了某一项，仅凭用户操作就再也回不到「全不选中」的状态了。要在代码中取消全部选中，请把该组中每个单选按钮的 `IsChecked` 都设为 `false`。

## 分组行为 {#grouping-behavior}

`GroupName` 取值相同的单选按钮构成一个互斥组。选中其中一项时，同组中先前选中的那一项会自动取消选中。

若不设置 `GroupName`，Avalonia 会按父容器给单选按钮分组：同一个父面板下的所有 `RadioButton` 控件算作一组。若要在同一个父级里分出互不相干的几组，请给每组指定不同的 `GroupName` 字符串。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性 | 说明 |
| ----------- | ----------- |
| `GroupName` | 定义一组互斥单选按钮共用的名称。 |
| `IsChecked` | 单选项是选中（`true`）还是未选中（`false`）。 |
| `IsEnabled` | 单选项是否可用。不可用的选项会显示为淡色。 |
| `Content` | 显示在单选圆圈旁边的标签或内容。 |
| `Command` | 单选按钮被选中时调用的 `ICommand`。 |

## Example

这个例子展示两组互不相干的单选按钮：

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui">
  <StackPanel Margin="20">
    <TextBlock Margin="0 10 0 5">First Group</TextBlock>
      <RadioButton GroupName="First Group"
                Content="First Option"/>
      <RadioButton GroupName="First Group"
                Content="Second Option"/>
      <RadioButton IsEnabled="False"
                GroupName="First Group"
                Content="Third Option"/>

    <TextBlock Margin="0 10 0 5">Second Group</TextBlock>
      <RadioButton GroupName="Second Group"
                Content="Fourth Option"/>
      <RadioButton GroupName="Second Group"
                Content="Fifth Option"/>
  </StackPanel>
</UserControl>
```

</XamlPreview>

## 绑定到视图模型 {#binding-to-a-view-model}

可以把 `IsChecked` 绑定到视图模型中的布尔属性。下面的例子为每个选项各用一个布尔值：

```csharp
public partial class NotificationViewModel : ObservableObject
{
    [ObservableProperty]
    private bool _notifyByEmail = true;

    [ObservableProperty]
    private bool _notifyBySms;

    [ObservableProperty]
    private bool _noNotifications;
}
```

```xml
<StackPanel Spacing="4">
    <RadioButton GroupName="Notify"
                 Content="Email"
                 IsChecked="{Binding NotifyByEmail}" />
    <RadioButton GroupName="Notify"
                 Content="SMS"
                 IsChecked="{Binding NotifyBySms}" />
    <RadioButton GroupName="Notify"
                 Content="None"
                 IsChecked="{Binding NoNotifications}" />
</StackPanel>
```

## 绑定到枚举 {#binding-to-an-enum}

一种常见做法是把单选按钮绑定到视图模型中的枚举属性，再用一个转换器把各个枚举值映射成布尔值：

```csharp
public enum ShippingMethod { Standard, Express, Overnight }

public partial class OrderViewModel : ObservableObject
{
    [ObservableProperty]
    private ShippingMethod _selectedShipping = ShippingMethod.Standard;
}
```

Avalonia 为此内置了 [`EnumToBoolConverter`](/api/avalonia/controls/converters/enumtoboolconverter)。在绑定中使用它之前，先把它注册为 `App.axaml` 中的应用资源，这样全应用都能用到：

```xml
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:converters="clr-namespace:Avalonia.Controls.Converters;assembly=Avalonia.Controls"
             x:Class="YourApp.App">

    <Application.Resources>
        <converters:EnumToBoolConverter x:Key="EnumToBoolConverter"/>
    </Application.Resources>

</Application>
```

然后在单选按钮的绑定中引用这个转换器：

```xml
<StackPanel Spacing="4">
    <RadioButton Content="Standard (5-7 days)"
                 IsChecked="{Binding SelectedShipping,
                     Converter={StaticResource EnumToBoolConverter},
                     ConverterParameter={x:Static vm:ShippingMethod.Standard}}" />
    <RadioButton Content="Express (2-3 days)"
                 IsChecked="{Binding SelectedShipping,
                     Converter={StaticResource EnumToBoolConverter},
                     ConverterParameter={x:Static vm:ShippingMethod.Express}}" />
    <RadioButton Content="Overnight"
                 IsChecked="{Binding SelectedShipping,
                     Converter={StaticResource EnumToBoolConverter},
                     ConverterParameter={x:Static vm:ShippingMethod.Overnight}}" />
</StackPanel>
```

## 横向排列 {#horizontal-layout}

把单选按钮放进横向的 `StackPanel`，就能让它们横着排：

```xml
<StackPanel Orientation="Horizontal" Spacing="16">
    <RadioButton GroupName="Size" Content="Small" />
    <RadioButton GroupName="Size" Content="Medium" IsChecked="True" />
    <RadioButton GroupName="Size" Content="Large" />
</StackPanel>
```

## 另请参阅 {#see-also}

- [CheckBox](/controls/input/selectors/checkbox)
- [ToggleButton](/controls/input/buttons/togglebutton)
- [Button](/controls/input/buttons/button)
- [RadioButton API Reference](/api/avalonia/controls/radiobutton)

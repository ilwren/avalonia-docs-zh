---
id: checkbox
title: CheckBox
description: 一个控件：让用户用勾选标记切换布尔值，还可选配表示不确定值的三态支持。
doc-type: reference
---

import CheckBoxTwoStateScreenshot from '/img/reference/controls/checkbox/checkbox-two-state.gif';
import CheckBoxThreeStateScreenshot from '/img/reference/controls/checkbox/checkbox-three-state.gif';

[`CheckBox`](/api/avalonia/controls/checkbox) 控件表示一个布尔值：true 画成勾选标记，false 画成空方框。你还可以启用三态模式，此时 null 表示「未知」，画成一个带底色的方框。

点击该控件会按以下顺序切换取值：选中、未选中、未知（启用三态时）。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性       | 类型    | 说明                                                                 |
| -------------- | ------- | --------------------------------------------------------------------------- |
| `IsChecked`    | `bool?` | 获取或设置勾选状态：`true` 为选中，`false` 为未选中，`null` 为不确定。 |
| `IsThreeState` | `bool`  | 为 `true` 时，控件在选中、未选中、不确定三个状态之间循环。 |
| `Content`      | `object`| 显示在勾选标记旁边的标签内容。                          |
| `Command`      | `ICommand` | 用户切换复选框时调用的命令。                   |

## 两态示例 {#two-state-example}

在默认的两态模式下，`IsChecked` 在 `true` 和 `false` 之间来回切换：

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui">
    <StackPanel Margin="20">
        <CheckBox>Not checked by default</CheckBox>
        <CheckBox IsChecked="True">Checked by default</CheckBox>
    </StackPanel>
</UserControl>
```

</XamlPreview>

<Image light={CheckBoxTwoStateScreenshot} alt="Two-state CheckBox" position="center" maxWidth={400} cornerRadius="true"/>

## 三态示例 {#three-state-example}

把 `IsThreeState` 设为 `true` 后，控件会多出一个不确定状态。把 `IsChecked` 设为 `{x:Null}` 可让它一开始就处于不确定状态：

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <StackPanel Margin="20">
        <CheckBox IsThreeState="True" IsChecked="False">Not checked by default</CheckBox>
        <CheckBox IsThreeState="True" IsChecked="True">Checked by default</CheckBox>
        <CheckBox IsThreeState="True" IsChecked="{x:Null}">Unknown by default</CheckBox>
    </StackPanel>
</UserControl>
```

</XamlPreview>

<Image light={CheckBoxThreeStateScreenshot} alt="Three-state CheckBox" position="center" maxWidth={400} cornerRadius="true"/>

把三态的 `CheckBox` 绑定到视图模型时，请使用可空的 `bool?` 属性，这样不确定状态才能正确地来回传递。

## 绑定到视图模型 {#binding-to-a-view-model}

把 `IsChecked` 绑定到视图模型中的 `bool` 属性。下面的例子用了 MVVM Toolkit 的源生成器：

```csharp
public partial class SettingsViewModel : ObservableObject
{
    [ObservableProperty]
    private bool _autoSave = true;

    [ObservableProperty]
    private bool _showLineNumbers;
}
```

```xml
<StackPanel Spacing="8">
    <CheckBox IsChecked="{Binding AutoSave}" Content="Auto-save on exit" />
    <CheckBox IsChecked="{Binding ShowLineNumbers}" Content="Show line numbers" />
</StackPanel>
```

若需要在值变化时作出响应，可以订阅 `PropertyChanged` 事件，或使用 `OnAutoSaveChanged` 这样的分部方法。

## 由集合生成的复选框列表 {#checkbox-list-from-a-collection}

把 `ItemsControl` 与条目模板中的 `CheckBox` 组合起来，就能做出一列可勾选的条目：

```xml
<ItemsControl ItemsSource="{Binding Features}">
    <ItemsControl.ItemTemplate>
        <DataTemplate>
            <CheckBox IsChecked="{Binding IsEnabled}" Content="{Binding Name}" />
        </DataTemplate>
    </ItemsControl.ItemTemplate>
</ItemsControl>
```

## 「全选」范式 {#select-all-pattern}

三态的 `CheckBox` 很适合用作「全选」控件：只有部分子项被选中时把它设为不确定，用户点击时再去更新各个子项：

```csharp
[ObservableProperty]
private bool? _selectAll = false;

partial void OnSelectAllChanged(bool? value)
{
    if (value.HasValue)
    {
        foreach (var item in Items)
            item.IsSelected = value.Value;
    }
}
```

```xml
<StackPanel Spacing="4">
    <CheckBox IsThreeState="True"
              IsChecked="{Binding SelectAll}"
              Content="Select all" />
    <ItemsControl ItemsSource="{Binding Items}" Margin="24,0,0,0">
        <ItemsControl.ItemTemplate>
            <DataTemplate>
                <CheckBox IsChecked="{Binding IsSelected}" Content="{Binding Name}" />
            </DataTemplate>
        </ItemsControl.ItemTemplate>
    </ItemsControl>
</StackPanel>
```

## 另请参阅 {#see-also}

- [ToggleSwitch](/controls/input/selectors/toggleswitch)
- [RadioButton](/controls/input/buttons/radiobutton)
- [CheckBox API 参考](/api/avalonia/controls/checkbox)
- [GitHub 上的 `CheckBox.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/CheckBox.cs)

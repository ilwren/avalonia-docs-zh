---
id: combobox-how-to
title: "操作指南：使用 ComboBox"
description: 用 Avalonia 的 ComboBox 控件绑定集合、自定义模板、启用可编辑下拉框，以及绑定枚举。
doc-type: how-to
---

import ComboBoxBasicBinding from '/img/controls/combobox/combobox-basic-binding.png';
import ComboBoxComplexObject from '/img/controls/combobox/combobox-complex-object.png';
import AutoCompleteBoxScreenshot from '/img/controls/autocompletebox/autocompletebox.gif';

本指南介绍 [`ComboBox`](/api/avalonia/controls/combobox) 的常见用法，包括绑定到集合、自定义项模板，以及处理枚举。

## 基本绑定 {#basic-binding}

要把 `ComboBox` 绑定到集合并跟踪当前选中项，请在视图模型中把 `ItemsSource` 设为你的集合，并绑定 `SelectedItem`。再用 `PlaceholderText` 在未选中任何项时给出提示：

<Tabs>

<TabItem value="window" label="Window">

```xml
<ComboBox ItemsSource="{Binding Countries}"
          SelectedItem="{Binding SelectedCountry}"
          PlaceholderText="Select a country..." />
```

</TabItem>

<TabItem value="viewmodel" label="View model">

```csharp
using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;

namespace ComboBoxTest.ViewModels;

public partial class MainWindowViewModel : ViewModelBase
{
    public ObservableCollection<string> Countries { get; } = new()
    {
        "Australia", "Canada", "Japan", "Singapore", "UK", "USA"
    };
    
    [ObservableProperty]
    private string? _selectedCountry;
}
```

</TabItem>

<TabItem value="preview" label="Preview">

<Image light={ComboBoxBasicBinding} maxWidth={300} cornerRadius="true" position="center" alt="A screenshot of an app with an open dropdown menu, in which several country names are listed." />

</TabItem>

</Tabs>

:::tip
用 `ObservableCollection<T>` 而不是 `List<T>`，意味着运行时增删项目后 `ComboBox` 能自动更新。
:::

## 自定义项模板 {#custom-item-template}

当项目是由多个部分组成的复杂对象时（比如含姓名、职位、邮箱的用户资料），用 `ComboBox.ItemTemplate` 来控制每一项在下拉列表中的呈现方式。这样你就能同时展示多个属性、图标或自定义布局：

<Tabs>

<TabItem value="window" label="MainWindow.axaml">

```xml
<ComboBox ItemsSource="{Binding Users}"
          SelectedItem="{Binding SelectedUser}">
    <ComboBox.ItemTemplate>
        <DataTemplate>
            <StackPanel Orientation="Horizontal" Spacing="8">
                <Border Width="24" Height="24" CornerRadius="12"
                        Background="#6366F1">
                    <TextBlock Text="{Binding Initials}" Foreground="White"
                               HorizontalAlignment="Center"
                               VerticalAlignment="Center" FontSize="10" />
                </Border>
                <StackPanel>
                    <TextBlock Text="{Binding Name}" />
                    <TextBlock Text="{Binding Role}" FontSize="11" Foreground="Gray" />
                </StackPanel>
            </StackPanel>
        </DataTemplate>
    </ComboBox.ItemTemplate>
</ComboBox>
```

</TabItem>

<TabItem value="viewmodel" label="MainWindowViewModel.cs">

```csharp
using System.Collections.ObjectModel;
using ComboBoxTest.Models;
using CommunityToolkit.Mvvm.ComponentModel;

namespace ComboBoxTest.ViewModels;

public partial class MainWindowViewModel : ViewModelBase
{
    public ObservableCollection<User> Users { get; } =
    [
        new() { Name = "Ray Sin", Role = "CEO" },
        new() { Name = "Scott Chegg", Role = "Manager" },
        new() { Name = "Isabelle Ringing", Role = "Analyst" }
    ];

    [ObservableProperty]
    private User? _selectedUser;
}
```

</TabItem>

<TabItem value="datamodel" label="User.cs">

```csharp
using System;
using System.Linq;

namespace ComboBoxTest.Models;

public class User
{
    public required string Name { get; init; }

    public required string Role { get; init; }

    public string Initials => string.Concat(
        Name.Split(' ', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
            .Select(word => char.ToUpperInvariant(word[0])));
}
```

</TabItem>

<TabItem value="preview" label="Preview">

<Image light={ComboBoxComplexObject} maxWidth={300} cornerRadius="true" position="center" alt="A screenshot of an app with an open dropdown menu, in which users are listed with their initials in a profile disc next to their names and job titles." />

</TabItem>

</Tabs>

对复杂对象使用自定义项模板时，`ComboBox` 会用与列表项相同的模板，把选中项显示在框内。若你希望选中项和下拉项用不同的布局，可以改用 `DataTemplateSelector`，或者写样式专门指向弹出层内的那些项。

## 绑定到枚举 {#binding-to-an-enum}

调用 `Enum.GetValues<T>()` 并把结果作为数组公开，就能把某个枚举的全部值填进 `ComboBox`。

<Tabs>

<TabItem value="window" label="Window">

```xml
<ComboBox ItemsSource="{Binding PriorityOptions}"
          SelectedItem="{Binding SelectedPriority}" />
```

</TabItem>

<TabItem value="viewmodel" label="View model">

```csharp
public enum Priority { Low, Normal, High, Critical }

public partial class TaskViewModel : ObservableObject
{
    public Priority[] PriorityOptions { get; } = Enum.GetValues<Priority>();

    [ObservableProperty]
    private Priority _selectedPriority = Priority.Normal;
}
```

</TabItem>

</Tabs>

### 带显示名称 {#with-display-names}

上面这种办法在 `ComboBox` 中显示的是枚举成员的原始名称，比如前例中显示的是 `"High"` 而非 `"High Priority"`。若你想要便于阅读的标签，可以把每个值包进一条 record 并提供 `ItemTemplate`。

<Tabs>

<TabItem value="window" label="Window">

```xml
<ComboBox ItemsSource="{Binding PriorityOptions}"
          SelectedItem="{Binding SelectedPriority}">
    <ComboBox.ItemTemplate>
        <DataTemplate>
            <TextBlock Text="{Binding Label}" />
        </DataTemplate>
    </ComboBox.ItemTemplate>
</ComboBox>
```

</TabItem>

<TabItem value="viewmodel" label="View model">

```csharp
public record PriorityOption(Priority Value, string Label);

public PriorityOption[] PriorityOptions { get; } = new[]
{
    new PriorityOption(Priority.Low, "Low Priority"),
    new PriorityOption(Priority.Normal, "Normal"),
    new PriorityOption(Priority.High, "High Priority"),
    new PriorityOption(Priority.Critical, "Critical!"),
};

[ObservableProperty]
private PriorityOption _selectedPriority;
```

</TabItem>

</Tabs>

## 绑定到 `SelectedValue` {#binding-to-selectedvalue}

若你要的只是复杂项中的某一个属性、而非整个对象，可以用 `SelectedValueBinding` 指定提取哪个属性，再用 `SelectedValue` 绑定结果。当你只需要保存复合数据对象的 ID 或编码时，常会用到这种绑定。

```xml
<ComboBox ItemsSource="{Binding Countries}"
          SelectedValueBinding="{Binding Code}"
          SelectedValue="{Binding SelectedCountryCode}">
    <ComboBox.ItemTemplate>
        <DataTemplate>
            <TextBlock Text="{Binding Name}" />
        </DataTemplate>
    </ComboBox.ItemTemplate>
</ComboBox>
```

## 在 XAML 中写死选项 {#static-items-in-xaml}

如果选项数量不多、运行时也不会变，你可以用 `ComboBoxItem` 直接在 XAML 里定义。设置菜单或输入表单往往适合这么做——那里的下拉选项在设计阶段早就定下来了。

<XamlPreview>

```xml
<ComboBox xmlns="https://github.com/avaloniaui"
          SelectedIndex="0"
          Margin="10">
    <ComboBoxItem Content="Small" />
    <ComboBoxItem Content="Medium" />
    <ComboBoxItem Content="Large" />
</ComboBox>
```

</XamlPreview>

## 用 `AutoCompleteBox` 实现输入即搜索 {#type-to-search-with-autocompletebox}

设置 `IsEditable="True"` 后，Avalonia 的 `ComboBox` 可以接受文本输入。不过这个设置并不会带来输入即搜索的能力。如果你需要一个边输入边搜索的框，请改用 [`AutoCompleteBox`](/controls/input/text-input/autocompletebox)。

<Image light={AutoCompleteBoxScreenshot} maxWidth={400} cornerRadius="true" position="center" alt="A short animation demonstrating the type-to-search functionality of the auto-complete box using a list of animals." />
<br />

```xml
<!-- Basic AutoCompleteBox -->

<AutoCompleteBox ItemsSource="{Binding Animals}"
                 Text="{Binding SearchText}"
                 FilterMode="StartsWith"
                 MinimumPrefixLength="1" />
```

`AutoCompleteBox` 会随用户输入实时筛选列表。你可以从几种内置筛选模式（`StartsWith`、`Contains`、`ContainsCaseSensitive` 等）中挑一个，也可以提供自定义筛选器：

```xml
<!-- AutoCompleteBox with custom filter and a DataTemplate to search complex objects. -->

<AutoCompleteBox ItemsSource="{Binding Users}"
                 FilterMode="Custom"
                 TextFilter="{Binding UserFilter}"
                 PlaceholderText="Search users...">
    <AutoCompleteBox.ItemTemplate>
        <DataTemplate>
            <TextBlock Text="{Binding Name}" />
        </DataTemplate>
    </AutoCompleteBox.ItemTemplate>
</AutoCompleteBox>
```

## Styling

### 自定义下拉宽度 {#custom-dropdown-width}

给 `ComboBox` 模板内的 `Popup` 单独设一个宽度，保证下拉框够宽、装得下内容。不妨试试把下面预览中的 `Width` 调成 `MinWidth` 看看效果：

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui">

    <UserControl.Styles>
        <Style Selector="ComboBox /template/ Popup">
            <Setter Property="Width" Value="20" />
        </Style>
    </UserControl.Styles>

    <ComboBox Margin="10">
        <ComboBoxItem Content="Short string" />
        <ComboBoxItem Content="Very long string" />
        <ComboBoxItem Content="Very very long string" />
    </ComboBox>

</UserControl>
```

</XamlPreview>

### 自定义占位文本样式 {#custom-placeholder-style}

写一条样式指向 `PlaceholderTextBlock` 元素，即可改变占位文本的外观。本例中还特意带上了 [`:not(:disabled)` 伪类](/docs/styling/pseudoclasses)，好让 `ComboBox` 处于活动状态时自定义的占位样式始终生效。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui">

    <UserControl.Styles>
        <Style Selector="ComboBox:not(:disabled) /template/ TextBlock#PlaceholderTextBlock">
            <Setter Property="Foreground" Value="LimeGreen" />
        </Style>
    </UserControl.Styles>

    <ComboBox Margin="10"
              PlaceholderText="Select one...">
        <ComboBoxItem Content="Option 1" />
        <ComboBoxItem Content="Option 2" />
        <ComboBoxItem Content="Option 3" />
    </ComboBox>

</UserControl>
```

</XamlPreview>

## 另请参阅 {#see-also}

- [ComboBox 参考](/controls/input/selectors/combobox)
- [如何绑定到集合](/docs/data-binding/how-to-bind-to-a-collection)：集合绑定基础。
- [数据模板入门](/docs/data-templates/introduction-to-data-templates)：自定义项目的显示方式。
- [集合视图](/docs/data-binding/collection-views)：对绑定的集合做排序、筛选和分组。

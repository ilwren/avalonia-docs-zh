---
id: listbox-how-to
title: "操作指南：使用 ListBox"
description: ListBox 的选择处理、项模板、虚拟化、样式与进阶用法。
doc-type: how-to
---

本指南介绍 ListBox 的常见场景：选择处理、项模板、虚拟化、样式以及一些进阶用法。

## Item Templates

用 `ItemTemplate` 自定义项目的外观：

```xml
<ListBox ItemsSource="{Binding Contacts}">
    <ListBox.ItemTemplate>
        <DataTemplate>
            <Grid ColumnDefinitions="48,*" Margin="4">
                <Border Grid.Column="0" Width="40" Height="40"
                        CornerRadius="20" Background="#E0E0E0"
                        ClipToBounds="True">
                    <TextBlock Text="{Binding Initials}"
                               HorizontalAlignment="Center"
                               VerticalAlignment="Center"
                               FontWeight="Bold" />
                </Border>
                <StackPanel Grid.Column="1" Margin="8,0,0,0"
                            VerticalAlignment="Center">
                    <TextBlock Text="{Binding Name}" FontWeight="SemiBold" />
                    <TextBlock Text="{Binding Email}" Foreground="Gray"
                               FontSize="12" />
                </StackPanel>
            </Grid>
        </DataTemplate>
    </ListBox.ItemTemplate>
</ListBox>
```

## Selection Modes

### 单选（默认） {#single-selection-default}

```xml
<ListBox SelectionMode="Single"
         SelectedItem="{Binding SelectedContact}"
         ItemsSource="{Binding Contacts}" />
```

### 多选 {#multiple-selection}

```xml
<ListBox SelectionMode="Multiple"
         ItemsSource="{Binding Contacts}" />
```

在多选模式下，用户点击项目即可切换它的选中状态。你可以通过 `SelectionChanged` 事件或 `SelectedItems` 属性拿到选中的项目。

### 切换式选择 {#toggle-selection}

```xml
<ListBox SelectionMode="Toggle"
         ItemsSource="{Binding Contacts}" />
```

切换模式下，用户点一下选中、再点一下取消，无需按住 Ctrl。

### 始终有选中项 {#always-selected}

```xml
<ListBox SelectionMode="AlwaysSelected"
         ItemsSource="{Binding Contacts}" />
```

不允许取消全部选中，至少会保留一项处于选中状态。

### 处理选择变化 {#handling-selection-changes}

```csharp
[ObservableProperty]
private Contact? _selectedContact;

partial void OnSelectedContactChanged(Contact? value)
{
    if (value is not null)
        LoadContactDetails(value);
}
```

也可以改用事件：

```xml
<ListBox SelectionChanged="OnSelectionChanged" />
```

```csharp
private void OnSelectionChanged(object? sender, SelectionChangedEventArgs e)
{
    foreach (var added in e.AddedItems)
    {
        // Handle newly selected items
    }
    foreach (var removed in e.RemovedItems)
    {
        // Handle deselected items
    }
}
```

## Virtualization

ListBox 默认启用虚拟化：只为可见的项目创建控件。这需要 ListBox 的高度受到约束才有效。

### 确认虚拟化真的生效了 {#ensuring-virtualization-is-active}

```xml
<!-- BAD: StackPanel gives infinite height, disabling virtualization -->
<StackPanel>
    <ListBox ItemsSource="{Binding LargeList}" />
</StackPanel>

<!-- GOOD: Grid constrains height -->
<Grid RowDefinitions="*">
    <ListBox ItemsSource="{Binding LargeList}" />
</Grid>

<!-- GOOD: Explicit height -->
<ListBox ItemsSource="{Binding LargeList}" Height="400" />
```

### 滚动到某一项 {#scroll-to-an-item}

用代码把某一项滚动到可见范围内：

```csharp
listBox.ScrollIntoView(targetItem);
```

或者滚动到某个索引：

```csharp
listBox.ScrollIntoView(listBox.ItemsSource.ElementAt(50));
```

## Horizontal ListBox

换一个项目面板，让项目横向排列：

```xml
<ListBox ItemsSource="{Binding Tags}">
    <ListBox.ItemsPanel>
        <ItemsPanelTemplate>
            <WrapPanel />
        </ItemsPanelTemplate>
    </ListBox.ItemsPanel>
    <ListBox.ItemTemplate>
        <DataTemplate>
            <Border Background="#E8E8E8" CornerRadius="12" Padding="12,4">
                <TextBlock Text="{Binding}" />
            </Border>
        </DataTemplate>
    </ListBox.ItemTemplate>
</ListBox>
```

若只要单独一行横排：

```xml
<ListBox ItemsSource="{Binding Items}">
    <ListBox.ItemsPanel>
        <ItemsPanelTemplate>
            <StackPanel Orientation="Horizontal" />
        </ItemsPanelTemplate>
    </ListBox.ItemsPanel>
</ListBox>
```

注意：用 `StackPanel` 或 `WrapPanel` 会关掉虚拟化。横向的长列表请用 `VirtualizingStackPanel` 并设置 `Orientation="Horizontal"`。

## Styling ListBox Items

### 自定义选中项的外观 {#custom-selection-appearance}

改写选中项的样子：

```xml
<ListBox.Styles>
    <Style Selector="ListBoxItem:selected /template/ ContentPresenter">
        <Setter Property="Background" Value="#6366F1" />
    </Style>
    <Style Selector="ListBoxItem:selected /template/ ContentPresenter TextBlock">
        <Setter Property="Foreground" Value="White" />
    </Style>
    <Style Selector="ListBoxItem:pointerover /template/ ContentPresenter">
        <Setter Property="Background" Value="#F0F0F0" />
    </Style>
</ListBox.Styles>
```

### 去掉选中高亮 {#removing-the-selection-highlight}

若想让列表只负责展示、不给出选中的视觉反馈：

```xml
<ListBox.Styles>
    <Style Selector="ListBoxItem">
        <Setter Property="Padding" Value="0" />
    </Style>
    <Style Selector="ListBoxItem:selected /template/ ContentPresenter">
        <Setter Property="Background" Value="Transparent" />
    </Style>
    <Style Selector="ListBoxItem:pointerover /template/ ContentPresenter">
        <Setter Property="Background" Value="Transparent" />
    </Style>
</ListBox.Styles>
```

### 项目间距 {#item-spacing}

不改模板也能为项目之间加上间距：

```xml
<ListBox.Styles>
    <Style Selector="ListBoxItem">
        <Setter Property="Margin" Value="0,2" />
        <Setter Property="CornerRadius" Value="4" />
    </Style>
</ListBox.Styles>
```

## 为 ListBox 项目挂上命令 {#commands-on-listbox-items}

点击某一项时调用命令，并把该项作为参数传过去：

```xml
<ListBox ItemsSource="{Binding Items}">
    <ListBox.ItemTemplate>
        <DataTemplate>
            <Button Content="{Binding Name}"
                    Command="{Binding $parent[ListBox].((vm:MainViewModel)DataContext).SelectItemCommand}"
                    CommandParameter="{Binding}"
                    HorizontalAlignment="Stretch"
                    Background="Transparent"
                    BorderThickness="0" />
        </DataTemplate>
    </ListBox.ItemTemplate>
</ListBox>
```

## Empty State

列表为空时显示一条提示：

```xml
<Panel>
    <ListBox ItemsSource="{Binding FilteredItems}"
             IsVisible="{Binding FilteredItems.Count}" />
    <TextBlock Text="No items found"
               IsVisible="{Binding !FilteredItems.Count}"
               HorizontalAlignment="Center"
               VerticalAlignment="Center"
               Foreground="Gray" />
</Panel>
```

## 带复选框的 ListBox {#listbox-with-checkboxes}

做一个可勾选的列表：

```xml
<ListBox ItemsSource="{Binding Tasks}" SelectionMode="Toggle,Multiple">
    <ListBox.ItemTemplate>
        <DataTemplate>
            <CheckBox Content="{Binding Title}"
                      IsChecked="{Binding IsCompleted}" />
        </DataTemplate>
    </ListBox.ItemTemplate>
</ListBox>
```

## Grouping Items

用「扁平列表 + 分组标题」的套路分组显示项目：

```csharp
public abstract class ListEntry { }

public class GroupHeader : ListEntry
{
    public string Title { get; init; } = "";
}

public class ContactEntry : ListEntry
{
    public Contact Contact { get; init; } = null!;
}
```

```xml
<ListBox ItemsSource="{Binding GroupedEntries}">
    <ListBox.DataTemplates>
        <DataTemplate DataType="local:GroupHeader">
            <TextBlock Text="{Binding Title}"
                       FontWeight="Bold" FontSize="14"
                       Margin="0,12,0,4" />
        </DataTemplate>
        <DataTemplate DataType="local:ContactEntry">
            <TextBlock Text="{Binding Contact.Name}" Margin="8,0" />
        </DataTemplate>
    </ListBox.DataTemplates>
    <ListBox.Styles>
        <!-- Make headers non-selectable -->
        <Style Selector="ListBoxItem:is(local:GroupHeader)">
            <Setter Property="IsHitTestVisible" Value="False" />
        </Style>
    </ListBox.Styles>
</ListBox>
```

构建分组列表的详细做法，请参阅[集合视图](/docs/data-binding/collection-views)。

## See Also

- [ListBox 控件参考](/controls/data-display/collections/listbox)：属性表与基础示例。
- [集合视图](/docs/data-binding/collection-views)：集合的排序、筛选与分组。
- [性能](/docs/app-development/performance)：虚拟化与大集合的优化建议。
- [数据模板](/docs/data-templates/introduction-to-data-templates)：模板的运作原理。

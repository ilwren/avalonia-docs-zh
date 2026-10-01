---
id: column-types
title: 列类型
tags:
  - avalonia pro
  - avalonia enterprise
---

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## TreeDataGridTextColumn

`TreeDataGridTextColumn` 把属性值当作文本显示，显示时用 `ToString()` 转成字符串。对可编辑的列，输入的文本会用 `Convert.ChangeType()` 转回属性本身的类型。

### XAML 用法 {#xaml-usage}

```xml
<!-- Read-only column -->
<TreeDataGridTextColumn Header="First Name" Binding="{Binding FirstName}" />

<!-- Column width -->
<TreeDataGridTextColumn Header="First Name" Binding="{Binding FirstName}" Width="200" />

<!-- Formatting -->
<TreeDataGridTextColumn Header="Birth Date" Binding="{Binding BirthDate, StringFormat='{}{0:yyyy-MM-dd}'}" />

<!-- Alignment and trimming -->
<TreeDataGridTextColumn Header="GDP" Binding="{Binding GDP}"
                        TextAlignment="Right"
                        MaxWidth="150" />
```

绑定到可写属性的列默认可编辑。要让某一列只读，请设置 `IsReadOnly="True"`。

### 在代码隐藏中使用 {#code-behind-usage}

使用 `WithTextColumn` 流式方法。只要取值表达式可写，它就会自动用于双向绑定。当列标题与属性同名时，标题可以省略：

```csharp
// Header inferred from property name
source.WithTextColumn(x => x.FirstName)

// Explicit header
source.WithTextColumn("First Name", x => x.FirstName)

// With options
source.WithTextColumn("First Name", x => x.FirstName, o =>
{
    o.Width = new GridLength(200);
    o.IsReadOnly = true;
})
```

### 选项 {#options}

这些选项既可以在 XAML 中写成特性，也可以在代码隐藏中通过 `TextColumnCreateOptions` lambda 配置：

| 选项 | XAML 特性 | 默认值 | 说明 |
|---|---|---|---|
| `Width` | `Width` | `Auto` | 列宽 |
| `IsReadOnly` | `IsReadOnly` | `false` | 该列是否只读 |
| `StringFormat` | 使用绑定 `StringFormat` | 不适用 | 显示用的格式字符串（比如用 `"{0:C}"` 表示货币） |
| `Culture` | 不适用 | `CurrentCulture` | 格式化所用的区域设置 |
| `TextAlignment` | `TextAlignment` | `Left` | 文本的水平对齐方式 |
| `TextTrimming` | `TextTrimming` | 不适用 | 文本过长时如何截断 |
| `TextWrapping` | `TextWrapping` | `NoWrap` | 文本在单元格内如何换行 |
| `IsTextSearchEnabled` | `IsTextSearchEnabled` | `true` | 该列是否参与文本检索 |
| `CanUserResize` | `CanUserResize` | `true` | 用户能否调整该列宽度 |
| `CanUserSortColumn` | `CanUserSortColumn` | `true` | 用户能否点击标题排序 |
| `AllowTriStateSorting` | `AllowTriStateSorting` | `false` | 是否允许升序/降序/不排序三种状态 |
| `MinWidth` / `MaxWidth` | `MinWidth` / `MaxWidth` | 不适用 | 列的最小宽度与最大宽度 |
| `CompareAscending` / `CompareDescending` | 不适用 | 不适用 | 排序所用的自定义比较函数 |
| `BeginEditGestures` | `BeginEditGestures` | 不适用 | 触发编辑模式的手势（`None`、`F2`、`Tap`、`DoubleTap`、`WhenSelected`） |

:::note
对文本列而言，`IsTextSearchEnabled` 默认为 `true`。若不想让某一列参与文本检索，请显式把它设为 `false`。
:::

## TreeDataGridCheckBoxColumn

`TreeDataGridCheckBoxColumn` 把布尔值显示为复选框。

### XAML 用法 {#xaml-usage-1}

```xml
<!-- Basic checkbox -->
<TreeDataGridCheckBoxColumn Header="Active" Binding="{Binding IsActive}" />

<!-- Read-only, non-resizable -->
<TreeDataGridCheckBoxColumn Binding="{Binding IsChecked}"
                            CanUserResize="False"
                            IsReadOnly="True" />
```

### 在代码隐藏中使用 {#code-behind-usage-1}

`bool` 属性用 `WithCheckBoxColumn`，`bool?`（可空）属性则用 `WithThreeStateCheckBoxColumn`：

```csharp
// Basic checkbox
source.WithCheckBoxColumn(x => x.IsActive)

// With explicit header
source.WithCheckBoxColumn("Active", x => x.IsActive)

// Three-state checkbox for nullable bool
source.WithThreeStateCheckBoxColumn(x => x.IsChecked)

// With options
source.WithCheckBoxColumn(x => x.IsActive, o =>
{
    o.CanUserResize = false;
    o.Width = new GridLength(80);
})
```

### 选项 {#options-1}

| 选项 | XAML 特性 | 默认值 | 说明 |
|---|---|---|---|
| `Width` | `Width` | `Auto` | 列宽 |
| `IsReadOnly` | `IsReadOnly` | `false` | 该列是否只读 |
| `CanUserResize` | `CanUserResize` | `true` | 用户能否调整该列宽度 |
| `CanUserSortColumn` | `CanUserSortColumn` | `true` | 用户能否点击标题排序 |
| `AllowTriStateSorting` | `AllowTriStateSorting` | `false` | 是否允许升序/降序/不排序三种状态 |
| `MinWidth` / `MaxWidth` | `MinWidth` / `MaxWidth` | 不适用 | 列的最小宽度与最大宽度 |
| `CompareAscending` / `CompareDescending` | 不适用 | 不适用 | 排序所用的自定义比较函数 |
| `BeginEditGestures` | `BeginEditGestures` | 不适用 | 触发编辑模式的手势 |

## TreeDataGridHierarchicalExpanderColumn

`TreeDataGridHierarchicalExpanderColumn` 用于展示层级树数据，带一个展开器控件来显示/隐藏子项。这种列类型只能用于层级数据。

展开器列会包住一个内层列（通常是 `TreeDataGridTextColumn` 或 `TreeDataGridTemplateColumn`），由后者决定展开器图标旁边显示什么内容。

### XAML 用法 {#xaml-usage-2}

在 XAML 中定义展开器列时，为子项集合写好绑定，再把内层列作为内容嵌进去：

```xml
<TreeDataGridHierarchicalExpanderColumn Header="Name" Width="*"
                                        ChildrenBinding="{Binding Children}"
                                        HasChildrenBinding="{Binding HasChildren}"
                                        IsExpandedBinding="{Binding IsExpanded}">
  <TreeDataGridTextColumn Binding="{Binding Name}" />
</TreeDataGridHierarchicalExpanderColumn>
```

| 特性 | 说明 |
|---|---|
| `ChildrenBinding` | 绑定到每一行的子项集合（必填） |
| `HasChildrenBinding` | 绑定到一个判断「该行是否有子项」的属性，无需加载子项即可判定（适合延迟加载） |
| `IsExpandedBinding` | 把展开状态持久化到模型某个属性上的绑定 |

### 在代码隐藏中使用 {#code-behind-usage-2}

展开器内若放文本列，请使用 `WithHierarchicalExpanderTextColumn`：

```csharp
source.WithHierarchicalExpanderTextColumn(x => x.Name, x => x.Children)

// With options
source.WithHierarchicalExpanderTextColumn(x => x.Name, x => x.Children, o =>
{
    o.Width = GridLength.Star;
    o.HasChildren = x => x.HasChildren;
    o.IsExpanded = x => x.IsExpanded;
})
```

若内层列是自定义的（比如模板列），请使用 `WithHierarchicalExpanderColumn`：

```csharp
source.WithHierarchicalExpanderColumn(
    "Name",
    new TreeDataGridTemplateColumn(null, "FileNameCell", "FileNameEditCell"),
    x => x.Children,
    o =>
    {
        o.Width = GridLength.Star;
        o.HasChildren = x => x.HasChildren;
        o.IsExpanded = x => x.IsExpanded;
    })
```

## TreeDataGridTemplateColumn

`TreeDataGridTemplateColumn` 用数据模板渲染单元格内容，外观和行为完全由你掌控。

### XAML 用法 {#xaml-usage-3}

就地定义单元格模板（以及可选的编辑模板）：

```xml
<TreeDataGridTemplateColumn Header="Region">
  <TreeDataGridTemplateColumn.CellTemplate>
    <DataTemplate DataType="m:Country">
      <TextBlock Text="{Binding Region}" />
    </DataTemplate>
  </TreeDataGridTemplateColumn.CellTemplate>
  <TreeDataGridTemplateColumn.CellEditingTemplate>
    <DataTemplate DataType="m:Country">
      <ComboBox ItemsSource="{x:Static m:Countries.Regions}"
                SelectedItem="{Binding Region}" />
    </DataTemplate>
  </TreeDataGridTemplateColumn.CellEditingTemplate>
</TreeDataGridTemplateColumn>
```

### 在代码隐藏中使用 {#code-behind-usage-3}

#### 使用 `IDataTemplate` 实例： {#using-idatatemplate-instances}

```csharp
source.WithTemplateColumn(
    "Selected",
    new FuncDataTemplate<Person>((_, _) => new CheckBox
    {
        [!CheckBox.IsCheckedProperty] = new Binding("IsSelected"),
    }))
```

#### 使用 XAML 资源键： {#using-xaml-resource-keys}

先在 `TreeDataGrid.Resources` 中定义模板：

```xml
<TreeDataGrid Source="{Binding Source}">
  <TreeDataGrid.Resources>
    <DataTemplate x:Key="CheckBoxCell">
      <CheckBox IsChecked="{Binding IsSelected}" />
    </DataTemplate>
  </TreeDataGrid.Resources>
</TreeDataGrid>
```

再按键引用它：

```csharp
source.WithTemplateColumnFromResourceKeys("Selected", "CheckBoxCell")

// With separate edit template
source.WithTemplateColumnFromResourceKeys("Selected", "CheckBoxCell", "CheckBoxCellEdit")
```

### 选项 {#options-2}

| 选项 | XAML 特性 | 默认值 | 说明 |
|---|---|---|---|
| `Width` | `Width` | `Auto` | 列宽 |
| `TextSearchBinding` | 不适用 | 不适用 | 用于从模型中取出可检索文本的绑定 |
| `CanUserResize` | `CanUserResize` | `true` | 用户能否调整该列宽度 |
| `CanUserSortColumn` | `CanUserSortColumn` | `true` | 用户能否点击标题排序 |
| `AllowTriStateSorting` | `AllowTriStateSorting` | `false` | 是否允许升序/降序/不排序三种状态 |
| `MinWidth` / `MaxWidth` | `MinWidth` / `MaxWidth` | 不适用 | 列的最小宽度与最大宽度 |
| `CompareAscending` / `CompareDescending` | 不适用 | 不适用 | 排序所用的自定义比较函数 |
| `BeginEditGestures` | `BeginEditGestures` | 不适用 | 触发编辑模式的手势 |

要为模板列启用文本检索，请用 `CompiledBinding.Create` 设置 `TextSearchBinding`：

```csharp
source.WithTemplateColumnFromResourceKeys("Name", "FileNameCell", "FileNameEditCell", o =>
{
    o.TextSearchBinding = CompiledBinding.Create<FileTreeNodeModel, string>(x => x.Name);
})
```

## TreeDataGridRowHeaderColumn

`TreeDataGridRowHeaderColumn` 在最左侧一列显示行标题（通常是行号）。

### XAML 用法 {#xaml-usage-4}

```xml
<TreeDataGrid ItemsSource="{Binding Data}">
  <TreeDataGridRowHeaderColumn />
  <TreeDataGridTextColumn Header="Name" Binding="{Binding Name}" />
</TreeDataGrid>
```

### 在代码隐藏中使用 {#code-behind-usage-4}

```csharp
source.WithRowHeaderColumn()
```

## 另请参阅 {#see-also}

- [TreeDataGrid](/controls/data-display/structured-data/treedatagrid/)

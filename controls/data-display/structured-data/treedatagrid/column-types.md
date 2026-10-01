---
id: column-types
title: Column types
tags:
  - avalonia pro
  - avalonia enterprise
---

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## TreeDataGridTextColumn

`TreeDataGridTextColumn` displays property values as text. Values are converted to strings using `ToString()` for display. For editable columns, text input is converted back to the property type using `Convert.ChangeType()`.

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

Columns bound to a writable property are editable by default. To make a column read-only, set `IsReadOnly="True"`.

### Code-behind usage

Use the `WithTextColumn` fluent method. The getter expression is used for two-way binding automatically when the expression is writable. When the header matches the property name, you can omit it:

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

Options can be set as attributes in XAML or configured via the `TextColumnCreateOptions` lambda in code-behind:

| 选项 | XAML attribute | 默认值 | 说明 |
|---|---|---|---|
| `Width` | `Width` | `Auto` | Column width |
| `IsReadOnly` | `IsReadOnly` | `false` | Whether the column is read-only |
| `StringFormat` | Use binding `StringFormat` | 不适用 | Format string for display (e.g. `"{0:C}"` for currency) |
| `Culture` | 不适用 | `CurrentCulture` | Culture for formatting |
| `TextAlignment` | `TextAlignment` | `Left` | Horizontal text alignment |
| `TextTrimming` | `TextTrimming` | 不适用 | How text is trimmed when too long |
| `TextWrapping` | `TextWrapping` | `NoWrap` | How text wraps within the cell |
| `IsTextSearchEnabled` | `IsTextSearchEnabled` | `true` | Whether the column participates in text search |
| `CanUserResize` | `CanUserResize` | `true` | Whether the user can resize the column |
| `CanUserSortColumn` | `CanUserSortColumn` | `true` | Whether the user can sort by clicking the header |
| `AllowTriStateSorting` | `AllowTriStateSorting` | `false` | Allow ascending/descending/unsorted states |
| `MinWidth` / `MaxWidth` | `MinWidth` / `MaxWidth` | 不适用 | Minimum and maximum column widths |
| `CompareAscending` / `CompareDescending` | 不适用 | 不适用 | Custom comparison functions for sorting |
| `BeginEditGestures` | `BeginEditGestures` | 不适用 | Gestures that trigger edit mode (`None`, `F2`, `Tap`, `DoubleTap`, `WhenSelected`) |

:::note
`IsTextSearchEnabled` defaults to `true` for text columns. Set it to `false` explicitly if you don't want a column to participate in text search.
:::

## TreeDataGridCheckBoxColumn

`TreeDataGridCheckBoxColumn` displays Boolean values as checkboxes.

### XAML 用法 {#xaml-usage-1}

```xml
<!-- Basic checkbox -->
<TreeDataGridCheckBoxColumn Header="Active" Binding="{Binding IsActive}" />

<!-- Read-only, non-resizable -->
<TreeDataGridCheckBoxColumn Binding="{Binding IsChecked}"
                            CanUserResize="False"
                            IsReadOnly="True" />
```

### Code-behind usage

Use `WithCheckBoxColumn` for `bool` properties, or `WithThreeStateCheckBoxColumn` for `bool?` (nullable) properties:

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

| 选项 | XAML attribute | 默认值 | 说明 |
|---|---|---|---|
| `Width` | `Width` | `Auto` | Column width |
| `IsReadOnly` | `IsReadOnly` | `false` | Whether the column is read-only |
| `CanUserResize` | `CanUserResize` | `true` | Whether the user can resize the column |
| `CanUserSortColumn` | `CanUserSortColumn` | `true` | Whether the user can sort by clicking the header |
| `AllowTriStateSorting` | `AllowTriStateSorting` | `false` | Allow ascending/descending/unsorted states |
| `MinWidth` / `MaxWidth` | `MinWidth` / `MaxWidth` | 不适用 | Minimum and maximum column widths |
| `CompareAscending` / `CompareDescending` | 不适用 | 不适用 | Custom comparison functions for sorting |
| `BeginEditGestures` | `BeginEditGestures` | 不适用 | Gestures that trigger edit mode |

## TreeDataGridHierarchicalExpanderColumn

`TreeDataGridHierarchicalExpanderColumn` displays hierarchical tree data with an expander control to show/hide child items. This column type can only be used with hierarchical data.

The expander column wraps an inner column (typically a `TreeDataGridTextColumn` or `TreeDataGridTemplateColumn`) which defines what content appears next to the expander icon.

### XAML 用法 {#xaml-usage-2}

Define the expander column in XAML with bindings for children, and nest the inner column as content:

```xml
<TreeDataGridHierarchicalExpanderColumn Header="Name" Width="*"
                                        ChildrenBinding="{Binding Children}"
                                        HasChildrenBinding="{Binding HasChildren}"
                                        IsExpandedBinding="{Binding IsExpanded}">
  <TreeDataGridTextColumn Binding="{Binding Name}" />
</TreeDataGridHierarchicalExpanderColumn>
```

| Attribute | 说明 |
|---|---|
| `ChildrenBinding` | Binding to the children collection for each row (required) |
| `HasChildrenBinding` | Binding to check if a row has children without loading them (useful for lazy loading) |
| `IsExpandedBinding` | Binding to persist the expanded state to a property in the model |

### Code-behind usage

For a text column inside the expander, use `WithHierarchicalExpanderTextColumn`:

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

For a custom inner column (e.g. a template column), use `WithHierarchicalExpanderColumn`:

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

`TreeDataGridTemplateColumn` uses data templates to render cell content, allowing complete control over appearance and behavior.

### XAML 用法 {#xaml-usage-3}

Define the cell template (and optional editing template) inline:

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

### Code-behind usage

#### Using `IDataTemplate` instances:

```csharp
source.WithTemplateColumn(
    "Selected",
    new FuncDataTemplate<Person>((_, _) => new CheckBox
    {
        [!CheckBox.IsCheckedProperty] = new Binding("IsSelected"),
    }))
```

#### Using XAML resource keys:

Define a template in your `TreeDataGrid.Resources`:

```xml
<TreeDataGrid Source="{Binding Source}">
  <TreeDataGrid.Resources>
    <DataTemplate x:Key="CheckBoxCell">
      <CheckBox IsChecked="{Binding IsSelected}" />
    </DataTemplate>
  </TreeDataGrid.Resources>
</TreeDataGrid>
```

Then reference it by key:

```csharp
source.WithTemplateColumnFromResourceKeys("Selected", "CheckBoxCell")

// With separate edit template
source.WithTemplateColumnFromResourceKeys("Selected", "CheckBoxCell", "CheckBoxCellEdit")
```

### 选项 {#options-2}

| 选项 | XAML attribute | 默认值 | 说明 |
|---|---|---|---|
| `Width` | `Width` | `Auto` | Column width |
| `TextSearchBinding` | 不适用 | 不适用 | Binding to extract searchable text from the model |
| `CanUserResize` | `CanUserResize` | `true` | Whether the user can resize the column |
| `CanUserSortColumn` | `CanUserSortColumn` | `true` | Whether the user can sort by clicking the header |
| `AllowTriStateSorting` | `AllowTriStateSorting` | `false` | Allow ascending/descending/unsorted states |
| `MinWidth` / `MaxWidth` | `MinWidth` / `MaxWidth` | 不适用 | Minimum and maximum column widths |
| `CompareAscending` / `CompareDescending` | 不适用 | 不适用 | Custom comparison functions for sorting |
| `BeginEditGestures` | `BeginEditGestures` | 不适用 | Gestures that trigger edit mode |

To enable text search on a template column, set `TextSearchBinding` using `CompiledBinding.Create`:

```csharp
source.WithTemplateColumnFromResourceKeys("Name", "FileNameCell", "FileNameEditCell", o =>
{
    o.TextSearchBinding = CompiledBinding.Create<FileTreeNodeModel, string>(x => x.Name);
})
```

## TreeDataGridRowHeaderColumn

`TreeDataGridRowHeaderColumn` displays row headers (typically row numbers) in the leftmost column.

### XAML 用法 {#xaml-usage-4}

```xml
<TreeDataGrid ItemsSource="{Binding Data}">
  <TreeDataGridRowHeaderColumn />
  <TreeDataGridTextColumn Header="Name" Binding="{Binding Name}" />
</TreeDataGrid>
```

### Code-behind usage

```csharp
source.WithRowHeaderColumn()
```

## 另请参阅 {#see-also}

- [TreeDataGrid](/controls/data-display/structured-data/treedatagrid/)

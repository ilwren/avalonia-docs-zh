---
id: selection-modes
title: 选择模式
tags:
  - avalonia pro
  - avalonia enterprise
---

支持两种选择类型：

- **行选择**让用户整行整行地选
- **单元格选择**让用户选中一个个单元格

两种选择类型都支持单选和多选，默认是单行选择。


:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## 在 XAML 中设置选择模式 {#setting-the-selection-mode-in-xaml}

直接在 `TreeDataGrid` 控件上设置 `SelectionMode` 特性即可。`ItemsSource` 和 `Source` 两种写法都适用：

```xml
<!-- Single row selection (default) -->
<TreeDataGrid ItemsSource="{Binding People}" SelectionMode="Row" />

<!-- Multiple row selection -->
<TreeDataGrid ItemsSource="{Binding People}" SelectionMode="Row,Multiple" />

<!-- Single cell selection -->
<TreeDataGrid ItemsSource="{Binding People}" SelectionMode="Cell" />

<!-- Multiple cell selection -->
<TreeDataGrid ItemsSource="{Binding People}" SelectionMode="Cell,Multiple" />
```

## SelectionChanged 事件 {#selectionchanged-event}

`TreeDataGrid` 控件有一个 `SelectionChanged` 事件，选择一有变化就会触发：

```csharp
treeDataGrid.SelectionChanged += (sender, e) =>
{
    // e is TreeDataGridSelectionChangedEventArgs
    foreach (var item in e.SelectedItems)
    {
        Debug.WriteLine($"Selected: {item}");
    }

    foreach (var item in e.DeselectedItems)
    {
        Debug.WriteLine($"Deselected: {item}");
    }
};
```

该事件在 XAML（`ItemsSource`）和代码隐藏（`Source`）两种写法下都可用。（详见[主参考页](/controls/data-display/structured-data/treedatagrid#two-approaches)。）

## 索引路径 {#index-paths}

由于 `TreeDataGrid` 支持层级数据，单凭一个简单的索引已不足以定位数据源中的某一行。为此，索引改用 `IndexPath` 结构体表示。

`IndexPath` 是一个索引数组，其中每个元素依次指明在数据层级中更深一层上的索引。

来看下面这个数据源：

```text
|- A
|  |- B
|  |- C
|     |- D
|- E
```

- `A` 的索引路径是 `0`，因为它是层级根部的第一项
- `B` 的索引路径是 `0,0`，因为它是第一项的第一个子项
- `C` 的索引路径是 `0,1`，因为它是第一项的第二个子项
- `D` 的索引路径是 `0,1,0`，因为它是 `C` 的第一个子项
- `E` 的索引路径是 `1`，因为它是根部的第二项

`IndexPath` 是一个不可变结构体，用一个整数数组来构造，比如 `new IndexPath(0, 1, 0)`。处理扁平数据源时，它还支持从 `int` 隐式转换。

## 行选择（代码隐藏） {#row-selection-code-behind}

采用代码隐藏中的 `Source` 写法时，行选择由数据源上的 `RowSelection` 属性对外提供。

行选择状态保存在一个 `TreeDataGridRowSelectionModel<TModel>` 实例中。

默认是单选。要启用多选，请把 `SingleSelect` 属性设为 `false`：

```csharp
Source = new FlatTreeDataGridSource<Person>(_people)
    .WithTextColumn("First Name", x => x.FirstName)
    .WithTextColumn("Last Name", x => x.LastName)
    .WithTextColumn(x => x.Age);

Source.RowSelection!.SingleSelect = false;
```

### 获取选中项 {#getting-selected-items}

通过选择模型访问选中项：

```csharp
// Get single selected item
if (Source.RowSelection?.SelectedItem is Person selectedPerson)
{
    Debug.WriteLine($"Selected: {selectedPerson.Name}");
}

// Get multiple selected items
var selectedItems = Source.RowSelection?.SelectedItems;
if (selectedItems != null)
{
    foreach (var item in selectedItems.OfType<Person>())
    {
        Debug.WriteLine($"Selected: {item.Name}");
    }
}
```

### 用代码选中行 {#programmatically-selecting-rows}

你可以借助选择模型用代码选中行：

```csharp
var selection = Source.RowSelection;

// Select by index
selection.SelectedIndex = 2;
selection.SelectedIndex = new IndexPath(2);
selection.SelectedIndex = new IndexPath(2, 1);

// Clear selection
selection.Clear();

// Select multiple items
selection.Select(2);
selection.Select(new IndexPath(2, 1));

// Deselect multiple items
selection.Deselect(2);
selection.Deselect(new IndexPath(2, 1));

// Batch selection changes
selection.BeginBatchUpdate();
selection.Select(0);
selection.Select(1);
selection.Deselect(2);
selection.EndBatchUpdate();
```

### 选择变更事件 {#selection-changed-event}

用选择模型上的 `SelectionChanged` 事件处理选择的变化：

```csharp
Source.RowSelection.SelectionChanged += (sender, e) =>
{
    // e is TreeDataGridSelectionChangedEventArgs<Person>
    Debug.WriteLine($"Selection changed");
    Debug.WriteLine($"Added: {e.SelectedItems.Count}");
    Debug.WriteLine($"Removed: {e.DeselectedItems.Count}");
};
```

## 单元格选择（代码隐藏） {#cell-selection-code-behind}

采用代码隐藏写法时，把一个 `TreeDataGridCellSelectionModel<TModel>` 实例赋给数据源的 `Selection` 属性，即可启用单元格选择：

```csharp
Source = new FlatTreeDataGridSource<Person>(_people)
    .WithTextColumn("First Name", x => x.FirstName)
    .WithTextColumn("Last Name", x => x.LastName)
    .WithTextColumn(x => x.Age);

Source.Selection = new TreeDataGridCellSelectionModel<Person>(Source);
```

启用单元格多选后，可以选中一块矩形区域内的单元格：

```csharp
Source.Selection = new TreeDataGridCellSelectionModel<Person>(Source)
{
    SingleSelect = false
};
```
单元格选择由数据源上的 `CellSelection` 属性对外提供。

`CellIndex` 结构体用「整数列索引 + `IndexPath` 行索引」的组合来定位单个单元格：

```csharp
// Access selected cell
if (Source.CellSelection?.SelectedIndex is { } selectedCell)
{
    Debug.WriteLine($"Selected cell - Row: {selectedCell.RowIndex}, Column: {selectedCell.ColumnIndex}");
}
```

### 获取选中项 {#getting-selected-items-1}

通过选择模型访问选中项：

```csharp
// Get single selected cell
var selection = Source.CellSelection!;

if (selection.SelectedIndex.ColumnIndex != -1 &&
    selection.SelectedIndex.RowIndex.Count == 1)
{
    var column = Source.Columns[selection.SelectedIndex.ColumnIndex];
    var model = _data[selection.SelectedIndex.RowIndex[0]];

    Debug.WriteLine("Selected column: " + column.Header);
    Debug.WriteLine("Selected item: " + model);
}

// Get multiple selected cells
foreach (var selected in selection.SelectedIndexes)
{
    if (selected.ColumnIndex != -1 && selected.RowIndex.Count == 1)
    {
        var column = Source.Columns[selected.ColumnIndex];
        var model = _data[selected.RowIndex[0]];

        Debug.WriteLine("Selected column: " + column.Header);
        Debug.WriteLine("Selected item: " + model);
    }
}
```

### 用代码选中单元格 {#programmatically-selecting-cells}

你可以借助选择模型用代码选中单元格：

```csharp
var selection = Source.CellSelection;

// Select by index
selection.SelectedIndex = new CellIndex(2, 1);
selection.SelectedIndex = new CellIndex(3, new IndexPath(2));

// Select a range
selection.SetSelectedRange(new CellIndex(1, 1), columnCount: 2, rowCount: 2);
```

### 选择变更事件 {#selection-changed-event-1}

用 `SelectionChanged` 事件处理选择的变化：

```csharp
Source.CellSelection!.SelectionChanged += (s, e) =>
{
    Debug.WriteLine($"Selection changed");
};
```

## 另请参阅 {#see-also}

- [TreeDataGrid](/controls/data-display/structured-data/treedatagrid/)

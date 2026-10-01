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
- `B` has an index path of `0,0` as it is the first child of the first item
- `C` has an index path of `0,1` as it is the second child of the first item
- `D` has an index path of `0,1,0` as it is the first child of `C`
- `E` has an index path of `1` as it is the second item in the root

`IndexPath` is an immutable struct which is constructed with an array of integers, e.g.: `new IndexPath(0, 1, 0)`. There is also an implicit conversion from `int` for when working with a flat data source.

## Row selection (code-behind)

When using the code-behind `Source` approach, row selection is exposed via the `RowSelection` property on the source.

Row selection is stored in an instance of the `TreeDataGridRowSelectionModel<TModel>` class.

The default is single selection. To enable multiple selection, set the `SingleSelect` property to `false`:

```csharp
Source = new FlatTreeDataGridSource<Person>(_people)
    .WithTextColumn("First Name", x => x.FirstName)
    .WithTextColumn("Last Name", x => x.LastName)
    .WithTextColumn(x => x.Age);

Source.RowSelection!.SingleSelect = false;
```

### Getting selected items

Access selected items through the selection model:

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

### Programmatically selecting rows

You can select rows programmatically using the selection model:

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

### Selection changed event

Handle selection changes with the `SelectionChanged` event on the selection model:

```csharp
Source.RowSelection.SelectionChanged += (sender, e) =>
{
    // e is TreeDataGridSelectionChangedEventArgs<Person>
    Debug.WriteLine($"Selection changed");
    Debug.WriteLine($"Added: {e.SelectedItems.Count}");
    Debug.WriteLine($"Removed: {e.DeselectedItems.Count}");
};
```

## Cell selection (code-behind)

To enable cell selection when using the code-behind approach, assign an instance of `TreeDataGridCellSelectionModel<TModel>` to the source's `Selection` property:

```csharp
Source = new FlatTreeDataGridSource<Person>(_people)
    .WithTextColumn("First Name", x => x.FirstName)
    .WithTextColumn("Last Name", x => x.LastName)
    .WithTextColumn(x => x.Age);

Source.Selection = new TreeDataGridCellSelectionModel<Person>(Source);
```

When multiple cell selection is enabled, a single rectangular range of cells can be selected:

```csharp
Source.Selection = new TreeDataGridCellSelectionModel<Person>(Source)
{
    SingleSelect = false
};
```
Cell selection is exposed via the `CellSelection` property on the source.

The `CellIndex` struct identifies an individual cell by a combination of an integer column index and an `IndexPath` row index:

```csharp
// Access selected cell
if (Source.CellSelection?.SelectedIndex is { } selectedCell)
{
    Debug.WriteLine($"Selected cell - Row: {selectedCell.RowIndex}, Column: {selectedCell.ColumnIndex}");
}
```

### Getting selected items

Access selected items through the selection model:

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

### Programmatically selecting cells

You can select cells programmatically using the selection model:

```csharp
var selection = Source.CellSelection;

// Select by index
selection.SelectedIndex = new CellIndex(2, 1);
selection.SelectedIndex = new CellIndex(3, new IndexPath(2));

// Select a range
selection.SetSelectedRange(new CellIndex(1, 1), columnCount: 2, rowCount: 2);
```

### Selection changed event

Handle selection changes with the `SelectionChanged` event:

```csharp
Source.CellSelection!.SelectionChanged += (s, e) =>
{
    Debug.WriteLine($"Selection changed");
};
```

## 另请参阅 {#see-also}

- [TreeDataGrid](/controls/data-display/structured-data/treedatagrid/)

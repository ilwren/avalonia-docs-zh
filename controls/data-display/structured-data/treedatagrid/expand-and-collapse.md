---
id: expand-and-collapse
title: 展开与折叠操作
description: 了解如何以编程方式展开和折叠层级 TreeDataGrid 中的行、响应展开/折叠事件，并实现按需延迟加载。
doc-type: reference
tags:
  - avalonia pro
  - avalonia enterprise
---

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

使用层级式 `TreeDataGrid` 时，用户可以展开和折叠行来浏览父子关系。Avalonia 在 `HierarchicalTreeDataGridSource<T>` 上提供了若干方法，让你以编程方式掌控这一行为：既可以展开单个节点，也可以一次性全部展开，还可以只展开符合某个条件的行。你也可以订阅在每次展开或折叠前后触发的事件。

:::note
以编程方式展开/折叠，以及展开/折叠事件，都要求采用代码隐藏中的 `Source` 写法，配合 `HierarchicalTreeDataGridSource<T>`。
:::

## 基本的展开与折叠操作 {#basic-expand-and-collapse-operations}

你可以用代码展开或折叠层级式 `TreeDataGrid` 中的行：

```csharp
var Source = new HierarchicalTreeDataGridSource<Person>(_people)
    .WithHierarchicalExpanderTextColumn(x => x.Name, x => x.Children)
    .WithTextColumn(x => x.Age);

// Expand a specific node by index path
Source.Expand(new IndexPath(0));  // Expand first root item

// Collapse a node
Source.Collapse(new IndexPath(0));
```

:::info
关于 `IndexPath` 的更多内容，请参阅[选择模式](/controls/data-display/structured-data/treedatagrid/selection-modes)
:::

### 全部展开与全部折叠 {#expand-all-and-collapse-all}

数据源内置了一次性展开或折叠所有行的方法：

```csharp
// Expand all rows in the tree
Source.ExpandAll();

// Collapse all rows in the tree
Source.CollapseAll();
```

### 按条件展开或折叠 {#expand-or-collapse-based-on-a-condition}

你可以按条件展开或折叠行：

```csharp
// Expand all rows where Person.Age > 18
Source.ExpandCollapseRecursive(person => person.Age > 18);

// Collapse all rows
Source.ExpandCollapseRecursive(_ => false);
```

## 响应展开与折叠事件 {#responding-to-expand-and-collapse-events}

你可以处理展开和折叠事件，用来按需加载数据或执行其他操作。这些事件使用 `TreeDataGridRowModelEventArgs`：

```csharp
Source.RowExpanding += (sender, e) =>
{
    var person = (Person)e.Row.Model!;
    var indexPath = e.Row.ModelIndexPath;
    Debug.WriteLine($"Expanding: {person.Name} at {indexPath}");
};

Source.RowExpanded += (sender, e) =>
{
    var person = (Person)e.Row.Model!;
    var indexPath = e.Row.ModelIndexPath;
    Debug.WriteLine($"Expanded: {person.Name} at {indexPath}");
};

Source.RowCollapsing += (sender, e) =>
{
    var person = (Person)e.Row.Model!;
    Debug.WriteLine($"Collapsing: {person.Name}");
};

Source.RowCollapsed += (sender, e) =>
{
    var person = (Person)e.Row.Model!;
    Debug.WriteLine($"Collapsed: {person.Name}");
};
```

## 展开时延迟加载数据 {#lazy-loading-data-on-expand}

一种常见做法是：不在一开始就把整棵树加载进来，而是等用户展开某一行时再加载它的子数据。你可以在 `RowExpanding` 事件中，赶在该行展开之前填充子项。这样初始加载会快得多，数据量大时尤其明显。

```csharp
Source.RowExpanding += (sender, e) =>
{
    var person = (Person)e.Row.Model!;

    if (!person.ChildrenLoaded)
    {
        var children = MyDataService.LoadChildren(person.Id);
        person.Children.Clear();
        person.Children.AddRange(children);
        person.ChildrenLoaded = true;
    }
};
```

## 另请参阅 {#see-also}

- [TreeDataGrid](/controls/data-display/structured-data/treedatagrid/)
- [Sorting](/controls/data-display/structured-data/treedatagrid/sorting)
- [Filtering](/controls/data-display/structured-data/treedatagrid/filtering)
- [选择模式](/controls/data-display/structured-data/treedatagrid/selection-modes)
- [列类型](/controls/data-display/structured-data/treedatagrid/column-types)

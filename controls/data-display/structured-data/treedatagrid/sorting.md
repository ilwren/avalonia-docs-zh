---
id: sorting
title: 排序
description: 如何在 Avalonia TreeDataGrid 控件中启用、关闭和定制列排序。
doc-type: reference
tags:
  - avalonia pro
  - avalonia enterprise
---

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

`TreeDataGrid` 控件支持点击列标题对行排序。你可以逐列开关排序、提供自定义的比较逻辑，也可以用代码触发排序。本页逐一介绍这些场景。

## 列排序 {#column-sorting}

### 启用排序 {#enable-sorting}

所有列默认都可排序，用户点击列标题即可。

若要为整个网格关闭排序：

```xml
<TreeDataGrid Source="{Binding Source}"
              CanUserSortColumns="False" />
```

### 让某些列不可排序 {#make-specific-columns-non-sortable}

在 XAML 中为该列设置 `CanUserSortColumn` 特性：

```xml
<TreeDataGridTextColumn Header="Name" Binding="{Binding Name}" CanUserSortColumn="False" />
```

在代码隐藏中则使用选项 lambda：

```csharp
source.WithTextColumn("Name", x => x.Name, o =>
{
    o.CanUserSortColumn = false;
})
```

### 用代码排序 {#programmatic-sorting}

你可以调用数据源上的 `SortBy` 和 `ClearSort` 方法，用代码对列排序：

```csharp
// Sort by a specific column
Source.SortBy(Source.Columns[0], ListSortDirection.Ascending);
Source.SortBy(Source.Columns[1], ListSortDirection.Descending);

// Clear sorting on a specific column
Source.ClearSort(Source.Columns[0]);
```

## 自定义排序 {#custom-sorting}

在代码隐藏中，你可以用比较委托提供自定义的排序逻辑。委托收到的是 `object?` 参数，需要强制转换成你自己的模型类型：

```csharp
source.WithTextColumn("Name", x => x.Name, o =>
{
    o.CompareAscending = (a, b) =>
        string.Compare(((Person?)a)?.Name, ((Person?)b)?.Name, StringComparison.OrdinalIgnoreCase);
    o.CompareDescending = (a, b) =>
        string.Compare(((Person?)b)?.Name, ((Person?)a)?.Name, StringComparison.OrdinalIgnoreCase);
})
```

如果你想在点击一次列标题时按多个字段排序，这一招就派得上用场。

必须分别提供两个比较函数：一个管升序，一个管降序。

:::note
`TreeDataGrid` 只支持单列排序。用户点击某个列标题（或你用代码调用 `SortBy`）时，其他列上已有的排序会被清除。若需要同时按多个字段排序，请在某一列上写一个自定义比较器：先比主字段，再用次字段决胜负。
:::

## 另请参阅 {#see-also}

- [TreeDataGrid](/controls/data-display/structured-data/treedatagrid/)
- [展开与折叠](/controls/data-display/structured-data/treedatagrid/expand-and-collapse)
- [Filtering](/controls/data-display/structured-data/treedatagrid/filtering)
- [选择模式](/controls/data-display/structured-data/treedatagrid/selection-modes)
- [列类型](/controls/data-display/structured-data/treedatagrid/column-types)

---
id: breaking-changes-v12
title: TreeDataGrid v12 破坏性变更
tags:
  - avalonia pro
  - avalonia enterprise
---

本文梳理 TreeDataGrid 11.x 到 12.x 之间的破坏性变更，并给出迁移指引。

TreeDataGrid 12.0 对其 API 作了一次大规模重构，目的是让 API 面向未来，并提供 11.x 时期所不具备的 API 稳定性承诺。

TreeDataGrid 12.x 需要 Avalonia 12。Avalonia 12 自身的破坏性变更请参阅 [Avalonia 12 破坏性变更](https://docs.avaloniaui.net/docs/avalonia12-breaking-changes)文档。

## 列类型不再带泛型参数 {#generic-type-parameters-removed-from-columns}

所有列类都去掉了泛型类型参数，并改用 `TreeDataGrid` 前缀重新命名。列不再按模型类型泛型化。

| 12.x | 取代 |
|---|---|
| `TreeDataGridTextColumn` | `TextColumn<TModel, TValue>` |
| `TreeDataGridCheckBoxColumn` | `CheckBoxColumn<TModel>` |
| `TreeDataGridTemplateColumn` | `TemplateColumn<TModel>` |
| `TreeDataGridHierarchicalExpanderColumn` | `HierarchicalExpanderColumn<TModel>` |
| `TreeDataGridRowHeaderColumn` | `RowHeaderColumn<TModel>` |
| `TreeDataGridColumns` | `ColumnList<TModel>` |

## XAML 支持 {#xaml-support}

TreeDataGrid 现在支持直接在 XAML 中定义列，不必再写代码隐藏里的数据源。设置 `ItemsSource` 属性，然后把各列作为内容写进去即可：

```xml
<TreeDataGrid ItemsSource="{Binding Countries}" SelectionMode="Row,Multiple">
    <TreeDataGridTextColumn Header="Country" Binding="{Binding Name}" Width="6*" />
    <TreeDataGridTextColumn Header="Region" Binding="{Binding Region}" Width="2*" />
    <TreeDataGridCheckBoxColumn Binding="{Binding IsChecked}" CanUserResize="False" />
</TreeDataGrid>
```

层级数据则使用 `TreeDataGridHierarchicalExpanderColumn`：

```xml
<TreeDataGrid ItemsSource="{Binding Files}">
    <TreeDataGridHierarchicalExpanderColumn Header="Name" Width="*"
                                            ChildrenBinding="{Binding Children}"
                                            HasChildrenBinding="{Binding HasChildren}"
                                            IsExpandedBinding="{Binding IsExpanded}">
        <TreeDataGridTextColumn Binding="{Binding Name}"/>
    </TreeDataGridHierarchicalExpanderColumn>
</TreeDataGrid>
```

代码隐藏中 `FlatTreeDataGridSource` / `HierarchicalTreeDataGridSource` 那套写法照旧可用（API 变动见本文所述）。

## 流式列 API {#fluent-column-api}

现在提供了一套流式 API，可用代码创建列。

不再需要分别写取值和赋值两个 lambda。只要取值表达式可写，它就会自动用于双向绑定。若想创建只读列，请在选项回调中设置 `IsReadOnly`。

当列标题与 lambda 所选的属性同名时，标题可以省略。

### `WithTextColumn`

```diff
-new TextColumn<Country, string>(
-    "Country",
-    x => x.Name,
-    (r, v) => r.Name = v,
-    new GridLength(6, GridUnitType.Star))
+source.WithTextColumn("Country", x => x.Name, o => o.Width = new GridLength(6, GridUnitType.Star))
```

几个例子：

```csharp
source.WithTextColumn("Name", x => x.Name)
source.WithTextColumn(x => x.Name)
source.WithTextColumn(x => x.Name, o => o.IsReadOnly = true)
source.WithTextColumn(x => x.Name, o => o.Width = GridLength.Star)
```

### `WithCheckBoxColumn`/`WithThreeStateCheckBoxColumn`

复选框可以用 `WithCheckBoxColumn` 或 `WithThreeStateCheckBoxColumn` 添加：

```diff
-new CheckBoxColumn<FileTreeNodeModel>(
-    null,
-    x => x.IsChecked,
-    (o, v) => o.IsChecked = v)
+source.WithCheckBoxColumn(null, x => x.IsChecked)
```

### `WithTemplateColumn`

模板列可以用 `IDataTemplate` 实例或资源键来添加：

```diff
-new TemplateColumn<Country>(
-    "Region",
-    "RegionCell",
-    "RegionEditCell")
+source.WithTemplateColumnFromResourceKeys("Region", "RegionCell", "RegionEditCell")
```

### `WithHierarchicalExpanderColumn`/`WithHierarchicalExpanderTextColumn`

若层级数据的展开器内要放一个文本列：

```diff
-new HierarchicalExpanderColumn<FileTreeNodeModel>(
-    new TextColumn<FileTreeNodeModel, string>(
-        "Name",
-        x => x.Name),
-    x => x.Children,
-    x => x.HasChildren,
-    x => x.IsExpanded)
+source.WithHierarchicalExpanderTextColumn(x => x.Name, x => x.Children, o =>
+{
+    o.HasChildren = x => x.HasChildren;
+    o.IsExpanded = x => x.IsExpanded;
+})
```

标题和宽度现已从内层列移到了展开器列上。

若展开器内要放自定义的内层列（比如模板列），请使用 `WithHierarchicalExpanderColumn`：

```csharp
source.WithHierarchicalExpanderColumn(
    "Name",
    new TreeDataGridTemplateColumn(null, "FileNameCell", "FileNameEditCell"),
    x => x.Children,
    o =>
    {
        o.Width = new GridLength(1, GridUnitType.Star);
        o.HasChildren = x => x.HasChildren;
        o.IsExpanded = x => x.IsExpanded;
    })
```

### 完整的链式调用示例 {#full-chaining-example}

```csharp
var source = new FlatTreeDataGridSource<Country>(data)
    .WithRowHeaderColumn()
    .WithTextColumn("Country", x => x.Name, o =>
    {
        o.Width = new GridLength(6, GridUnitType.Star);
        o.IsTextSearchEnabled = true;
    })
    .WithTemplateColumnFromResourceKeys("Region", "RegionCell", "RegionEditCell")
    .WithTextColumn(x => x.Population, o => o.Width = new GridLength(3, GridUnitType.Star))
    .WithTextColumn(x => x.Area, o => o.Width = new GridLength(3, GridUnitType.Star));
```

## 列的选项 {#column-options}

各个列选项类已被顶层的 `*CreateOptions` 类取代，改为通过流式方法上的 lambda 回调来配置：

| 12.x | 取代 |
|---|---|
| `ColumnCreateOptions` | `ColumnOptions<TModel>` |
| `TextColumnCreateOptions` | `TextColumnOptions<TModel>` |
| `TemplateColumnCreateOptions` | `TemplateColumnOptions<TModel>` |
| `CheckBoxColumnCreateOptions` | `CheckBoxColumnOptions<TModel>` |

```diff
-new TextColumn<Country, string>(
-    "Country",
-    x => x.Name,
-    options: new TextColumnOptions<Country>
-    {
-        CanUserResizeColumn = false,
-        IsTextSearchEnabled = true,
-    })
+source.WithTextColumn("Country", x => x.Name, o =>
+{
+    o.CanUserResize = false;
+    o.IsTextSearchEnabled = true;
+})
```

`CanUserResizeColumn` 属性已更名为 `CanUserResize`。

`TextColumnCreateOptions` 上的 `IsTextSearchEnabled` 现在默认为 `true`，而在 11.x 中默认是 `false`。如果你不希望某个文本列参与文本检索，现在必须显式关掉它：

```csharp
source.WithTextColumn("Name", x => x.Name, o => o.IsTextSearchEnabled = false)
```

## 接口改为抽象类 {#interfaces-replaced-with-abstract-classes}

TreeDataGrid API 中的几个主要接口已改为抽象类：

| 12.x | 取代 |
|---|---|
| `TreeDataGridSource` | `ITreeDataGridSource` |
| `TreeDataGridSource<TModel>` | `ITreeDataGridSource<TModel>` |
| `TreeDataGridColumn` | `IColumn` |
| `TreeDataGridColumns` | `IColumns` |
| `TreeDataGridRows` | `IRows` |
| `TreeDataGridSelectionModel` | `ITreeDataGridSelection` |
| `TreeDataGridRowSelectionModel<T>` | `ITreeDataGridRowSelectionModel<T>` |
| `TreeDataGridCellSelectionModel<T>` | `ITreeDataGridCellSelectionModel<T>` |

## 更名的类型 {#renamed-types}

下列类型已更名：

| 12.x | 取代 |
|---|---|
| `ITreeDataGridCellModel` | `ICell` |
| `ITreeDataGridRowModel` | `IRow` |

## 移除的类型 {#removed-types}

下列类型已被移除：

- `NotifyingBase`, `ReadOnlyListBase<T>`, `SortableRowsBase<TModel, TRow>`
- `AnonymousSortableRows<TModel>`, `HierarchicalRows<TModel>`, `HierarchicalRow<TModel>`
- `TextCell`, `CheckBoxCell`, `ExpanderCell`, `TemplateCell`, `RowHeaderCell`
- `IExpander`, `IExpanderCell`, `IExpanderRow`, `IExpanderRow<TModel>`,
  `IExpanderRowController<TModel>`
- `IIndentedRow`, `IRow<TModel>`
- `ICellOptions`, `ITextCellOptions`, `ITemplateCellOptions`
- `IUpdateColumnLayout`
- `NotifyingListBase<T>`
- `DragInfo`

如果你依赖其中任何一个类型，请提交 issue，我们再一起讨论替代方案。

## 数据源类型现已 sealed {#sources-are-now-sealed}

`FlatTreeDataGridSource<TModel>` 和 `HierarchicalTreeDataGridSource<TModel>` 现在是 `sealed` 类，不能再派生子类。

## 自定义排序比较改用 `object?` {#custom-sort-comparisons-use-object}

`CompareAscending` 和 `CompareDescending` 上的自定义排序比较委托，已从 `Comparison<TModel?>?` 改为 `Comparison<object?>?`：

```diff
-options: new ColumnOptions<Country>
-{
-    CompareAscending = (a, b) => string.Compare(a?.Name, b?.Name),
-}
+source.WithTextColumn("Country", x => x.Name, o =>
+{
+    o.CompareAscending = (a, b) => string.Compare(((Country?)a)?.Name, ((Country?)b)?.Name);
+})
```

## Unified `SelectionChangedEventArgs`

选择变更事件现在使用 `TreeDataGridSelectionChangedEventArgs`（或泛型版 `TreeDataGridSelectionChangedEventArgs<TModel>`），取代原先的 `TreeSelectionModelSelectionChangedEventArgs<T>`。新的事件参数提供：

- `SelectedIndexes` / `DeselectedIndexes`
- `SelectedItems` / `DeselectedItems`
- `SelectedCellIndexes` / `DeselectedCellIndexes`

`TreeDataGrid` 控件自身也新增了一个 `SelectionChanged` 事件。

## 行相关事件改用 `TreeDataGridRowModelEventArgs` {#row-events-use-treedatagridrowmodeleventargs}

`RowExpanding`、`RowExpanded`、`RowCollapsing` 和 `RowCollapsed` 这几个事件现在改用 `TreeDataGridRowModelEventArgs`，不再使用 `RowEventArgs<HierarchicalRow<TModel>>`。

## 文本检索改用绑定 {#text-search-uses-bindings}

文本检索的配置方式，已从基于 lambda 的取值选择器改为 Avalonia 绑定。

对模板列而言，`TemplateColumnOptions` 上的 `TextSearchValueSelector` lambda 已被 `TemplateColumnCreateOptions` 上的 `TextSearchBinding` 属性取代：

```diff
-new TemplateColumn<FileTreeNodeModel>(
-    "Name",
-    "FileNameCell",
-    "FileNameEditCell",
-    options: new TemplateColumnOptions<FileTreeNodeModel>
-    {
-        TextSearchValueSelector = x => x.Name,
-    })
+source.WithTemplateColumnFromResourceKeys("Name", "FileNameCell", "FileNameEditCell", o =>
+{
+    o.TextSearchBinding = CompiledBinding.Create<FileTreeNodeModel, string>(x => x.Name);
+})
```

对文本列而言，文本检索通过 `TextColumnCreateOptions` 上的 `IsTextSearchEnabled` 属性默认开启，并自动复用该列自己的绑定。

## 命名空间变更 {#namespace-changes}

`Avalonia.Controls.Models.TreeDataGrid` 命名空间（原先存放 `TextColumn<TModel, TValue>`、`TemplateColumn<TModel>`、`HierarchicalExpanderColumn<TModel>`、`TextColumnOptions<TModel>` 等旧列类型）已被移除。新的列类型和选项类位于 `Avalonia.Controls` 命名空间下。请把代码中的 `using Avalonia.Controls.Models.TreeDataGrid` 删掉。

## 实验性绑定已移除 {#experimental-bindings-removed}

`Avalonia.Experimental.Data` 命名空间及其全部类型已被移除，其中包括 `TypedBinding<TIn, TOut>`、`TypedBindingExpression<TIn, TOut>`、`LightweightObservableBase<T>`、`SingleSubscriberObservableBase<T>` 以及相关类型。

TreeDataGrid 12.x 改用标准的 Avalonia 绑定。

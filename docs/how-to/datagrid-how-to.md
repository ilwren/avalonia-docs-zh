---
id: datagrid-how-to
title: "操作指南：使用 DataGrid"
description: DataGrid 的排序、筛选、分组、模板列、选择、校验与编辑。
doc-type: how-to
---

本指南涵盖 DataGrid 的常见场景：排序、筛选、分组、模板列、选择、校验与编辑。

## 配置 {#setup}

安装 NuGet 包并添加样式引用：

```bash
dotnet add package Avalonia.Controls.DataGrid
```

```xml title='App.axaml'
<Application.Styles>
    <FluentTheme />
    <StyleInclude Source="avares://Avalonia.Controls.DataGrid/Themes/Fluent.xaml"/>
</Application.Styles>
```

## Basic Bound DataGrid

```xml
<DataGrid ItemsSource="{Binding Products}" AutoGenerateColumns="False"
          IsReadOnly="True" GridLinesVisibility="All"
          BorderThickness="1" BorderBrush="Gray">
    <DataGrid.Columns>
        <DataGridTextColumn Header="Name" Binding="{Binding Name}" Width="2*" />
        <DataGridTextColumn Header="Price" Binding="{Binding Price, StringFormat='{}{0:C}'}" Width="*" />
        <DataGridCheckBoxColumn Header="In Stock" Binding="{Binding InStock}" Width="Auto" />
    </DataGrid.Columns>
</DataGrid>
```

```csharp
public partial class MainViewModel : ObservableObject
{
    public ObservableCollection<Product> Products { get; } = new()
    {
        new Product("Widget", 9.99m, true),
        new Product("Gadget", 24.99m, false),
        new Product("Gizmo", 14.50m, true),
    };
}

public class Product
{
    public string Name { get; set; }
    public decimal Price { get; set; }
    public bool InStock { get; set; }

    public Product(string name, decimal price, bool inStock)
    {
        Name = name;
        Price = price;
        InStock = inStock;
    }
}
```

## Sorting

排序默认开启（`CanUserSortColumns="True"`）。点击列标题按升序排序，再点一次改为降序。

若要用 `DataGridTemplateColumn` 自定义排序行为，请设置 `SortMemberPath`：

```xml
<DataGridTemplateColumn Header="Age" SortMemberPath="AgeInYears">
    <DataGridTemplateColumn.CellTemplate>
        <DataTemplate>
            <TextBlock Text="{Binding AgeInYears, StringFormat='{}{0} years'}" />
        </DataTemplate>
    </DataGridTemplateColumn.CellTemplate>
</DataGridTemplateColumn>
```

### 用代码排序 {#programmatic-sorting}

```csharp
var column = myDataGrid.Columns[0];
myDataGrid.Columns.Clear();
myDataGrid.Columns.Add(column);
// Or use CollectionView sorting (see Filtering section below)
```

## Filtering

在视图模型中绑定一个筛选后的集合，即可筛选数据：

```csharp
public partial class MainViewModel : ObservableObject
{
    private readonly List<Product> _allProducts;

    [ObservableProperty]
    private string _filterText = "";

    [ObservableProperty]
    private ObservableCollection<Product> _filteredProducts;

    public MainViewModel()
    {
        _allProducts = LoadProducts();
        _filteredProducts = new ObservableCollection<Product>(_allProducts);
    }

    partial void OnFilterTextChanged(string value)
    {
        var filtered = string.IsNullOrWhiteSpace(value)
            ? _allProducts
            : _allProducts.Where(p =>
                p.Name.Contains(value, StringComparison.OrdinalIgnoreCase));

        FilteredProducts = new ObservableCollection<Product>(filtered);
    }
}
```

```xml
<StackPanel Spacing="8">
    <TextBox Text="{Binding FilterText}" PlaceholderText="Search products..." />
    <DataGrid ItemsSource="{Binding FilteredProducts}" AutoGenerateColumns="True"
              IsReadOnly="True" />
</StackPanel>
```

## Grouping

把集合包进 `DataGridCollectionView` 并添加分组描述，即可对行分组。DataGrid 会自动为每个分组渲染一个可折叠的 `DataGridRowGroupHeader`。

### 基本分组 {#basic-grouping}

```csharp
using Avalonia.Collections;

public partial class MainViewModel : ObservableObject
{
    public DataGridCollectionView GroupedProducts { get; }

    public MainViewModel()
    {
        var products = new List<Product>
        {
            new("Widget", "Hardware", 9.99m),
            new("Gadget", "Hardware", 24.99m),
            new("App", "Software", 4.99m),
            new("Plugin", "Software", 14.50m),
        };

        GroupedProducts = new DataGridCollectionView(products);
        GroupedProducts.GroupDescriptions.Add(
            new DataGridPathGroupDescription("Category"));
    }
}
```

```xml
<DataGrid ItemsSource="{Binding GroupedProducts}" AutoGenerateColumns="False"
          IsReadOnly="True">
    <DataGrid.Columns>
        <DataGridTextColumn Header="Name" Binding="{Binding Name}" Width="*" />
        <DataGridTextColumn Header="Price" Binding="{Binding Price, StringFormat='{}{0:C}'}" Width="*" />
    </DataGrid.Columns>
</DataGrid>
```

### 多级分组 {#multiple-group-levels}

添加多个 `DataGridPathGroupDescription` 即可实现嵌套分组：

```csharp
GroupedProducts.GroupDescriptions.Add(new DataGridPathGroupDescription("Category"));
GroupedProducts.GroupDescriptions.Add(new DataGridPathGroupDescription("SubCategory"));
```

### 自定义分组标题 {#customizing-the-group-header}

处理 `LoadingRowGroup` 事件，即可改写标题文字或加上汇总信息：

```csharp
private void OnLoadingRowGroup(object? sender, DataGridRowGroupHeaderEventArgs e)
{
    var group = e.RowGroupHeader.DataContext as DataGridCollectionViewGroup;
    if (group is null)
        return;

    e.RowGroupHeader.PropertyName = "Category";
    e.RowGroupHeader.PropertyValue = $"{group.Key} ({group.ItemCount} products)";
}
```

```xml
<DataGrid ItemsSource="{Binding GroupedProducts}"
          LoadingRowGroup="OnLoadingRowGroup" />
```

### 以编程方式展开和折叠分组 {#expanding-and-collapsing-groups-programmatically}

使用 DataGrid 上的 `ExpandRowGroup` 和 `CollapseRowGroup`：

```csharp
if (viewModel.GroupedProducts.Groups is { } groups)
{
    foreach (var group in groups.OfType<DataGridCollectionViewGroup>())
    {
        myDataGrid.CollapseRowGroup(group, collapseAllSubgroups: true);
    }
}
```

## Column Types

| Column Type | 适用场景 |
|---|---|
| `DataGridTextColumn` | 文本的显示与编辑。 |
| `DataGridCheckBoxColumn` | 布尔值。配合 `bool?` 可支持三态。 |
| `DataGridTemplateColumn` | 用任意控件自定义显示与编辑。 |

## Template Columns

要自定义单元格渲染，请使用 `DataGridTemplateColumn`：

```xml
<DataGridTemplateColumn Header="Status">
    <DataGridTemplateColumn.CellTemplate>
        <DataTemplate>
            <Border Background="{Binding StatusColor}" CornerRadius="4"
                    Padding="8,2" HorizontalAlignment="Center">
                <TextBlock Text="{Binding Status}" Foreground="White"
                           FontSize="11" />
            </Border>
        </DataTemplate>
    </DataGridTemplateColumn.CellTemplate>
</DataGridTemplateColumn>
```

### 可编辑的模板列 {#editable-template-column}

同时提供 `CellTemplate`（显示）和 `CellEditingTemplate`（编辑）：

```xml
<DataGridTemplateColumn Header="Rating">
    <DataGridTemplateColumn.CellTemplate>
        <DataTemplate>
            <TextBlock Text="{Binding Rating}" HorizontalAlignment="Center" />
        </DataTemplate>
    </DataGridTemplateColumn.CellTemplate>
    <DataGridTemplateColumn.CellEditingTemplate>
        <DataTemplate>
            <NumericUpDown Value="{Binding Rating}" Minimum="0" Maximum="5"
                           FormatString="N0" />
        </DataTemplate>
    </DataGridTemplateColumn.CellEditingTemplate>
</DataGridTemplateColumn>
```

## Selection

### 单选 {#single-selection}

```xml
<DataGrid ItemsSource="{Binding Products}"
          SelectedItem="{Binding SelectedProduct}"
          SelectionMode="Single" />
```

```csharp
[ObservableProperty]
private Product? _selectedProduct;

partial void OnSelectedProductChanged(Product? value)
{
    // React to selection change
}
```

### 多选 {#multiple-selection}

```xml
<DataGrid ItemsSource="{Binding Products}"
          SelectionMode="Extended" />
```

在代码隐藏中访问选中项：

```csharp
var selectedItems = myDataGrid.SelectedItems;
```

## Editing

默认情况下，只要 `IsReadOnly` 为 `false`，DataGrid 就允许编辑。双击单元格或按 F2 进入编辑模式，按 Enter 提交，按 Esc 取消。

```xml
<DataGrid ItemsSource="{Binding Products}" IsReadOnly="False"
          CellEditEnding="OnCellEditEnding" />
```

### 处理编辑事件 {#handling-edit-events}

```csharp
private void OnCellEditEnding(object? sender, DataGridCellEditEndingEventArgs e)
{
    if (e.EditAction == DataGridEditAction.Commit)
    {
        // Validate or process the edit
    }
}
```

## Column Width Modes

| 宽度 | 行为 |
|---|---|
| `Auto` | 按内容自适应大小。 |
| `*` | 平分剩余空间。 |
| `2*` | 占 `*` 列两倍的份额。 |
| `200` | 固定宽度，单位为像素。 |
| `SizeToCells` | 按单元格内容自适应大小。 |
| `SizeToHeader` | 按标题内容自适应大小。 |

```xml
<DataGrid.Columns>
    <DataGridTextColumn Header="Name" Width="2*" Binding="{Binding Name}" />
    <DataGridTextColumn Header="Code" Width="Auto" Binding="{Binding Code}" />
    <DataGridTextColumn Header="Price" Width="*" Binding="{Binding Price}" />
</DataGrid.Columns>
```

## Row Details

在某一行被选中时显示额外内容：

```xml
<DataGrid ItemsSource="{Binding Products}" IsReadOnly="True"
          RowDetailsVisibilityMode="VisibleWhenSelected">
    <DataGrid.RowDetailsTemplate>
        <DataTemplate>
            <Border Background="#F5F5F5" Padding="16" Margin="4">
                <StackPanel Spacing="4">
                    <TextBlock Text="{Binding Description}" TextWrapping="Wrap" />
                    <TextBlock Text="{Binding LastUpdated, StringFormat='Updated: {0:d}'}"
                               Foreground="Gray" FontSize="11" />
                </StackPanel>
            </Border>
        </DataTemplate>
    </DataGrid.RowDetailsTemplate>
    <DataGrid.Columns>
        <DataGridTextColumn Header="Name" Binding="{Binding Name}" Width="*" />
    </DataGrid.Columns>
</DataGrid>
```

## 网格线与交替行 {#grid-lines-and-alternating-rows}

```xml
<DataGrid ItemsSource="{Binding Products}"
          GridLinesVisibility="Horizontal"
          AlternatingRowBackground="#F8F8F8" />
```

| GridLinesVisibility | 说明 |
|---|---|
| `None` | 不显示网格线（默认）。 |
| `Horizontal` | 只显示横线。 |
| `Vertical` | 只显示竖线。 |
| `All` | 横线竖线都显示。 |

## Frozen Columns

横向滚动时让某些列始终可见：

```xml
<DataGrid ItemsSource="{Binding Products}" FrozenColumnCount="1">
    <DataGrid.Columns>
        <DataGridTextColumn Header="ID" Binding="{Binding Id}" Width="60" />
        <!-- This column stays visible while scrolling -->
        <DataGridTextColumn Header="Name" Binding="{Binding Name}" Width="200" />
        <DataGridTextColumn Header="Category" Binding="{Binding Category}" Width="200" />
        <!-- More columns that can scroll horizontally -->
    </DataGrid.Columns>
</DataGrid>
```

## Styling Rows Conditionally

使用 `DataGridRowTheme`，或在代码隐藏中处理 `LoadingRow`：

```csharp
private void OnLoadingRow(object? sender, DataGridRowEventArgs e)
{
    if (e.Row.DataContext is Product product && !product.InStock)
    {
        e.Row.Background = Brushes.MistyRose;
    }
    else
    {
        e.Row.Background = null;
    }
}
```

```xml
<DataGrid ItemsSource="{Binding Products}" LoadingRow="OnLoadingRow" />
```

## 另请参阅 {#see-also}

- [DataGrid 控件参考](/controls/data-display/structured-data/datagrid)：安装配置与属性表。
- [TreeDataGrid](/controls/data-display/structured-data/treedatagrid)：用于展示层级数据。
- [绑定到集合](/docs/data-binding/how-to-bind-to-a-collection)：ObservableCollection 的用法。
- [集合的性能优化](/docs/app-development/performance#collections)：大集合的批量更新与虚拟化。

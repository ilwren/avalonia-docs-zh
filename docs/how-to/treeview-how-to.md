---
id: treeview-how-to
title: "操作指南：使用 TreeView"
description: TreeView 的层级数据绑定、惰性加载、选择处理与自定义。
doc-type: how-to
---

本指南介绍 TreeView 的常见场景：层级数据绑定、惰性加载、选择处理与自定义。

## Basic Hierarchical Binding

用 `HierarchicalDataTemplate` 把 [`TreeView`](/api/avalonia/controls/treeview) 绑定到一棵视图模型对象树：

```csharp
public class FolderItem
{
    public string Name { get; set; } = "";
    public ObservableCollection<FolderItem> Children { get; } = new();
}
```

```xml
<TreeView ItemsSource="{Binding RootFolders}">
    <TreeView.ItemTemplate>
        <TreeDataTemplate ItemsSource="{Binding Children}">
            <TextBlock Text="{Binding Name}" />
        </TreeDataTemplate>
    </TreeView.ItemTemplate>
</TreeView>
```

关键在于 [`TreeDataTemplate`](/api/avalonia/markup/xaml/templates/treedatatemplate)：它的 `ItemsSource` 属性告诉 `TreeView` 去哪里找每个节点的子项。同一个模板会在每一层递归套用。

### 多种节点类型 {#multiple-node-types}

用 `DataTemplateSelector` 的写法配合 `DataType` 来显示不同类型的节点：

```csharp
public class FolderNode
{
    public string Name { get; set; } = "";
    public ObservableCollection<object> Children { get; } = new();
}

public class FileNode
{
    public string Name { get; set; } = "";
    public long Size { get; set; }
}
```

```xml
<TreeView ItemsSource="{Binding RootItems}">
    <TreeView.DataTemplates>
        <TreeDataTemplate DataType="local:FolderNode" ItemsSource="{Binding Children}">
            <StackPanel Orientation="Horizontal" Spacing="4">
                <PathIcon Data="{StaticResource FolderIcon}" />
                <TextBlock Text="{Binding Name}" />
            </StackPanel>
        </TreeDataTemplate>
        <DataTemplate DataType="local:FileNode">
            <StackPanel Orientation="Horizontal" Spacing="4">
                <PathIcon Data="{StaticResource FileIcon}" />
                <TextBlock Text="{Binding Name}" />
                <TextBlock Text="{Binding Size, StringFormat='{}{0:N0} bytes'}"
                           Foreground="Gray" />
            </StackPanel>
        </DataTemplate>
    </TreeView.DataTemplates>
</TreeView>
```

`FileNode` 用的是普通的 `DataTemplate`（没有 `ItemsSource`），因为文件没有子项；`FolderNode` 则用 `TreeDataTemplate` 以支持展开。

## Selection

### 单选 {#single-selection}

绑定 `SelectedItem` 来跟踪选中的节点：

```xml
<TreeView ItemsSource="{Binding Items}"
          SelectedItem="{Binding SelectedNode}">
```

```csharp
[ObservableProperty]
private object? _selectedNode;

partial void OnSelectedNodeChanged(object? value)
{
    if (value is FolderNode folder)
        LoadFolderContents(folder);
}
```

### 多选 {#multiple-selection}

用 `SelectionMode` 启用多选：

```xml
<TreeView ItemsSource="{Binding Items}"
          SelectionMode="Multiple">
```

在代码隐藏中通过 `SelectedItems` 属性访问选中项，或者使用 `SelectionChanged` 事件：

```csharp
private void OnSelectionChanged(object? sender, SelectionChangedEventArgs e)
{
    var tree = (TreeView)sender!;
    var selectedItems = tree.SelectedItems;
    // Process selected items
}
```

## 惰性加载（展开时才加载） {#lazy-loading-load-on-expand}

若树很大、一上来就加载全部子节点代价太高，可以等用户展开节点时再按需加载：

```csharp
public partial class LazyFolderNode : ObservableObject
{
    private bool _isLoaded;

    public string Name { get; }
    public string Path { get; }
    public ObservableCollection<LazyFolderNode> Children { get; } = new();

    // Start with a dummy child so the expand arrow appears
    public LazyFolderNode(string name, string path, bool hasChildren = true)
    {
        Name = name;
        Path = path;
        if (hasChildren)
            Children.Add(new LazyFolderNode("Loading...", "", false));
    }

    [ObservableProperty]
    private bool _isExpanded;

    partial void OnIsExpandedChanged(bool value)
    {
        if (value && !_isLoaded)
        {
            _isLoaded = true;
            LoadChildren();
        }
    }

    private void LoadChildren()
    {
        Children.Clear();
        foreach (var dir in Directory.GetDirectories(Path))
        {
            var name = System.IO.Path.GetFileName(dir);
            Children.Add(new LazyFolderNode(name, dir));
        }
    }
}
```

在 `TreeDataTemplate` 中绑定 `IsExpanded`：

```xml
<TreeView ItemsSource="{Binding RootFolders}">
    <TreeView.Styles>
        <Style Selector="TreeViewItem">
            <Setter Property="IsExpanded" Value="{Binding IsExpanded, Mode=TwoWay}" />
        </Style>
    </TreeView.Styles>
    <TreeView.ItemTemplate>
        <TreeDataTemplate ItemsSource="{Binding Children}">
            <TextBlock Text="{Binding Name}" />
        </TreeDataTemplate>
    </TreeView.ItemTemplate>
</TreeView>
```

`TreeViewItem` 样式把容器上的 `IsExpanded` 绑定到视图模型属性。用户展开节点时，setter 会触发 `OnIsExpandedChanged`，由它把子节点加载进来。

## Async Lazy Loading

若要从数据库或 API 加载子节点：

```csharp
partial void OnIsExpandedChanged(bool value)
{
    if (value && !_isLoaded)
    {
        _isLoaded = true;
        _ = LoadChildrenAsync();
    }
}

private async Task LoadChildrenAsync()
{
    var items = await _service.GetChildrenAsync(Id);

    Children.Clear();
    foreach (var item in items)
        Children.Add(new LazyFolderNode(item));
}
```

由于 `LoadChildrenAsync` 是 `async`，`await` 之后代码会回到 UI 线程，所以更新 `Children` 无需显式调用 dispatcher。

## 用代码展开与折叠 {#expanding-and-collapsing-programmatically}

要展开或折叠所有节点，遍历整棵树即可：

```csharp
private void ExpandAll(IEnumerable<LazyFolderNode> nodes)
{
    foreach (var node in nodes)
    {
        node.IsExpanded = true;
        ExpandAll(node.Children);
    }
}

private void CollapseAll(IEnumerable<LazyFolderNode> nodes)
{
    foreach (var node in nodes)
    {
        node.IsExpanded = false;
        CollapseAll(node.Children);
    }
}
```

## 搜索与筛选 {#search-and-filter}

筛选树的办法是把不匹配搜索词的节点藏起来。由于 `TreeView` 没有内置筛选，得从源数据重新构建出可见的那棵树：

```csharp
[ObservableProperty]
private string _searchText = "";

partial void OnSearchTextChanged(string value)
{
    FilteredItems.Clear();
    foreach (var root in _allItems)
    {
        var filtered = FilterNode(root, value);
        if (filtered is not null)
            FilteredItems.Add(filtered);
    }
}

private FolderNode? FilterNode(FolderNode node, string search)
{
    // Check if this node matches
    var matches = node.Name.Contains(search, StringComparison.OrdinalIgnoreCase);

    // Recursively filter children
    var filteredChildren = node.Children
        .Select(c => FilterNode(c, search))
        .Where(c => c is not null)
        .ToList();

    // Include this node if it matches or has matching children
    if (matches || filteredChildren.Count > 0)
    {
        var result = new FolderNode { Name = node.Name };
        foreach (var child in filteredChildren)
            result.Children.Add(child!);
        return result;
    }

    return null;
}
```

## TreeView 中的拖放 {#drag-and-drop-in-treeview}

启用拖放来重新排列树节点：

```xml
<TreeView ItemsSource="{Binding Items}"
          DragDrop.AllowDrop="True">
    <TreeView.Styles>
        <Style Selector="TreeViewItem">
            <Setter Property="DragDrop.AllowDrop" Value="True" />
        </Style>
    </TreeView.Styles>
</TreeView>
```

在代码隐藏中处理拖拽事件，或者改用行为（behavior）。完整 API 请参阅[拖放](/docs/input-interaction/drag-and-drop)。

## Styling TreeViewItem

自定义树节点的外观：

```xml
<TreeView.Styles>
    <!-- Change the expand/collapse icon -->
    <Style Selector="TreeViewItem:empty /template/ ToggleButton#PART_ExpandCollapseChevron">
        <Setter Property="IsVisible" Value="False" />
    </Style>

    <!-- Highlight selected items -->
    <Style Selector="TreeViewItem:selected /template/ ContentPresenter#PART_HeaderPresenter">
        <Setter Property="Background" Value="{DynamicResource SystemAccentColor}" />
        <Setter Property="Foreground" Value="White" />
    </Style>

    <!-- Add indentation -->
    <Style Selector="TreeViewItem">
        <Setter Property="Padding" Value="4" />
    </Style>
</TreeView.Styles>
```

## See Also

- [TreeView 控件参考](/controls/data-display/structured-data/treeview)：属性表与基础示例。
- [数据模板](/docs/data-templates/introduction-to-data-templates)：数据模板的运作原理。
- [拖放](/docs/input-interaction/drag-and-drop)：拖放支持。
- [集合视图](/docs/data-binding/collection-views)：集合的筛选与排序。

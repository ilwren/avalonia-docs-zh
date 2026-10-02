---
id: collection-views
title: 集合的排序、筛选与分组
description: 借助 DataGridCollectionView 和 DynamicData，对绑定的集合做排序、筛选和分组。
doc-type: how-to
---

Avalonia 没有内置 WPF 那样的 `ICollectionView` 等价物。排序、筛选和分组通常在视图模型里做完，再绑定给控件。这样界面层保持简单，逻辑也更容易测试。

## 筛选集合 {#filtering-a-collection}

最常见的做法是用一个随筛选条件变化的派生集合。可以用 LINQ，也可以用类似 `CollectionViewSource` 的包装：

### 用 ObservableCollection 手工筛选 {#manual-filtering-with-observablecollection}

```csharp
public partial class MainViewModel : ObservableObject
{
    private readonly ObservableCollection<Person> _allPeople;

    [ObservableProperty]
    private string _searchText = "";

    public ObservableCollection<Person> FilteredPeople { get; } = new();

    public MainViewModel()
    {
        _allPeople = new ObservableCollection<Person>
        {
            new("Alice", 30),
            new("Bob", 25),
            new("Charlie", 35),
        };

        ApplyFilter();
    }

    partial void OnSearchTextChanged(string value)
    {
        ApplyFilter();
    }

    private void ApplyFilter()
    {
        FilteredPeople.Clear();
        var filtered = string.IsNullOrEmpty(SearchText)
            ? _allPeople
            : _allPeople.Where(p =>
                p.Name.Contains(SearchText, StringComparison.OrdinalIgnoreCase));

        foreach (var person in filtered)
            FilteredPeople.Add(person);
    }
}
```

```xml
<StackPanel Spacing="8">
    <TextBox Text="{Binding SearchText}" PlaceholderText="Search..." />
    <ListBox ItemsSource="{Binding FilteredPeople}">
        <ListBox.ItemTemplate>
            <DataTemplate>
                <TextBlock Text="{Binding Name}" />
            </DataTemplate>
        </ListBox.ItemTemplate>
    </ListBox>
</StackPanel>
```

### 用 DynamicData（复杂场景推荐） {#using-dynamicdata-recommended-for-complex-scenarios}

[DynamicData](https://github.com/reactivemarbles/DynamicData) 这个库提供了响应式的集合变换能力，与 Avalonia 的响应式模型配合得相当好：

```csharp
using DynamicData;
using DynamicData.Binding;

public class MainViewModel : ObservableObject
{
    private readonly SourceList<Person> _source = new();
    private readonly ReadOnlyObservableCollection<Person> _filtered;

    [ObservableProperty]
    private string _searchText = "";

    public ReadOnlyObservableCollection<Person> FilteredPeople => _filtered;

    public MainViewModel()
    {
        _source.AddRange(new[]
        {
            new Person("Alice", 30),
            new Person("Bob", 25),
            new Person("Charlie", 35),
        });

        var filterPredicate = this.WhenPropertyChanged(x => x.SearchText)
            .Select(x => CreateFilter(x.Value));

        _source.Connect()
            .Filter(filterPredicate)
            .Sort(SortExpressionComparer<Person>.Ascending(p => p.Name))
            .Bind(out _filtered)
            .Subscribe();
    }

    private static Func<Person, bool> CreateFilter(string? searchText)
    {
        if (string.IsNullOrEmpty(searchText))
            return _ => true;

        return person =>
            person.Name.Contains(searchText, StringComparison.OrdinalIgnoreCase);
    }
}
```

当有项被增删、或筛选文本发生变化时，DynamicData 会自动更新 `FilteredPeople`。

## 集合排序 {#sorting-a-collection}

### 简单排序 {#simple-sorting}

绑定之前先把源集合排好序：

```csharp
public ObservableCollection<Person> People { get; }

public MainViewModel()
{
    var sorted = _rawData.OrderBy(p => p.Name);
    People = new ObservableCollection<Person>(sorted);
}
```

### 动态排序 {#dynamic-sorting}

用一个属性来控制排序方式：

```csharp
[ObservableProperty]
private string _sortProperty = "Name";

[ObservableProperty]
private bool _sortDescending = false;

partial void OnSortPropertyChanged(string value) => ApplySort();
partial void OnSortDescendingChanged(bool value) => ApplySort();

private void ApplySort()
{
    var sorted = SortProperty switch
    {
        "Name" => SortDescending
            ? _allPeople.OrderByDescending(p => p.Name)
            : _allPeople.OrderBy(p => p.Name),
        "Age" => SortDescending
            ? _allPeople.OrderByDescending(p => p.Age)
            : _allPeople.OrderBy(p => p.Age),
        _ => _allPeople.AsEnumerable()
    };

    People.Clear();
    foreach (var person in sorted)
        People.Add(person);
}
```

```xml
<StackPanel Spacing="8">
    <StackPanel Orientation="Horizontal" Spacing="8">
        <ComboBox SelectedItem="{Binding SortProperty}">
            <ComboBoxItem Content="Name" />
            <ComboBoxItem Content="Age" />
        </ComboBox>
        <ToggleButton Content="Descending" IsChecked="{Binding SortDescending}" />
    </StackPanel>
    <ListBox ItemsSource="{Binding People}" />
</StackPanel>
```

### 用 DynamicData 实现 {#with-dynamicdata}

```csharp
_source.Connect()
    .Sort(SortExpressionComparer<Person>.Ascending(p => p.Name))
    .Bind(out _sorted)
    .Subscribe();
```

## Grouping

Avalonia 的 `ItemsControl` 不像 WPF 的 `CollectionViewSource` 那样内置分组支持。要展示分组数据，就把各个分组摊平成一个集合，中间穿插分组标题。

:::tip
`DataGrid` 控件通过 `DataGridCollectionView` 内置了分组支持，详见 [DataGrid 分组指南](/docs/how-to/datagrid-how-to#grouping)。
:::

### 用带标题的扁平列表 {#using-a-flat-list-with-headers}

创建一个既能表示标题、也能表示数据项的视图模型：

```csharp
public abstract class ListItem { }

public class GroupHeader : ListItem
{
    public string Title { get; }
    public GroupHeader(string title) => Title = title;
}

public class PersonItem : ListItem
{
    public Person Person { get; }
    public PersonItem(Person person) => Person = person;
}
```

构建分组后的列表：

```csharp
public ObservableCollection<ListItem> GroupedPeople { get; } = new();

private void BuildGroups()
{
    GroupedPeople.Clear();
    var groups = _allPeople.GroupBy(p => p.Age / 10 * 10); // Group by decade

    foreach (var group in groups.OrderBy(g => g.Key))
    {
        GroupedPeople.Add(new GroupHeader($"{group.Key}s"));
        foreach (var person in group.OrderBy(p => p.Name))
            GroupedPeople.Add(new PersonItem(person));
    }
}
```

用 `DataTemplateSelector`（通过 `DataTemplate` 配合 `DataType`）把标题和数据项渲染成不同样式：

```xml
<ListBox ItemsSource="{Binding GroupedPeople}">
    <ListBox.DataTemplates>
        <DataTemplate DataType="local:GroupHeader">
            <TextBlock Text="{Binding Title}"
                       FontWeight="Bold" FontSize="14"
                       Margin="0,8,0,4" />
        </DataTemplate>
        <DataTemplate DataType="local:PersonItem">
            <StackPanel Orientation="Horizontal" Spacing="8" Margin="12,0,0,0">
                <TextBlock Text="{Binding Person.Name}" />
                <TextBlock Text="{Binding Person.Age}" Foreground="Gray" />
            </StackPanel>
        </DataTemplate>
    </ListBox.DataTemplates>
</ListBox>
```

### 用 DynamicData 的 GroupOn {#with-dynamicdata-groupon}

```csharp
_source.Connect()
    .GroupOn(p => p.Department)
    .Transform(group => new DepartmentGroup(group.Key, group.List))
    .Bind(out _groups)
    .Subscribe();
```

## 实践建议 {#best-practices}

- 把筛选、排序、分组的逻辑放在视图模型里，别写进代码隐藏。
- 集合较大时，用 DynamicData 做高效的响应式更新，不要每次变化都重建整个集合。
- 排序或筛选条件变化时，尽量避免清空后重新添加。DynamicData 会自动处理增量更新。
- 对外暴露的属性请用 `ReadOnlyObservableCollection<T>`，防止被外部改动。
- 对于每敲一个键就触发筛选的搜索框，考虑给输入加上防抖（例如用 `Throttle`）。

## 另请参阅 {#see-also}

- [如何绑定到集合](/docs/data-binding/how-to-bind-to-a-collection)：集合绑定的基本写法。
- [数据模板](/docs/data-templates/introduction-to-data-templates)：控制数据项的呈现方式。
- [INotifyPropertyChanged](/docs/data-binding/inotifypropertychanged)：视图模型的变更通知。

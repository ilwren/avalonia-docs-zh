---
id: filtering
title: 筛选
description: 了解如何用谓词函数筛选 Avalonia TreeDataGrid 控件中的行，包括多条件筛选、枚举筛选、空值安全筛选和层级筛选等写法。
doc-type: reference
tags:
  - avalonia pro
  - avalonia enterprise
---

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

筛选让你只显示 `TreeDataGrid` 中符合特定条件的行。`FlatTreeDataGridSource` 和 `HierarchicalTreeDataGridSource` 都通过谓词函数支持筛选。

:::note
筛选必须采用代码隐藏中的 `Source` 写法，目前没有对应的 XAML 做法。你需要在视图模型里创建一个 `FlatTreeDataGridSource` 或 `HierarchicalTreeDataGridSource`。
:::

## 启用筛选 {#enabling-filtering}

在 `FlatTreeDataGridSource` 或 `HierarchicalTreeDataGridSource` 上调用 `Filter` 方法并传入一个谓词函数，即可启用筛选。该谓词接收每个模型项，若该项应当可见则返回 `true`，应当隐藏则返回 `false`。

### 基本的字符串筛选 {#basic-string-filtering}

若要按 `_filterString` 中保存的值来筛选模型的字符串属性 `Name`：

```csharp
Source.Filter(x => x.Name.Contains(_filterString, StringComparison.CurrentCultureIgnoreCase));
```

### 多条件筛选 {#multiple-criteria-filtering}

你可以在筛选谓词中组合多个条件：

```csharp
// Filter by name AND minimum age
Source.Filter(x =>
    x.Name.Contains(_filterString, StringComparison.CurrentCultureIgnoreCase) &&
    x.Age >= _minimumAge);

// Filter by first name OR last name OR email
Source.Filter(x =>
    x.FirstName.Contains(_searchText, StringComparison.CurrentCultureIgnoreCase) ||
    x.LastName.Contains(_searchText, StringComparison.CurrentCultureIgnoreCase) ||
    x.Email.Contains(_searchText, StringComparison.CurrentCultureIgnoreCase));
```

### 枚举与分类筛选 {#enum-and-category-filtering}

当模型带有枚举或分类属性时，你可以按选中的取值来筛选：

```csharp
// Filter by a selected department enum
Source.Filter(x => _selectedDepartment == null || x.Department == _selectedDepartment);
```

### 空值安全的筛选 {#null-safe-filtering}

如果用于筛选的属性可能为 `null`，请在谓词中先挡住 `NullReferenceException`：

```csharp
Source.Filter(x =>
    (x.Name?.Contains(_filterString, StringComparison.CurrentCultureIgnoreCase) ?? false) ||
    (x.Email?.Contains(_filterString, StringComparison.CurrentCultureIgnoreCase) ?? false));
```

### 复杂筛选 {#complex-filtering}

筛选谓词里可以写任意 C# 表达式，包括 LINQ 方法和辅助函数：

```csharp
// Filter using LINQ methods
Source.Filter(x => x.Tags.Any(tag => tag.Contains(_filterText)));

// Filter using a helper method
Source.Filter(x => IsMatchingCriteria(x));

private bool IsMatchingCriteria(Person person)
{
    if (string.IsNullOrWhiteSpace(_filterText))
        return true;

    return person.Name.Contains(_filterText, StringComparison.CurrentCultureIgnoreCase) ||
           person.Department.Contains(_filterText, StringComparison.CurrentCultureIgnoreCase);
}
```

## 更新筛选 {#updating-the-filter}

当筛选谓词依赖外部变量时（比如上面例子中的 `_filterString`），这些变量一变，你就得刷新筛选。调用 `RefreshFilter` 即可对每一项重新求值：

```csharp
private string _filterString = string.Empty;

public string FilterString
{
    get => _filterString;
    set
    {
        _filterString = value;
        Source.RefreshFilter();
    }
}
```

:::info
调用 `Filter` 替换谓词本身时，不必再调用 `RefreshFilter`。只有当现有谓词所依赖的外部变量发生变化时，才需要调用它。
:::

## 清除筛选 {#clearing-the-filter}

若要取消筛选、重新显示全部条目，给 `Filter` 方法传 `null` 即可：

```csharp
Source.Filter(null);
```

用户清空搜索框或重置筛选控件时，这一招很有用。

## 层级数据的筛选 {#hierarchical-data-filtering}

用 `HierarchicalTreeDataGridSource` 筛选层级数据时，谓词会对层级中每一层的每一项各自独立求值。每一项是显示还是隐藏，只取决于它自己是否匹配。控件不会因为某项的子项匹配就自动显示该父项，反之亦然。

:::warning
筛选庞大的层级树开销不小，因为每个节点都得走一遍。若在意性能，可以考虑把筛选状态做进数据模型里，这样就能整棵子树一起跳过。
:::

### 让父项保持可见 {#keeping-parent-items-visible}

如果你希望只要有子项匹配、父项就一直可见，这段逻辑得自己实现。一种做法是预先算出一组匹配项的 ID（连同其祖先的 ID），再在谓词里判断是否在这组 ID 之中：

```csharp
var matchingIds = new HashSet<int>();

void CollectMatches(IEnumerable<TreeNode> nodes)
{
    foreach (var node in nodes)
    {
        if (node.Name.Contains(_filterText, StringComparison.CurrentCultureIgnoreCase))
        {
            // Add the node and all its ancestors
            var current = node;
            while (current != null)
            {
                matchingIds.Add(current.Id);
                current = current.Parent;
            }
        }

        CollectMatches(node.Children);
    }
}

CollectMatches(_rootNodes);
Source.Filter(x => matchingIds.Contains(x.Id));
```

## 性能考量 {#performance-considerations}

筛选操作在 UI 线程上执行，并会对数据源中的每一项重新求值。面对大数据集，请记住以下几点：

- **给用户输入加节流。**当筛选由 [`TextBox`](/api/avalonia/controls/textbox) 驱动时，请用 `Observable.Throttle` 或延时计时器，别让谓词每敲一个键就跑一遍。
- **让谓词跑得快。**谓词内部要避免分配内存、使用正则表达式或访问数据库。
- **预先算好开销大的值。**把可检索的文本存进一个专门的属性，这样谓词只需做一次简单的字符串比较。
- **超大集合请在上游筛选。**如果数据集有几万行，不妨先筛好底层集合，再绑定到网格上。

### 节流筛选示例 {#throttled-filtering-example}

你可以用 Reactive Extensions 为来自 `TextBox` 的筛选更新加节流：

```csharp
this.WhenAnyValue(x => x.SearchText)
    .Throttle(TimeSpan.FromMilliseconds(300))
    .ObserveOn(RxApp.MainThreadScheduler)
    .Subscribe(_ => ApplyFilter());
```

## 完整示例 {#complete-example}

下面这个例子把一个搜索用的 `TextBox` 接到了 `FlatTreeDataGridSource<Person>` 的筛选上。

**ViewModel:**

```csharp
public class PersonListViewModel : ViewModelBase
{
    private readonly ObservableCollection<Person> _allPeople;
    private string _searchText = string.Empty;

    public FlatTreeDataGridSource<Person> Source { get; }

    public string SearchText
    {
        get => _searchText;
        set
        {
            if (_searchText != value)
            {
                _searchText = value;
                OnPropertyChanged();
                ApplyFilter();
            }
        }
    }

    public PersonListViewModel()
    {
        _allPeople = new ObservableCollection<Person>
        {
            new Person { Name = "John Doe", Age = 30, Department = "IT" },
            new Person { Name = "Jane Smith", Age = 25, Department = "HR" },
            new Person { Name = "Bob Johnson", Age = 35, Department = "IT" },
        };

        Source = new FlatTreeDataGridSource<Person>(_allPeople)
            .WithTextColumn(x => x.Name)
            .WithTextColumn(x => x.Age)
            .WithTextColumn(x => x.Department);
    }

    private void ApplyFilter()
    {
        if (string.IsNullOrWhiteSpace(_searchText))
        {
            Source.Filter(null);
        }
        else
        {
            Source.Filter(x =>
                x.Name.Contains(_searchText, StringComparison.CurrentCultureIgnoreCase) ||
                x.Department.Contains(_searchText, StringComparison.CurrentCultureIgnoreCase));
        }
    }
}
```

**View:**

```xml
<StackPanel>
    <TextBox Text="{Binding SearchText}"
             PlaceholderText="Search..."
             Margin="0,0,0,10" />
    <TreeDataGrid Source="{Binding Source}"
                  Height="400" />
</StackPanel>
```

## 另请参阅 {#see-also}

- [TreeDataGrid 总览](/controls/data-display/structured-data/treedatagrid/)
- [列类型](/controls/data-display/structured-data/treedatagrid/column-types)
- [Sorting](/controls/data-display/structured-data/treedatagrid/sorting)
- [选择模式](/controls/data-display/structured-data/treedatagrid/selection-modes)
- [展开与折叠操作](/controls/data-display/structured-data/treedatagrid/expand-and-collapse)

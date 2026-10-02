---
id: how-to-bind-to-a-collection
title: 如何绑定到集合
description: 把 ObservableCollection 绑定到列表控件，让界面在增删或修改元素时自动刷新。
doc-type: how-to
---

当应用需要展示一份动态的列表时，就把集合属性绑定到 [`ListBox`](/api/avalonia/controls/listbox)、[`ItemsControl`](/api/avalonia/controls/itemscontrol) 或 `ComboBox` 这类列表控件上。借助 `ObservableCollection<T>`，无论你增删元素还是调整顺序，界面都会保持同步。本文带你走一遍 Avalonia 中集合绑定的常见场景。

## 为什么要用 `ObservableCollection<T>` {#why-use-observablecollection}

普通的 `List<T>` 在内容变化时不会通知界面。运行时往 `List<T>` 里加一个元素，控件是不会更新的。`ObservableCollection<T>` 实现了 `INotifyCollectionChanged`，会引发 Avalonia 监听的那些事件，绑定的控件因此能自动刷新。

以下情况请使用 `ObservableCollection<T>`：

- 初次加载之后还会增删元素。
- 你希望界面自动反映变化，而不用手动重新绑定。

如果集合是静态的（加载一次之后不再改动），用普通的 `List<T>` 或数组就够了。

## 绑定到简单的 `ObservableCollection` {#bind-to-a-simple-observablecollection}

先从绑定到 `ListBox` 的 `ObservableCollection<string>` 开始。

在视图模型中定义集合：

```csharp
public class MainViewModel : ObservableObject
{
    private ObservableCollection<string> _items;

    public ObservableCollection<string> Items
    {
        get => _items;
        set => SetProperty(ref _items, value);
    }

    public MainViewModel()
    {
        Items = new ObservableCollection<string> { "Item 1", "Item 2", "Item 3" };
    }
}
```

在 AXAML 中把集合绑定到 `ListBox`：

```xml
<ListBox ItemsSource="{Binding Items}" />
```

当你在视图模型中调用 `Items.Add("Item 4")` 时，`ListBox` 会立刻显示出新增的那一项。

## 绑定到由复杂对象组成的集合 {#bind-to-a-collection-of-complex-objects}

如果集合里装的是带多个属性的对象，就用 `DataTemplate` 控制每一项的外观。另外，要让单个元素的属性变化也能反映到界面上，元素类自身同样得实现变更通知。

定义一个继承自 `ObservableObject` 的 `Person` 类：

```csharp
public class Person : ObservableObject
{
    private string _name;
    private int _age;

    public string Name
    {
        get => _name;
        set => SetProperty(ref _name, value);
    }

    public int Age
    {
        get => _age;
        set => SetProperty(ref _age, value);
    }
}
```

在视图模型中暴露一个 `ObservableCollection<Person>`：

```csharp
public class MainViewModel : ObservableObject
{
    private ObservableCollection<Person> _people;

    public ObservableCollection<Person> People
    {
        get => _people;
        set => SetProperty(ref _people, value);
    }

    public MainViewModel()
    {
        People = new ObservableCollection<Person>
        {
            new Person { Name = "John Doe", Age = 30 },
            new Person { Name = "Jane Doe", Age = 28 }
        };
    }
}
```

把集合绑定到带 `DataTemplate` 的 `ListBox`：

```xml
<ListBox ItemsSource="{Binding People}">
    <ListBox.ItemTemplate>
        <DataTemplate>
            <StackPanel Orientation="Horizontal">
                <TextBlock Text="{Binding Name}" Margin="0,0,10,0" />
                <TextBlock Text="{Binding Age}" />
            </StackPanel>
        </DataTemplate>
    </ListBox.ItemTemplate>
</ListBox>
```

每个 `Person` 的 `Name` 和 `Age` 会并排显示出来。由于 `Person` 继承自 `ObservableObject`，在代码中修改某人的 `Name` 或 `Age`，对应的 `ListBox` 行会自动更新，不需要额外写任何代码。

## 在运行时增删元素 {#add-and-remove-items-at-runtime}

一种常见的做法是把集合绑定和命令搭配起来，让用户自己增删条目：

```csharp
public class MainViewModel : ObservableObject
{
    public ObservableCollection<string> Items { get; } = new();

    public ICommand AddItemCommand { get; }
    public ICommand RemoveItemCommand { get; }

    public MainViewModel()
    {
        Items.Add("First item");

        AddItemCommand = new RelayCommand(() =>
        {
            Items.Add($"Item {Items.Count + 1}");
        });

        RemoveItemCommand = new RelayCommand(() =>
        {
            if (Items.Count > 0)
                Items.RemoveAt(Items.Count - 1);
        },
        () => Items.Count > 0);
    }
}
```

```xml
<DockPanel>
    <StackPanel DockPanel.Dock="Top" Orientation="Horizontal" Spacing="8" Margin="0,0,0,8">
        <Button Content="Add" Command="{Binding AddItemCommand}" />
        <Button Content="Remove" Command="{Binding RemoveItemCommand}" />
    </StackPanel>
    <ListBox ItemsSource="{Binding Items}" />
</DockPanel>
```

## 不需要选中行为时改用 `ItemsControl` {#use-itemscontrol-for-non-selectable-lists}

如果你用不上选中功能，就用 `ItemsControl` 代替 `ListBox`。它只负责渲染每一项，不带选中高亮，也没有键盘导航：

```xml
<ItemsControl ItemsSource="{Binding People}">
    <ItemsControl.ItemTemplate>
        <DataTemplate>
            <Border Padding="8" Margin="0,0,0,4" Background="#f0f0f0" CornerRadius="4">
                <TextBlock Text="{Binding Name}" />
            </Border>
        </DataTemplate>
    </ItemsControl.ItemTemplate>
</ItemsControl>
```

## 常见问题 {#common-pitfalls}

| 问题 | 原因 | 解决办法 |
|---|---|---|
| 新增元素后界面不刷新 | 用的是 `List<T>` 而不是 `ObservableCollection<T>` | 改用 `ObservableCollection<T>` |
| 元素的某个属性变了，界面却不刷新 | 元素类没有实现 `INotifyPropertyChanged` | 让元素类继承 `ObservableObject`，或自行实现 `INotifyPropertyChanged` |
| 整体替换集合后界面不刷新 | 持有集合的那个属性缺少变更通知 | 给持有集合的属性加上 `SetProperty`（或 `[ObservableProperty]` 特性） |

## 另请参阅 {#see-also}

- [集合视图](/docs/data-binding/collection-views)：对绑定的集合做排序、筛选和分组。
- [主从绑定](/docs/data-binding/master-detail)：显示列表中选中项的详细信息。
- [数据模板](/docs/data-templates/introduction-to-data-templates)：控制数据项的呈现方式。
- [INotifyPropertyChanged](/docs/data-binding/inotifypropertychanged)：视图模型的变更通知。
- [绑定到命令](/docs/data-binding/binding-to-commands)：把按钮等操作接起来。










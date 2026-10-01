---
id: master-detail
title: 主从绑定
description: 实现主从（master-detail）模式：选中某一项时，在绑定的视图中显示它的详细信息。
doc-type: how-to
---

主从模式在一侧显示条目列表（「主」），在另一侧显示当前选中项的详情。邮件客户端、设置界面、文件管理器等等，到处都能见到这种模式。借助数据绑定和 `DataContext` 的继承机制，在 Avalonia 中搭起这套结构相当省事。

## 基本的主从结构 {#basic-master-detail}

把 [`ListBox`](/api/avalonia/controls/listbox) 绑定到一个集合，并在相邻的面板中显示选中项的各个属性。详情面板把自己的 `DataContext` 设为 `SelectedPerson` 属性，这样面板内部的每一处绑定都相对选中对象来解析：

```xml
<Grid ColumnDefinitions="250,*">
    <!-- Master: list of items -->
    <ListBox Grid.Column="0"
             ItemsSource="{Binding People}"
             SelectedItem="{Binding SelectedPerson}">
        <ListBox.ItemTemplate>
            <DataTemplate>
                <TextBlock Text="{Binding Name}" />
            </DataTemplate>
        </ListBox.ItemTemplate>
    </ListBox>

    <!-- Detail: selected item properties -->
    <StackPanel Grid.Column="1" Margin="16"
                DataContext="{Binding SelectedPerson}"
                IsVisible="{Binding $parent[Grid].((vm:MainViewModel)DataContext).SelectedPerson,
                            Converter={x:Static ObjectConverters.IsNotNull}}">
        <TextBlock Text="{Binding Name}" FontSize="20" FontWeight="Bold" />
        <TextBlock Text="{Binding Email}" Margin="0,4,0,0" />
        <TextBlock Text="{Binding Department}" Margin="0,4,0,0" />
    </StackPanel>
</Grid>
```

视图模型：

```csharp
public partial class MainViewModel : ObservableObject
{
    public ObservableCollection<Person> People { get; } = new()
    {
        new Person("Alice", "alice@example.com", "Engineering"),
        new Person("Bob", "bob@example.com", "Design"),
        new Person("Charlie", "charlie@example.com", "Marketing"),
    };

    [ObservableProperty]
    private Person? _selectedPerson;
}

public record Person(string Name, string Email, string Department);
```

:::tip
一旦给详情面板设置了 `DataContext`，面板内部的所有绑定都相对选中项来解析。这让 XAML 简洁不少 —— 不必在每个属性路径前都重复写一遍 `SelectedPerson.`。
:::

:::note
详情面板上的 `IsVisible` 绑定会沿视觉树向上找到父级 `Grid`，再把它的 `DataContext` 转换为你的视图模型类型。这一步是必要的：没有选中项时，详情面板自身的 `DataContext` 为 `null`，直接写本地的 `IsVisible` 绑定是求不出正确结果的。
:::

## 可编辑的详情视图 {#editable-detail-view}

要在详情面板中做双向绑定，请使用 `TwoWay` 模式，并确保模型实现了 `INotifyPropertyChanged`。若你用的是 MVVM Toolkit，`[ObservableProperty]` 特性会自动生成所需的通知逻辑：

```csharp
public partial class Person : ObservableObject
{
    [ObservableProperty]
    private string _name;

    [ObservableProperty]
    private string _email;

    [ObservableProperty]
    private string _department;

    public Person(string name, string email, string department)
    {
        _name = name;
        _email = email;
        _department = department;
    }
}
```

```xml
<StackPanel Grid.Column="1" Margin="16"
            DataContext="{Binding SelectedPerson}">
    <TextBox Text="{Binding Name}" PlaceholderText="Name" />
    <TextBox Text="{Binding Email}" PlaceholderText="Email" Margin="0,8,0,0" />
    <TextBox Text="{Binding Department}" PlaceholderText="Department" Margin="0,8,0,0" />
</StackPanel>
```

由于两侧面板引用的是同一个对象，文本框里的改动会自动反映到主列表的条目上。如果模型用的是 `record` 类型（就像前面的基础示例那样），遇到可编辑场景就得换成一个会引发 `PropertyChanged` 通知的类。

:::warning
如果 `ListBox.ItemTemplate` 中显示的正是你正在编辑的那个属性（比如 `Name`），那么只有当模型引发 `PropertyChanged` 时，列表项才会实时更新。普通的 POCO 或 C# record 是不会触发主列表刷新的。
:::

## 为详情单独准备一个视图模型 {#master-detail-with-a-separate-detail-view-model}

详情视图较复杂时，可以为它专门写一个视图模型，并在选中项变化时更新。需要加载额外数据、执行校验，或管理详情专属命令时，这种做法尤其合适：

```csharp
public partial class MainViewModel : ObservableObject
{
    public ObservableCollection<Person> People { get; } = new();

    [ObservableProperty]
    private Person? _selectedPerson;

    [ObservableProperty]
    private PersonDetailViewModel? _detail;

    partial void OnSelectedPersonChanged(Person? value)
    {
        Detail = value is not null ? new PersonDetailViewModel(value) : null;
    }
}

public partial class PersonDetailViewModel : ObservableObject
{
    private readonly Person _person;

    public PersonDetailViewModel(Person person)
    {
        _person = person;
        LoadDetails();
    }

    [ObservableProperty]
    private string _biography = "";

    [ObservableProperty]
    private ObservableCollection<string> _recentActivity = new();

    private void LoadDetails()
    {
        // Load additional data for the selected person.
    }
}
```

```xml
<ContentControl Grid.Column="1" Content="{Binding Detail}">
    <ContentControl.DataTemplates>
        <DataTemplate DataType="vm:PersonDetailViewModel">
            <StackPanel Margin="16" Spacing="8">
                <TextBlock Text="{Binding Biography}" TextWrapping="Wrap" />
                <ItemsControl ItemsSource="{Binding RecentActivity}" />
            </StackPanel>
        </DataTemplate>
    </ContentControl.DataTemplates>
</ContentControl>
```

:::tip
如果详情数据是异步加载的，不妨在构造函数里先填上占位值（或显示加载指示器），等异步操作完成后再更新属性。这样可以避免加载期间内容一闪而过的空白。
:::

## 带导航的主从结构 {#master-detail-with-navigation}

在移动端或空间紧凑的布局中，详情不是并排显示，而是直接把主列表替换掉。用一个可见性开关配合 `TransitioningContentControl` 就能实现带动画的切换：

```csharp
public partial class MainViewModel : ObservableObject
{
    public ObservableCollection<Person> People { get; } = new();

    [ObservableProperty]
    private Person? _selectedPerson;

    [ObservableProperty]
    private bool _showDetail;

    partial void OnSelectedPersonChanged(Person? value)
    {
        ShowDetail = value is not null;
    }

    [RelayCommand]
    private void GoBack()
    {
        SelectedPerson = null;
        ShowDetail = false;
    }
}
```

```xml
<Panel>
    <!-- Master list -->
    <ListBox ItemsSource="{Binding People}"
             SelectedItem="{Binding SelectedPerson}"
             IsVisible="{Binding !ShowDetail}" />

    <!-- Detail view -->
    <StackPanel IsVisible="{Binding ShowDetail}" Margin="16">
        <Button Content="Back" Command="{Binding GoBackCommand}" />
        <TextBlock Text="{Binding SelectedPerson.Name}" FontSize="20" />
    </StackPanel>
</Panel>
```

:::note
如果希望用户返回时主列表仍停留在原来的滚动位置，请让 `ListBox` 留在视觉树中（用 `IsVisible` 控制），而不要用 `ContentControl` 把它整个换掉。隐藏的控件会保留自身状态。
:::

## 嵌套的主从结构 {#nested-master-detail}

对于「分类下面挂条目」这类层级数据，可以把多级主从串联起来。每一列都把自己的 `ItemsSource` 绑定到上一级的选中项：

```xml
<Grid ColumnDefinitions="200,200,*">
    <!-- Level 1: Categories -->
    <ListBox Grid.Column="0"
             ItemsSource="{Binding Categories}"
             SelectedItem="{Binding SelectedCategory}">
        <ListBox.ItemTemplate>
            <DataTemplate>
                <TextBlock Text="{Binding Name}" />
            </DataTemplate>
        </ListBox.ItemTemplate>
    </ListBox>

    <!-- Level 2: Items in category -->
    <ListBox Grid.Column="1"
             ItemsSource="{Binding SelectedCategory.Items}"
             SelectedItem="{Binding SelectedItem}">
        <ListBox.ItemTemplate>
            <DataTemplate>
                <TextBlock Text="{Binding Title}" />
            </DataTemplate>
        </ListBox.ItemTemplate>
    </ListBox>

    <!-- Level 3: Item details -->
    <StackPanel Grid.Column="2" Margin="16"
                DataContext="{Binding SelectedItem}">
        <TextBlock Text="{Binding Title}" FontSize="20" FontWeight="Bold" />
        <TextBlock Text="{Binding Description}" TextWrapping="Wrap" />
    </StackPanel>
</Grid>
```

:::warning
用户选中新分类时，第二级的 `ListBox` 会拿到新的 `ItemsSource` 并丢失原有选中项。如果 `SelectedCategory` 变化时你没有在视图模型中显式清空 `SelectedItem`，界面上可能还留着上一个分类的陈旧详情。解决办法是在 `OnSelectedCategoryChanged` 中把 `SelectedItem` 重置为 `null`。
:::

## 未选中时的占位内容 {#placeholder-for-empty-selection}

没有选中任何条目时显示一段提示文字或一张图，免得详情区域一片空白：

```xml
<Panel Grid.Column="1">
    <!-- Shown when nothing is selected -->
    <TextBlock Text="Select an item to view details"
               HorizontalAlignment="Center"
               VerticalAlignment="Center"
               Foreground="Gray"
               IsVisible="{Binding SelectedPerson,
                           Converter={x:Static ObjectConverters.IsNull}}" />

    <!-- Detail panel -->
    <StackPanel DataContext="{Binding SelectedPerson}"
                IsVisible="{Binding $parent[Panel].((vm:MainViewModel)DataContext).SelectedPerson,
                            Converter={x:Static ObjectConverters.IsNotNull}}">
        <TextBlock Text="{Binding Name}" FontSize="20" />
    </StackPanel>
</Panel>
```

你可以把占位用的 `TextBlock` 换成图片、图标，或任何契合应用设计风格的自定义布局。

## 另请参阅 {#see-also}

- [绑定到集合](/docs/data-binding/how-to-bind-to-a-collection)：`ItemsSource` 与 `DataTemplate` 的用法。
- [数据模板](/docs/data-templates/introduction-to-data-templates)：控制数据项的呈现方式。
- [数据上下文](/docs/data-binding/data-context)：`DataContext` 在控件树中如何向下流动。
- [集合视图](/docs/data-binding/collection-views)：对绑定的集合做排序、筛选和分组。
- [编译绑定](/docs/data-binding/compiled-bindings)：提升绑定性能，并在编译期发现错误。

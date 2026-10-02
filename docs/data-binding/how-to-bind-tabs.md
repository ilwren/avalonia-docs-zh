---
id: how-to-bind-tabs
title: 如何绑定选项卡
description: 把 TabControl 绑定到一组视图模型，构建动态的选项卡界面。
doc-type: how-to
---

当应用需要显示数量不定的选项卡时，与其在 XAML 里一个个静态声明，不如把 [`TabControl`](/api/avalonia/controls/tabcontrol) 数据绑定到一组视图模型上。选项卡数量要到运行时才确定的场合（比如由用户操作、载入的数据或插件系统决定），这种做法尤其合适。

总体套路是：

1. 定义一个代表单个选项卡的视图模型类（标题文字、内容，以及其他需要的状态）。
2. 在主视图模型中暴露一个由这些视图模型组成的 `ObservableCollection`。
3. 把 `TabControl.ItemsSource` 绑定到该集合，再用 `ItemTemplate` 和 `ContentTemplate` 控制每个选项卡的呈现方式。

## 绑定示例 {#binding-support-example}

你可以用**数据绑定**动态创建选项卡项：把 `TabControl` 的 `ItemsSource` 属性绑定到一组对象，这些对象分别承载选项卡的标题和内容。

然后用**数据模板**来展示这些对象。

本例使用的集合，其元素由下面这个 `ItemViewModel` 类创建：

```csharp
namespace MyApp.ViewModel;

public class ItemViewModel
{
    public string Header { get; }
    public string Content { get; }
    public ItemViewModel(string header, string content)
    {
        Header = header;
        Content = content;
    }
}
```

创建一个属性，用于访问由 `ItemViewModel` 实例组成的集合。

```csharp
public ObservableCollection<ItemViewModel> Items { get; set; } = new() {
    new ItemViewModel("One", "Some content on first tab"),
    new ItemViewModel("Two", "Some content on second tab"),
};
```

`TabStrip` 的标题内容由 `ItemTemplate` 属性决定，`TabItem` 的内容则由 `ContentTemplate` 属性决定。

最后创建一个 `TabControl`，把它的 `ItemsSource` 属性绑定到 `Items`。

```xml
<TabControl ItemsSource="{Binding Items}">
    <TabControl.ItemTemplate>
      <DataTemplate>
        <TextBlock Text="{Binding Header}" />
      </DataTemplate>
    </TabControl.ItemTemplate>
    <TabControl.ContentTemplate>
        <!-- ContentTemplate's DataTemplate must specify the view model in DataType.
        The alias 'vm' references the specification of the view model's namespace in
        an attribute of the XAML's root element, which will look like
            xmlns:vm="using:MyApp.ViewModel"
        or
            xmlns:vm="clr-namespace:MyApp.ViewModel;assembly=MyApp.ViewModel" -->
      <DataTemplate DataType="vm:ItemViewModel">
        <DockPanel LastChildFill="True">
          <TextBlock Text="This is content of selected tab" DockPanel.Dock="Top" FontWeight="Bold" />
          <TextBlock Text="{Binding Content}" />
        </DockPanel>
      </DataTemplate>
    </TabControl.ContentTemplate>
  </TabControl>
```

## 关于选项卡生命周期 {#tab-lifecycle-notes}

使用数据绑定的选项卡时，请留意以下几点：

- **增删选项卡。** 由于 `ItemsSource` 绑定的是 `ObservableCollection`，往集合里增删元素，运行时的选项卡也会随之增删。
- **内容的回收。** 用户切换选项卡时，`TabControl` 会重新创建内容的视觉元素。如果选项卡内容构建起来开销较大，可以考虑缓存已生成的视图，或者改用带有自身视图模型的 `UserControl` 来保留状态。
- **选中的选项卡。** 绑定 `TabControl` 上的 `SelectedItem` 或 `SelectedIndex`，即可跟踪或控制当前激活的是哪个选项卡。当你把当前选中项从集合中移除时，选中状态会自动重置。
- **ContentTemplate 上的 DataType。** `ContentTemplate` 里用到的 `DataTemplate` 一定要设置 `DataType`，否则绑定上下文可能解析不正确。

## 另请参阅 {#see-also}

- [TabControl](/controls/navigation/tabcontrol)：`TabControl` 控件的完整参考。
- [如何使用 TabControl](/docs/how-to/tabcontrol-how-to)：静态选项卡、可关闭选项卡与选项卡样式。
- [数据模板](/docs/data-templates/introduction-to-data-templates)：控制数据项的呈现方式。
- [数据绑定语法](/docs/data-binding/data-binding-syntax)：绑定路径与绑定模式。

---
id: tabcontrol-how-to
title: "操作指南：使用 TabControl"
description: 学会用 Avalonia 的 TabControl 做出静态标签、动态标签、可关闭标签以及带样式的标签。
doc-type: how-to
---

本指南带你走一遍 `TabControl` 的常见场景，包括静态标签、由数据绑定出的标签、可关闭标签、带图标的标题、标签位置以及样式。

## 静态标签 {#static-tabs}

最简单的做法是在 XAML 里用 [`TabItem`](/api/avalonia/controls/tabitem) 元素直接定义标签。每个 `TabItem` 都有一个 `Header`（标签文字）和子内容（选中该标签时显示的东西）。

```xml
<TabControl>
    <TabItem Header="General">
        <StackPanel Margin="16" Spacing="8">
            <TextBlock Text="General settings content" />
        </StackPanel>
    </TabItem>
    <TabItem Header="Appearance">
        <StackPanel Margin="16" Spacing="8">
            <TextBlock Text="Appearance settings content" />
        </StackPanel>
    </TabItem>
    <TabItem Header="Advanced">
        <StackPanel Margin="16" Spacing="8">
            <TextBlock Text="Advanced settings content" />
        </StackPanel>
    </TabItem>
</TabControl>
```

标签数量在设计阶段就确定时，这种写法很合适。若需要在运行时增删标签，请用下面介绍的动态做法。

## 从集合动态生成选项卡 {#dynamic-tabs-from-a-collection}

当标签需要由数据驱动时，请把 `ItemsSource` 属性绑定到视图模型中的 `ObservableCollection`。这样你就能在运行时增删标签，界面与逻辑也保持分离。

### 第 1 步：创建标签项的视图模型 {#step-1-create-a-tab-item-view-model}

定义一个表示单个标签的简单类：

```csharp
public class TabItemViewModel
{
    public string Header { get; }
    public object Content { get; }

    public TabItemViewModel(string header, object content)
    {
        Header = header;
        Content = content;
    }
}
```

### 第 2 步：在主视图模型中公开一个集合 {#step-2-expose-a-collection-from-your-main-view-model}

```csharp
public partial class MainViewModel : ObservableObject
{
    public ObservableCollection<TabItemViewModel> Tabs { get; } = new()
    {
        new TabItemViewModel("Home", new HomeViewModel()),
        new TabItemViewModel("Settings", new SettingsViewModel()),
    };

    [ObservableProperty]
    private TabItemViewModel? _selectedTab;
}
```

### 第 3 步：在 XAML 中绑定 {#step-3-bind-in-xaml}

用 `ItemTemplate` 定义标签标题的呈现方式，用 `ContentTemplate` 定义标签正文：

```xml
<TabControl ItemsSource="{Binding Tabs}"
            SelectedItem="{Binding SelectedTab}">
    <TabControl.ItemTemplate>
        <DataTemplate>
            <TextBlock Text="{Binding Header}" />
        </DataTemplate>
    </TabControl.ItemTemplate>
    <TabControl.ContentTemplate>
        <DataTemplate>
            <ContentControl Content="{Binding Content}" />
        </DataTemplate>
    </TabControl.ContentTemplate>
</TabControl>
```

:::tip
若各标签的 `Content` 是不同的视图模型类型，你可以用 `DataTemplateSelector`，或者在 `Application.DataTemplates` 集合里定义若干 `DataTemplate` 条目，让每个视图模型自动解析到正确的视图。
:::

## 可关闭的标签 {#closeable-tabs}

你可以给每个标签标题加一个关闭按钮，让用户能把标签关掉。关闭按钮的 `Command` 通过祖先绑定找到 `MainViewModel`。

```xml
<TabControl ItemsSource="{Binding Tabs}"
            SelectedItem="{Binding SelectedTab}">
    <TabControl.ItemTemplate>
        <DataTemplate>
            <StackPanel Orientation="Horizontal" Spacing="8">
                <TextBlock Text="{Binding Header}" VerticalAlignment="Center" />
                <Button Content="x" FontSize="10" Padding="4,2"
                        Background="Transparent" BorderThickness="0"
                        Command="{Binding $parent[TabControl].((vm:MainViewModel)DataContext).CloseTabCommand}"
                        CommandParameter="{Binding}" />
            </StackPanel>
        </DataTemplate>
    </TabControl.ItemTemplate>
    <TabControl.ContentTemplate>
        <DataTemplate>
            <ContentControl Content="{Binding Content}" />
        </DataTemplate>
    </TabControl.ContentTemplate>
</TabControl>
```

在视图模型中处理移除逻辑，并顺手更新选中项，免得用户停在一个空白标签上：

```csharp
[RelayCommand]
private void CloseTab(TabItemViewModel tab)
{
    Tabs.Remove(tab);
    if (SelectedTab == tab)
        SelectedTab = Tabs.FirstOrDefault();
}
```

:::note
祖先绑定里的 XAML 命名空间 `vm` 必须与你的视图模型命名空间一致。例如在 XAML 文件的根元素上加一句 `xmlns:vm="using:MyApp.ViewModels"`。
:::

:::tip
若你不想让最后一个标签被关掉，可以在移除前先检查 `Tabs.Count`：

```csharp
if (Tabs.Count > 1)
    Tabs.Remove(tab);
```
:::

## 带图标的标签 {#tabs-with-icons}

你可以自定义标签标题，让图标与文字并排显示。

### 带图标的静态标签 {#static-tab-with-an-icon}

把 `TabItem.Header` 设成一个同时装着 `PathIcon` 和 `TextBlock` 的面板：

```xml
<TabItem>
    <TabItem.Header>
        <StackPanel Orientation="Horizontal" Spacing="6">
            <PathIcon Data="{StaticResource HomeIcon}" Width="14" Height="14" />
            <TextBlock Text="Home" />
        </StackPanel>
    </TabItem.Header>
    <views:HomeView />
</TabItem>
```

### 带图标的动态标签 {#dynamic-tabs-with-icons}

若你的 `TabItemViewModel` 公开了一个 `StreamGeometry` 类型的 `IconData` 属性，就可以在 `ItemTemplate` 中用上它：

```xml
<TabControl.ItemTemplate>
    <DataTemplate>
        <StackPanel Orientation="Horizontal" Spacing="6">
            <PathIcon Data="{Binding IconData}" Width="14" Height="14" />
            <TextBlock Text="{Binding Header}" />
        </StackPanel>
    </DataTemplate>
</TabControl.ItemTemplate>
```

## 选项卡位置 {#tab-placement}

标签默认出现在顶部。你可以用 `TabStripPlacement` 属性换个位置，可选值有 `Top`、`Bottom`、`Left` 和 `Right`。

```xml
<!-- Tabs on the left (vertical layout) -->
<TabControl TabStripPlacement="Left">
    <TabItem Header="Page 1"><TextBlock Text="Content 1" /></TabItem>
    <TabItem Header="Page 2"><TextBlock Text="Content 2" /></TabItem>
</TabControl>

<!-- Tabs at the bottom -->
<TabControl TabStripPlacement="Bottom">
    <TabItem Header="Tab 1"><TextBlock Text="Content 1" /></TabItem>
</TabControl>
```

:::note
采用 `Left` 或 `Right` 时，标签标题会纵向排列。若标题较宽，你可能需要给 `TabItem` 设一个固定的 `Width`，或者约束标签条的尺寸，以免布局出问题。
:::

## Binding `SelectedIndex`

若你更想按数字索引、而非按项目引用来跟踪选中的标签，请绑定 `SelectedIndex` 属性：

```xml
<TabControl SelectedIndex="{Binding ActiveTabIndex}">
```

```csharp
[ObservableProperty]
private int _activeTabIndex;
```

需要用代码切换标签时这很好使，比如在向导式界面中跳到某个特定步骤。

## 惰性加载标签内容 {#lazy-tab-content}

默认情况下，`TabControl` 在首次加载时就会为每个标签创建内容。若标签里装着开销很大的控件或大批数据，你可以把创建推迟到标签真正被选中之时：

```csharp
public partial class LazyTabViewModel : ObservableObject
{
    private ObservableObject? _content;

    public string Header { get; }
    private readonly Func<ObservableObject> _contentFactory;

    public LazyTabViewModel(string header, Func<ObservableObject> contentFactory)
    {
        Header = header;
        _contentFactory = contentFactory;
    }

    public ObservableObject Content => _content ??= _contentFactory();
}
```

`Content` 属性用了一个工厂委托和空合并赋值运算符（`??=`），因此内容视图模型只在首次被访问时创建。当你把 `ContentTemplate` 绑定到 `{Binding Content}` 时，getter 只有在标签被选中后才会执行。

## 为标签设置样式 {#styling-tabs}

### 自定义标签标题的外观 {#custom-tab-header-appearance}

你可以在 `TabControl.Styles` 内加入样式，调整间距、字号以及选中标签的指示条：

```xml
<TabControl.Styles>
    <!-- Tab strip background -->
    <Style Selector="TabControl /template/ ItemsPresenter#PART_ItemsPresenter">
        <Setter Property="Margin" Value="0" />
    </Style>

    <!-- Individual tab items -->
    <Style Selector="TabItem">
        <Setter Property="Padding" Value="16,8" />
        <Setter Property="FontSize" Value="13" />
    </Style>

    <!-- Selected tab indicator -->
    <Style Selector="TabItem:selected">
        <Setter Property="Foreground" Value="#6366F1" />
    </Style>
</TabControl.Styles>
```

### 去掉标签边框 {#removing-the-tab-border}

让你的标签呈现扁平、无边框的观感：

```xml
<TabControl.Styles>
    <Style Selector="TabItem">
        <Setter Property="Background" Value="Transparent" />
    </Style>
</TabControl.Styles>
```

:::tip
你也可以组合多个样式选择器，顺带照顾悬停和按下状态。比如 `TabItem:pointerover` 会在指针悬停在标签上时生效。
:::

## 另请参阅 {#see-also}

- [TabControl 参考](/controls/navigation/tabcontrol)：完整的属性表与更多示例。
- [如何绑定标签](/docs/data-binding/how-to-bind-tabs)：把标签内容绑定到集合的详细演练。
- [导航操作指南](/docs/how-to/navigation-how-to)：`Carousel` 以及基于页面的导航等其他套路。
- [数据绑定入门](/docs/data-binding/introduction-to-data-binding)：把界面绑定到视图模型的核心概念。

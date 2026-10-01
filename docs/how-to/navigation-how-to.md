---
id: navigation-how-to
title: "操作指南：在视图之间导航"
description: Avalonia 应用中切换视图与页面的常见套路。
doc-type: how-to
---

本指南介绍在 Avalonia 应用中切换视图（页面）的常见套路。从只有两个页面的小应用，到带历史导航的完整桌面外壳，每种套路各有适用的场景。

## 挑选导航套路 {#choosing-a-navigation-pattern}

动手之前，先想想哪种套路合你的需求：

| 套路 | 适用场景 |
|---|---|
| [`ContentControl`](/api/avalonia/controls/contentcontrol) 配数据模板 | 页面固定、数量不多的小应用 |
| [`TransitioningContentControl`](/api/avalonia/controls/transitioningcontentcontrol) | 同上，但带过渡动画 |
| `TabControl` | 设置界面、文档编辑器 |
| 侧边栏导航 | 带主菜单的桌面应用 |
| 带后退栈的导航 | 向导式流程、浏览器那样的历史记录 |

## 用 ContentControl 切换视图 {#view-switching-with-contentcontrol}

最简单的导航套路是用一个 `ContentControl` 显示不同的视图模型，再靠数据模板找出对应的视图。

```xml
<Window x:Class="MyApp.Views.MainWindow"
        xmlns:vm="using:MyApp.ViewModels"
        xmlns:views="using:MyApp.Views">
    <Window.DataTemplates>
        <DataTemplate DataType="vm:HomeViewModel">
            <views:HomeView />
        </DataTemplate>
        <DataTemplate DataType="vm:SettingsViewModel">
            <views:SettingsView />
        </DataTemplate>
    </Window.DataTemplates>

    <Grid RowDefinitions="Auto,*">
        <StackPanel Grid.Row="0" Orientation="Horizontal" Spacing="8" Margin="8">
            <Button Content="Home" Command="{Binding GoHomeCommand}" />
            <Button Content="Settings" Command="{Binding GoSettingsCommand}" />
        </StackPanel>

        <ContentControl Grid.Row="1" Content="{Binding CurrentPage}" />
    </Grid>
</Window>
```

视图模型：

```csharp
public partial class MainViewModel : ObservableObject
{
    [ObservableProperty]
    private ObservableObject _currentPage;

    public MainViewModel()
    {
        _currentPage = new HomeViewModel();
    }

    [RelayCommand]
    private void GoHome() => CurrentPage = new HomeViewModel();

    [RelayCommand]
    private void GoSettings() => CurrentPage = new SettingsViewModel();
}
```

`CurrentPage` 一变，`ContentControl` 就会查出匹配的 [`DataTemplate`](/api/avalonia/markup/xaml/templates/datatemplate) 并自动显示对应的视图。这之所以行得通，是因为 Avalonia 会沿视觉树往上找，寻找 `DataType` 与赋给 `Content` 的对象相匹配的 `DataTemplate`。

:::tip
视图模型一多，手写每一个 `DataTemplate` 就很烦人了。自动化的替代方案请见本指南后面的[视图定位器套路](#view-locator-pattern)。
:::

## 带过渡的视图切换 {#view-switching-with-transitions}

把 `ContentControl` 换成 `TransitioningContentControl`，就能为视图切换加上页面过渡动画：

```xml
<TransitioningContentControl Content="{Binding CurrentPage}">
    <TransitioningContentControl.PageTransition>
        <CrossFade Duration="0:0:0.25" />
    </TransitioningContentControl.PageTransition>
</TransitioningContentControl>
```

可用的内置过渡有：

| 过渡动画 | 效果 |
|---|---|
| `CrossFade` | 在新旧内容之间淡入淡出 |
| `PageSlide` | 让内容横向或纵向滑动 |
| `CompositePageTransition` | 把多种过渡组合到一起 |

```xml
<!-- Slide transition -->
<TransitioningContentControl.PageTransition>
    <PageSlide Duration="0:0:0.3" Orientation="Horizontal" />
</TransitioningContentControl.PageTransition>

<!-- Combined: slide + fade -->
<TransitioningContentControl.PageTransition>
    <CompositePageTransition>
        <CrossFade Duration="0:0:0.2" />
        <PageSlide Duration="0:0:0.3" Orientation="Horizontal" />
    </CompositePageTransition>
</TransitioningContentControl.PageTransition>
```

## 标签页式导航 {#tab-based-navigation}

当你希望用户在一组固定的面板之间切换时（比如设置分类或文档标签），请用 `TabControl`。

```xml
<TabControl>
    <TabItem Header="General">
        <views:GeneralSettingsView />
    </TabItem>
    <TabItem Header="Appearance">
        <views:AppearanceSettingsView />
    </TabItem>
    <TabItem Header="Advanced">
        <views:AdvancedSettingsView />
    </TabItem>
</TabControl>
```

### 从集合动态生成选项卡 {#dynamic-tabs-from-a-collection}

若标签需要由数据驱动（比如已打开的文档），请把 `ItemsSource` 绑定到视图模型中的集合。

```xml
<TabControl ItemsSource="{Binding OpenDocuments}"
            SelectedItem="{Binding ActiveDocument}">
    <TabControl.ItemTemplate>
        <DataTemplate>
            <StackPanel Orientation="Horizontal" Spacing="8">
                <TextBlock Text="{Binding Title}" />
                <Button Content="x" FontSize="10"
                        Command="{Binding $parent[TabControl].((vm:MainViewModel)DataContext).CloseDocumentCommand}"
                        CommandParameter="{Binding}" />
            </StackPanel>
        </DataTemplate>
    </TabControl.ItemTemplate>
    <TabControl.ContentTemplate>
        <DataTemplate>
            <views:DocumentView />
        </DataTemplate>
    </TabControl.ContentTemplate>
</TabControl>
```

## 侧边栏导航 {#sidebar-navigation}

桌面端有个常见做法：侧边栏放一份常驻菜单，主内容区则来回换视图。本例用 `ListBox` 做菜单，用 `TransitioningContentControl` 承载内容。

```xml
<Grid ColumnDefinitions="220,*">
    <!-- Sidebar -->
    <Border Grid.Column="0" Background="#F3F4F6">
        <ListBox ItemsSource="{Binding MenuItems}"
                 SelectedItem="{Binding SelectedMenuItem}"
                 Background="Transparent">
            <ListBox.ItemTemplate>
                <DataTemplate>
                    <StackPanel Orientation="Horizontal" Spacing="8" Margin="8,4">
                        <PathIcon Data="{Binding Icon}" Width="16" Height="16" />
                        <TextBlock Text="{Binding Title}" />
                    </StackPanel>
                </DataTemplate>
            </ListBox.ItemTemplate>
        </ListBox>
    </Border>

    <!-- Content area -->
    <TransitioningContentControl Grid.Column="1" Content="{Binding CurrentPage}" />
</Grid>
```

```csharp
public partial class MainViewModel : ObservableObject
{
    public ObservableCollection<MenuItem> MenuItems { get; } = new()
    {
        new MenuItem("Home", "HomeIcon", () => new HomeViewModel()),
        new MenuItem("Settings", "SettingsIcon", () => new SettingsViewModel()),
        new MenuItem("About", "InfoIcon", () => new AboutViewModel()),
    };

    [ObservableProperty]
    private MenuItem? _selectedMenuItem;

    [ObservableProperty]
    private ObservableObject? _currentPage;

    partial void OnSelectedMenuItemChanged(MenuItem? value)
    {
        CurrentPage = value?.CreatePage();
    }
}

public record MenuItem(string Title, string Icon, Func<ObservableObject> CreatePage);
```

## 带后退栈的导航 {#navigation-with-back-stack}

若你的应用需要浏览器那样的前进后退按钮（比如向导或文件浏览器），可以用两个栈来维护访问历史。

```csharp
public partial class NavigationViewModel : ObservableObject
{
    private readonly Stack<ObservableObject> _backStack = new();
    private readonly Stack<ObservableObject> _forwardStack = new();

    [ObservableProperty]
    private ObservableObject? _currentPage;

    public bool CanGoBack => _backStack.Count > 0;
    public bool CanGoForward => _forwardStack.Count > 0;

    public void NavigateTo(ObservableObject page)
    {
        if (CurrentPage is not null)
            _backStack.Push(CurrentPage);

        _forwardStack.Clear();
        CurrentPage = page;

        OnPropertyChanged(nameof(CanGoBack));
        OnPropertyChanged(nameof(CanGoForward));
    }

    [RelayCommand(CanExecute = nameof(CanGoBack))]
    private void GoBack()
    {
        if (CurrentPage is not null)
            _forwardStack.Push(CurrentPage);

        CurrentPage = _backStack.Pop();

        OnPropertyChanged(nameof(CanGoBack));
        OnPropertyChanged(nameof(CanGoForward));
        GoBackCommand.NotifyCanExecuteChanged();
        GoForwardCommand.NotifyCanExecuteChanged();
    }

    [RelayCommand(CanExecute = nameof(CanGoForward))]
    private void GoForward()
    {
        if (CurrentPage is not null)
            _backStack.Push(CurrentPage);

        CurrentPage = _forwardStack.Pop();

        OnPropertyChanged(nameof(CanGoBack));
        OnPropertyChanged(nameof(CanGoForward));
        GoBackCommand.NotifyCanExecuteChanged();
        GoForwardCommand.NotifyCanExecuteChanged();
    }
}
```

```xml
<Grid RowDefinitions="Auto,*">
    <StackPanel Grid.Row="0" Orientation="Horizontal" Spacing="4" Margin="8">
        <Button Content="Back" Command="{Binding GoBackCommand}" />
        <Button Content="Forward" Command="{Binding GoForwardCommand}" />
    </StackPanel>

    <TransitioningContentControl Grid.Row="1" Content="{Binding CurrentPage}" />
</Grid>
```

## 视图定位器套路 {#view-locator-pattern}

与其为每个视图模型都声明一个 `DataTemplate`，不如用视图定位器按约定自动解析视图。定位器会把完全限定类型名中的 `ViewModel` 换成 `View`，再把结果实例化出来。

```csharp
public class ViewLocator : IDataTemplate
{
    public Control Build(object? data)
    {
        if (data is null) return new TextBlock { Text = "No data" };

        var name = data.GetType().FullName!
            .Replace("ViewModel", "View", StringComparison.Ordinal);

        var type = Type.GetType(name);

        if (type is not null)
            return (Control)Activator.CreateInstance(type)!;

        return new TextBlock { Text = $"View not found: {name}" };
    }

    public bool Match(object? data)
    {
        return data is ObservableObject;
    }
}
```

在 `App.axaml` 中注册这个定位器，让它全局生效：

```xml
<Application.DataTemplates>
    <local:ViewLocator />
</Application.DataTemplates>
```

现在任何绑定到视图模型的 `ContentControl` 都会自动解析出对应视图。例如 `HomeViewModel` 映射到 `HomeView`，`SettingsViewModel` 映射到 `SettingsView`。

:::note
这套约定要求视图类和视图模型类处在平行的命名空间中（比如 `MyApp.ViewModels.HomeViewModel` 和 `MyApp.Views.HomeView`）。若你的项目目录结构不同，请相应调整 `Build` 方法里的字符串替换逻辑。
:::

## 另请参阅 {#see-also}

- [页面过渡](/docs/graphics-animation/page-transitions)：视图之间的过渡动画。
- [数据模板](/docs/data-templates/introduction-to-data-templates)：数据模板如何解析出视图。
- [视图定位器](/docs/data-templates/view-locator)：视图模型到视图的自动映射。
- [MVVM 模式](/docs/fundamentals/the-mvvm-pattern)：视图模型的架构。

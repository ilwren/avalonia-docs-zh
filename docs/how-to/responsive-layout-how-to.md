---
id: responsive-layout-how-to
title: "操作指南：构建响应式布局"
description: 做出能适应不同窗口尺寸和设备形态的 Avalonia 布局。
doc-type: how-to
---

import ResponsiveCardGrid from '/img/how-to/responsive-card-grid.gif';

本指南介绍如何做出适应不同窗口尺寸与设备形态的布局。你将学到形态因子标记扩展、容器查询、断点驱动的视图模型，以及会自动重排的项目布局，从而搭出桌面和移动端都好用的界面。

## 自适应的网格列 {#adaptive-grid-columns}

用 `OnFormFactor` 标记扩展，根据设备类型改变布局结构。在下面的例子里，桌面端是带侧边栏的两列网格，而移动端用户看到的是单列布局：

```xml
<Grid ColumnDefinitions="{OnFormFactor Desktop='250,*', Mobile='*'}">
    <Border Grid.Column="0" Background="#F3F4F6"
            IsVisible="{OnFormFactor Desktop=True, Mobile=False}">
        <!-- Sidebar: visible on desktop, hidden on mobile -->
        <ListBox ItemsSource="{Binding MenuItems}" />
    </Border>

    <ContentControl Grid.Column="{OnFormFactor Desktop=1, Mobile=0}"
                    Content="{Binding CurrentPage}" />
</Grid>
```

`OnFormFactor` 在启动时就解析完毕，所以运行时改变窗口大小并不会让它的取值跟着变。若你的布局需要实时响应尺寸变化，请改用容器查询或基于断点的做法。

## 容器查询 {#container-queries}

容器查询依据的是控件自身的渲染尺寸，而非窗口尺寸。因此它特别适合那些可能被放进不同宽度面板的可复用组件。

下面这个例子让 `StackPanel` 依据父级 `Border` 的宽度，在纵向和横向之间切换朝向：

```xml
<Border>
    <Border.Styles>
        <!-- Vertical layout when container is narrow -->
        <Style Selector="Border[Width<400] > StackPanel">
            <Setter Property="Orientation" Value="Vertical" />
        </Style>
        <!-- Horizontal layout when container is wide -->
        <Style Selector="Border[Width>=400] > StackPanel">
            <Setter Property="Orientation" Value="Horizontal" />
        </Style>
    </Border.Styles>

    <StackPanel Spacing="8">
        <TextBlock Text="Label" />
        <TextBox Text="{Binding Value}" />
    </StackPanel>
</Border>
```

完整语法以及具名容器的支持，请参阅[容器查询](/docs/styling/container-queries)。

## 基于断点的布局 {#breakpoint-based-layout}

若你需要对布局切换有更精细的掌控，可以在视图模型中观察窗口宽度，自行实现断点：为每个断点档位定义一个布尔属性，再在 XAML 里绑定它们：

```csharp
public partial class MainViewModel : ObservableObject
{
    [ObservableProperty]
    private bool _isCompact;

    [ObservableProperty]
    private bool _isWide;

    public void UpdateLayout(double windowWidth)
    {
        IsCompact = windowWidth < 640;
        IsWide = windowWidth >= 1024;
    }
}
```

在窗口的 `OnSizeChanged` 重写中调用 `UpdateLayout`，这样用户调整窗口大小时你的属性才能保持同步：

```csharp
// In MainWindow code-behind
protected override void OnSizeChanged(SizeChangedEventArgs e)
{
    base.OnSizeChanged(e);
    if (DataContext is MainViewModel vm)
        vm.UpdateLayout(e.NewSize.Width);
}
```

在 AXAML 中，把 `IsVisible` 绑定到这些断点属性，即可在紧凑视图和宽视图之间切换：

```xml
<Grid>
    <!-- Compact layout: single column -->
    <StackPanel IsVisible="{Binding IsCompact}" Spacing="8">
        <views:SidebarView />
        <views:ContentView />
    </StackPanel>

    <!-- Wide layout: two columns -->
    <Grid IsVisible="{Binding !IsCompact}" ColumnDefinitions="280,*">
        <views:SidebarView Grid.Column="0" />
        <views:ContentView Grid.Column="1" />
    </Grid>
</Grid>
```

这种做法让你在代码里完全说了算，而且当布局逻辑不止于简单的宽度阈值时（比如还要结合朝向和平台判断）尤其好使。

## 用 `SplitView` 做可折叠的侧边栏 {#use-splitview-for-a-collapsible-sidebar}

`SplitView` 控件自带一套可折叠窗格的做法。把 `DisplayMode` 设为 `CompactInline`，窗格折叠时会缩成只显示图标的窄条，切换 `IsPaneOpen` 后再展开露出文字标签：

```xml
<SplitView IsPaneOpen="{Binding IsSidebarOpen}"
           DisplayMode="CompactInline"
           CompactPaneLength="48"
           OpenPaneLength="250">
    <SplitView.Pane>
        <StackPanel>
            <Button Content="☰" Command="{Binding ToggleSidebarCommand}"
                    HorizontalAlignment="Left" Width="48" />
            <ListBox ItemsSource="{Binding MenuItems}"
                     SelectedItem="{Binding SelectedMenuItem}">
                <ListBox.ItemTemplate>
                    <DataTemplate>
                        <StackPanel Orientation="Horizontal" Spacing="12">
                            <PathIcon Data="{Binding Icon}" Width="16" />
                            <TextBlock Text="{Binding Title}" />
                        </StackPanel>
                    </DataTemplate>
                </ListBox.ItemTemplate>
            </ListBox>
        </StackPanel>
    </SplitView.Pane>

    <SplitView.Content>
        <ContentControl Content="{Binding CurrentPage}" />
    </SplitView.Content>
</SplitView>
```

你可以把 `IsPaneOpen` 绑定到自己的断点属性，这样宽屏下侧边栏自动展开，窄屏下自动折叠。

## 响应式卡片网格 {#responsive-card-grid}

用 `ItemsControl` 搭配 `WrapPanel` 作为显示面板，就能做出随可用宽度自动重排的卡片网格。关于如何在 `ItemsControl` 中自定义 `ItemsPanel`，请参阅[自定义面板](/docs/how-to/itemscontrol-how-to#custom-panel)。

<Tabs>

<TabItem value="preview" label="Preview">

<Image light={ResponsiveCardGrid} maxWidth={400} cornerRadius="true" position="center" alt="Screen recording showing a window changing size. The card arrangement in the window adjusts according to the window's width." />
<br />

</TabItem>

<TabItem value="main-window" label="MainWindow.axaml">

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:vm="using:ResponsiveCardGrid.ViewModels"
        xmlns:models="using:ResponsiveCardGrid.Models"
        x:Class="ResponsiveCardGrid.Views.MainWindow"
        x:DataType="vm:MainViewModel">

  <ItemsControl ItemsSource="{Binding Cards}">
    <ItemsControl.ItemsPanel>
      <ItemsPanelTemplate>
        <WrapPanel />
      </ItemsPanelTemplate>
    </ItemsControl.ItemsPanel>
    <ItemsControl.ItemTemplate>
      <DataTemplate x:DataType="models:CardItem">
        <Border Background="White"
                CornerRadius="8"
                Padding="16"
                BorderBrush="#E5E7EB"
                BorderThickness="1">
          <StackPanel Spacing="8">
            <TextBlock Text="{Binding Title}"
                       FontWeight="Bold"
                       Foreground="Black" />
            <TextBlock Text="{Binding Description}"
                       TextWrapping="Wrap"
                       Foreground="Gray" />
          </StackPanel>
        </Border>
      </DataTemplate>
    </ItemsControl.ItemTemplate>
  </ItemsControl>
</Window>
```

</TabItem>

<TabItem value="main-view-model" label="MainViewModel.cs">

```csharp
using System.Collections.ObjectModel;
using ResponsiveCardGrid.Models;

namespace ResponsiveCardGrid.ViewModels;

public partial class MainWindowViewModel : ViewModelBase
{
    public ObservableCollection<CardItem> Cards { get; } =
    [
        new() { Title = "Inbox", Description = "Messages waiting for a reply from the team." },
        new() { Title = "Drafts", Description = "Unfinished notes you started but never sent." },
        new() { Title = "Scheduled", Description = "Items queued to go out later this week." },
        new() { Title = "Archive", Description = "Everything you have filed away for later reference." },
        new() { Title = "Starred", Description = "Cards you flagged as worth a second look." },
        new() { Title = "Trash", Description = "Deleted items, kept for thirty days before removal." }
    ];
}
```

</TabItem>

<TabItem value="card-item-model" label="Models/CardItem.cs">

```csharp
using CommunityToolkit.Mvvm.ComponentModel;

namespace ResponsiveCardGrid.Models;

public partial class CardItem : ObservableObject
{
    [ObservableProperty]
    public partial string Title { get; set; } = string.Empty;

    [ObservableProperty]
    public partial string Description { get; set; } = string.Empty;
}
```

</TabItem>

</Tabs>

## 随平台而变的间距 {#platform-specific-spacing}

用 `OnFormFactor` 按平台调整间距、外边距和字号。移动端界面通常更适合大一点的触摸目标和略大的文字：

```xml
<StackPanel Spacing="{OnFormFactor Desktop=8, Mobile=12}"
            Margin="{OnFormFactor Desktop='16', Mobile='8'}">
    <TextBlock Text="Content" FontSize="{OnFormFactor Desktop=14, Mobile=16}" />
</StackPanel>
```

## 自适应字号 {#adaptive-font-sizes}

用[容器查询](/docs/styling/container-queries)依据祖先元素的尺寸缩放文字：先在父元素上用 `Container.Name` 和 `Container.Sizing` 声明一个容器，再用 `ContainerQuery` 为不同宽度设定不同字号：

```xml
<Panel Container.Name="content" Container.Sizing="Width">
    <Panel.Styles>
        <Style Selector="TextBlock.title">
            <Setter Property="FontSize" Value="24" />
        </Style>

        <!-- Smaller title when the container is narrow -->
        <ContainerQuery Name="content" Query="max-width:500">
            <Style Selector="TextBlock.title">
                <Setter Property="FontSize" Value="18" />
            </Style>
        </ContainerQuery>
    </Panel.Styles>

    <TextBlock Classes="title" Text="Responsive heading" />
</Panel>
```

这招让你的排版无需依赖窗口级断点也能保持响应式，于是哪怕控件被放进拆分窗格或对话框里，文字照样能正确适配。

## 另请参阅 {#see-also}

- [容器查询](/docs/styling/container-queries)：依据容器尺寸的响应式样式。
- [布局](/docs/layout)：Avalonia 布局系统概览。
- [Grid 操作指南](/docs/how-to/grid-how-to)：Grid 布局的各种用法。
- [跨平台架构](/docs/fundamentals/cross-platform-architecture)：平台检测与分支处理。

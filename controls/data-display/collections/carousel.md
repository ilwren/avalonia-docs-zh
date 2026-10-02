---
id: carousel
title: Carousel
description: Avalonia 中 Carousel 控件的参考文档：它每次呈现一个条目，支持翻页动画、导航方法和数据绑定。
doc-type: reference
---

import CarouselScreenshot from '/img/reference/controls/carousel/carousel.gif';

`Carousel` 有一个条目集合，它按顺序把每个条目当作一页来显示，并填满整个控件。你可以用它做幻灯片、新手引导流程，或任何需要让用户逐页浏览内容的界面。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `PageTransition` | `IPageTransition?` | `null` | 选中项变化时播放的过渡动画。内置选项有 `PageSlide`、`CrossFade`、`Rotate3DTransition` 和 `CompositePageTransition`。 |
| `IsSwipeEnabled` | `bool` | `false` | 启用滑动和指针拖动手势来翻页。 |
| `ViewportFraction` | `double` | `1.0` | 每一页所占视口的比例。小于 `1.0` 的取值会让相邻页露出一角（比如 `0.8` 会露出两侧邻页，`0.33` 则同时显示三项）。 |
| `IsSwiping` | `bool` | `false` | 只读。滑动手势进行期间为 `true`。 |
| `WrapSelection` | `bool` | `false` | 为 `true` 时，`Next()` 会从最后一项绕回第一项，`Previous()` 则从第一项绕回最后一项。 |
| `SelectedIndex` | `int` | `-1` | 当前所显示条目的索引，从零开始。 |
| `SelectedItem` | `object?` | `null` | 所绑定集合中当前显示的那一项。 |
| `ItemsSource` | `IEnumerable?` | `null` | 用作数据源的绑定集合。 |
| `ItemTemplate` | `IDataTemplate?` | `null` | 作用于每个条目的 `DataTemplate`，用来控制条目的外观。 |
| `ItemsPanel` | `ITemplate<Panel?>` | `VirtualizingCarouselPanel` | 用于排布各条目的容器面板。定制条目面板的细节请参阅 [ItemsControl](/controls/data-display/collections/itemscontrol)。 |
| `AutoScrollToSelectedItem` | `bool` | `true` | 自动滚动，把选中项带入可见区域。 |

## 示例 {#examples}

下面这个例子的条目集合中有三张图片，并配了两个按钮用于前后切换。按钮的点击事件处理程序写在 C# 代码隐藏文件里。

```xml title='XAML'
<Panel>
    <Carousel Name="slides">
        <Carousel.PageTransition>
            <CompositePageTransition>
                <PageSlide Duration="0:00:01.500" Orientation="Horizontal" />
            </CompositePageTransition>
        </Carousel.PageTransition>
        <Carousel.Items>
            <Image Source="avares://AvaloniaControls/Assets/pipes.jpg" />
            <Image Source="avares://AvaloniaControls/Assets/controls.jpg" />
            <Image Source="avares://AvaloniaControls/Assets/vault.jpg" />
        </Carousel.Items>
    </Carousel>
    <Panel Margin="20">
        <Button Background="White" Click="Previous">&lt;</Button>
        <Button Background="White" Click="Next"
                HorizontalAlignment="Right">&gt;</Button>
    </Panel>
</Panel>
```

```csharp title='C#'
using Avalonia.Controls;
using Avalonia.Interactivity;

namespace AvaloniaControls.Views
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        public void Next(object source, RoutedEventArgs args)
        {
            slides.Next();
        }

        public void Previous(object source, RoutedEventArgs args)
        {
            slides.Previous();
        }
    }
}
```

<Image light={CarouselScreenshot} alt="Carousel control cycling through slides" position="center" maxWidth={400} cornerRadius="true"/>

## 绑定到集合 {#binding-to-a-collection}

用 `ItemsSource` 把 `Carousel` 绑定到数据集合，并提供自定义的 `DataTemplate`：

```xml title='XAML'
<Carousel ItemsSource="{Binding Slides}" SelectedIndex="{Binding CurrentSlide}">
    <Carousel.PageTransition>
        <CrossFade Duration="0:00:00.300" />
    </Carousel.PageTransition>
    <Carousel.ItemTemplate>
        <DataTemplate>
            <StackPanel HorizontalAlignment="Center" VerticalAlignment="Center">
                <TextBlock Text="{Binding Title}" FontSize="24" FontWeight="Bold" />
                <TextBlock Text="{Binding Description}" TextWrapping="Wrap" />
            </StackPanel>
        </DataTemplate>
    </Carousel.ItemTemplate>
</Carousel>
```

视图模型对外提供该集合和当前索引：

```csharp title='C#'
public class SlidesViewModel : ViewModelBase
{
    public ObservableCollection<Slide> Slides { get; } = new()
    {
        new Slide("Welcome",   "Get started with Avalonia."),
        new Slide("Features",  "Cross-platform, high-performance UI."),
        new Slide("Community", "Join the Avalonia community today."),
    };

    private int _currentSlide;
    public int CurrentSlide
    {
        get => _currentSlide;
        set => this.RaiseAndSetIfChanged(ref _currentSlide, value);
    }
}
```

由于 `SelectedIndex` 默认双向绑定，你既可以在视图模型中改动 `CurrentSlide` 来翻页，也可以让用户用按钮导航、由控件回写该属性。

## 页面过渡 {#page-transitions}

给 `PageTransition` 属性赋一个过渡动画，即可设定条目切换时播放的动画。Avalonia 内置了若干过渡动画：

| 过渡动画 | 说明 |
|---|---|
| `PageSlide` | 让内容从指定方向滑入。`Orientation` 可设为 `Horizontal`（默认）或 `Vertical`。 |
| `CrossFade` | 通过不透明度动画，把当前项淡出、把新项淡入。 |
| `Rotate3DTransition` | 让当前项与新进入的项在三维空间中翻转，支持横轴和纵轴。 |
| `CompositePageTransition` | 把多个过渡动画组合起来同时播放。 |

### `PageSlide` example

```xml title='XAML'
<Carousel.PageTransition>
    <PageSlide Duration="0:00:00.500" Orientation="Horizontal" />
</Carousel.PageTransition>
```

### `CrossFade` example

```xml title='XAML'
<Carousel.PageTransition>
    <CrossFade Duration="0:00:00.300" />
</Carousel.PageTransition>
```

### 组合过渡动画示例 {#composite-transition-example}

你可以用 `CompositePageTransition` 把多个过渡动画叠加起来：

```xml title='XAML'
<Carousel.PageTransition>
    <CompositePageTransition>
        <CrossFade Duration="0:00:00.500" />
        <PageSlide Duration="0:00:00.500" Orientation="Horizontal" />
    </CompositePageTransition>
</Carousel.PageTransition>
```

### 关闭过渡动画 {#disabling-transitions}

若要切换条目时不播放任何动画，把 `PageTransition` 设为 `{x:Null}`：

```xml title='XAML'
<Carousel PageTransition="{x:Null}" />
```

页面过渡动画的完整指南（包括如何自定义过渡动画）请参阅[设置页面过渡动画](/docs/graphics-animation/page-transitions)。

## Navigation

改变当前显示项的方式有好几种：

| 技术 | 说明 |
|---|---|
| `Next()` | 切到集合中的下一项。 |
| `Previous()` | 退回上一项。 |
| `SelectedIndex` | 设置或绑定要显示那一项的索引（从零开始）。 |
| `SelectedItem` | 直接设置或绑定条目对象本身。 |

### 用按钮导航（代码隐藏） {#navigating-with-buttons-code-behind}

最简单的做法是在按钮点击处理程序里调用 `Next()` 和 `Previous()`，就像上面的[示例](#examples)那样。

### 用数据绑定导航 {#navigating-with-data-binding}

把 `SelectedIndex` 绑定到视图模型的某个属性，这样就能从应用逻辑中控制翻页：

```xml title='XAML'
<Carousel ItemsSource="{Binding Pages}" SelectedIndex="{Binding PageIndex}" />
```

```csharp title='C#'
public int PageIndex
{
    get => _pageIndex;
    set => this.RaiseAndSetIfChanged(ref _pageIndex, value);
}

public void GoToNext()
{
    if (PageIndex < Pages.Count - 1)
        PageIndex++;
}

public void GoToPrevious()
{
    if (PageIndex > 0)
        PageIndex--;
}
```

## 滑动手势 {#swipe-gestures}

设置 `IsSwipeEnabled` 即可启用滑动和指针拖动导航：

```xml title='XAML'
<Carousel IsSwipeEnabled="True">
    <!-- items -->
</Carousel>
```

启用之后，用户可以拖动翻页，并获得相应的视觉反馈。控件还支持快速轻扫（flick）手势：滑动速度要超过一定阈值，这次切换才会完成。手势进行期间，`IsSwiping` 属性为 `true`。

## 循环选择（首尾相接） {#wrap-selection-looping}

开启循环之后，在最后一项上调用 `Next()` 会绕回第一项，在第一项上调用 `Previous()` 则绕回最后一项：

```xml title='XAML'
<Carousel WrapSelection="True">
    <!-- items -->
</Carousel>
```

## 视口占比 {#viewport-fraction}

把 `ViewportFraction` 设为小于 `1.0` 的值，即可在选中页旁边露出相邻页：

```xml title='XAML'
<Carousel ViewportFraction="0.8">
    <!-- items -->
</Carousel>
```

取 `1.0`（默认）时只显示完整的一页。取 `0.8` 这类数值会产生「露边」效果，相邻页的边缘会露出来。取 `0.33` 时视野内大致能容下三项。

## 键盘导航 {#keyboard-navigation}

`Carousel` 获得焦点后支持键盘导航：

| 按键 | 动作 |
|---|---|
| 左方向键 / 上方向键 | 切到上一项。 |
| 右方向键 / 下方向键 | 切到下一项。 |
| Home | 跳到第一项。 |
| End | 跳到最后一项。 |

## 另请参阅 {#see-also}

- [PipsPager](/controls/layout/containers/pipspager)——圆点式的分页指示器
- [CarouselPage](/controls/navigation/carouselpage)——按页导航的轮播
- [设置页面过渡动画](/docs/graphics-animation/page-transitions)
- [TransitioningContentControl](/controls/data-display/transitioningcontentcontrol)
- [ItemsControl](/controls/data-display/collections/itemscontrol)
- [ListBox](/controls/data-display/collections/listbox)
- [Carousel API 参考](/api/avalonia/controls/carousel)
- [GitHub 上的 `Carousel.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Carousel.cs)

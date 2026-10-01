---
title: CarouselPage
description: '`CarouselPage` 以可横向滚动的轮播形式展示一组页面。'
doc-type: reference
---

import CarouselPageBasicScreenshot from '/img/controls/carouselpage/carouselpage-basic.png';
import CarouselPageDataTemplateScreenshot from '/img/controls/carouselpage/carouselpage-data-template.png';

# CarouselPage

`CarouselPage` 以可横向滚动的轮播形式展示一组页面。用户可以滑动或用方向键在页面之间切换，还可以配上页面过渡动画。

`CarouselPage` 继承自 `SelectingMultiPage`，后者又继承自 `MultiPage`。这条继承链带来了：

- `Pages` collection
- `ItemsSource`
- `PageTemplate`
- `SelectedIndex`
- `SelectedPage`
- `CurrentPage`
- `SelectionChanged` event
- `PagesChanged` event
- `CurrentPageChanged` event

## Useful Properties

下面这些属性你多半会经常用到：

| 属性 | 类型 | 默认值 | 说明 |
| -------- | ---- | ------- | ----------- |
| `Pages` | `IEnumerable<Page>?` | `null` | 子页面的集合。它是 XAML 的内容属性，支持任意 `IEnumerable<Page>`，包括可观察集合。 |
| `ItemsSource` | `IEnumerable?` | `null` | 视图模型集合。一旦设置，它作为数据源的优先级高于 `Pages`。请与 `PageTemplate` 搭配使用，把每一项转换成 `Page`。 |
| `PageTemplate` | `IDataTemplate?` | `DefaultPageDataTemplate` | 当数据源里装的是数据对象而非页面本身时，用这个数据模板来生成 `Page` 实例。 |
| `PageTransition` | `IPageTransition?` | `null` | 选中页切换时播放的过渡动画。 |
| `IsGestureEnabled` | `bool` | `true` | 启用滑动与滚轮手势来切换页面。 |
| `IsKeyboardNavigationEnabled` | `bool` | `true` | 启用方向键、Home 和 End 键来切换页面。 |
| `ItemsPanel` | `ITemplate<Panel?>` | `VirtualizingCarouselPanel` | 用于在底层 `Carousel` 内部排布页面项的面板模板。 |
| `SelectedIndex` | `int` | `-1` | 当前选中页的索引，从 0 开始。 |
| `SelectedPage` | `Page?` | `null` | 只读，当前选中的页面。 |

## 事件 {#events}

| 事件 | 说明 |
| ----- | ----------- |
| `SelectionChanged` | 选中页发生变化时引发，提供 `PreviousPage` 和 `CurrentPage`。 |
| `CurrentPageChanged` | `CurrentPage` 变化时引发。 |
| `PagesChanged` | `Pages` 集合发生变化时引发。 |

活动页切换时，各个子 `Page` 上会触发导航生命周期事件（`NavigatedTo`、`Navigating`、`NavigatedFrom`）。

## Keyboard Navigation

当 `IsKeyboardNavigationEnabled` 为 `true` 时：

- 左右方向键切换到上一页和下一页。从右到左的布局中方向相反。
- 上方向键切到上一页，下方向键切到下一页。
- `Home` 跳到第一页，`End` 跳到最后一页。

## Gesture Navigation

当 `IsGestureEnabled` 为 `true` 时：

- 左右滑动可在页面之间切换。
- 鼠标滚轮可在页面之间切换。从右到左的布局中方向相反。

## 示例 {#examples}

### XAML 中的基础 CarouselPage {#basic-carouselpage-in-xaml}

```xml
<CarouselPage xmlns="https://github.com/avaloniaui"
              xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
              x:Class="MyApp.OnboardingCarousel">

    <ContentPage Header="Welcome">
        <StackPanel VerticalAlignment="Center"
                    HorizontalAlignment="Center"
                    Spacing="16">
            <TextBlock Text="Welcome to MyApp"
                       FontSize="28"
                       HorizontalAlignment="Center" />
            <TextBlock Text="Swipe to learn more"
                       Opacity="0.6"
                       HorizontalAlignment="Center" />
        </StackPanel>
    </ContentPage>

    <ContentPage Header="Features">
        <StackPanel VerticalAlignment="Center"
                    HorizontalAlignment="Center"
                    Spacing="16">
            <TextBlock Text="Powerful Features"
                       FontSize="28"
                       HorizontalAlignment="Center" />
            <TextBlock Text="Everything you need in one place"
                       Opacity="0.6"
                       HorizontalAlignment="Center" />
        </StackPanel>
    </ContentPage>

    <ContentPage Header="Get Started">
        <StackPanel VerticalAlignment="Center"
                    HorizontalAlignment="Center"
                    Spacing="16">
            <TextBlock Text="Ready?"
                       FontSize="28"
                       HorizontalAlignment="Center" />
            <Button Content="Get Started"
                    HorizontalAlignment="Center"
                    Click="OnGetStartedClick" />
        </StackPanel>
    </ContentPage>

</CarouselPage>
```

### 在代码中使用 CarouselPage {#carouselpage-in-code}

```csharp
var carousel = new CarouselPage
{
    Pages = new AvaloniaList<Page>
    {
        new ContentPage { Header = "Step 1", Content = step1View },
        new ContentPage { Header = "Step 2", Content = step2View },
        new ContentPage { Header = "Step 3", Content = step3View }
    }
};

window.Page = carousel;
```

<Image light={CarouselPageBasicScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

### Page Transitions

用内置过渡为页面切换加上动画：

```csharp
var carousel = new CarouselPage
{
    PageTransition = new PageSlide(TimeSpan.FromMilliseconds(300))
};

// Other available transitions
carousel.PageTransition = new CrossFade(TimeSpan.FromMilliseconds(300));
carousel.PageTransition = new PageSlide(TimeSpan.FromMilliseconds(300), PageSlide.SlideAxis.Vertical);
```

在 XAML 中，`PageSlide` 横向和纵向都支持：

```xml
<CarouselPage>
    <CarouselPage.PageTransition>
        <PageSlide Duration="0:0:0.3" Orientation="Horizontal" />
    </CarouselPage.PageTransition>
    <!-- pages -->
</CarouselPage>
```

### Programmatic Navigation

```csharp
// Jump to a specific page by index
carousel.SelectedIndex = 2;

// Navigate forward
private void OnNext()
{
    var pageCount = (carousel.Pages as IList)?.Count ?? 0;
    if (carousel.SelectedIndex < pageCount - 1)
        carousel.SelectedIndex++;
}

// Navigate backward
private void OnPrevious()
{
    if (carousel.SelectedIndex > 0)
        carousel.SelectedIndex--;
}
```

### 响应页面切换 {#responding-to-page-changes}

`SelectionChanged` 事件通过 `PageSelectionChangedEventArgs` 提供 `PreviousPage` 和 `CurrentPage`：

```csharp
carousel.SelectionChanged += (sender, e) =>
{
    var pageCount = (carousel.Pages as IList)?.Count ?? 0;
    Console.WriteLine($"Page {carousel.SelectedIndex + 1} of {pageCount}: {e.CurrentPage?.Header}");
};
```

### Tracking Navigation Lifecycle Events

订阅各个子页面上的生命周期事件，即可跟踪它们何时变为活动或非活动状态：

```csharp
var page = new ContentPage { Header = "Home" };

page.NavigatedTo += (_, args) =>
    Console.WriteLine($"NavigatedTo: Home (from {(args.PreviousPage as ContentPage)?.Header})");

page.NavigatedFrom += (_, args) =>
    Console.WriteLine($"NavigatedFrom: Home (to {(args.DestinationPage as ContentPage)?.Header})");
```

也可以在子类中重写这些生命周期方法：

```csharp
public partial class FeaturePage : ContentPage
{
    protected override void OnNavigatedTo(NavigatedToEventArgs args)
    {
        base.OnNavigatedTo(args);
        // This page is now visible, start animations or load data.
        _ = PlayIntroAnimationAsync();
    }
}
```

### 配置手势与键盘 {#configuring-gestures-and-keyboard}

手势导航与键盘导航可以分别开关：

```xml
<CarouselPage IsGestureEnabled="True"
              IsKeyboardNavigationEnabled="True">
    <CarouselPage.PageTransition>
        <PageSlide Duration="0:0:0.3" Orientation="Horizontal" />
    </CarouselPage.PageTransition>
    <!-- pages -->
</CarouselPage>
```

```csharp
// Disable swipe when content has conflicting horizontal scroll
carousel.IsGestureEnabled = false;

// Disable keyboard when embedded in a form with its own arrow key handling
carousel.IsKeyboardNavigationEnabled = false;
```

### 用 ItemsSource 做数据驱动的页面 {#data-driven-pages-with-itemssource}

一旦设置了 `ItemsSource`，它的优先级就高于 `Pages`。请用 `PageTemplate` 把每一项转换成 `Page`：

```xml
<CarouselPage xmlns="https://github.com/avaloniaui"
              xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
              xmlns:vm="clr-namespace:MyApp.ViewModels"
              x:Class="MyApp.PhotoCarousel"
              ItemsSource="{Binding Photos}">

    <CarouselPage.PageTemplate>
        <DataTemplate x:DataType="vm:PhotoViewModel">
            <ContentPage Header="{Binding Title}">
                <Image Source="{Binding ImageSource}"
                       Stretch="Uniform" />
            </ContentPage>
        </DataTemplate>
    </CarouselPage.PageTemplate>

</CarouselPage>
```

在代码中，用 `ObservableCollection` 实现动态更新，用 `FuncDataTemplate` 创建页面：

```csharp
var items = new ObservableCollection<PhotoViewModel>(viewModel.Photos);

var carousel = new CarouselPage
{
    ItemsSource = items,
    PageTemplate = new FuncDataTemplate<PhotoViewModel>((photo, _) =>
        new ContentPage
        {
            Header = photo.Title,
            Content = new Image
            {
                Source = photo.ImageSource,
                Stretch = Stretch.Uniform
            }
        })
};

// Add or remove items at runtime, the carousel updates automatically
items.Add(new PhotoViewModel { Title = "New Photo", ImageSource = newBitmap });
```

<Image light={CarouselPageDataTemplateScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

### 把 CarouselPage 放进 NavigationPage {#carouselpage-inside-a-navigationpage}

把 `CarouselPage` 嵌进 `NavigationPage` 即可获得堆栈式导航：

```csharp
window.Page = new NavigationPage { Content = new OnboardingCarousel() };
```

`CarouselPage.Header` 会显示在导航栏标题处；当堆栈深度大于 1 时，返回按钮就会出现。

### Dynamic Page Management

页面可以在运行时增删，轮播会自动跟着更新：

```csharp
var pages = new AvaloniaList<Page>();
carousel.Pages = pages;

// Add a page
pages.Add(new ContentPage
{
    Header = "New Page",
    Content = new TextBlock { Text = "Added dynamically" }
});

// Remove a page
if (pages.Count > 1)
    pages.RemoveAt(pages.Count - 1);
```

## 另请参阅 {#see-also}

- [API 参考](/api/avalonia/controls/carouselpage)
- [源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Page/CarouselPage.cs)

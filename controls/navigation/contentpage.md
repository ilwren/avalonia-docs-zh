---
id: contentpage
title: ContentPage
description: '`ContentPage` 是 Avalonia 应用中构建屏幕的基础积木。它承载单个根视图，并与其他页面容器协同工作。'
doc-type: reference
---

import ContentPageInNavigationScreenshot from '/img/controls/contentpage/contentpage-in-navigationpage.png';
import ContentPageStandaloneScreenshot from '/img/controls/contentpage/contentpage-standalone.png';
import ContentPageTopCommandBarScreenshot from '/img/controls/contentpage/contentpage-top-commandbar.png';
import ContentPageBottomCommandBarScreenshot from '/img/controls/contentpage/contentpage-bottom-commandbar.png';
import ContentPageSafeAreaDisabledScreenshot from '/img/controls/contentpage/contentpage-safe-area-disabled.png';
import ContentPageAsTabScreenshot from '/img/controls/contentpage/contentpage-as-tab.png';

[`ContentPage`](/api/avalonia/controls/contentpage) 是 Avalonia 中构建屏幕式界面的基础积木，代表一页内容，并内置了对页头、图标、安全区内边距和命令栏的支持。用户看到的每一屏，通常都是一个 `ContentPage`（或它的子类）。

`ContentPage` 最常见的用法是作为 [`NavigationPage`](/controls/navigation/navigationpage)、[`TabbedPage`](/controls/navigation/tabbedpage) 或 [`DrawerPage`](/controls/navigation/drawerpage) 的子元素；单页应用中也可以把它直接放进 [`Window`](/api/avalonia/controls/window)。

## 页头如何显示 {#how-the-header-displays}

`Header` 属性的作用取决于承载该页面的是哪种容器：

| 宿主控件 | 页头出现的位置 |
| --- | --- |
| [`NavigationPage`](/api/avalonia/controls/navigationpage) | 显示在屏幕顶部的导航栏中。 |
| [`TabbedPage`](/api/avalonia/controls/tabbedpage) | 用作选项卡的标签文字。 |
| [`DrawerPage`](/api/avalonia/controls/drawerpage) | 对子 `ContentPage` 内容不会自动显示。请使用 `DrawerPage.Header`、`DrawerHeader`，或自行渲染页头内容。 |
| 独立使用（放在 `Window` 中） | 不会自动显示。如有需要，得你自己渲染。 |

## 常用属性 {#useful-properties}

### ContentPage 的属性 {#contentpage-properties}

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `Content` | `object?` | `null` | 页面上显示的主体内容。它不能又是一个 `Page`；要承载子页面，请用 `NavigationPage`、`TabbedPage`、`DrawerPage` 或其他 `MultiPage` 控件。 |
| `ContentTemplate` | `IDataTemplate?` | `null` | 用于渲染内容的数据模板。 |
| `Header` | `object?` | `null` | 页头。当页面由 `NavigationPage` 承载时，它显示在导航栏中。 |
| `HeaderTemplate` | `IDataTemplate?` | `null` | 用于渲染页头的数据模板。 |
| `Icon` | `object?` | `null` | 页面图标。当页面由 `TabbedPage` 承载时，它显示在选项卡栏中。 |
| `IconTemplate` | `IDataTemplate?` | `null` | 用于渲染图标的数据模板。 |
| `Background` | `IBrush?` | `null` | 页面背景画刷。若要用图片作背景，请使用 `ImageBrush` 并设置它的 `Stretch` 属性。 |
| `AutomaticallyApplySafeAreaPadding` | `bool` | `true` | 自动为设备安全区（刘海、状态栏）调整内边距。 |
| `TopCommandBar` | `object?` | `null` | 显示在页面内容上方命令栏区域中的内容。 |
| `BottomCommandBar` | `object?` | `null` | 显示在页面内容下方命令栏区域中的内容。 |
| `HorizontalContentAlignment` | `HorizontalAlignment` | `Stretch` | 页面内容的水平对齐方式。 |
| `VerticalContentAlignment` | `VerticalAlignment` | `Stretch` | 页面内容的垂直对齐方式。 |
| `SafeAreaPadding` | `Thickness` | `0` | 页面当前被赋予的安全区内边距。安全区边衬变化时，页面容器会更新该值。 |

### Page 基类的属性 {#page-base-properties}

下列属性继承自 `Page`，所有页面类型都有：

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `Navigation` | `INavigation?` | `null` | 提供对承载它的 `NavigationPage` 的访问，用于入栈/出栈操作。 |
| `CurrentPage` | `Page?` | `null` | 页面容器控件当前活动的子页面。对 `ContentPage` 而言，它通常就是 `null`。 |
| `IsInNavigationPage` | `bool` | `false` | 指示该页面当前是否由 `NavigationPage` 承载。 |

## 导航事件 {#navigation-events}

每个 `Page`（包括 `ContentPage`）都支持在导航期间触发的生命周期事件。一次导航发生时，这些事件按固定顺序触发：

| 事件 | 说明 | 顺序 |
| --- | --- | --- |
| `Navigating` | 在离开**当前**页面之前，于该页面上引发。它使用 `NavigatingFromEventArgs`，可通过 `e.Cancel = true` 取消导航。 | 1 |
| `NavigatedFrom` | 导航完成之后，在**原**页面上引发。 | 2 |
| `NavigatedTo` | 导航完成之后，在**新**页面上引发。 | 3 |

### 重写生命周期方法 {#overriding-lifecycle-methods}

除了订阅事件，你也可以重写对应的 `protected` 方法：

```csharp
public class HomePage : ContentPage
{
    protected override void OnNavigatedTo(NavigatedToEventArgs args)
    {
        base.OnNavigatedTo(args);
        // Page is now visible, load or refresh data here
    }

    protected override void OnNavigatingFrom(NavigatingFromEventArgs args)
    {
        base.OnNavigatingFrom(args);
        if (HasUnsavedChanges)
        {
            args.Cancel = true; // Prevent navigation away
        }
    }

    protected override void OnNavigatedFrom(NavigatedFromEventArgs args)
    {
        base.OnNavigatedFrom(args);
        // Page is no longer visible, clean up resources
    }
}
```

:::note
`NavigatedTo` 和 `Loaded` 事件不是一回事。`Loaded` 只在控件首次加入视觉树时触发一次，而 `NavigatedTo` 每次页面成为活动页时都会触发（比如用户点返回回到它时）。
:::

## 示例 {#examples}

### 最简 XAML 页面 {#minimal-xaml-page}

一个内联内容的最简 `ContentPage`：

```xml
<ContentPage xmlns="https://github.com/avaloniaui"
             Header="Home">
    <TextBlock Text="Hello, world!" Margin="16" />
</ContentPage>
```

### 在代码中创建 ContentPage {#creating-a-contentpage-in-code}

```csharp
var page = new ContentPage
{
    Header = "Home",
    Content = new TextBlock
    {
        Text = "Hello from code!",
        Margin = new Thickness(16)
    }
};
```

### NavigationPage 中的 ContentPage {#contentpage-inside-a-navigationpage}

当页面由 `NavigationPage` 承载时，`Header` 会显示在导航栏中：

```xml
<NavigationPage xmlns="https://github.com/avaloniaui">
    <ContentPage Header="Dashboard">
        <StackPanel Margin="16" Spacing="8">
            <TextBlock Text="Welcome back!" FontSize="24" FontWeight="Bold" />
            <Button Content="Go to Details" Click="OnGoToDetails" />
        </StackPanel>
    </ContentPage>
</NavigationPage>
```

<Image light={ContentPageInNavigationScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="ContentPage inside a NavigationPage"/>

### 把 ContentPage 作为窗口根元素 {#contentpage-as-a-window-root}

单页应用可以把 `ContentPage` 直接放进 `Window`：

```xml
<Window xmlns="https://github.com/avaloniaui"
        Title="My App">
    <ContentPage>
        <StackPanel Margin="16" Spacing="8">
            <TextBlock Text="Single-page app" FontSize="24" />
            <TextBlock Text="No navigation container needed." />
        </StackPanel>
    </ContentPage>
</Window>
```

<Image light={ContentPageStandaloneScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="ContentPage standalone in a Window"/>

### 可滚动的布局 {#scrollable-layout}

`ContentPage` 本身不带滚动视图。如果内容可能超出屏幕，请把它包进 `ScrollViewer`：

```xml
<ContentPage xmlns="https://github.com/avaloniaui"
             Header="Long Content">
    <ScrollViewer>
        <StackPanel Margin="16" Spacing="8">
            <TextBlock Text="Item 1" />
            <TextBlock Text="Item 2" />
            <TextBlock Text="Item 3" />
            <!-- Many more items -->
        </StackPanel>
    </ScrollViewer>
</ContentPage>
```

### MVVM 绑定 {#mvvm-binding}

用 `ContentTemplate` 把页面内容绑定到视图模型：

```xml
<ContentPage xmlns="https://github.com/avaloniaui"
             Header="{Binding Title}"
             Content="{Binding}">
    <ContentPage.ContentTemplate>
        <DataTemplate>
            <StackPanel Margin="16" Spacing="8">
                <TextBlock Text="{Binding Description}" FontSize="18" />
                <TextBlock Text="{Binding Detail}" />
            </StackPanel>
        </DataTemplate>
    </ContentPage.ContentTemplate>
</ContentPage>
```

### TopCommandBar

在页面内容上方显示一个工具栏：

```xml
<ContentPage xmlns="https://github.com/avaloniaui"
             Header="Inbox">
    <ContentPage.TopCommandBar>
        <StackPanel Orientation="Horizontal" Spacing="4" Margin="8">
            <Button Content="Filter" />
            <Button Content="Sort" />
        </StackPanel>
    </ContentPage.TopCommandBar>

    <TextBlock Text="Messages go here" Margin="16" />
</ContentPage>
```

<Image light={ContentPageTopCommandBarScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="ContentPage with a top command bar"/>

### BottomCommandBar

在页面内容下方显示一个工具栏：

```xml
<ContentPage xmlns="https://github.com/avaloniaui"
             Header="Settings">
    <ContentPage.BottomCommandBar>
        <StackPanel Orientation="Horizontal" Spacing="8" Margin="8">
            <Button Content="Save" />
            <Button Content="Cancel" />
        </StackPanel>
    </ContentPage.BottomCommandBar>

    <TextBlock Text="Page content goes here" Margin="16" />
</ContentPage>
```

<Image light={ContentPageBottomCommandBarScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="ContentPage with a bottom command bar"/>

### 取消导航 {#cancelling-navigation}

用 `Navigating` 事件、或重写 `OnNavigatingFrom`，可以在有未保存改动时阻止用户离开页面：

```csharp
public class EditPage : ContentPage
{
    public bool HasUnsavedChanges { get; set; }

    protected override void OnNavigatingFrom(NavigatingFromEventArgs args)
    {
        base.OnNavigatingFrom(args);

        if (HasUnsavedChanges)
        {
            args.Cancel = true;
            // Optionally show a confirmation dialog here
        }
    }
}
```

### 拦截系统返回键 {#intercepting-the-system-back-button}

在带有硬件或系统返回键的平台上（Android、浏览器），`Navigating` 会在返回动作发生之前触发。取消它同时也会取消系统的返回导航：

```csharp
protected override void OnNavigatingFrom(NavigatingFromEventArgs args)
{
    base.OnNavigatingFrom(args);

    if (ShouldPreventBack())
    {
        args.Cancel = true;
    }
}
```

### 页面重新出现时刷新数据 {#refreshing-data-when-the-page-reappears}

`NavigatedTo` 在页面每次变为活动状态时触发，正是刷新数据的好时机：

```csharp
public class OrdersPage : ContentPage
{
    protected override async void OnNavigatedTo(NavigatedToEventArgs args)
    {
        base.OnNavigatedTo(args);
        await ViewModel.LoadOrdersAsync();
    }
}
```

### 全屏贯通布局（关闭安全区内边距） {#full-bleed-layout-disabling-safe-area-padding}

把 `AutomaticallyApplySafeAreaPadding` 设为 `false`，内容就能延伸到刘海和状态栏下方：

```xml
<ContentPage xmlns="https://github.com/avaloniaui"
             AutomaticallyApplySafeAreaPadding="False">
    <Image Source="avares://MyApp/Assets/hero.jpg"
           Stretch="UniformToFill" />
</ContentPage>
```

<Image light={ContentPageSafeAreaDisabledScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="ContentPage with safe area padding disabled"/>

### 图片背景 {#image-background}

`ContentPage` 没有 `BackgroundImage` 和 `BackgroundImageStretch` 属性。请改用继承而来的 `Background` 属性，配上 `ImageBrush`：

```xml
<ContentPage xmlns="https://github.com/avaloniaui"
             Header="Welcome">
    <ContentPage.Background>
        <ImageBrush Source="avares://MyApp/Assets/background.jpg"
                    Stretch="UniformToFill" />
    </ContentPage.Background>

    <TextBlock Text="Page content" Margin="16" />
</ContentPage>
```

### 带图标的选项卡 {#tab-with-icon}

当页面用在 `TabbedPage` 中时，`Header` 和 `Icon` 属性决定选项卡的外观：

```xml
<TabbedPage xmlns="https://github.com/avaloniaui"
            TabPlacement="Bottom">
    <ContentPage Header="Home">
        <ContentPage.Icon>
            <PathIcon Data="{StaticResource HomeIcon}" />
        </ContentPage.Icon>
        <TextBlock Text="Home content" Margin="16" />
    </ContentPage>
    <ContentPage Header="Settings">
        <ContentPage.Icon>
            <PathIcon Data="{StaticResource SettingsIcon}" />
        </ContentPage.Icon>
        <TextBlock Text="Settings content" Margin="16" />
    </ContentPage>
</TabbedPage>
```

<Image light={ContentPageAsTabScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="ContentPage used as a tab in TabbedPage"/>

## 另请参阅 {#see-also}

- [NavigationPage](/controls/navigation/navigationpage)
- [TabbedPage](/controls/navigation/tabbedpage)
- [DrawerPage](/controls/navigation/drawerpage)
- [ContentPage API 参考](/api/avalonia/controls/contentpage)
- [GitHub 上的 `ContentPage.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Page/ContentPage.cs)

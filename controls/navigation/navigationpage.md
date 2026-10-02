---
id: navigationpage
title: NavigationPage
description: '`NavigationPage` 提供基于栈的页面导航，自带导航栏、返回按钮，还可以为每个页面配上专属命令栏。'
doc-type: reference
---

import NavigationPageRootScreenshot from '/img/controls/navigationpage/navigationpage-root.png';
import NavigationPagePushedScreenshot from '/img/controls/navigationpage/navigationpage-pushed.png';
import NavigationPageCustomBackButtonScreenshot from '/img/controls/navigationpage/navigationpage-custom-back-button.png';
import NavigationPageNoNavbarScreenshot from '/img/controls/navigationpage/navigationpage-no-navbar.png';
import NavigationPageOverlayBarScreenshot from '/img/controls/navigationpage/navigationpage-overlay-bar.png';
import NavigationPageTopCommandBarScreenshot from '/img/controls/navigationpage/navigationpage-top-commandbar.png';
import NavigationPageAppearanceScreenshot from '/img/controls/navigationpage/navigationpage-appearance.png';
import NavigationPageModalScreenshot from '/img/controls/navigationpage/navigationpage-modal.png';
import NavigationPageDrawerIntegrationScreenshot from '/img/controls/navigationpage/navigationpage-drawer-integration.png';

[`NavigationPage`](/api/avalonia/controls/navigationpage) 管理一套基于栈的导航系统，让你把页面推入、弹出，并配上过渡动画。它会显示一个导航栏，其中含返回按钮和当前页面的页头。

`NavigationPage` 实现了 `INavigation` 接口，提供了一整套异步导航方法，用于推入、弹出和替换页面。

## 导航栏的布局 {#navigation-bar-layout}

导航栏分为三个区域：

| 区域 | 内容 |
| --- | --- |
| Left | 返回按钮（在合适的时候）或自定义的 `BackButtonContent` |
| Center | 当前页面的 `Header` |
| Right | 来自 `NavigationPage.TopCommandBar` 的、各页面专属的命令内容 |

## 常用属性 {#useful-properties}

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `Content` | `object?` | `null` | 导航栈中显示的初始根页面，赋值为一个 [`Page`](/api/avalonia/controls/page) 实例。 |
| `PageTransition` | [`IPageTransition?`](/api/avalonia/animation/ipagetransition) | 主题默认值 | 页面之间导航时使用的过渡动画。 |
| `ModalTransition` | `IPageTransition?` | 主题默认值 | 呈现或关闭模态页面时使用的过渡动画。 |
| `HasShadow` | `bool` | `false` | 在导航栏下方显示阴影。 |
| `BarHeight` | `double` | `48` | 导航栏的高度。 |
| `EffectiveBarHeight` | `double` | Computed | 只读。计入安全区边衬与各项覆盖设置之后，导航栏的实际高度。 |
| `IsBackButtonVisible` | `bool` | `true` | 控制在可以返回时是否显示返回按钮。 |
| `IsGestureEnabled` | `bool` | `true` | 启用滑动手势来返回上一页。 |
| `IsNavigating` | `bool` | `false` | 只读。导航操作进行期间返回 `true`。 |
| `CanGoBack` | `bool` | `false` | 只读。当导航栈中不止一个页面时返回 `true`。 |
| `IsBackButtonEffectivelyVisible` | `bool` | Computed | 只读。综合栈深度、`IsBackButtonVisible` 以及各页面的覆盖设置后，返回按钮最终的可见性。 |
| `NavigationStack` | `IReadOnlyList<Page>` | Empty | 只读。当前的页面栈。 |
| `ModalStack` | `IReadOnlyList<Page>` | Empty | 只读。当前的模态页面栈。 |
| `StackDepth` | `int` | `0` | 只读。导航栈中的页面数量。 |

## 附加属性 {#attached-properties}

下列属性可以设在单个 `Page` 实例上，用来定制它在 `NavigationPage` 中的外观：

| Attached Property | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `NavigationPage.HasNavigationBar` | `bool` | `true` | 该页面是否显示导航栏。 |
| `NavigationPage.HasBackButton` | `bool` | `true` | 该页面是否显示返回按钮。 |
| `NavigationPage.IsBackButtonEnabled` | `bool` | `true` | 该页面的返回按钮是否可用。 |
| `NavigationPage.BackButtonContent` | `object?` | `null` | 返回按钮的自定义内容。 |
| `NavigationPage.TopCommandBar` | `Control?` | `null` | 该页面显示在导航栏右侧的命令内容。 |
| `NavigationPage.BottomCommandBar` | `Control?` | `null` | 显示在页面内容下方的命令栏。 |
| `NavigationPage.BarLayoutBehavior` | `BarLayoutBehavior?` | `null` | 控制导航栏与页面内容之间的相处方式。 |
| `NavigationPage.BarHeightOverride` | `double?` | `null` | 为该页面单独指定导航栏高度。 |

### BarLayoutBehavior 的取值 {#barlayoutbehavior-values}

| 值 | 说明 |
| --- | --- |
| `Inset` | 导航栏把页面内容往下挤，这是默认行为。 |
| `Overlay` | 导航栏浮在页面内容之上，不影响内容布局。 |

## 导航方法 {#navigation-methods}

会改变当前可见页面的导航方法都是异步的，返回 `Task`。它们都有一个接受 `IPageTransition` 参数的重载，可用于覆盖默认过渡。`InsertPage` 和 `RemovePage` 只修改栈而不播放动画，返回 `void`。

| 方法 | 说明 |
| --- | --- |
| `PushAsync(Page)` | 把一个新页面推入导航栈。 |
| `PopAsync()` | 把当前页面从栈中移除并返回它。 |
| `PopToRootAsync()` | 弹出除根页面之外的所有页面。 |
| `PopToPageAsync(Page)` | 不断弹出页面，直到指定页面位于栈顶。 |
| `ReplaceAsync(Page)` | 用新页面替换当前页面。 |
| `InsertPage(Page, Page)` | 把一个页面插入到指定页面之前。 |
| `RemovePage(Page)` | 把指定页面从栈中移除。 |

### 模态导航 {#modal-navigation}

| 方法 | 说明 |
| --- | --- |
| `PushModalAsync(Page)` | 以模态浮层的形式呈现一个页面。 |
| `PopModalAsync()` | 关闭当前模态页面并返回它。 |
| `PopAllModalsAsync()` | 关闭所有模态页面。 |

### 栈相关属性 {#stack-properties}

| 属性 | 说明 |
| --- | --- |
| `NavigationStack` | 只读列表，列出当前位于导航栈中的页面。 |
| `ModalStack` | 只读列表，列出当前以模态形式呈现的页面。 |
| `StackDepth` | 导航栈中的页面数量。 |
| `CanGoBack` | 当栈中不止一个页面时返回 `true`。 |

## 事件 {#events}

| 事件 | 说明 |
| --- | --- |
| `Pushed` | 页面被推入栈之后引发。 |
| `Popped` | 页面被弹出栈之后引发。 |
| `PoppedToRoot` | 所有页面被弹回根页面之后引发。 |
| `PageInserted` | 页面被插入栈之后引发。 |
| `PageRemoved` | 页面被移出栈之后引发。 |
| `ModalPushed` | 模态页面呈现之后引发。 |
| `ModalPopped` | 模态页面关闭之后引发。 |

## 示例 {#examples}

### XAML 中的基础 NavigationPage {#basic-navigationpage-in-xaml}

定义一个带初始根页面的 `NavigationPage`：

```xml
<NavigationPage xmlns="https://github.com/avaloniaui">
    <ContentPage Header="Home">
        <StackPanel Margin="16" Spacing="8">
            <TextBlock Text="Home Page" FontSize="24" />
            <Button Content="Go to Details" Click="OnGoToDetails" />
        </StackPanel>
    </ContentPage>
</NavigationPage>
```

<Image light={NavigationPageRootScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="NavigationPage with root page"/>

### 代码中的基础 NavigationPage {#basic-navigationpage-in-code}

你也可以在代码里创建 `NavigationPage` 并设置它的根页面：

```csharp
var navigationPage = new NavigationPage
{
    Content = new ContentPage
    {
        Header = "Home",
        Content = new StackPanel
        {
            Margin = new Thickness(16),
            Spacing = 8,
            Children =
            {
                new TextBlock { Text = "Home Page", FontSize = 24 },
                new Button { Content = "Go to Details" }
            }
        }
    }
};
```

### 推入与弹出页面 {#pushing-and-popping-pages}

每个 `Page` 都有一个 `Navigation` 属性（类型为 `INavigation`），指向最近的 `NavigationPage` 祖先。在任意页面内都可以靠它来导航：

```csharp
// Push a new page onto the stack
await Navigation.PushAsync(new DetailsPage());

// Pop back to the previous page
await Navigation.PopAsync();

// Pop all the way back to the root page
await Navigation.PopToRootAsync();
```

<Image light={NavigationPagePushedScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="NavigationPage after pushing a page"/>

### 跟踪栈深度 {#tracking-stack-depth}

用 `StackDepth` 属性或 `CanGoBack` 属性响应导航变化：

```csharp
navigationPage.Pushed += (sender, args) =>
{
    Console.WriteLine($"Stack depth: {navigationPage.StackDepth}");
    Console.WriteLine($"Can go back: {navigationPage.CanGoBack}");
};

navigationPage.Popped += (sender, args) =>
{
    Console.WriteLine($"Returned to: {navigationPage.NavigationStack.Last().Header}");
};
```

### 隐藏导航栏 {#hiding-the-navigation-bar}

在页面上把 `NavigationPage.HasNavigationBar` 附加属性设为 `False`，即可为该页面隐藏导航栏：

```xml
<ContentPage xmlns="https://github.com/avaloniaui"
             Header="Immersive View"
             NavigationPage.HasNavigationBar="False">
    <!-- Full-screen content with no navigation bar -->
    <Image Source="avares://MyApp/Assets/hero.jpg" Stretch="UniformToFill" />
</ContentPage>
```

<Image light={NavigationPageNoNavbarScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="NavigationPage with hidden navigation bar"/>

### 隐藏返回按钮 {#hiding-the-back-button}

在页面上把 `NavigationPage.HasBackButton` 附加属性设为 `False`，即可只隐藏返回按钮而保留导航栏：

```xml
<ContentPage xmlns="https://github.com/avaloniaui"
             Header="No Back Button"
             NavigationPage.HasBackButton="False">
    <TextBlock Text="The back button is hidden on this page" Margin="16" />
</ContentPage>
```

### 自定义返回按钮内容 {#custom-back-button-content}

用 `NavigationPage.BackButtonContent` 附加属性为返回按钮提供自定义内容：

```xml
<ContentPage xmlns="https://github.com/avaloniaui"
             Header="Custom Back">
    <NavigationPage.BackButtonContent>
        <StackPanel Orientation="Horizontal" Spacing="4">
            <PathIcon Data="{StaticResource ArrowLeftIcon}" />
            <TextBlock Text="Return" VerticalAlignment="Center" />
        </StackPanel>
    </NavigationPage.BackButtonContent>

    <TextBlock Text="Page with custom back button" Margin="16" />
</ContentPage>
```

<Image light={NavigationPageCustomBackButtonScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="NavigationPage with custom back button content"/>

### 为单个页面设置 TopCommandBar {#per-page-topcommandbar}

用 `NavigationPage.TopCommandBar` 附加属性，为某个页面在导航栏右侧添加命令内容：

```xml
<ContentPage xmlns="https://github.com/avaloniaui"
             Header="Search">
    <NavigationPage.TopCommandBar>
        <CommandBar IsDynamicOverflowEnabled="True">
            <CommandBar.PrimaryCommands>
                <CommandBarButton Label="Search">
                    <CommandBarButton.Icon>
                        <PathIcon Data="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3Z" />
                    </CommandBarButton.Icon>
                </CommandBarButton>
                <CommandBarButton Label="Share" />
            </CommandBar.PrimaryCommands>
        </CommandBar>
    </NavigationPage.TopCommandBar>

    <TextBlock Text="Search results appear here" Margin="16" />
</ContentPage>
```

<Image light={NavigationPageTopCommandBarScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="NavigationPage with top command bar"/>

### 页面过渡 {#page-transitions}

定制推入和弹出页面时使用的过渡动画：

```xml
<NavigationPage xmlns="https://github.com/avaloniaui">
    <NavigationPage.PageTransition>
        <PageSlide Duration="0:00:00.300" Orientation="Horizontal" />
    </NavigationPage.PageTransition>

    <ContentPage Header="Home">
        <TextBlock Text="Slide transitions" Margin="16" />
    </ContentPage>
</NavigationPage>
```

你也可以只为某一次导航调用覆盖过渡效果：

```csharp
var customTransition = new PageSlide(TimeSpan.FromMilliseconds(500));
await Navigation.PushAsync(new DetailsPage(), customTransition);
```

<Image light={NavigationPageAppearanceScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="NavigationPage appearance and transitions"/>

### 模态页面 {#modal-pages}

模态页面呈现在当前导航栈之上，它们有自己独立的栈：

```csharp
// Present a modal page
await Navigation.PushModalAsync(new LoginPage());

// Dismiss the modal page
await Navigation.PopModalAsync();

// Dismiss all modal pages at once
await Navigation.PopAllModalsAsync();
```

<Image light={NavigationPageModalScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="NavigationPage with modal page"/>

### 模态过渡 {#modal-transitions}

模态页面的过渡动画可以与普通页面过渡分开定制：

```xml
<NavigationPage xmlns="https://github.com/avaloniaui">
    <NavigationPage.ModalTransition>
        <PageSlide Duration="0:00:00.400" Orientation="Vertical" />
    </NavigationPage.ModalTransition>

    <ContentPage Header="Home">
        <Button Content="Show Modal" Click="OnShowModal" />
    </ContentPage>
</NavigationPage>
```

### 定制导航栏高度 {#customizing-bar-height}

既可以为所有页面统一设置导航栏高度，也可以为某个页面单独覆盖：

```xml
<!-- Global bar height -->
<NavigationPage xmlns="https://github.com/avaloniaui"
                BarHeight="64">
    <ContentPage Header="Tall Bar">
        <TextBlock Text="This page has a taller navigation bar" Margin="16" />
    </ContentPage>
</NavigationPage>
```

```xml
<!-- Per-page bar height override -->
<ContentPage xmlns="https://github.com/avaloniaui"
             Header="Custom Height"
             NavigationPage.BarHeightOverride="72">
    <TextBlock Text="This page overrides the bar height" Margin="16" />
</ContentPage>
```

### 导航栏阴影 {#navigation-bar-shadow}

在导航栏下方加一层阴影，带来淡淡的层次感：

```xml
<NavigationPage xmlns="https://github.com/avaloniaui"
                HasShadow="True">
    <ContentPage Header="Home">
        <TextBlock Text="The navigation bar has a shadow" Margin="16" />
    </ContentPage>
</NavigationPage>
```

### 浮层式导航栏 {#overlay-navigation-bar}

用 `BarLayoutBehavior` 附加属性，让导航栏浮在页面内容之上，而不是把内容往下挤：

```xml
<ContentPage xmlns="https://github.com/avaloniaui"
             Header="Overlay"
             NavigationPage.BarLayoutBehavior="Overlay">
    <!-- Content extends behind the navigation bar -->
    <Image Source="avares://MyApp/Assets/hero.jpg" Stretch="UniformToFill" />
</ContentPage>
```

<Image light={NavigationPageOverlayBarScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="NavigationPage with overlay bar layout"/>

### 替换登录页 {#replacing-a-login-screen}

用 `ReplaceAsync` 换掉当前页面而不往返回栈里加东西。登录成功后把登录页换成主界面，正适合这么做：

```csharp
// After successful login, replace the login page with the main page
await Navigation.ReplaceAsync(new MainPage());
```

用户将无法再返回到被替换掉的那个页面。

### 与 DrawerPage 的集成 {#drawerpage-integration}

当 `DrawerPage` 把 `NavigationPage` 作为它的 `Content` 时，栈根部的导航栏里会显示汉堡菜单图标；一旦有页面被推入，它会自动切换成返回按钮：

```xml
<DrawerPage xmlns="https://github.com/avaloniaui"
            DrawerLength="280">
    <DrawerPage.Drawer>
        <StackPanel Spacing="4" Margin="8">
            <Button Content="Home" />
            <Button Content="Settings" />
        </StackPanel>
    </DrawerPage.Drawer>

    <NavigationPage>
        <ContentPage Header="Home">
            <StackPanel Margin="16" Spacing="8">
                <TextBlock Text="Home Page" FontSize="24" />
                <Button Content="Go to Details" Click="OnGoToDetails" />
            </StackPanel>
        </ContentPage>
    </NavigationPage>
</DrawerPage>
```

<Image light={NavigationPageDrawerIntegrationScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="NavigationPage with DrawerPage integration"/>

### 停用侧滑返回手势 {#disabling-back-swipe-gesture}

全局停用侧滑返回手势，或查询它当前是否启用：

```xml
<NavigationPage xmlns="https://github.com/avaloniaui"
                IsGestureEnabled="False">
    <ContentPage Header="No Swipe">
        <TextBlock Text="Back-swipe gesture is disabled" Margin="16" />
    </ContentPage>
</NavigationPage>
```

## 另请参阅 {#see-also}

- [ContentPage](/controls/navigation/contentpage)
- [TabbedPage](/controls/navigation/tabbedpage)
- [DrawerPage](/controls/navigation/drawerpage)
- [Page Transitions](/docs/graphics-animation/page-transitions)
- [NavigationPage API 参考](/api/avalonia/controls/navigationpage)
- [GitHub 上的 `NavigationPage.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Page/NavigationPage.cs)

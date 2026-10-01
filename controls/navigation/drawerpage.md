---
id: drawerpage
title: DrawerPage
description: '`DrawerPage` 把一个可滑出的抽屉面板与主内容区组合在一起。抽屉既可以作为浮层滑出，也可以作为分栏侧边栏常驻在内容旁边，还可以呈现为紧凑的导航栏。'
doc-type: reference
---

import DrawerPageClosedScreenshot from '/img/controls/drawerpage/drawerpage-closed.png';
import DrawerPageOpenScreenshot from '/img/controls/drawerpage/drawerpage-open.png';
import DrawerPageHeaderFooterScreenshot from '/img/controls/drawerpage/drawerpage-header-footer.png';
import DrawerPageCompactCollapsedScreenshot from '/img/controls/drawerpage/drawerpage-compact-collapsed.png';
import DrawerPageCompactExpandedScreenshot from '/img/controls/drawerpage/drawerpage-compact-expanded.png';
import DrawerPageSplitScreenshot from '/img/controls/drawerpage/drawerpage-split.png';
import DrawerPageRightScreenshot from '/img/controls/drawerpage/drawerpage-right.png';
import DrawerPageRtlScreenshot from '/img/controls/drawerpage/drawerpage-rtl.png';

[`DrawerPage`](/api/avalonia/controls/drawerpage) 把一个可滑出的抽屉面板与主内容区组合在一起，是应用中常见的导航范式。它构建在 `SplitView` 之上，并补充了基于页面的各项能力，比如生命周期事件、安全区支持，以及与 [`NavigationPage`](/api/avalonia/controls/navigationpage) 的自动集成。

当 `DrawerPage` 的 `Content` 是 `NavigationPage` 时，导航栈根部会在导航栏中显示抽屉开关按钮；一旦导航栈里不止一个页面，它会自动切换成返回按钮。

:::info
`DrawerPage` 与 [`SplitView`](/controls/layout/containers/splitview) 相似，但补充了基于页面的各项能力，比如生命周期事件、安全区支持，以及与 `NavigationPage` 的自动集成。
:::

<Tabs>

<TabItem value="closed" label="Drawer closed">
  <Image light={DrawerPageClosedScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="DrawerPage with the drawer closed"/>
</TabItem>

<TabItem value="open" label="Drawer open">
  <Image light={DrawerPageOpenScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="DrawerPage with the drawer open"/>
</TabItem>

</Tabs>

## 常用属性 {#useful-properties}

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `Content` | `object?` | `null` | 页面的主内容区。 |
| `ContentTemplate` | `IDataTemplate?` | 主题默认模板 | 主内容使用的数据模板。 |
| `Drawer` | `object?` | `null` | 抽屉面板内显示的内容。 |
| `DrawerTemplate` | `IDataTemplate?` | `null` | 抽屉内容使用的数据模板。 |
| `IsOpen` | `bool` | `false` | 控制抽屉是否打开。 |
| `DrawerLength` | `double` | `320` | 抽屉打开时的宽度（或高度）。 |
| `CompactDrawerLength` | `double` | `48` | 紧凑导航栏的宽度；抽屉位于顶部或底部时则为高度。 |
| `DrawerBreakpointLength` | `double` | `0` | 抽屉在浮层模式与内联模式之间自动切换的容器宽度；抽屉位于顶部或底部时则为高度。设为 `0` 可关闭该断点。 |
| `IsGestureEnabled` | `bool` | `true` | 启用滑动手势来开关抽屉。 |
| `DrawerBehavior` | `DrawerBehavior` | `Auto` | 控制抽屉的显示行为，取值见下方 DrawerBehavior 取值表。 |
| `DrawerLayoutBehavior` | `DrawerLayoutBehavior` | `Overlay` | 抽屉与内容区之间的相处方式，取值见下方 DrawerLayoutBehavior 取值表。 |
| `DrawerPlacement` | `DrawerPlacement` | `Left` | 抽屉出现的逻辑侧边。当 `FlowDirection` 为 `RightToLeft` 时，左右会镜像对调。取值见[下方 DrawerPlacement 取值表](#drawerplacement-values)。 |
| `DrawerHeader` | `object?` | `null` | 显示在抽屉顶部的内容。 |
| `DrawerHeaderTemplate` | `IDataTemplate?` | `null` | `DrawerHeader` 使用的数据模板。 |
| `DrawerHeaderBackground` | `IBrush?` | `null` | 抽屉页眉背景所用的画刷。 |
| `DrawerHeaderForeground` | `IBrush?` | `null` | 抽屉页眉前景所用的画刷。 |
| `DrawerFooter` | `object?` | `null` | 显示在抽屉底部的内容。 |
| `DrawerFooterTemplate` | `IDataTemplate?` | `null` | `DrawerFooter` 使用的数据模板。 |
| `DrawerFooterBackground` | `IBrush?` | `null` | 抽屉页脚背景所用的画刷。 |
| `DrawerFooterForeground` | `IBrush?` | `null` | 抽屉页脚前景所用的画刷。 |
| `DrawerIcon` | `object?` | `null` | 抽屉开关按钮上显示的图标。 |
| `DrawerIconTemplate` | `IDataTemplate?` | `null` | 当图标值是非可视数据时，`DrawerIcon` 使用的数据模板。 |
| `DrawerBackground` | [`IBrush?`](/api/avalonia/media/ibrush) | `null` | 抽屉背景所用的画刷。 |
| `BackdropBrush` | `IBrush?` | `null` | 抽屉打开时，遮罩背景所用的画刷。 |
| `DisplayMode` | `SplitViewDisplayMode` | `Overlay` | 由 `DrawerBehavior`、`DrawerLayoutBehavior` 和 `DrawerBreakpointLength` 共同决定的实际 `SplitView` 显示模式。 |
| `HorizontalContentAlignment` | `HorizontalAlignment` | `Stretch` | 主内容的水平对齐方式。 |
| `VerticalContentAlignment` | `VerticalAlignment` | `Stretch` | 主内容的垂直对齐方式。 |

### DrawerBehavior 的取值 {#drawerbehavior-values}

| 值 | 说明 |
| --- | --- |
| `Auto` | 抽屉可以正常开关。至于它是浮在内容之上还是占用布局空间，由 `DrawerLayoutBehavior` 和 `DrawerBreakpointLength` 决定。 |
| `Flyout` | 抽屉表现为浮出层，用户点击外部时自动关闭。 |
| `Locked` | 抽屉保持打开，用户无法关闭。 |
| `Disabled` | 抽屉被隐藏，且无法打开。 |

### DrawerLayoutBehavior 的取值 {#drawerlayoutbehavior-values}

| 值 | 说明 |
| --- | --- |
| `Overlay` | 抽屉滑动覆盖在内容之上，内容区尺寸不变。 |
| `Split` | 抽屉把内容挤到一边，抽屉与内容同时可见。 |
| `CompactOverlay` | 抽屉始终露出窄窄的一条（显示图标）。打开时，抽屉覆盖在内容之上。 |
| `CompactInline` | 抽屉始终露出窄窄的一条。打开时，抽屉把内容挤到一边。 |

### DrawerPlacement 的取值 {#drawerplacement-values}

| 值 | 说明 |
| --- | --- |
| `Left` | 抽屉出现在起始侧：从左到右布局中在左边，从右到左布局中在右边。 |
| `Right` | 抽屉出现在末尾侧：从左到右布局中在右边，从右到左布局中在左边。 |
| `Top` | 抽屉出现在顶部。 |
| `Bottom` | 抽屉出现在底部。 |

## 事件 {#events}

| 事件 | 说明 |
| --- | --- |
| `Opened` | 抽屉完全打开后引发。 |
| `Closing` | 抽屉即将关闭时引发。把事件参数的 `Cancel = true` 置位即可阻止关闭。 |
| `Closed` | 抽屉完全关闭后引发。 |

## 手势与键盘 {#gestures-and-keyboard}

在支持触摸的设备上，`DrawerPage` 支持用滑动手势开关抽屉。这一行为可以用 `IsGestureEnabled` 属性开关。

在桌面端，当抽屉以 `Overlay` 或 `CompactOverlay` 模式打开时，按 `Escape` 键可将其关闭。

## 与 NavigationPage 的集成 {#navigationpage-integration}

当 `DrawerPage` 把 `NavigationPage` 作为它的 `Content`，且有页面被推入导航栈时，导航栏里的汉堡菜单图标会自动变成返回按钮。不用额外写代码，抽屉导航与层级式页面导航之间就能自然衔接。

## 示例 {#examples}

### Basic XAML

```xml
<DrawerPage xmlns="https://github.com/avaloniaui"
            Header="My App"
            DrawerLength="280">
    <DrawerPage.Drawer>
        <StackPanel Spacing="4" Margin="8">
            <Button Content="Home" Click="OnHomeClicked" />
            <Button Content="Settings" Click="OnSettingsClicked" />
            <Button Content="About" Click="OnAboutClicked" />
        </StackPanel>
    </DrawerPage.Drawer>

    <TextBlock Text="Select an item from the drawer"
               Margin="16" FontSize="18" />
</DrawerPage>
```

### 基础代码 {#basic-code}

```csharp
var drawerPage = new DrawerPage
{
    Header = "My App",
    DrawerLength = 280,
    Drawer = new StackPanel
    {
        Spacing = 4,
        Margin = new Thickness(8),
        Children =
        {
            new Button { Content = "Home" },
            new Button { Content = "Settings" },
            new Button { Content = "About" }
        }
    },
    Content = new TextBlock
    {
        Text = "Select an item from the drawer",
        Margin = new Thickness(16),
        FontSize = 18
    }
};
```

### 开关抽屉 {#toggling-the-drawer}

```csharp
private void ToggleDrawer()
{
    myDrawerPage.IsOpen = !myDrawerPage.IsOpen;
}
```

### 从抽屉发起导航 {#navigating-from-the-drawer}

```csharp
private async void OnSettingsClicked(object? sender, RoutedEventArgs e)
{
    myDrawerPage.IsOpen = false;
    if (myDrawerPage.Content is NavigationPage navigation)
    {
        await navigation.PushAsync(new SettingsPage());
    }
}
```

### 页眉与页脚 {#header-and-footer}

用 `DrawerHeader` 和 `DrawerFooter` 在抽屉主体上下放置固定内容，它们不会取代抽屉内容。菜单项应放进 `DrawerPage.Drawer`。

```xml
<DrawerPage xmlns="https://github.com/avaloniaui"
            Header="My App"
            DrawerLength="280">
    <DrawerPage.DrawerHeader>
        <Border Background="#1E3A5F" Padding="16">
            <StackPanel>
                <TextBlock Text="My App"
                           Foreground="White"
                           FontSize="20"
                           FontWeight="SemiBold" />
                <TextBlock Text="user@example.com"
                           Foreground="#AAD4F5"
                           FontSize="13" />
            </StackPanel>
        </Border>
    </DrawerPage.DrawerHeader>

    <DrawerPage.DrawerFooter>
        <Border Padding="12">
            <Button Content="Sign Out"
                    HorizontalAlignment="Stretch" />
        </Border>
    </DrawerPage.DrawerFooter>

    <DrawerPage.Drawer>
        <StackPanel Spacing="4" Margin="8">
            <Button Content="Home" />
            <Button Content="Profile" />
            <Button Content="Settings" />
        </StackPanel>
    </DrawerPage.Drawer>

    <TextBlock Text="Main content" Margin="16" />
</DrawerPage>
```

<Image light={DrawerPageHeaderFooterScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="DrawerPage with header and footer"/>

### 分栏布局 {#split-layout}

若希望抽屉打开时占用布局空间而不是覆盖内容，请使用 `DrawerLayoutBehavior="Split"`。

设置 `IsOpen="True"` 可让抽屉一开始就是打开的。

用 `DrawerBehavior="Locked"` 可把抽屉变成常驻可见的侧边栏。

```xml
<DrawerPage xmlns="https://github.com/avaloniaui"
            Header="My App"
            DrawerLayoutBehavior="Split"
            IsOpen="True"
            DrawerLength="250">
    <DrawerPage.Drawer>
        <StackPanel Spacing="4" Margin="8">
            <Button Content="Home" />
            <Button Content="Settings" />
        </StackPanel>
    </DrawerPage.Drawer>

    <TextBlock Text="Content is pushed to the side" Margin="16" />
</DrawerPage>
```

<Image light={DrawerPageSplitScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="DrawerPage in split mode"/>

### 紧凑导航栏 {#compact-navigation-rail}

用 `CompactOverlay` 或 `CompactInline`，可让抽屉在关闭时仍露出窄窄的一条（比如一列图标按钮），打开时再展开为完整抽屉。

```xml
<DrawerPage xmlns="https://github.com/avaloniaui"
            Header="My App"
            DrawerLayoutBehavior="CompactInline"
            CompactDrawerLength="48"
            DrawerLength="250">
    <DrawerPage.Drawer>
        <StackPanel Spacing="4">
            <Button Width="48" Content="H" />
            <Button Width="48" Content="S" />
        </StackPanel>
    </DrawerPage.Drawer>

    <TextBlock Text="Content adjusts when drawer opens" Margin="16" />
</DrawerPage>
```

<Tabs>

<TabItem value="collapsed" label="DrawerPage collapsed">
  <Image light={DrawerPageCompactCollapsedScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="DrawerPage compact mode collapsed"/>
</TabItem>

<TabItem value="expanded" label="DrawerPage expanded">
  <Image light={DrawerPageCompactExpandedScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="DrawerPage compact mode expanded"/>
</TabItem>

</Tabs>

### 响应式布局 {#responsive-layout}

根据容器宽度（顶部和底部抽屉则看高度）在浮层与内联之间自动切换。

```xml
<DrawerPage xmlns="https://github.com/avaloniaui"
            Header="Responsive App"
            DrawerBreakpointLength="800"
            DrawerLayoutBehavior="Split">
    <DrawerPage.Drawer>
        <StackPanel Spacing="4" Margin="8">
            <Button Content="Home" />
            <Button Content="Settings" />
        </StackPanel>
    </DrawerPage.Drawer>

    <TextBlock Text="Resize the window to see the drawer adapt" Margin="16" />
</DrawerPage>
```

### RTL 支持 {#rtl-support}

`DrawerPage` 在抽屉位置、手势方向和安全区处理上都会遵循 `FlowDirection`。`DrawerPlacement="Left"` 指的是起始侧，因此在从右到左（RTL）布局中它出现在右边。

```xml
<DrawerPage xmlns="https://github.com/avaloniaui"
            Header="RTL App"
            FlowDirection="RightToLeft">
    <DrawerPage.Drawer>
        <StackPanel Spacing="4" Margin="8">
            <Button Content="الصفحة الرئيسية" />
            <Button Content="الإعدادات" />
        </StackPanel>
    </DrawerPage.Drawer>

    <TextBlock Text="محتوى من اليمين إلى اليسار" Margin="16" />
</DrawerPage>
```

<Image light={DrawerPageRtlScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="DrawerPage with RTL layout"/>

### 右侧抽屉 {#right-side-drawer}

```xml
<DrawerPage xmlns="https://github.com/avaloniaui"
            Header="Right Drawer"
            DrawerPlacement="Right"
            DrawerLength="280">
    <DrawerPage.Drawer>
        <StackPanel Spacing="4" Margin="8">
            <Button Content="Option A" />
            <Button Content="Option B" />
        </StackPanel>
    </DrawerPage.Drawer>

    <TextBlock Text="The drawer opens from the right" Margin="16" />
</DrawerPage>
```

<Image light={DrawerPageRightScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="DrawerPage with right-side drawer"/>

### 背景遮罩 {#backdrop-scrim}

用 `BackdropBrush` 属性，可在抽屉以浮层模式打开时于其后方加一层半透明遮罩。

```xml
<DrawerPage xmlns="https://github.com/avaloniaui"
            Header="Scrim Example"
            BackdropBrush="#80000000">
    <DrawerPage.Drawer>
        <StackPanel Spacing="4" Margin="8">
            <Button Content="Home" />
        </StackPanel>
    </DrawerPage.Drawer>

    <TextBlock Text="A scrim appears behind the drawer" Margin="16" />
</DrawerPage>
```

### 取消关闭 {#cancelling-close}

处理 `Closing` 事件，即可在特定条件下阻止抽屉关闭。

```csharp
private void OnDrawerClosing(object sender, DrawerClosingEventArgs e)
{
    if (hasUnsavedChanges)
    {
        e.Cancel = true;
    }
}
```

### 响应开关状态 {#responding-to-openclose}

```csharp
private void OnDrawerOpened(object? sender, RoutedEventArgs e)
{
    Debug.WriteLine("Drawer opened");
}

private void OnDrawerClosed(object? sender, RoutedEventArgs e)
{
    Debug.WriteLine("Drawer closed");
}
```

### MVVM 绑定 {#mvvm-binding}

把 `IsOpen` 属性绑定到视图模型，即可完全掌控抽屉状态。

```xml
<DrawerPage xmlns="https://github.com/avaloniaui"
            Header="MVVM Example"
            IsOpen="{Binding IsDrawerOpen}">
    <DrawerPage.Drawer>
        <StackPanel Spacing="4" Margin="8">
            <Button Content="Home" Command="{Binding GoHomeCommand}" />
            <Button Content="Settings" Command="{Binding GoSettingsCommand}" />
        </StackPanel>
    </DrawerPage.Drawer>

    <ContentControl Content="{Binding CurrentContent}" />
</DrawerPage>
```

### 自定义抽屉图标 {#custom-drawer-icon}

把默认的汉堡图标换成自定义图标。

```xml
<DrawerPage xmlns="https://github.com/avaloniaui"
            Header="Custom Icon">
    <DrawerPage.DrawerIcon>
        <PathIcon Data="M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z" />
    </DrawerPage.DrawerIcon>

    <DrawerPage.Drawer>
        <StackPanel Spacing="4" Margin="8">
            <Button Content="Home" />
        </StackPanel>
    </DrawerPage.Drawer>

    <TextBlock Text="Custom drawer icon" Margin="16" />
</DrawerPage>
```

### 锁定抽屉 {#locked-drawer}

用 `DrawerBehavior="Locked"` 让抽屉保持常开。

```xml
<DrawerPage xmlns="https://github.com/avaloniaui"
            Header="Locked Drawer"
            DrawerBehavior="Locked"
            DrawerLayoutBehavior="Split"
            DrawerLength="250">
    <DrawerPage.Drawer>
        <StackPanel Spacing="4" Margin="8">
            <Button Content="Home" />
            <Button Content="Settings" />
        </StackPanel>
    </DrawerPage.Drawer>

    <TextBlock Text="The drawer cannot be closed" Margin="16" />
</DrawerPage>
```

### 停用抽屉 {#disabling-the-drawer}

用 `DrawerBehavior="Disabled"` 把抽屉彻底隐藏。

```xml
<DrawerPage xmlns="https://github.com/avaloniaui"
            Header="No Drawer"
            DrawerBehavior="Disabled">
    <TextBlock Text="The drawer is disabled on this page" Margin="16" />
</DrawerPage>
```

### 以 NavigationPage 作内容 {#navigationpage-content}

当主内容是 `NavigationPage` 时，一旦有页面被推入栈中，汉堡菜单图标会自动变成返回按钮。

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

### 导航过渡 {#navigation-transitions}

`DrawerPage` 本身没有 `PageTransition` 属性。如果抽屉里承载的是 `NavigationPage`，请在那个 `NavigationPage` 上配置过渡：

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
        <NavigationPage.PageTransition>
            <CrossFade Duration="0:00:00.300" />
        </NavigationPage.PageTransition>

        <ContentPage Header="Home">
            <TextBlock Text="Home Page" Margin="16" />
        </ContentPage>
    </NavigationPage>
</DrawerPage>
```

## 另请参阅 {#see-also}

- [ContentPage](/controls/navigation/contentpage)
- [NavigationPage](/controls/navigation/navigationpage)
- [SplitView](/controls/layout/containers/splitview)
- [DrawerPage API 参考](/api/avalonia/controls/drawerpage)
- [GitHub 上的 `DrawerPage.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Page/DrawerPage.cs)

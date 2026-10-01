---
id: tabbedpage
title: TabbedPage
description: '`TabbedPage` 用一条选项卡栏来展示一组页面，每个子 `Page` 对应一个选项卡。'
doc-type: reference
---

import TabbedPageBottomScreenshot from '/img/controls/tabbedpage/tabbedpage-bottom.png';
import TabbedPageIconsScreenshot from '/img/controls/tabbedpage/tabbedpage-icons.png';
import TabbedPageTopScreenshot from '/img/controls/tabbedpage/tabbedpage-top.png';
import TabbedPageLeftScreenshot from '/img/controls/tabbedpage/tabbedpage-left.png';
import TabbedPageRightScreenshot from '/img/controls/tabbedpage/tabbedpage-right.png';
import TabbedPageInDrawerPageScreenshot from '/img/controls/tabbedpage/tabbedpage-in-drawerpage.png';

[`TabbedPage`](/api/avalonia/controls/tabbedpage) 用一条选项卡栏来展示一组页面，用户点选项卡即可切换。每个子页面对应一个选项卡，选项卡的标题和图标取自页面的 `Header` 和 `Icon` 属性。

`TabbedPage` 继承自 `SelectingMultiPage`，后者又继承自 `MultiPage`。这条继承链自带选中项跟踪、页面生命周期管理和页面过渡支持。

:::info
如果你只想要一条简单的选项卡栏，并不需要页面级的能力（生命周期事件、安全区处理），不妨改用标准的 [TabControl](/controls/navigation/tabcontrol)。
:::

## 常用属性 {#useful-properties}

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `Pages` | `IEnumerable<Page>?` | 空列表 | 作为选项卡显示的 [`Page`](/api/avalonia/controls/page) 子页面集合。 |
| `ItemsSource` | `IEnumerable?` | `null` | 配合 `PageTemplate` 生成页面的视图模型集合。一旦设置，它的优先级高于 `Pages`。 |
| `PageTemplate` | `IDataTemplate?` | 主题默认模板 | 当用 `ItemsSource` 绑定非 `Page` 的数据项时，用于创建 `Page` 实例的数据模板。 |
| [`TabPlacement`](/api/avalonia/controls/tabplacement) | `TabPlacement` | `Auto` | 控制选项卡的位置，取值见下方 TabPlacement 取值表。 |
| `IsKeyboardNavigationEnabled` | `bool` | `true` | 允许用键盘切换选项卡。 |
| `IsGestureEnabled` | `bool` | `false` | 启用滑动手势来切换选项卡。 |
| `PageTransition` | `IPageTransition?` | `null` | 切换选项卡时使用的过渡动画。 |
| `IndicatorTemplate` | `IDataTemplate?` | `null` | 选中项指示器使用的数据模板。 |
| `SelectedIndex` | `int` | `-1` | 当前选中选项卡的索引。选项卡项实例化之后，会有一个页面被选中。 |
| `SelectedPage` | `Page?` | `null` | 只读。当前选中的 `Page`。 |

### TabPlacement 的取值 {#tabplacement-values}

| 值 | 说明 |
| --- | --- |
| `Auto` | 根据目标平台自动决定选项卡位置：在 iOS 和 Android 上解析为 `Bottom`，其他平台上解析为 `Top`。 |
| `Top` | 选项卡沿顶边排列。 |
| `Bottom` | 选项卡沿底边排列。 |
| `Left` | 选项卡沿左边排列。 |
| `Right` | 选项卡沿右边排列。 |

### 附加属性 {#attached-properties}

| Attached Property | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `TabbedPage.IsTabEnabled` | `bool` | `true` | 设在子 `Page` 上，用于启用或停用它对应的选项卡。被停用的选项卡无法被用户选中。 |

### 选项卡图标 {#tab-icons}

子页面的 `Icon` 属性接受任意对象。在默认模板中，请传入 `PathIcon` 之类的可视元素；若图标值是几何图形、图像对象这类非可视数据，则请提供 `IconTemplate`。

常见的图标取值包括：

- `PathIcon`
- `DrawingImage`，搭配相应的 `IconTemplate`
- `Bitmap` 或其他 `IImage` 实现，搭配相应的 `IconTemplate`
- `Geometry` 或 `StreamGeometry`，搭配相应的 `IconTemplate`

## 事件 {#events}

| 事件 | 说明 |
| --- | --- |
| `SelectionChanged` | 选中的选项卡变化时引发，提供 `PreviousPage` 和 `CurrentPage`。 |
| `CurrentPageChanged` | 当前页面变化时引发。 |
| `PagesChanged` | `Pages` 集合发生改动（增删选项卡）时引发。 |

## 键盘导航 {#keyboard-navigation}

当 `IsKeyboardNavigationEnabled` 为 `true`（默认值）时，用户可以用键盘切换选项卡。具体按键取决于 `TabPlacement` 的取值：

- **顶部/底部选项卡：** 左右方向键在选项卡之间移动。
- **左侧/右侧选项卡：** 上下方向键在选项卡之间移动。

## 示例 {#examples}

### 基础选项卡布局（XAML） {#basic-tabbed-layout-xaml}

```xml
<TabbedPage xmlns="https://github.com/avaloniaui">
    <ContentPage Header="Home">
        <ContentPage.Icon>
            <PathIcon Data="{StaticResource HomeIcon}" />
        </ContentPage.Icon>
        <TextBlock Text="Home content" Margin="16" />
    </ContentPage>
    <ContentPage Header="Search">
        <ContentPage.Icon>
            <PathIcon Data="{StaticResource SearchIcon}" />
        </ContentPage.Icon>
        <TextBlock Text="Search content" Margin="16" />
    </ContentPage>
    <ContentPage Header="Profile">
        <ContentPage.Icon>
            <PathIcon Data="{StaticResource ProfileIcon}" />
        </ContentPage.Icon>
        <TextBlock Text="Profile content" Margin="16" />
    </ContentPage>
</TabbedPage>
```

<Image light={TabbedPageTopScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="TabbedPage with top tabs"/>

### 基础选项卡布局（代码） {#basic-tabbed-layout-code}

```csharp
var tabbedPage = new TabbedPage();

var homePage = new ContentPage
{
    Header = "Home",
    Content = new TextBlock { Text = "Home content", Margin = new Thickness(16) }
};

var searchPage = new ContentPage
{
    Header = "Search",
    Content = new TextBlock { Text = "Search content", Margin = new Thickness(16) }
};

var profilePage = new ContentPage
{
    Header = "Profile",
    Content = new TextBlock { Text = "Profile content", Margin = new Thickness(16) }
};

tabbedPage.Pages = new[] { homePage, searchPage, profilePage };
```

### 选项卡图标 {#tab-icons-1}

在每个子页面上用 `Icon` 属性即可为选项卡指定图标，图标会显示在选项卡标题文字旁边。

```xml
<TabbedPage xmlns="https://github.com/avaloniaui"
            TabPlacement="Bottom">
    <ContentPage Header="Home">
        <ContentPage.Icon>
            <PathIcon Data="M10,20V14H14V20H19V12H22L12,3L2,12H5V20H10Z" />
        </ContentPage.Icon>
        <TextBlock Text="Home content" Margin="16" />
    </ContentPage>
    <ContentPage Header="Search">
        <ContentPage.Icon>
            <PathIcon Data="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z" />
        </ContentPage.Icon>
        <TextBlock Text="Search content" Margin="16" />
    </ContentPage>
</TabbedPage>
```

```csharp
var homePage = new ContentPage
{
    Header = "Home",
    Icon = new PathIcon
    {
        Data = StreamGeometry.Parse("M10,20V14H14V20H19V12H22L12,3L2,12H5V20H10Z")
    },
    Content = new TextBlock { Text = "Home content", Margin = new Thickness(16) }
};
```

<Image light={TabbedPageIconsScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="TabbedPage with tab icons"/>

### Controlling TabPlacement

用 `TabPlacement` 属性可以把选项卡摆到控件的不同边上。

```xml
<TabbedPage xmlns="https://github.com/avaloniaui"
            TabPlacement="Bottom">
    <ContentPage Header="Feed">
        <TextBlock Text="Feed content" Margin="16" />
    </ContentPage>
    <ContentPage Header="Messages">
        <TextBlock Text="Messages content" Margin="16" />
    </ContentPage>
</TabbedPage>
```

<Tabs>

<TabItem value="bottom" label="Bottom tabs">
  <Image light={TabbedPageBottomScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="TabbedPage with bottom tabs"/>
</TabItem>

<TabItem value="left" label="Left tabs">
  <Image light={TabbedPageLeftScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="TabbedPage with left tabs"/>
</TabItem>

<TabItem value="right" label="Right tabs">
  <Image light={TabbedPageRightScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="TabbedPage with right tabs"/>
</TabItem>

</Tabs>

### 动态管理选项卡 {#dynamic-tab-management}

把一个可观察的 `Pages` 集合赋给控件，之后改动该集合，就能在运行时增删选项卡。

```csharp
var pages = new ObservableCollection<Page>
{
    homePage,
    searchPage,
    profilePage
};

tabbedPage.Pages = pages;

// Add a new tab
var newPage = new ContentPage
{
    Header = "New Tab",
    Content = new TextBlock { Text = "Dynamically added tab", Margin = new Thickness(16) }
};
pages.Add(newPage);

// Remove a tab
pages.Remove(newPage);
```

### 启用滑动手势 {#enabling-swipe-gestures}

把 `IsGestureEnabled` 设为 `True`，触摸设备上的用户就能滑动切换选项卡。

```xml
<TabbedPage xmlns="https://github.com/avaloniaui"
            IsGestureEnabled="True"
            TabPlacement="Bottom">
    <ContentPage Header="Page 1">
        <TextBlock Text="Swipe left or right" Margin="16" />
    </ContentPage>
    <ContentPage Header="Page 2">
        <TextBlock Text="Page 2 content" Margin="16" />
    </ContentPage>
</TabbedPage>
```

### 停用某个选项卡 {#disabling-a-tab}

用 `TabbedPage.IsTabEnabled` 附加属性，可以让某个选项卡无法被选中。

```xml
<TabbedPage xmlns="https://github.com/avaloniaui">
    <ContentPage Header="Active Tab">
        <TextBlock Text="This tab is enabled" Margin="16" />
    </ContentPage>
    <ContentPage Header="Locked Tab" TabbedPage.IsTabEnabled="False">
        <TextBlock Text="This tab is disabled" Margin="16" />
    </ContentPage>
</TabbedPage>
```

### 响应选中项变化 {#responding-to-selection-changes}

处理 `SelectionChanged` 事件，即可在用户切换选项卡时作出响应。

```csharp
tabbedPage.SelectionChanged += (sender, args) =>
{
    var previousPage = args.PreviousPage;
    var currentPage = args.CurrentPage;
    Console.WriteLine($"Switched from {previousPage?.Header} to {currentPage?.Header}");
};
```

### 用代码切换选项卡 {#programmatic-tab-selection}

在代码中设置 `SelectedIndex` 即可切换当前选项卡。`SelectedPage` 是只读的，反映当前的选中项。

```csharp
// Select by index
tabbedPage.SelectedIndex = 2;

// Select by page reference
if (tabbedPage.Pages is IList<Page> pages)
{
    var index = pages.IndexOf(profilePage);
    if (index >= 0)
    {
        tabbedPage.SelectedIndex = index;
    }
}
```

### 每个选项卡拥有独立的导航栈 {#independent-navigation-stack-per-tab}

一种常见做法是在每个选项卡里放一个 `NavigationPage`，让各个选项卡各自拥有独立的导航栈。

```xml
<TabbedPage xmlns="https://github.com/avaloniaui"
            TabPlacement="Bottom">
    <NavigationPage Header="Home">
        <NavigationPage.Icon>
            <PathIcon Data="{StaticResource HomeIcon}" />
        </NavigationPage.Icon>
        <ContentPage Header="Home">
            <Button Content="View Details" Click="OnViewDetails" />
        </ContentPage>
    </NavigationPage>
    <NavigationPage Header="Settings">
        <NavigationPage.Icon>
            <PathIcon Data="{StaticResource SettingsIcon}" />
        </NavigationPage.Icon>
        <ContentPage Header="Settings">
            <TextBlock Text="Settings page" Margin="16" />
        </ContentPage>
    </NavigationPage>
</TabbedPage>
```

### 用 PageTemplate 做数据驱动的选项卡 {#data-driven-tabs-with-pagetemplate}

用 `ItemsSource` 和 `PageTemplate` 可以从绑定的数据集合生成选项卡：集合中的每一项都会按指定模板转换成一个 `Page`。

```xml
<TabbedPage xmlns="https://github.com/avaloniaui"
            ItemsSource="{Binding Tabs}">
    <TabbedPage.PageTemplate>
        <DataTemplate>
            <ContentPage Header="{Binding Title}">
                <TextBlock Text="{Binding Body}" Margin="16" />
            </ContentPage>
        </DataTemplate>
    </TabbedPage.PageTemplate>
</TabbedPage>
```

```csharp
public class MainViewModel
{
    public ObservableCollection<TabItem> Tabs { get; } = new()
    {
        new TabItem { Title = "Home", Body = "Home content" },
        new TabItem { Title = "News", Body = "News content" },
        new TabItem { Title = "Settings", Body = "Settings content" }
    };
}

public class TabItem
{
    public string Title { get; set; } = string.Empty;
    public string Body { get; set; } = string.Empty;
}
```

### 把 TabbedPage 放进 DrawerPage {#tabbedpage-inside-a-drawerpage}

把 `TabbedPage` 嵌进 `DrawerPage`，即可把侧边抽屉与选项卡导航结合起来。

```xml
<DrawerPage xmlns="https://github.com/avaloniaui">
    <DrawerPage.Drawer>
        <StackPanel Margin="16">
            <TextBlock Text="Drawer Menu" FontSize="20" />
            <Button Content="Option A" />
            <Button Content="Option B" />
        </StackPanel>
    </DrawerPage.Drawer>
    <TabbedPage TabPlacement="Bottom">
        <ContentPage Header="Home">
            <TextBlock Text="Home content" Margin="16" />
        </ContentPage>
        <ContentPage Header="Search">
            <TextBlock Text="Search content" Margin="16" />
        </ContentPage>
    </TabbedPage>
</DrawerPage>
```

<Image light={TabbedPageInDrawerPageScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="TabbedPage inside a DrawerPage"/>

## 另请参阅 {#see-also}

- [ContentPage](/controls/navigation/contentpage)
- [NavigationPage](/controls/navigation/navigationpage)
- [TabControl](/controls/navigation/tabcontrol)
- [TabbedPage API 参考](/api/avalonia/controls/tabbedpage)
- [GitHub 上的 `TabbedPage.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Page/TabbedPage.cs)

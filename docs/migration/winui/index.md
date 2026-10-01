---
title: WinUI / UWP
description: 把 WinUI 和 UWP 应用迁移到 Avalonia，沿用相近的 XAML、控件与 MVVM 套路。
doc-type: migration
---

WinUI 3 和 UWP 是微软的现代 XAML 框架，但它们只面向 Windows。若你的应用还想触及 macOS、Linux、移动端或 Web，这就是一道硬天花板。Avalonia 采用相近的 XAML 模型，支持同样的 MVVM 套路，而且 .NET 能跑的地方它都能跑。

若你已经懂 WinUI 或 UWP，那你离 Avalonia 比想象中更近。XAML 方言、数据绑定系统和控件模型都似曾相识，差异主要在样式、命名，以及少数几个工作方式不同的控件上。

:::tip[迁移上需要帮助？]
Avalonia 团队有大量把 WinUI、UWP 应用迁移到 Avalonia 的实战经验。若你希望得到专业指导，我们提供相应服务，详见 [Avalonia 服务](https://avaloniaui.net/services)。
:::

## 主要差异 {#key-differences}

### Styling

WinUI 用 `VisualStateManager` 配合视觉状态和故事板来处理控件外观的变化，Avalonia 则干脆用类 CSS 的选择器和伪类把这一套全盘取代。

**WinUI (VisualStateManager):**

```xml
<VisualStateManager.VisualStateGroups>
    <VisualStateGroup x:Name="CommonStates">
        <VisualState x:Name="PointerOver">
            <VisualState.Setters>
                <Setter Target="RootBorder.Background" Value="{ThemeResource ButtonBackgroundPointerOver}" />
            </VisualState.Setters>
        </VisualState>
    </VisualStateGroup>
</VisualStateManager.VisualStateGroups>
```

**Avalonia（伪类）：**

```xml
<Style Selector="Button:pointerover /template/ Border#RootBorder">
    <Setter Property="Background" Value="{DynamicResource ButtonBackgroundPointerOver}" />
</Style>
```

Avalonia 的做法更精炼，也更易于组合。样式机制的完整说明请参阅[样式](/docs/styling/styles)。

#### 从 AdaptiveTrigger 到容器查询 {#adaptivetrigger-to-container-queries}

WinUI 在 `VisualStateManager` 中用 `AdaptiveTrigger` 依据窗口尺寸调整布局，Avalonia 则用容器查询取而代之——它能响应任意祖先控件的尺寸，而不限于窗口。

**WinUI (AdaptiveTrigger):**

```xml
<VisualStateManager.VisualStateGroups>
    <VisualStateGroup>
        <VisualState x:Name="Narrow">
            <VisualState.StateTriggers>
                <AdaptiveTrigger MinWindowWidth="0" />
            </VisualState.StateTriggers>
            <VisualState.Setters>
                <Setter Target="ContentGrid.Columns" Value="1" />
            </VisualState.Setters>
        </VisualState>
        <VisualState x:Name="Wide">
            <VisualState.StateTriggers>
                <AdaptiveTrigger MinWindowWidth="800" />
            </VisualState.StateTriggers>
            <VisualState.Setters>
                <Setter Target="ContentGrid.Columns" Value="3" />
            </VisualState.Setters>
        </VisualState>
    </VisualStateGroup>
</VisualStateManager.VisualStateGroups>
```

**Avalonia（容器查询）：**

```xml
<Panel Container.Name="root" Container.Sizing="Width">
    <Panel.Styles>
        <ContainerQuery Name="root" Query="max-width:800">
            <Style Selector="UniformGrid#ContentGrid">
                <Setter Property="Columns" Value="1" />
            </Style>
        </ContainerQuery>
        <ContainerQuery Name="root" Query="min-width:800">
            <Style Selector="UniformGrid#ContentGrid">
                <Setter Property="Columns" Value="3" />
            </Style>
        </ContainerQuery>
    </Panel.Styles>

    <UniformGrid x:Name="ContentGrid">
        <!-- content -->
    </UniformGrid>
</Panel>
```

相比 WinUI 的 `AdaptiveTrigger`，容器查询有两点好处：

- **组件级的响应式。**`AdaptiveTrigger` 量的永远是窗口；容器查询量的则是任意祖先，于是无论组件是铺满整行、嵌在侧边栏里，还是摆在对话框中，它都能正确适配。
- **没有视觉状态的样板代码。**你在一处就把查询和样式都定义好了，不必声明状态组、状态名或触发器对象。

你还可以用 `and` 或 `,` 运算符，把宽度和高度条件写进同一条查询里；除布局属性外，任何可设样式的属性（字号、间距、可见性、颜色）都能作为目标。

完整的查询语法请参阅[容器查询](/docs/styling/container-queries)。至于该在容器查询、`OnFormFactor`、自动重排面板和代码断点之间怎么选，请参阅[响应式布局](/docs/layout/responsive-layouts)。

### XAML 命名空间 {#xaml-namespace}

| WinUI / UWP | Avalonia |
|---|---|
| `xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"` | `xmlns="https://github.com/avaloniaui"` |
| `xmlns:muxc="using:Microsoft.UI.Xaml.Controls"` | `xmlns:controls="using:Avalonia.Controls"`（通常用不上，默认命名空间已覆盖多数控件） |
| 自定义类型用 `clr-namespace:` 或 `using:` | `using:`（推荐）或 `clr-namespace:` |

### 数据绑定 {#data-binding}

核心的绑定语法是一样的。WinUI 的 `x:Bind`（编译绑定）在 Avalonia 里也有对应物：

| WinUI / UWP | Avalonia | 注释支持情况 |
|---|---|---|
| `{Binding Path}` | `{Binding Path}` | Same |
| `{x:Bind ViewModel.Name}` | `{Binding Name}` with `x:DataType` | Avalonia 用 `x:CompileBindings` 和 `x:DataType` 实现编译绑定 |
| `{Binding ElementName=myControl, Path=Text}` | `{Binding #myControl.Text}` | `#name` shorthand |
| `{Binding RelativeSource={RelativeSource Self}}` | `{Binding $self.Property}` | |
| `x:DefaultBindMode` | `x:CompileBindings="True"` | |

### Controls

多数 WinUI 控件在 Avalonia 中都有直接对应者，主要差异在于命名，以及少数需要单独装包的控件。

| WinUI / UWP | Avalonia | 注释支持情况 |
|---|---|---|
| `NavigationView` | 没有直接对应者 | 改用 [`SplitView`](/api/avalonia/controls/splitview) 配 [`ListBox`](/api/avalonia/controls/listbox)，或者第三方控件 |
| `InfoBar` | 没有直接对应者 | 用带样式、带内容的 `Border` |
| `TeachingTip` | 没有直接对应者 | 改用 `Popup` 或 `Flyout` |
| `PersonPicture` | 没有直接对应者 | 用 `Ellipse` 和 `Image` 拼出来 |
| `RatingControl` | 没有直接对应者 | 使用第三方控件 |
| `NumberBox` | `NumericUpDown` | 名称不同 |
| `Pivot` | `TabControl` | |
| `PivotItem` | `TabItem` | |
| `CalendarView` | `Calendar` | |
| `CalendarDatePicker` | `CalendarDatePicker` | Same |
| `CommandBar` | `Menu` or `ToolBar` | |
| `ContentDialog` | Dialog `Window` | Avalonia 用窗口来做对话框 |
| `MenuBar` | `Menu` | |
| `MenuFlyout` | `ContextMenu` | |
| `FlipView` | `Carousel` | |
| `ProgressRing` | 没有直接内置的对应者 | 改用第三方控件或自定义动画 |
| `SplitView` | `SplitView` | Same |
| `TreeView` | `TreeView` | Same |
| `ListView` / `GridView` | `ListBox` | 网格布局请用 `ListBox` 配合 `ItemTemplate` 和 `WrapPanel` |
| `Page` / `Frame` | [`NavigationPage`](/api/avalonia/controls/navigationpage) / `ContentPage` | See [NavigationPage](/controls/navigation/navigationpage) |

### Navigation

Avalonia 提供 `NavigationPage`，这是一套基于栈的导航系统，与 WinUI 的 `Frame` 和 `Page` 模型相仿。它支持带动画过渡的页面压栈与出栈、带返回按钮的内置导航栏，以及模态呈现。

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

```csharp
// Push a new page onto the stack
await Navigation.PushAsync(new DetailsPage());

// Pop back to the previous page
await Navigation.PopAsync();
```

若你的应用偏爱更轻的做法，也可以靠视图模型组合来实现导航——按应用状态替换 `ContentControl` 的内容即可：

```xml
<ContentControl Content="{Binding CurrentPage}" />
```

只要你为每种视图模型类型注册了数据模板，Avalonia 就会自动解析出对应的视图。对于不需要导航栏和页面过渡动画的应用，这种办法很合适。

`NavigationPage` 的完整说明请参阅 [NavigationPage](/controls/navigation/navigationpage)。

### 资源与主题 {#resources-and-theming}

| WinUI / UWP | Avalonia | 注释支持情况 |
|---|---|---|
| `ThemeResource` | `DynamicResource` | 随主题而变的值，Avalonia 用 `DynamicResource` |
| `StaticResource` | `StaticResource` | Same |
| `ResourceDictionary.ThemeDictionaries` | `ResourceDictionary.ThemeDictionaries` | 概念相同 |
| `ElementTheme.Light` / `.Dark` | `RequestedThemeVariant` | |
| `AcrylicBrush` | `ExperimentalAcrylicBorder` | Different API |

### 文件结构 {#file-structure}

| WinUI / UWP | Avalonia |
|---|---|
| `.xaml` extension | `.axaml` extension |
| `App.xaml` | `App.axaml` |
| `MainWindow.xaml` | `MainWindow.axaml` |
| `.xaml.cs` code-behind | `.axaml.cs` code-behind |
| `Package.appxmanifest` | 没有对应者（就是个标准的 .NET 项目） |

### Threading

| WinUI / UWP | Avalonia |
|---|---|
| `DispatcherQueue.TryEnqueue()` | `Dispatcher.UIThread.Post()` |
| `DispatcherQueue.GetForCurrentThread()` | `Dispatcher.UIThread` |
| `CoreDispatcher.RunAsync()` | `Dispatcher.UIThread.InvokeAsync()` |

## 你能得到什么 {#what-you-gain}

从 WinUI 转到 Avalonia，图的不只是跨平台。有几处地方，Avalonia 如今给得比 WinUI 更多：

- **类 CSS 的样式：**选择器、样式类和伪类让你对样式的掌控更强，写起来也比 `VisualStateManager` 省事得多。
- **编译绑定配上更好的工具：**`x:DataType` 和 `x:CompileBindings` 能在整个项目范围内，于编译期校验绑定路径。
- **不必打 MSIX 包：**Avalonia 应用就是标准的 .NET 可执行文件。不需要应用清单，不需要打包流水线，也不必上应用商店。
- **Linux 和 macOS 是一等目标平台：**它们既不是事后补的，也不是靠兼容层凑的。

## 另请参阅 {#see-also}

- [Avalonia 入门](/docs/get-started/create-your-first-project)：创建你的第一个 Avalonia 应用。
- [样式](/docs/styling/styles)：Avalonia 类 CSS 样式机制的运作方式。
- [容器查询](/docs/styling/container-queries)：基于尺寸的样式，用来取代 WinUI 的 AdaptiveTrigger。
- [响应式布局](/docs/layout/responsive-layouts)：用容器查询和自动重排面板搭出自适应布局。
- [数据绑定语法](/docs/data-binding/data-binding-syntax)：Avalonia 绑定语法参考。
- [控件参考](/controls)：Avalonia 控件的完整文档。

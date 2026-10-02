---
title: .NET MAUI
description: 从 .NET MAUI 迁移到 Avalonia，或用 Avalonia MAUI 后端扩展现有的 MAUI 应用。
doc-type: migration
---

如果你是 .NET MAUI 开发者，通往 Avalonia 有两条路：一是保留现有的 MAUI 代码库，用 Avalonia MAUI 后端把它扩展到更多平台；二是直接把应用迁移到 Avalonia，从而完全掌控 UI 框架。本页把两条路都讲一讲。

:::tip[需要帮助？]
Avalonia 团队有大量与 MAUI 代码库打交道的实战经验。无论你是想采用 Avalonia MAUI 后端，还是打算完整迁移到 Avalonia，我们都提供相应服务。详见 [Avalonia 服务](https://avaloniaui.net/services)。
:::

## 方案一：Avalonia MAUI 后端 {#option-1-avalonia-maui-backend}

Avalonia MAUI 后端让你保留现有的 .NET MAUI 代码库，只把渲染层换成 Avalonia。你现有的 MAUI 代码、控件、handler 和布局照常工作，只是改由 Avalonia 的跨平台引擎渲染，而不再走平台原生控件。

这让你的 MAUI 应用得以涉足 MAUI 本身并不支持的平台：

- **桌面 Linux：**在 Ubuntu、Debian、Fedora 等发行版上获得一流的桌面支持，所用的正是如今支撑着严苛生产级桌面应用的那个 Avalonia 渲染器。
- **嵌入式 Linux：**从树莓派面板到工业 HMI，Avalonia 早已跑在各类嵌入式 Linux 设备上。MAUI 后端把这些能力一并带给你的 MAUI 应用。
- **WebAssembly：**把你的 MAUI 应用部署到浏览器，客户端不带任何原生依赖。
- **更好的桌面性能：**在 Windows 和 macOS 上，Avalonia 后端接入了 Avalonia 成熟的桌面方案。macOS 上的早期测试表明，其性能比走 Mac Catalyst 的路子有显著提升。

由于每个控件都由 Avalonia 亲自绘制，你的 MAUI 应用无论跑在 Windows、macOS、Linux、移动端还是浏览器标签页里，观感和行为都始终如一。

### 运作原理 {#how-it-works}

Avalonia MAUI 后端的核心，是构建一套把 MAUI 控件映射到 Avalonia 控件的 handler。当你在 MAUI 中创建 [`Button`](/api/avalonia/controls/button) 时，它在所有平台上都渲染为 Avalonia 的 `Button`，而不是各平台的原生控件。

MAUI 的布局系统也是同理：定位和约束计算仍由 MAUI 自己完成，Avalonia 后端严格按 MAUI 给出的结果摆放控件。实际效果是，许多标准的 MAUI 布局控件无需改动即可工作。

用到 `SkiaSharp` 和 `Microsoft.Maui.Graphics` 的库同样能用，因为 Avalonia 自带基于 SkiaSharp 的渲染器。这让自绘控件得以直接映射过来，改动极少。

### 这对你的代码意味着什么 {#what-this-means-for-your-code}

你不必重写应用。只需把 Avalonia MAUI 后端的库加进现有项目，并把新平台设为目标即可。你的 MAUI XAML、视图模型、服务和业务逻辑统统照旧。

Resizetizer 之类的构建期工具照常可用。构建过程中，Resizetizer 会把你的图片、SVG 和字体转成资源，Avalonia 后端再自动把它们映射为 Avalonia 资源。

### 当前进展 {#current-status}

Avalonia 团队正在与 MAUI 生态的工程师合作开发这个 MAUI 后端，目标是与 .NET 11 同步发布稳定版。预览版将跟随 .NET MAUI 的发布节奏，CI 上也会提供每夜构建。

由于 MAUI 目前并不支持 Linux 和 WebAssembly，前期工作会先聚焦这两个平台。该后端在 Windows 和 macOS 上同样可以运行，并计划支持 Avalonia 的全部目标平台。

这个项目不会 fork .NET MAUI。为支撑这项集成所需的改动，都会回馈到 .NET MAUI 官方仓库的上游，让整个生态都受益。

:::note
Avalonia MAUI 后端正在积极开发中。欢迎在 [avaloniaui.net](https://avaloniaui.net) 登记意向，以获取最新进展和抢先体验资格。
:::

## 方案二：迁移到 Avalonia {#option-2-migrate-to-avalonia}

若你想完全掌控 UI 框架，或者你的应用需要 MAUI 给不了的能力（类 CSS 样式、自定义渲染、进阶桌面特性），那就直接把 MAUI 应用迁移到 Avalonia 吧。

### 前置条件 {#prerequisites}

动手之前，请先确认以下几点已经就位：

- 已安装 **.NET 8 或更高版本**。Avalonia 11+ 最低要求 .NET 8。
- 已安装 **Avalonia 模板**。在命令行运行 `dotnet new install Avalonia.Templates` 即可。
- **你现有的 MAUI 项目能编译、能运行。**动手前请先把已有的构建问题修掉。有个能跑起来的基线，每一步的验证都会轻松许多。
- 熟悉 XAML 和 MVVM 模式。既然你从 MAUI 过来，这一条想必早就满足了。

### 渲染模型不同 {#different-rendering-models}

MAUI 与 Avalonia 最要紧的区别，在于二者的渲染方式。

**MAUI** 把自己的控件映射到平台原生控件。iOS 上的 `Button` 其实是 `UIButton`，Android 上的 `Button` 其实是 `Android.Widget.Button`。这意味着各平台的外观多少会有出入（有时还相当明显），平台专属的 bug 也屡见不鲜。

**Avalonia** 用 Skia 或 Direct2D 亲自绘制每一个控件。Avalonia 中的 `Button` 在 Windows、macOS、Linux、iOS、Android 和 WebAssembly 上长得一模一样。拍板的是你选的主题，而不是平台。

这个区别影响到方方面面：样式、布局精度、调试，以及你最终得写多少平台专属代码。

### 主要差异 {#key-differences}

#### XAML 方言 {#xaml-dialect}

两个框架都用 XAML，但方言有别。MAUI 的 XAML 源自 Xamarin.Forms 的那套惯例，Avalonia 的 XAML 则更贴近 WPF。

| .NET MAUI | Avalonia | 注释支持情况 |
|---|---|---|
| `xmlns="http://schemas.microsoft.com/dotnet/2021/maui"` | `xmlns="https://github.com/avaloniaui"` | |
| 用 `x:DataType` 启用编译绑定 | `x:DataType` + `x:CompileBindings` | 概念相同，配置略有不同 |
| `{Binding Path}` | `{Binding Path}` | 语法相同 |
| `{Binding Source={RelativeSource Self}}` | `{Binding $self.Property}` | 简写写法 |
| `{Binding Source={x:Reference myControl}, Path=Text}` | `{Binding #myControl.Text}` | `#name` shorthand |

#### Layout

MAUI 和 Avalonia 都用面板来布局，但名称和行为不尽相同。

| .NET MAUI | Avalonia | 注释支持情况 |
|---|---|---|
| `StackLayout` / `VerticalStackLayout` | `StackPanel` | Avalonia 用的是 `Orientation` 属性 |
| `HorizontalStackLayout` | `StackPanel Orientation="Horizontal"` | |
| `Grid` | `Grid` | 概念相同。Avalonia 支持 `ColumnDefinitions="Auto,*"` 简写 |
| `FlexLayout` | `WrapPanel` | 没有完全对应者，但多数用途都能覆盖 |
| `AbsoluteLayout` | `Canvas` | |
| `ScrollView` | `ScrollViewer` | |
| `Frame` | `Border` | |
| `ContentView` | `UserControl` or `ContentControl` | |
| `Padding`, `Margin` | `Padding`, `Margin` | Same |
| 布局上的 `Spacing` | `Spacing` on `StackPanel` | 概念相同 |

#### Controls

| .NET MAUI | Avalonia | 注释支持情况 |
|---|---|---|
| `Entry` | [`TextBox`](/api/avalonia/controls/textbox) | |
| `Editor` | `TextBox` with `AcceptsReturn="True"` | |
| `Label` | `TextBlock` | |
| `Button` | `Button` | Same |
| `ImageButton` | 带图片内容的 `Button` | |
| `CheckBox` | `CheckBox` | Same |
| `Switch` | `ToggleSwitch` | |
| `Slider` | `Slider` | Same |
| `Stepper` | `NumericUpDown` | |
| `Picker` | `ComboBox` | |
| `DatePicker` | `DatePicker` | Same |
| `TimePicker` | `TimePicker` | Same |
| `ActivityIndicator` | `ProgressBar IsIndeterminate="True"` | |
| `ProgressBar` | `ProgressBar` | Same |
| `ListView` / `CollectionView` | `ListBox` or `ItemsControl` | |
| `CarouselView` | `Carousel` | |
| `TableView` | 没有直接对应者 | 改用 `DataGrid`，或者用面板拼出来 |
| `WebView` | 没有内置的对应者 | 使用第三方控件 |
| `RefreshView` | `RefreshContainer` | |
| `SearchBar` | 带自定义样式的 `TextBox` | 或者用 `AutoCompleteBox` 做输入建议 |
| `Shell` | 没有对应者 | Avalonia 不强加某一套导航框架 |
| `FlyoutPage` | `SplitView` | |
| `TabbedPage` | `TabControl` | |
| [`NavigationPage`](/api/avalonia/controls/navigationpage) | `NavigationPage` | See [NavigationPage](/controls/navigation/navigationpage) |
| `ContentPage` | `ContentPage` | 在 `NavigationPage` 内使用 |
| `BoxView` | `Border` or `Rectangle` | |

#### Styling

MAUI 走的是资源字典那一套，用指向类型的 `Style` 元素；Avalonia 用的则是类似 CSS 的选择器。

**MAUI:**

```xml
<Style TargetType="Button">
    <Setter Property="BackgroundColor" Value="SteelBlue" />
    <Setter Property="TextColor" Value="White" />
</Style>
```

**Avalonia:**

```xml
<Style Selector="Button">
    <Setter Property="Background" Value="SteelBlue" />
    <Setter Property="Foreground" Value="White" />
</Style>
```

表面上看语法相仿，但 Avalonia 的选择器本事更大。你可以按样式类、名称、状态、嵌套关系等等来匹配控件：

```xml
<Style Selector="Button.primary:pointerover">
    <Setter Property="Background" Value="LightBlue" />
</Style>
```

MAUI 用 `VisualStateManager` 表示交互状态，Avalonia 则把伪类（`:pointerover`、`:pressed`、`:disabled`、`:checked`）直接写进选择器，更为紧凑。完整参考请见[样式](/docs/styling/styles)。

#### Navigation

MAUI 内置了 `Shell`、`NavigationPage`、`FlyoutPage` 和 `TabbedPage` 几种导航模式。Avalonia 提供的是 `NavigationPage`——一套基于栈的导航系统，用过 MAUI 的 `NavigationPage` 就会觉得眼熟。它支持带动画过渡的页面压栈与出栈、带返回按钮的内置导航栏，以及模态呈现。

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

完整说明请参阅 [NavigationPage](/controls/navigation/navigationpage)。

#### 平台专属代码 {#platform-specific-code}

在 MAUI 中，平台差异总会不断渗出来。为了修好某个平台上的行为，你少不了要写 handler、自定义渲染器，或者 `#if` 条件编译块。

在 Avalonia 中，平台专属代码很少见。由于渲染由 Avalonia 自己说了算，同一份代码在哪儿都给出同样的结果。确实需要平台专属行为时（比如调用某个原生 API），Avalonia 也提供了清爽的抽象，不必让你去继承什么渲染器。

#### 文件结构 {#file-structure}

| .NET MAUI | Avalonia |
|---|---|
| `.xaml` extension | `.axaml` extension |
| `App.xaml` | `App.axaml` |
| `MainPage.xaml` | `MainWindow.axaml` |
| `.xaml.cs` code-behind | `.axaml.cs` code-behind |
| 带有各平台代码的 `Platforms/` 文件夹 | 通常不需要平台专属文件夹 |
| `MauiProgram.cs` builder | `Program.cs` with `AppBuilder` |

#### Threading

| .NET MAUI | Avalonia |
|---|---|
| `MainThread.BeginInvokeOnMainThread()` | `Dispatcher.UIThread.Post()` |
| `MainThread.InvokeOnMainThreadAsync()` | `Dispatcher.UIThread.InvokeAsync()` |
| `MainThread.IsMainThread` | `Dispatcher.UIThread.CheckAccess()` |

### 迁移步骤 {#migration-steps}

目前还没有从 MAUI 到 Avalonia 的自动转换工具，迁移是个手工活。好在两个框架颇多相似之处，这件事还算得上可控。逐层推进，一层一层来。

#### 1. 新建一个 Avalonia 项目 {#1-create-a-new-avalonia-project}

先用模板起一个全新的 Avalonia 项目：

```bash
dotnet new avalonia.mvvm -n MyApp
```

这样你就有了一套能跑的项目结构，含 `App.axaml`、`MainWindow.axaml` 和一个视图模型基类。不要试图就地改造你的 MAUI `.csproj`。

#### 2. 搬运模型与服务 {#2-move-your-models-and-services}

把模型类、服务，以及所有与界面框架无关的业务逻辑复制到新项目里。它们通常不需要任何改动，因为压根不依赖 UI 框架。

#### 3. 迁移视图模型 {#3-migrate-your-view-models}

把视图模型复制过来。若你用的是 `CommunityToolkit.Mvvm`，它在 Avalonia 下无需改动即可使用。若视图模型引用了 MAUI 专属的类型（比如 `Microsoft.Maui.Controls.Application`），请换成 Avalonia 中对应的东西。

#### 4. 转换 XAML 文件 {#4-convert-your-xaml-files}

为 MAUI 项目中的每个 `.xaml` 页面，在 Avalonia 项目里建一个对应的 `.axaml` 文件。控件名、属性和绑定语法怎么换，请参考上面[主要差异](#key-differences)一节中的控件与布局映射表。

每个文件都要改的地方：
- 把根元素的 XML 命名空间换成 `xmlns="https://github.com/avaloniaui"`
- 给控件改名（`Entry` 改成 `TextBox`，`Label` 改成 `TextBlock`，诸如此类）
- 把 `VisualStateManager` 块换成 Avalonia 的样式选择器和伪类
- 按需更新绑定语法（`{x:Reference}` 改成 `#name`，`RelativeSource Self` 改成 `$self`）

#### 5. 转换样式与资源 {#5-convert-your-styles-and-resources}

把资源字典搬过来，再把基于 `TargetType` 的样式换成 Avalonia 基于选择器的样式。示例请见上面的[样式](#styling)一节。

#### 6. 替换导航 {#6-replace-navigation}

若你的 MAUI 应用用了 `Shell` 或 `NavigationPage`，请换成 Avalonia 的 `NavigationPage` 或视图模型组合的做法。详见上面的[导航](#navigation)一节。

#### 7. 处理平台专属代码 {#7-handle-platform-specific-code}

把 MAUI `Platforms/` 文件夹里的代码都过一遍。那些为了抹平渲染差异而做的平台变通，多半已经没必要了。至于真正需要调用平台 API 的部分（相机、文件系统、传感器），可以把 .NET MAUI Essentials 当作独立包来用，或者改为直接调用平台 API。

### Verification

迁移完成后，请逐项确认应用工作正常：

1. **构建项目。**把漏改的类型名或命名空间导致的编译错误都修掉。
2. **在你的主力平台上运行。**确认主窗口能加载、导航能用。
3. **换一个平台再测一遍。**换个操作系统跑跑看（比如你在 Windows 上开发，那就试试 macOS），确认跨平台渲染的一致性。
4. **把核心用户流程走一遍。**确认数据绑定、命令和输入处理都如预期工作。
5. **检查样式。**确认视觉呈现符合你的本意，尤其留意此前用 `VisualStateManager` 实现的悬停/按下状态。

### 你能得到什么 {#what-you-gain}

从 MAUI 转到 Avalonia，会改变你日常的工作方式：

- **像素级一致：**你的界面在每个平台上渲染得分毫不差。再也不用追查只在 Android 上冒出来的布局 bug，或是 iOS 上的样式怪癖。
- **一流的桌面支持：**Avalonia 从一开始就是为桌面而生的。窗口管理、菜单、键盘导航和多窗口支持，统统如你所愿。
- **支持 Linux：**Avalonia 原生跑在 Linux 上，而 MAUI 压根不支持 Linux。
- **没有原生控件包装层：**你不必穿过层层平台抽象去调试。XAML 里写的是什么，渲染出来就是什么。
- **WebAssembly：**Avalonia 支持通过 WebAssembly 部署到浏览器，这是 MAUI 没有的目标平台。

## 另请参阅 {#see-also}

- [Avalonia 入门](/docs/get-started/create-your-first-project)：创建你的第一个 Avalonia 应用。
- [样式](/docs/styling/styles)：Avalonia 类 CSS 样式机制的运作方式。
- [数据绑定语法](/docs/data-binding/data-binding-syntax)：Avalonia 绑定语法参考。
- [控件参考](/controls)：Avalonia 控件的完整文档。
- [NavigationPage](/controls/navigation/navigationpage)：Avalonia 中基于栈的页面导航。

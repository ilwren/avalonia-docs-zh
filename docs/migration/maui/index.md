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

- **.NET 8 or later** installed. Avalonia 11+ targets .NET 8 as the minimum.
- **Avalonia templates** installed. Run `dotnet new install Avalonia.Templates` from the command line.
- **Your existing MAUI project compiles and runs.** Fix any existing build issues before starting. Having a working baseline makes it easier to verify each step.
- Familiarity with XAML and the MVVM pattern. If you are coming from MAUI, you already have this.

### Different rendering models

The most important difference between MAUI and Avalonia is how they render.

**MAUI** maps its controls to native platform controls. A `Button` on iOS is a `UIButton`. A `Button` on Android is an `Android.Widget.Button`. This means every platform can look subtly (or significantly) different, and platform-specific bugs are common.

**Avalonia** draws every control itself using Skia or Direct2D. A `Button` in Avalonia looks the same on Windows, macOS, Linux, iOS, Android, and WebAssembly. You choose the theme, not the platform.

This distinction affects everything: styling, layout precision, debugging, and how much platform-specific code you end up writing.

### Key differences

#### XAML dialect

Both frameworks use XAML, but the dialects differ. MAUI's XAML is rooted in Xamarin.Forms conventions. Avalonia's XAML is closer to WPF.

| .NET MAUI | Avalonia | 注释支持情况 |
|---|---|---|
| `xmlns="http://schemas.microsoft.com/dotnet/2021/maui"` | `xmlns="https://github.com/avaloniaui"` | |
| `x:DataType` for compiled bindings | `x:DataType` + `x:CompileBindings` | Same concept, slightly different setup |
| `{Binding Path}` | `{Binding Path}` | Same syntax |
| `{Binding Source={RelativeSource Self}}` | `{Binding $self.Property}` | 简写写法 |
| `{Binding Source={x:Reference myControl}, Path=Text}` | `{Binding #myControl.Text}` | `#name` shorthand |

#### Layout

MAUI and Avalonia both use panels for layout, but the names and behaviour differ.

| .NET MAUI | Avalonia | 注释支持情况 |
|---|---|---|
| `StackLayout` / `VerticalStackLayout` | `StackPanel` | Avalonia uses `Orientation` property |
| `HorizontalStackLayout` | `StackPanel Orientation="Horizontal"` | |
| `Grid` | `Grid` | Same concept. Avalonia supports shorthand `ColumnDefinitions="Auto,*"` |
| `FlexLayout` | `WrapPanel` | Not a direct equivalent, but covers most use cases |
| `AbsoluteLayout` | `Canvas` | |
| `ScrollView` | `ScrollViewer` | |
| `Frame` | `Border` | |
| `ContentView` | `UserControl` or `ContentControl` | |
| `Padding`, `Margin` | `Padding`, `Margin` | Same |
| `Spacing` on layouts | `Spacing` on `StackPanel` | Same concept |

#### Controls

| .NET MAUI | Avalonia | 注释支持情况 |
|---|---|---|
| `Entry` | [`TextBox`](/api/avalonia/controls/textbox) | |
| `Editor` | `TextBox` with `AcceptsReturn="True"` | |
| `Label` | `TextBlock` | |
| `Button` | `Button` | Same |
| `ImageButton` | `Button` with image content | |
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
| `TableView` | No direct equivalent | Use `DataGrid` or compose with panels |
| `WebView` | No built-in equivalent | Use a third-party control |
| `RefreshView` | `RefreshContainer` | |
| `SearchBar` | `TextBox` with custom styling | Or `AutoCompleteBox` for suggestions |
| `Shell` | No equivalent | Avalonia does not impose a navigation framework |
| `FlyoutPage` | `SplitView` | |
| `TabbedPage` | `TabControl` | |
| [`NavigationPage`](/api/avalonia/controls/navigationpage) | `NavigationPage` | See [NavigationPage](/controls/navigation/navigationpage) |
| `ContentPage` | `ContentPage` | Used within `NavigationPage` |
| `BoxView` | `Border` or `Rectangle` | |

#### Styling

MAUI uses a resource-dictionary approach with `Style` elements that target types. Avalonia uses CSS-like selectors.

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

The syntax is similar on the surface, but Avalonia's selectors support additional capabilities. You can target controls by class, name, state, nesting, and more:

```xml
<Style Selector="Button.primary:pointerover">
    <Setter Property="Background" Value="LightBlue" />
</Style>
```

MAUI has `VisualStateManager` for interactive states. Avalonia uses pseudo-classes (`:pointerover`, `:pressed`, `:disabled`, `:checked`) as part of the selector, which is more concise. See [Styles](/docs/styling/styles) for the full reference.

#### Navigation

MAUI provides `Shell`, `NavigationPage`, `FlyoutPage`, and `TabbedPage` as built-in navigation patterns. Avalonia provides `NavigationPage`, a stack-based navigation system that will feel familiar if you have used MAUI's `NavigationPage`. It supports pushing and popping pages with animated transitions, a built-in navigation bar with a back button, and modal presentation.

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

For applications that prefer a lighter approach, you can also handle navigation through view model composition by swapping the content of a `ContentControl` based on application state:

```xml
<ContentControl Content="{Binding CurrentPage}" />
```

Avalonia resolves the correct view automatically if you register data templates for each view model type. This approach works well for applications that do not need a navigation bar or animated page transitions.

For full details, see [NavigationPage](/controls/navigation/navigationpage).

#### Platform-specific code

In MAUI, platform differences leak through constantly. You end up writing handlers, custom renderers, or `#if` conditional compilation blocks to fix behaviour on specific platforms.

In Avalonia, platform-specific code is rare. Because Avalonia controls its own rendering, the same code produces the same result everywhere. When you do need platform-specific behaviour (for example, accessing a native API), Avalonia provides clean abstractions without requiring you to subclass renderers.

#### File structure

| .NET MAUI | Avalonia |
|---|---|
| `.xaml` extension | `.axaml` extension |
| `App.xaml` | `App.axaml` |
| `MainPage.xaml` | `MainWindow.axaml` |
| `.xaml.cs` code-behind | `.axaml.cs` code-behind |
| `Platforms/` folder with per-platform code | Typically no platform folders needed |
| `MauiProgram.cs` builder | `Program.cs` with `AppBuilder` |

#### Threading

| .NET MAUI | Avalonia |
|---|---|
| `MainThread.BeginInvokeOnMainThread()` | `Dispatcher.UIThread.Post()` |
| `MainThread.InvokeOnMainThreadAsync()` | `Dispatcher.UIThread.InvokeAsync()` |
| `MainThread.IsMainThread` | `Dispatcher.UIThread.CheckAccess()` |

### Migration steps

There is no automated converter from MAUI to Avalonia. The migration is a manual process, but the similarities between the two frameworks make the process manageable. Work through your application one layer at a time.

#### 1. Create a new Avalonia project

Start with a fresh Avalonia project using the templates:

```bash
dotnet new avalonia.mvvm -n MyApp
```

This gives you a working project structure with `App.axaml`, `MainWindow.axaml`, and a view model base class. Do not try to convert your MAUI `.csproj` in place.

#### 2. Move your models and services

Copy your model classes, services, and any platform-independent business logic into the new project. These typically require no changes since they have no UI framework dependency.

#### 3. Migrate your view models

Copy your view models. If you use `CommunityToolkit.Mvvm`, it works with Avalonia without modification. If your view models reference MAUI-specific types (such as `Microsoft.Maui.Controls.Application`), replace those references with Avalonia equivalents.

#### 4. Convert your XAML files

For each `.xaml` page in your MAUI project, create a corresponding `.axaml` file in the Avalonia project. Use the control and layout mapping tables in the [Key differences](#key-differences) section above to translate control names, properties, and binding syntax.

Key changes for every file:
- Replace the root XML namespace with `xmlns="https://github.com/avaloniaui"`
- Rename controls (`Entry` to `TextBox`, `Label` to `TextBlock`, etc.)
- Replace `VisualStateManager` blocks with Avalonia style selectors and pseudo-classes
- Update binding syntax where needed (`{x:Reference}` to `#name`, `RelativeSource Self` to `$self`)

#### 5. Convert your styles and resources

Move your resource dictionaries. Replace `TargetType`-based styles with Avalonia selector-based styles. See the [Styling](#styling) section above for examples.

#### 6. Replace navigation

If your MAUI app uses `Shell` or `NavigationPage`, replace it with Avalonia's `NavigationPage` or a view model composition pattern. See the [Navigation](#navigation) section above.

#### 7. Handle platform-specific code

Review any code in your MAUI `Platforms/` folder. Most platform-specific workarounds for rendering inconsistencies are no longer needed. For genuine platform API access (camera, file system, sensors), use .NET MAUI Essentials as a standalone package or replace with direct platform API calls.

### Verification

After completing the migration, verify that your application works correctly:

1. **Build the project.** Fix any remaining compilation errors from missed type renames or namespace changes.
2. **Run on your primary platform.** Confirm that the main window loads and navigation works.
3. **Test on a second platform.** Run on a different OS (for example, macOS if you developed on Windows) to confirm cross-platform rendering consistency.
4. **Walk through your core user flows.** Verify that data binding, commands, and input handling work as expected.
5. **Check your styles.** Confirm that visual appearance matches your intent, paying attention to hover/pressed states that previously used `VisualStateManager`.

### What you gain

Moving from MAUI to Avalonia changes how you work day to day:

- **Pixel-perfect consistency:** Your UI renders identically on every platform. No more chasing layout bugs that only appear on Android or styling quirks on iOS.
- **First-class desktop support:** Avalonia was built for desktop from the start. Window management, menus, keyboard navigation, and multi-window support all work as expected.
- **Linux support:** Avalonia runs natively on Linux. MAUI does not support Linux at all.
- **No native control wrappers:** You are not debugging through layers of platform abstraction. What you see in XAML is what renders.
- **WebAssembly:** Avalonia supports browser deployment through WebAssembly, a target MAUI does not offer.

## 另请参阅 {#see-also}

- [Get started with Avalonia](/docs/get-started/create-your-first-project): Create your first Avalonia application.
- [Styles](/docs/styling/styles): How Avalonia's CSS-like styling works.
- [Data binding syntax](/docs/data-binding/data-binding-syntax): Avalonia binding syntax reference.
- [Controls reference](/controls): Full Avalonia controls documentation.
- [NavigationPage](/controls/navigation/navigationpage): Stack-based page navigation in Avalonia.

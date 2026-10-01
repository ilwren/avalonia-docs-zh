---
title: 其他框架
description: 从 Delphi、Qt、Electron 或 ASP.NET MVC 桌面应用迁移到 Avalonia。
doc-type: migration
---

Avalonia 并非只为从微软 XAML 生态过来的开发者准备。若你正用 Delphi、Qt、Electron 或 ASP.NET MVC 构建桌面或跨平台应用，又想找一个现代的 .NET 方案，那么 Avalonia 很可能相当合适。

本页讲的是从 XAML 世界之外的框架迁移过来时，都会遇上些什么。

:::tip[迁移上需要帮助？]
Avalonia 团队帮助过不少团队从形形色色的 UI 框架迁移过来。若你希望得到专业指导，我们提供相应服务，详见 [Avalonia 服务](https://avaloniaui.net/services)。
:::

## 从 Delphi（VCL / FireMonkey）迁移 {#from-delphi-vcl-firemonkey}

几十年来，Delphi 一直是桌面开发的中流砥柱，许多关乎业务命脉的应用至今仍跑在 VCL 或 FireMonkey 上。但 Delphi 的生态正在萎缩：开发者越来越少，库越来越少，授权费用却越来越高。想招到 Delphi 开发者，一年比一年难。

Avalonia 为你铺了一条通往 .NET 的路：那里开发者数量庞大得多，开源生态活跃，工具链也现代。这趟转型需要你学会 XAML 和 MVVM，但核心概念的对应关系出乎意料地顺畅。

### 概念对照 {#concept-mapping}

| Delphi (VCL / FMX) | Avalonia | 注释支持情况 |
|---|---|---|
| `TForm` | `Window` | |
| `TFrame` | `UserControl` | 可复用的界面组件 |
| `TPanel` | `Border` or `Panel` | |
| `TButton` | `Button` | |
| `TEdit` | [`TextBox`](/api/avalonia/controls/textbox) | |
| `TMemo` | `TextBox` with `AcceptsReturn="True"` | |
| `TLabel` | `TextBlock` | |
| `TCheckBox` | `CheckBox` | |
| `TRadioButton` | `RadioButton` | |
| `TComboBox` | `ComboBox` | |
| `TListBox` | `ListBox` | |
| `TTreeView` | `TreeView` | |
| `TStringGrid` / `TDBGrid` | `DataGrid`（NuGet 包） | |
| `TTabControl` | `TabControl` | |
| `TImage` | `Image` | |
| `TScrollBox` | `ScrollViewer` | |
| `TPopupMenu` | `ContextMenu` | |
| `TMainMenu` | `Menu` | |
| `TTimer` | `DispatcherTimer` | |
| `TAction` / `TActionList` | `ICommand`（MVVM 模式） | |
| 挂在组件上的事件处理程序 | 数据绑定 + MVVM | 架构上最大的转变 |
| DFM 窗体文件 | `.axaml` XAML 文件 | 声明式布局 |
| `Application.CreateForm()` | `AppBuilder` pipeline | |

### 主要差异 {#key-differences}

- **没有可视化窗体设计器（拖放式）：**Avalonia 用 XAML 声明布局。虽然有实时预览器，但你是在写标记，而不是把组件拖到画布上。多数开发者挺过最初的学习曲线后，反而觉得这样更快。
- **MVVM 取代事件驱动的写法：**在 Delphi 里，你把按钮点击直接接到某个方法上；在 Avalonia 里，你把控件绑定到视图模型上的属性和命令。这种分离让代码更好测试、也更好维护。
- **没有组件面板：**你不是从面板里拖组件，而是在 XAML 中声明控件，再通过属性和绑定来配置它们。
- **.NET 生态：**NuGet 取代了 Delphi 的组件市场，而 .NET 的包生态规模要大得多。

## 从 Qt（QML / Qt Widgets）迁移 {#from-qt-qml-qt-widgets}

Qt 是久经考验的跨平台框架，但它以 C++ 为根基、授权关系复杂（LGPL 与商业授权之分），再加上 Qt Widgets 与 QML 的割裂，难免带来摩擦。若你的团队已经在用 .NET，或者正有此意，那么 Avalonia 能让你不离开 .NET 生态就拿到一个跨平台 UI 框架。

### 概念对照 {#concept-mapping-1}

| Qt | Avalonia | 注释支持情况 |
|---|---|---|
| `QMainWindow` | `Window` | |
| `QWidget` | `Control` | |
| `QML` 声明式界面 | XAML 声明式界面 | 两者都是基于标记的界面定义 |
| 信号与槽 | 数据绑定 + `ICommand` | Avalonia 走的是 MVVM，而非信号/槽 |
| `QVBoxLayout` / `QHBoxLayout` | `StackPanel` | |
| `QGridLayout` | `Grid` | |
| `QPushButton` | `Button` | |
| `QLineEdit` | `TextBox` | |
| `QTextEdit` | `TextBox` with `AcceptsReturn="True"` | |
| `QLabel` | `TextBlock` | |
| `QCheckBox` | `CheckBox` | |
| `QComboBox` | `ComboBox` | |
| `QListView` / `QListWidget` | `ListBox` | |
| `QTreeView` / `QTreeWidget` | `TreeView` | |
| `QTableView` | `DataGrid`（NuGet 包） | |
| `QTabWidget` | `TabControl` | |
| `QScrollArea` | `ScrollViewer` | |
| `QMenu` | `ContextMenu` / `Menu` | |
| Qt Style Sheets (QSS) | 类 CSS 的选择器与样式 | Avalonia 的样式系统在概念上与 QSS 相仿 |
| `QThread` / 线程亲和性 | `Dispatcher.UIThread` | UI 线程亲和性的概念相同 |
| `.ui` 文件（Qt Designer） | `.axaml` files | |
| `qmake` / `CMake` | MSBuild / `dotnet` CLI | |

### 主要差异 {#key-differences-1}

- **不需要 C++：**Avalonia 是纯 .NET（C# 或 F#）。做基础界面时既无需桥接层，也无需 P/Invoke。
- **授权更省心：**Avalonia 采用 MIT 许可。既不必操心 LGPL 合规，框架本身也不收商业授权费。
- **样式一上手就熟：**若你用过 Qt 样式表，Avalonia 那套类 CSS 的选择器会让你感到亲切。它支持伪类、嵌套选择器和样式类。
- **界面语言只有一种：**Qt 分成 Widgets（C++）和 QML（类 JavaScript）两套，Avalonia 则自始至终只用 XAML。

## 从 Electron 迁移 {#from-electron}

Electron 应用本质上是用 Chromium 打包起来的 Web 应用。它们当然能跑，但内存和 CPU 开销不小、启动慢，而且与操作系统格格不入。若你的团队当初选 Electron 只是因为那是走向跨平台最快的路，那么 Avalonia 能给你同样的覆盖面，外加原生的性能。

### 团队为什么要离开 Electron {#why-teams-move-away-from-electron}

- **内存占用：**每个 Electron 应用都捆着一整个 Chromium 实例。一个简单应用就能吃掉几百兆内存。
- **启动时间：**加载 Chromium 带来的延迟肉眼可见，在低端硬件上尤其明显。
- **没有原生感：**Electron 应用的外观和行为像网页，而不像桌面程序。窗口管理、键盘快捷键和系统集成样样都得额外花工夫。
- **更新与打包麻烦：**把 Chromium 一并发出去，构建产物更大，更新也更沉。

### Avalonia 能给你什么 {#what-avalonia-offers-instead}

- **原生性能：**Avalonia 直接渲染，不经浏览器引擎。内存占用和启动时间都大幅降低。
- **真正的跨平台：**一套 .NET 代码库，覆盖 Windows、macOS、Linux、iOS、Android 和 WebAssembly。
- **桌面原生的行为：**窗口管理、系统菜单、键盘导航和托盘图标，在各平台上都如用户所料地工作。
- **用 C# 而非 JavaScript：**强类型、编译型，工具链和调试支持都很成熟。

## 从 ASP.NET MVC / Blazor（Web 转桌面）迁移 {#from-aspnet-mvc-blazor-web-to-desktop}

若你有一个用 ASP.NET MVC 或 Blazor 做的 Web 应用，又想提供原生的桌面体验，那 Avalonia 是个天作之合。你的后端、数据层和业务逻辑（统统是 .NET 写的）都可以直接与 Avalonia 桌面客户端共享。你不是在重写应用逻辑，而是在给它加一个原生前端。

### 可以直接搬过来的 {#what-transfers-directly}

- **模型与 DTO：**你的数据类在 Avalonia 中无需改动即可使用。
- **服务与业务逻辑：**只要不依赖 ASP.NET 的 HTTP 管线，都能直接拿来用。
- **依赖注入：**Avalonia 支持 `Microsoft.Extensions.DependencyInjection`，用法与你在 ASP.NET 中的那一套别无二致。
- **校验：**`INotifyDataErrorInfo` 和数据注解校验器都能与 Avalonia 的绑定系统配合。

### 会变的地方 {#what-changes}

- **没有 HTML/CSS/Razor：**Avalonia 用 XAML 做布局，用类 CSS 的样式系统管外观。这些概念与 HTML 不同，但做界面时 XAML 更为精炼。
- **没有 HTTP 请求/响应循环：**桌面应用是有状态的。你把界面控件绑定到视图模型的属性上、让它们实时更新，而不是每次请求都渲染一遍页面。
- **导航由应用自己管：**这里没有 URL 路由。导航要么靠按应用状态替换视图来实现，要么用 [NavigationPage](/controls/navigation/navigationpage) 做基于栈的页面导航。

## 快速上手 {#getting-started}

不管你从哪个框架过来，起手的地方都是同样这几处：

1. **[创建你的第一个 Avalonia 应用](/docs/get-started/create-your-first-project)：**几分钟就能跑起一个应用。
2. **[学习 XAML 基础](/docs/xaml)：**弄懂 Avalonia 是怎么声明界面的。
3. **[学习数据绑定](/docs/data-binding/introduction-to-data-binding)：**Avalonia 把界面与数据连起来的根基。
4. **[逛一逛控件库](/controls)：**看看开箱就有哪些东西可用。

## 另请参阅 {#see-also}

- [样式](/docs/styling/styles)：Avalonia 类 CSS 样式机制的运作方式。
- [MVVM 模式](/docs/fundamentals/the-mvvm-pattern)：把界面与逻辑分开。
- [控件参考](/controls)：Avalonia 控件的完整文档。

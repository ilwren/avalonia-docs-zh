---
title: Windows Forms
description: 把 Windows Forms 应用迁移到 Avalonia，获得跨平台支持与现代界面。
doc-type: migration
---

自 2002 年起，Windows Forms 一直在支撑着生产环境里的应用。若你手上的 WinForms 应用运转良好，继续用下去自有其道理。但 Windows Forms 只能跑在 Windows 上，而它所能提供的，与用户心目中现代界面该有的样子，差距一年比一年大。

Avalonia 为你指出了一条向前的路。它是个跨平台 .NET UI 框架，带有基于 XAML 的布局系统、数据绑定、样式机制和一整套控件库，可运行在 Windows、macOS、Linux、iOS、Android 和 WebAssembly 上。若你一直在用 WinForms、又在琢磨下一步该往哪走，Avalonia 正是为处在这个位置的开发者准备的。

:::tip[迁移上需要帮助？]
Avalonia 团队有大量把 Windows Forms 应用移植到 Avalonia 的经验。若你不想单打独斗、希望得到专业指导，我们提供相应服务，详见 [Avalonia 服务](https://avaloniaui.net/services)。
:::

## 会变的地方 {#what-changes}

Windows Forms 与 Avalonia 的界面模型从根子上就不一样。这不像在 XAML 框架之间迁移（比如从 WPF 到 Avalonia），多数概念都找不到一一对应者。请做好学习新套路的准备，而不是把旧的翻译过来。

| Windows Forms | Avalonia | 注释支持情况 |
|---|---|---|
| 由设计器生成的布局 | XAML 声明式布局 | 布局写在 `.axaml` 文件里，而不是生成的代码中 |
| `Control` 基类 | `Control` / `TemplatedControl` | Avalonia 把非模板化控件与模板化控件分得很清楚 |
| 凡事都靠事件处理程序 | 数据绑定 + MVVM | Avalonia 极力主张把界面与逻辑分开 |
| `Dock` 与 `Anchor` 定位 | 布局面板（`Grid`、`StackPanel`、`DockPanel`） | 基于面板的布局取代了锚定/停靠定位 |
| `DataGridView` | `DataGrid`（NuGet 包） | 独立的包：`Avalonia.Controls.DataGrid` |
| `ToolStrip` / `MenuStrip` | `Menu` / `ToolTip` / `ContextMenu` | 控件名不同，概念相同 |
| `Form` | `Window` | |
| `UserControl` | [`UserControl`](/api/avalonia/controls/usercontrol) | 名字相同，基类不同 |
| `MessageBox.Show()` | 对话框窗口或自定义覆盖层 | 没有内置的消息框 |
| GDI+ 绘图（`OnPaint`） | `DrawingContext` 或者重写自定义的 `Render` | 渲染 API 不同 |
| `Application.Run(new MainForm())` | `AppBuilder` pipeline | Avalonia 的应用启动采用构建器模式 |

## 迁移策略 {#migration-strategy}

把 WinForms 迁到 Avalonia 可不是查找替换那么简单。最稳妥的做法是渐进式推进：新界面先用 Avalonia 做，现有的 WinForms 界面照常运行，其余部分日后再逐步迁移。

### 方案一：另起炉灶，逐步迁移 {#option-1-start-fresh-migrate-incrementally}

新建一个 Avalonia 项目，从最简单的界面开始，一块一块地重建。这是最干净的做法，结果也最好，只是前期投入最大。

1. 按[入门指南](/docs/get-started/create-your-first-project)新建一个 Avalonia 项目。
2. 搭好视图模型和数据层（这些往往可以直接从 WinForms 项目里共享过来）。
3. 把每个界面重建为 Avalonia 的 `Window` 或 `UserControl`。
4. 所有界面都迁完之后，让 WinForms 项目退役。

### 方案二：在 WinForms 中承载 Avalonia 控件（仅限 Windows） {#option-2-host-avalonia-controls-inside-winforms-windows-only}

若你希望 WinForms 应用照常运行、同时逐步引入 Avalonia，可以用 `WinFormsAvaloniaControlHost` 把 Avalonia 控件嵌进 WinForms 窗口里。你也可以在 WinForms 应用中，把全新的界面做成独立的 Avalonia 窗口。这样你就能用 Avalonia 开发新功能，而不必动现有的 WinForms 代码。

这个办法只能在 Windows 上奏效，毕竟 Windows Forms 本身就只支持 Windows。不过，若你把 Avalonia 控件放进单独的类库里，日后这些控件照样能用在独立的跨平台 Avalonia 应用中。

配置步骤请参阅[在 Windows Forms 中使用 Avalonia](/docs/platform-specific-guides/windows#using-avalonia-in-windows-forms)。

## 需要学的关键概念 {#key-concepts-to-learn}

若你从 WinForms 过来、又没接触过 XAML，下面这几块最需要适应：

- **[XAML 基础](/docs/xaml)：**Avalonia 用 XAML 声明界面的布局与结构，它取代了 WinForms 的设计器。
- **[数据绑定](/docs/data-binding/introduction-to-data-binding)：**你不再在事件处理程序里设置控件属性，而是把控件绑定到视图模型的属性上，变化会自动流动起来。
- **[MVVM 模式](/docs/fundamentals/the-mvvm-pattern)：**Avalonia 的设计思路就是把界面（视图）与应用逻辑（视图模型）分开。这是从 WinForms 过来后最大的观念转变。
- **[样式](/docs/styling/styles)：**Avalonia 用的是带选择器和样式类的类 CSS 样式系统，而不是逐个控件设置属性。
- **[布局面板](/docs/layout)：**Avalonia 不用绝对定位或停靠/锚定，而是用 `Grid`、`StackPanel`、`DockPanel` 这类面板来摆放控件。

## 另请参阅 {#see-also}

- [Avalonia 入门](/docs/get-started/create-your-first-project)：创建你的第一个 Avalonia 应用。
- [在 Windows Forms 中使用 Avalonia](/docs/platform-specific-guides/windows#using-avalonia-in-windows-forms)：在现有的 WinForms 应用里用上 Avalonia 控件。
- [控件参考](/controls)：Avalonia 控件的完整文档。

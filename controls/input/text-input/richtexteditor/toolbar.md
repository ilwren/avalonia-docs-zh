---
id: toolbar
title: 工具栏与选区浮层
doc-type: reference
tags:
 - avalonia pro
 - avalonia enterprise
---

import DefaultToolbar from '/img/controls/richtexteditor/default-toolbar.png';
import CustomToolbarMinimal from '/img/controls/richtexteditor/custom-toolbar-minimal.png';
import WordCountTool from '/img/controls/richtexteditor/word-count-tool.png';
import AreaAware from '/img/controls/richtexteditor/area-aware.gif';
import DefaultMiniBar from '/img/controls/richtexteditor/default-mini-bar.png';
import CustomMiniBarMinimal from '/img/controls/richtexteditor/custom-mini-bar-minimal.png';
import DefaultContextMenu from '/img/controls/richtexteditor/default-context-menu.png';
import CustomContextMenu from '/img/controls/richtexteditor/custom-context-menu.png';
import CustomContextMenuSpecialized from '/img/controls/richtexteditor/custom-context-menu-specialized.png';
import CustomThemeToolbar from '/img/controls/richtexteditor/custom-theme-toolbar.png';

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

默认情况下，`RichTextEditor` 自带一条主工具栏、一条选区迷你工具条和一个右键上下文菜单。这几条工具栏都建立在同一套基础机制之上，可以各自独立地定制：换布局、加自己的工具、调教溢出菜单、给按钮换主题，等等。本指南按从常见到进阶的顺序，带你过一遍可用的定制手段。

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## 工具栏架构 {#toolbar-architecture}

工具栏系统把界面呈现与行为逻辑分了开来。`EditorToolbar` 是一个 `TemplatedControl`，带有一个强类型的 `Tools` 集合（`AvaloniaList<EditorTool>`）并被标记为 `[Content]` 属性——XAML 子元素会自动加入 `Tools`，且只能是 `EditorTool` 的实例。带动作的工具派生自 `ActionTool`（它补充了 `Action`/`Icon`/`ToolTipText`）；分隔线和分组则直接派生自 `EditorTool`。

- **`EditorTool`**：凡是寄宿在 `EditorToolbar` 或 `ToolbarGroup` 中的项，都以它为抽象基类。它负责按目标区域控制可见性、承载溢出相关的元数据，并负责发现编辑器宿主。
- **`ActionTool`**：绑定到 `IEditorAction` 的那类工具的抽象基类。它补充了 `Action`、`Icon` 和 `ToolTipText`，并让 `IsEnabled` 与 `Action.CanExecute(host)` 保持同步。大多数具体工具（按钮、切换、下拉框、浮层）都派生自它。
- **`ToolbarGroup`**：它本身就是一个 `EditorTool`，内部寄宿着自己那套强类型的子工具 `Tools` 集合。同一分组共享可见性状态，也就是说空间不够时它们会一起收进溢出菜单。分组可以嵌套，而嵌套分组会把自己的子项并入外层顶级分组的溢出区，而不是作为一个整体折叠——因为分组本身没有一个溢出菜单项来代表它的子项。
- **`EditorToolbar`**：一个 `TemplatedControl`，对外暴露强类型的 `Tools` 集合（`AvaloniaList<EditorTool>`）并标记为 `[Content]` 属性。它负责把各项接到编辑器上、把当前活动的目标区域推送给每个工具，并执行溢出折叠的布局遍历。各项会被插入到控件模板中名为 `PART_ItemsHost` 的 `Panel` 里，该名称以常量 `EditorToolbar.PartItemsHost` 的形式公开。

`EditorToolbar` 和 `ToolbarGroup` 都使用一个名为 `PART_ItemsHost` 的 `Panel` 模板部件。默认主题用的是 `WrapPanel`；嵌在 `RichTextEditor` 里的那条工具栏则用横向的 `StackPanel`。给任一控件重做模板、换成任意面板类型，即可改变布局。每个模板化的工具栏控件都用 `[TemplatePart]` 声明自己的部件，并把名称以 `public const string Part*` 成员的形式公开。

```
RichTextEditor
  └─ EditorToolbar            (TemplatedControl with [Content] Tools : AvaloniaList<EditorTool>)
       ├─ ToolbarGroup        (EditorTool with [Content] Tools, collective visibility)
       │    ├─ ButtonTool     (ActionTool)
       │    ├─ ToggleTool     (ActionTool)
       │    ├─ ToolbarGroup   (groups may nest)
       │    └─ ...
       ├─ SeparatorTool       (EditorTool, no action surface)
       └─ OverflowTool        (ActionTool, the "..." button that hosts collapsed tools)
```

### Namespaces

```csharp
using Avalonia.Controls.Documents.Primitives.Toolbar; // EditorToolbar, tools, groups
using Avalonia.Controls.Documents.Primitives.Actions; // EditorActions, IEditorAction
using Avalonia.Controls.Documents.Primitives; // EditorSelectionFlyout, EditorContextMenu
using Avalonia.Controls.Documents.Primitives.Adorners; // ToolbarTargetAreas
```

以上这些类型在 XAML 中都位于 Avalonia 的默认命名空间（`https://github.com/avaloniaui`）下。

## 从早期 `EditorToolbar` API 迁移 {#migration-from-earlier-editortoolbar-api}

如果你的现有代码还在用基于 `ItemsControl` 的旧接口，请按下表更新：

| 旧写法 | 新写法 |
|---|---|
| `EditorToolbar.Items` / `ToolbarGroup.Items` | `Tools` (typed `AvaloniaList<EditorTool>`, `[Content]`) |
| `EditorToolbar.ItemsPanel` / `ItemsSource` | 已移除。请给工具栏重做模板，放一个名为 `PART_ItemsHost` 的 `Panel`。 |
| `EditorToolbar`/`ToolbarGroup` 派生自 `ItemsControl` | 两者现在都是 `TemplatedControl`。`ToolbarGroup` 派生自 `EditorTool`。 |
| `EditorTool.Action` / `Icon` / `ToolTipText` | 已移至 `ActionTool`。绑定动作的自定义工具应派生自 `ActionTool`（被动型工具仍留在 `EditorTool` 上）。 |
<br />

XAML 的隐式子元素写法（`<EditorToolbar><ToolbarGroup>…</ToolbarGroup></EditorToolbar>`）没有变化——子元素通过 `[Content]` 特性加入 `Tools`。只有显式写成 `<EditorToolbar.Items>` / `<EditorToolbar.ItemsPanel>` 元素形式的地方需要改名。在代码中，把 `toolbar.Items.Add(...)` 换成 `toolbar.Tools.Add(...)`。

### 12.3 中的变化 {#changes-in-123}

| 变更 | 含义 |
|---|---|
| `ToolbarGroup` nests | 过去把分组加进另一个分组的 `Tools` 会抛异常，在解析时表现为 `XamlLoadException`。现在溢出逻辑会沿树下探。 |
| `EditorToolbar.EditorHost` | 把工具栏绑定到编辑宿主。`Editor` 保持 `RichTextEditor?` 类型不变。两者中哪个有值，工具栏就驱动哪个。 |
| 工具栏推送 `ActiveTargetAreas` | 该值在每次选区和文档变化时重新推导。过去用于传播它的那些逐工具主题 setter 已经没有了。需要跟随插入符的工具，请把 `IsVisible` 绑定到 `IsVisibleForTargetArea`，两者都是可写属性。 |
| `ToolbarTargetAreas.CaretAreas` | 指明普通插入符可以抵达的区域。`EditorTool.TargetAreas` 的默认值。 |
| 点击绑定了块属性动作的工具 | 什么也不会发生。过去它会从一个无人观察的任务中抛出 `NotSupportedException`。 |

## 默认工具栏 {#default-toolbar}

内置的 `EditorToolbar` 由编辑器默认控件主题中的 `RichTextEditor.Toolbar` 填充，包含下列工具，按此顺序排列并归入这些分组。

<Image light={DefaultToolbar} position="center" cornerRadius="true" alt="The default RichTextEditor toolbar with history, clipboard, font, inline formatting, lists, table, block layout, and overflow groups."/>
<br />

1. **历史** —— 撤销、重做
2. **剪贴板** —— 剪切、复制、粘贴、全选
3. **字体** —— 字体、字号、前景色、背景色
4. **行内格式** —— 加粗、斜体、下划线、删除线、上标、下标、链接
5. **列表** —— 项目符号列表、编号列表
6. **插入** —— 插入表格、插入图片、页眉和页脚
7. **块布局** —— 文本对齐、块边框
8. **图片** —— 图片尺寸（仅在插入符位于图片上时显示）
9. **溢出** —— 「...」按钮，点击后列出被折叠的工具

还有第二条 `EditorToolbar`，用的是同一套工具机制，寄宿在表格覆盖层的操作浮层中——即悬停单元格、以及选中行列条带时出现的那个「...」按钮。它只包含表格结构相关的操作。

大多数工具会随上下文变化：脱离相应语境就自动隐去，比如列表工具在列表之外不显示，表格工具在表格之外不显示。这是通过声明每个工具或分组的 [`ToolbarTargetAreas`](#toolbar-target-areas) 来实现的。

## 替换默认工具栏 {#replacing-the-default-toolbar}

定制默认工具栏有两条路子，取决于你的界面需求。

### Option 1: Set `RichTextEditor.Toolbar`

把一个自定义的 `EditorToolbar` 赋给 `RichTextEditor` 上的 `Toolbar` setter。把它放进编辑器的控件主题，即可作用于应用中的每一个 `RichTextEditor`：

```xml
<Application.Resources>
  <ControlTheme x:Key="{x:Type RichTextEditor}"
                TargetType="RichTextEditor"
                BasedOn="{StaticResource {x:Type RichTextEditor}}">
    <Setter Property="Toolbar">
      <Template>
        <EditorToolbar>
          <ToolbarGroup>
            <ButtonTool Action="{x:Static EditorActions.Undo}" />
            <ButtonTool Action="{x:Static EditorActions.Redo}" />
          </ToolbarGroup>

          <SeparatorTool />

          <ToolbarGroup Classes="AreaAware" TargetAreas="Text">
            <ToggleTool Action="{x:Static EditorActions.Bold}" />
            <ToggleTool Action="{x:Static EditorActions.Italic}" />
            <ToggleTool Action="{x:Static EditorActions.Underline}" />
          </ToolbarGroup>

          <OverflowTool />
        </EditorToolbar>
      </Template>
    </Setter>
  </ControlTheme>
</Application.Resources>
```

### 方案二：把工具栏与编辑器分开摆放 {#option-2-build-a-toolbar-separately-from-the-editor}

若工具栏不该待在编辑器上方，而要放到别处（比如侧边栏、窗口外框里，或由多个编辑器共用），可以隐藏内置工具栏，再把一个 `EditorToolbar` 摆到你想要的位置。

做法是：在 XAML 中定义独立的 `EditorToolbar`，再在对应的代码隐藏中把它挂到编辑器上。

<Tabs>
<TabItem value="xaml" label="XAML">

```xml
<DockPanel>
  <EditorToolbar x:Name="MyToolbar" DockPanel.Dock="Top">
    <ToolbarGroup>
      <ButtonTool Action="{x:Static EditorActions.Undo}" />
      <ButtonTool Action="{x:Static EditorActions.Redo}" />
    </ToolbarGroup>
    <ToolbarGroup Classes="AreaAware" TargetAreas="Text">
      <ToggleTool Action="{x:Static EditorActions.Bold}" />
      <ToggleTool Action="{x:Static EditorActions.Italic}" />
    </ToolbarGroup>
  </EditorToolbar>

  <RichTextEditor x:Name="MyEditor" ShowToolbar="False" />
</DockPanel>
```

</TabItem>
<TabItem value="csharp" label="Code-behind">

```csharp
public MainWindow()
{
    InitializeComponent();
    MyToolbar.Editor = MyEditor;
}
```

</TabItem>
</Tabs>

:::tip
运行时重新给 `EditorToolbar.Editor` 赋值，就能让同一个 `EditorToolbar` 为不同的编辑器服务。多标签页的文档界面常用这一招——一条共享工具栏跟随当前活动的标签页。
:::

### 极简示例 {#minimalist-example}

一条只有撤销/重做和加粗/斜体的极简工具栏。注意工具图标是在与工具动作不同的标签中设置的。

<Image light={CustomToolbarMinimal} position="center" cornerRadius="true" alt="A minimal custom toolbar containing Undo, Redo, Bold, and Italic tools separated by a divider."/>
<br />

```xml
<ControlTheme x:Key="{x:Type RichTextEditor}"
              TargetType="RichTextEditor"
              BasedOn="{StaticResource {x:Type RichTextEditor}}">
  <Setter Property="Toolbar">
    <Template>
      <EditorToolbar Margin="4">

        <ButtonTool Action="{x:Static EditorActions.Undo}">
            <ButtonTool.Icon>
                <ContentPresenter ContentTemplate="{StaticResource EditorIcons.Undo}" />
            </ButtonTool.Icon>
        </ButtonTool>

        <ButtonTool Action="{x:Static EditorActions.Redo}">
            <ButtonTool.Icon>
                <ContentPresenter ContentTemplate="{StaticResource EditorIcons.Redo}" />
            </ButtonTool.Icon>
        </ButtonTool>

        <SeparatorTool />

        <ToggleTool Action="{x:Static EditorActions.Bold}">
            <ToggleTool.Icon>
                <ContentPresenter ContentTemplate="{StaticResource EditorIcons.Bold}" />
            </ToggleTool.Icon>
        </ToggleTool>

        <ToggleTool Action="{x:Static EditorActions.Italic}" >
            <ToggleTool.Icon>
                <ContentPresenter ContentTemplate="{StaticResource EditorIcons.Italic}" />
            </ToggleTool.Icon>
        </ToggleTool>

      </EditorToolbar>
    </Template>
  </Setter>
</ControlTheme>
```

## EditorTool 的各种类型 {#editortool-types}

工具栏上的各类组件——按钮、切换、下拉框等等——都是 `EditorTool` 的子类。这套继承体系分成两支：

- `EditorTool` 本身是所有工具栏项的抽象基类，负责按目标区域控制可见性、承载溢出元数据、提供焦点归还辅助，以及发现编辑器宿主。`SeparatorTool` 和 `ToolbarGroup` 不绑定动作，因此直接派生自它。
- `ActionTool` 是中间层抽象类，补充了与动作相关的属性（`Action`、`Icon`、`ToolTipText`），并让状态与编辑器保持同步。大多数具体控件——按钮、切换、下拉框、浮层——都派生自它。

实际开发中，你很少需要直接用这两个基类。下面列出的内置子类已经能覆盖绝大多数场景。

### 内置子类 {#built-in-subclasses}

| 类 | 基类 | 控件形态 | 典型用途 |
|---|---|---|---|
| `ButtonTool` | `ActionTool` | Button | 一次性命令，比如撤销、剪切、粘贴。 |
| `ToggleTool` | `ActionTool` | 切换按钮 | 格式设置，比如加粗、斜体。 |
| `ListToggleTool` | `ToggleTool` | 分段切换按钮 | 列表开关（项目符号/编号），同时还能反映当前的标记样式。 |
| `ComboBoxTool` | `ActionTool` | Combobox | 从列表中选择，比如字体、字号。 |
| `ColorTool` | `ActionTool` | 抽象基类 | 两种拾色工具共用的基类。它的 `SelectedColor` 是 `Color?`，其中 `null` 表示无颜色。 |
| `ColorPickerTool` | `ColorTool` | 分段按钮 + Avalonia `ColorPicker` 浮层 | 挑选任意颜色，比如前景色、背景色。 |
| `ColorSwatchTool` | `ColorTool` | 分段按钮 + 色块调色板浮层 | 从固定调色板中挑选。 |
| `AlignmentFlyoutTool` | `ActionTool` | 带浮层的按钮 | 文本对齐：左对齐、右对齐、居中、两端对齐。 |
| `HyperlinkFlyoutTool` | `ActionTool` | 带浮层的按钮 | 插入/编辑超链接。 |
| `ImageFlyoutTool` | `ActionTool` | 带浮层的按钮 | 插入行内图片并调整尺寸。 |
| `ImageLinkFlyoutTool` | `ActionTool` | 带浮层的按钮 | 给选中的图片附加或清除超链接。 |
| `PageBandFlyoutTool` | `ActionTool` | 带浮层的按钮 | 把页眉页脚相关工具收进一个浮层。详见[页眉与页脚](#headers-and-footers)。 |
| `TablePickerTool` | `ActionTool` | 网格选择器 | 通过拉选网格大小来插入表格。 |
| `BorderFlyoutTool` | `ActionTool` | 带浮层的按钮 | 块边框的配置，比如边、粗细、颜色。 |
| `OverflowTool` | `ActionTool` | 带浮层的「...」按钮 | 用菜单浮层列出被折叠的工具。 |
| `SeparatorTool` | `EditorTool` | 竖线 | 视觉分隔线。 |

列表标记样式通过 `ListToggleTool` 使用，默认的选区迷你工具条用的就是它。在列表之外，它就是个普通切换按钮；进入匹配的列表后，它变成分段按钮，副半边会打开该列表类型的标记选项，驱动 `EditorActions.BulletMarkerStyle` 和 `EditorActions.NumberedMarkerStyle`。主工具栏的两个列表开关用的是普通的 `ToggleTool`，因此默认并不暴露标记样式。

### 核心属性 {#core-properties}

`EditorTool` 为每个工具栏项提供下列成员：

| 属性 | 类型 | 说明 |
|---|---|---|
| `TargetAreas` | `ToolbarTargetAreas` | 该工具应在哪些上下文中出现。默认值为 `CaretAreas`。参阅 [ToolbarTargetAreas](#toolbar-target-areas)。 |
| `ActiveTargetAreas` | `ToolbarTargetAreas` | 只读。插入符当前所处的区域，由宿主工具栏随选区移动推送过来。 |
| `IsVisibleForTargetArea` | `bool` | 只读。`TargetAreas` 是否与 `ActiveTargetAreas` 匹配。 |
| `OverflowMenuItem` | `MenuItem?` | 该工具被折叠进溢出菜单时所显示的菜单项。`null` 表示该工具不可折叠。 |
| `CanCollapseOverride` | `bool?` | 显式指定是否折叠进溢出菜单，覆盖自动判断。 |

`ActionTool` 补充了与动作相关的那部分接口（所有可交互工具都继承它）：

| 属性 | 类型 | 说明 |
|---|---|---|
| `Action` | `IEditorAction?` | 该工具执行的动作。 |
| `Icon` | `object?` | 该工具显示的图标。 |
| `ToolTipText` | `string?` | 悬停时作为工具提示显示的文字。未设置时默认取 `Action.DisplayName`。 |

`EditorToolbar` 自身则带有：

| 属性 | 类型 | 说明 |
|---|---|---|
| `Editor` | `RichTextEditor?` | 该工具栏所驱动的宿主。重新赋值即可在运行时让工具栏改换目标。 |
| `EditorHost` | `ITextEditorHost?` | 该工具栏所驱动的、并非 `RichTextEditor` 的那个宿主。 |
| `Tools` | `AvaloniaList<EditorTool>` | 工具栏项的 `[Content]` 集合。 |
| `ActiveTargetAreas` | `ToolbarTargetAreas` | 只读。由选区推导得出，并推送给每一个工具。 |
| `ShowShortcuts` | `bool` | 工具提示中是否显示该动作的键盘手势。 |
| `ToolSpacing` | `double` | 工具栏面板中各项之间的统一间距。`ToolbarGroup` 对其子项另有一个自己的间距。 |

### XAML 用法 {#xaml-usage}

```xml
<!-- One-shot command -->
<ButtonTool Action="{x:Static EditorActions.Undo}">
  <ButtonTool.Icon>
    <ContentPresenter ContentTemplate="{StaticResource EditorIcons.Undo}" />
  </ButtonTool.Icon>
</ButtonTool>

<!-- Formatting toggle -->
<ToggleTool Action="{x:Static EditorActions.Bold}">
  <ToggleTool.Icon>
    <ContentPresenter ContentTemplate="{StaticResource EditorIcons.Bold}" />
  </ToggleTool.Icon>
</ToggleTool>

<!-- Property combo with custom item template -->
<ComboBoxTool Action="{x:Static EditorActions.FontFamily}" Width="170">
  <ComboBoxTool.ItemTemplate>
    <DataTemplate DataType="FontFamily">
      <TextBlock Text="{Binding Name}" FontFamily="{Binding}" />
    </DataTemplate>
  </ComboBoxTool.ItemTemplate>
</ComboBoxTool>
```

## 创建自定义工具 {#creating-a-custom-tool}

若内置子类覆盖不了你想要的控件形态，可以自行派生实现。请按使用场景挑选基类：

- **`EditorTool`** —— 用于不绑定动作的被动型控件（状态显示、装饰性标签）。重写 `OnApplyTemplate` 来获取模板部件，重写 `OnEditorHostAttached` 以便在编辑器宿主就位时作出反应。
- **`ActionTool`** —— 用于执行 `IEditorAction` 的交互式工具。你会继承到 `Action`、`Icon`、`ToolTipText`，以及一个在选区/内容/文档发生变化时触发的虚方法 `UpdateState()`。

两种情况下都要：

1. 提供一个控件模板来渲染你的控件。
2. 重写 `OnApplyTemplate` 以取得模板部件的引用。
3. 若基类是 `ActionTool`，重写 `UpdateState` 来刷新额外状态（比如自定义徽标）；若是 `EditorTool`，则挂上 `OnEditorHostAttached` 并自行订阅所需事件。
4. 在处理程序中，请先调用 `EnsureEditorFocus()` 再执行动作，好让焦点回到编辑器。

### 示例：字数统计工具 {#example-word-count-tool}

<Image light={WordCountTool} position="center" cornerRadius="true" alt="A custom word count tool docked at the end of the toolbar, displaying the current word count."/>
<br />

字数显示是个被动型控件，不执行任何动作，因此直接派生自 `EditorTool`。`UpdateState` 定义在 `ActionTool` 上，所以被动型工具要在 `OnEditorHostAttached` 中订阅宿主自身的事件来刷新自己，并在 `OnEditorHostDetached` 中退订。

这个实现通过遍历文档的 `DocumentSnapshot` 来统计字数。它枚举 `Run` 节点，并把块边界和换行当作词的分隔符，这样既不必分配一整份纯文本字符串，也不会把上一段的末词与下一段的首词粘在一起。

<Tabs>
<TabItem value="class" label="C#">

```csharp
using Avalonia.Controls;
using Avalonia.Controls.Primitives;
using Avalonia.Controls.Documents.TextModel;
using Avalonia.Controls.Documents.Serialization.Snapshot;

public class WordCountTool : EditorTool
{
    private TextBlock? _countText;

    protected override void OnApplyTemplate(TemplateAppliedEventArgs e)
    {
        base.OnApplyTemplate(e);
        _countText = e.NameScope.Find<TextBlock>("PART_Count");
        Refresh();
    }

    protected override void OnEditorHostAttached()
    {
        base.OnEditorHostAttached();

        if (EditorHost is { } host)
        {
            host.ContentChanged += OnHostChanged;
            host.DocumentChanged += OnHostChanged;
        }

        Refresh();
    }

    protected override void OnEditorHostDetached()
    {
        if (EditorHost is { } host)
        {
            host.ContentChanged -= OnHostChanged;
            host.DocumentChanged -= OnHostChanged;
        }

        base.OnEditorHostDetached();
    }

    private void OnHostChanged(object? sender, EventArgs e) => Refresh();

    private void Refresh()
    {
        if (_countText is null) return;

        var doc = EditorHost?.TextDocument;
        if (doc is null)
        {
            _countText.Text = "0 words";
            return;
        }

        var snapshot = doc.CreateSnapshot();
        int words = CountWords(snapshot);
        _countText.Text = $"{words} word{(words == 1 ? "" : "s")}";
    }

    private static int CountWords(DocumentSnapshot snapshot)
    {
        int count = 0;
        bool inWord = false;

        foreach (var node in snapshot.EnumerateNodes())
        {
            var kind = node.Kind;
            if (kind == TextDocumentNodeKind.Run)
            {
                int remaining = node.Length;
                int pos = node.StartOffset;
                while (remaining > 0)
                {
                    var chunk = snapshot.GetTextMemory(pos, remaining);
                    if (chunk.IsEmpty) break;

                    foreach (char c in chunk.Span)
                    {
                        if (char.IsWhiteSpace(c)) inWord = false;
                        else if (!inWord) { inWord = true; count++; }
                    }

                    pos += chunk.Length;
                    remaining -= chunk.Length;
                }
            }
            else if (kind == TextDocumentNodeKind.LineBreak
                || (kind.Flags & NodeKindFlags.Block) != 0)
            {
                // Block boundary — never merge the last word of one paragraph
                // with the first word of the next.
                inWord = false;
            }
        }

        return count;
    }
}
```

</TabItem>
<TabItem value="theme" label="XAML control theme">

```xml
<ControlTheme x:Key="{x:Type local:WordCountTool}" TargetType="local:WordCountTool">
  <Setter Property="Template">
    <ControlTemplate>
      <Border Padding="8,4"
              MinWidth="72"
              VerticalAlignment="Center">
        <TextBlock Name="PART_Count"
                   Classes="Caption"
                   Foreground="{DynamicResource TextControlForeground}"
                   VerticalAlignment="Center" />
      </Border>
    </ControlTemplate>
  </Setter>
</ControlTheme>
```

</TabItem>
<TabItem value="usage" label="Usage">

```xml
<EditorToolbar>
  <!-- ...other groups... -->
  <SeparatorTool />
  <local:WordCountTool />
</EditorToolbar>
```

</TabItem>
</Tabs>

## 编辑器动作 {#editor-actions}

每个工具都绑定到由静态类 `EditorActions` 提供的某个 `IEditorAction`。动作告诉工具：命令怎么执行、什么时候可用，以及（对切换类和属性类动作而言）该显示什么状态。在 XAML 中用 `{x:Static EditorActions.<Name>}` 绑定，也可以在代码中直接调用动作：

```csharp
if (EditorActions.Bold.CanExecute(editorHost))
    EditorActions.Bold.Execute(editorHost);

// Clipboard actions are asynchronous
await EditorActions.Paste.ExecuteAsync(editorHost);

// Property actions get and set typed values
EditorActions.FontSize.SetValue(editorHost, 16.0);
var current = EditorActions.FontSize.GetValue(editorHost);

// Toggles report their checked state
bool isBold = EditorActions.Bold.IsChecked(editorHost);
```

引用内置动作的方式就是这些 `EditorActions` 单例。它们背后的具体动作类（比如 `BoldAction`）都是 internal 的。`InsertImageAction` 和 `InsertTableAction` 是例外：它们是公开的，以便提供带参数的入口。

你仍然可以用这些公开类编写自定义编辑器动作：`IEditorAction`、`IToggleAction`、`IPropertyAction`、`IPropertyAction<T>`、`IBlockPropertyAction`、`IBlockPropertyAction<T>`、`EditorAction`、`FormattingToggleAction<T>`、`PropertyAction<T>` 和 `BlockPropertyAction<T>`。

:::note
动作的 `Gesture` 只是工具提示和菜单项上显示的内容，它不注册任何东西。真正触发的快捷键由编辑器的键盘组件处理。
:::

### 读取动作状态 {#reading-action-state}

每个单例的声明类型都是 `IEditorAction`。要取哪种状态，就转换成携带该状态的那个接口。

| 动作 | 接口 | 状态访问器 |
|---|---|---|
| `Bold`, `Italic`, `Underline`, `Strikethrough`, `Superscript`, `Subscript`, `BlockBorder`, `AlignLeft`, `AlignCenter`, `AlignRight`, `AlignJustify`, `ToggleBulletList`, `ToggleNumberedList`, `DifferentFirstPage`, `DifferentOddAndEvenPages`, `LinkToPrevious` | `IToggleAction` | `IsChecked(host)` |
| `FontFamily` | `IPropertyAction<FontFamily>` | `GetValue(host)`, `SetValue(host, value)`, `ClearValue(host)` |
| `FontSize` | `IPropertyAction<double>` | same |
| `ForegroundColor`, `BackgroundColor` | `IPropertyAction<IBrush?>` | same |
| `LineHeight` | `IBlockPropertyAction<double>` | 同上，外加 `HasConsistentValue(host)` |
| `Margin`, `Padding`, `BorderThickness` | `IBlockPropertyAction<Thickness>` | same |
| `BlockBackground`, `BorderBrush` | `IBlockPropertyAction<IBrush?>` | same |
| `BulletMarkerStyle`, `NumberedMarkerStyle` | `IBlockPropertyAction<TextMarkerStyle>` | same |
| `TextAlignmentAction` | `IBlockPropertyAction<TextAlignment>` | same |
| `InsertImage` | `InsertImageAction` | `ExecuteWith(host, ...)` |
| `InsertTable` | `InsertTableAction` | `ExecuteWithSize(host, rowCount, columnCount)` |
<br />

`IBlockPropertyAction<T>` 派生自 `IPropertyAction<T>`，因此那些取值成员是继承来的，并未重新声明。

`IEditorAction.GetState(host)` 返回同一个值，但不带类型。它是为兼容而保留的，无法说明这个值出自哪一族。

调用块属性动作时若不传值，则什么也不会发生。要应用块属性，必须使用 `SetValue`。

### 编辑操作 {#edit-operations}

| 动作 | 快捷键 | 说明 |
|---|---|---|
| `Undo` | Ctrl+Z | 撤销上一步操作。 |
| `Redo` | Ctrl+Y | 重做上一步被撤销的操作。 |
| `Cut` | Ctrl+X | 把当前选区剪切到剪贴板。 |
| `Copy` | Ctrl+C | 把当前选区复制到剪贴板。 |
| `Paste` | Ctrl+V | 在插入符处粘贴剪贴板内容。 |
| `PasteUnformatted` | 不适用 | 以纯文本形式粘贴剪贴板内容。 |
| `SelectAll` | Ctrl+A | 全选内容。 |

### 文本格式 {#text-formatting}

| 动作 | 快捷键 | 说明 |
|---|---|---|
| `Bold` | Ctrl+B | 切换加粗。 |
| `Italic` | Ctrl+I | 切换斜体。 |
| `Underline` | Ctrl+U | 切换下划线。 |
| `Strikethrough` | Ctrl+- | 切换删除线。 |
| `Superscript` | Ctrl+Shift++ | 切换上标基线对齐。 |
| `Subscript` | Ctrl++ | 切换下标基线对齐。 |
| `FontFamily` | 不适用 | 获取或设置字体。 |
| `FontSize` | 不适用 | 获取或设置字号。 |

### Colors

| 动作 | 说明 |
|---|---|
| `ForegroundColor` | 获取或设置文本前景色。 |
| `BackgroundColor` | 获取或设置文本背景色（高亮色）。 |

### 块对齐 {#block-alignment}

| 动作 | 说明 |
|---|---|
| `TextAlignmentAction` | 按值获取或设置块对齐方式。 |
| `AlignLeft` | 块左对齐。 |
| `AlignCenter` | 块居中对齐。 |
| `AlignRight` | 块右对齐。 |
| `AlignJustify` | 块两端对齐。 |

### 块的间距与样式 {#block-spacing-and-styling}

| 动作 | 说明 |
|---|---|
| `LineHeight` | 获取或设置块的行高。 |
| `Margin` | 获取或设置块的外边距，四边一致。 |
| `Padding` | 获取或设置块的内边距，四边一致 |
| `BlockBackground` | 获取或设置块的背景色。 |
| `BorderThickness` | 获取或设置块的边框粗细。 |
| `BorderBrush` | 获取或设置块的边框颜色。 |
| `BlockBorder` | 开关块边框。 |

### Lists

| 动作 | 说明 |
|---|---|
| `ToggleBulletList` | 包成无序列表，或解除无序列表。 |
| `ToggleNumberedList` | 包成有序列表，或解除有序列表。 |
| `BulletMarkerStyle` | 设置项目符号的标记样式（比如 Disc、Circle、Square）。 |
| `NumberedMarkerStyle` | 设置编号的标记样式（比如 Decimal、LowerLatin、UpperRoman）。 |

### Tables

| 动作 | 说明 |
|---|---|
| `InsertTable` | 在插入符处插入表格，默认 3×3。 |
| `InsertRowBefore` | 在当前行上方插入一行。 |
| `InsertRowAfter` | 在当前行下方插入一行。 |
| `DeleteRow` | 删除当前行。 |
| `InsertColumnBefore` | 在当前列左侧插入一列。 |
| `InsertColumnAfter` | 在当前列右侧插入一列。 |
| `DeleteColumn` | 删除当前列。 |
| `MergeCells` | 把选中的单元格合并成一个。 |
| `SplitCell` | 拆分当前已合并的单元格。 |
| `DeleteTable` | 删除整个表格。 |

### Images

| 动作 | 说明 |
|---|---|
| `InsertImage` | 在插入符处插入行内图片。`ExecuteWith` 直接接受图片数据。 |
| `ReplaceImage` | 替换选中的图片。 |
| `DeleteImage` | 删除选中的图片。 |

### 页眉与页脚 {#headers-and-footers}

| 动作 | 说明 |
|---|---|
| `GoToHeader` | 进入插入符所在页的页眉。若尚无页眉，则创建通栏页眉。 |
| `GoToFooter` | 进入插入符所在页的页脚。若尚无页脚，则创建通栏页脚。 |
| `RemoveHeader` | 移除插入符所在页的、或插入符当前所处的页眉。 |
| `RemoveFooter` | 移除插入符所在页的、或插入符当前所处的页脚。 |
| `DifferentFirstPage` | 开关首页单独的页眉页脚。 |
| `DifferentOddAndEvenPages` | 开关奇偶页各自独立的页眉页脚。 |
| `LinkToPrevious` | 开关插入符所在小节是否沿用上一小节的页眉和页脚。 |
| `InsertPageNumber` | 插入当前页码字段。 |
| `InsertPageCount` | 插入总页数字段。 |
| `ReturnToBody` | 离开页眉页脚带，把插入符带回正文。 |

### Footnotes

| 动作 | 说明 |
|---|---|
| `InsertFootnote` | 在插入符处插入脚注锚点并打开该注释。 |
| `GoToFootnote` | 把插入符从锚点移进它的注释。 |
| `GoToFootnoteReference` | 把插入符从注释移回它的锚点。 |

### 按 ID 查找 {#lookup-by-id}

动作 ID 遵循 `"Category.Name"` 的格式（比如 `"Format.Bold"`、`"Table.InsertRowAfter"`）。`EditorActionIds` 把每个内置动作的 ID 都定义成了 `public const string`，于是查找时可以引用常量而不必写字面量。

```csharp
var action = EditorActions.GetById(EditorActionIds.Bold);
action?.Execute(editorHost);

// Enumerate every built-in action. All is an IReadOnlyList in
// declaration order, grouped by category.
foreach (var a in EditorActions.All)
    Console.WriteLine($"{a.Id}: {a.DisplayName}");
```

### 预载格式（springload）行为 {#springload-behavior}

选区为空时，切换类和属性类动作会设置一个 _预载_，意即该格式将作用于接下来键入的字符。这与常见文字处理软件给用户的预期是一致的。

## ToolbarGroup

`ToolbarGroup` 把一组相关工具归在一起，共享同一份可见性。若该分组的 `TargetAreas` 与当前插入符所处的语境不匹配，整个分组都会隐藏。

### 嵌套分组 {#nesting-groups}

Groups can nest. A `ToolbarGroup` is an `EditorTool`, so it can sit in another group's `Tools`. Nesting is how a sub-group gets its own `TargetAreas` or `ToolSpacing` inside a wider group.

Overflow descends the whole tree, and a nested group contributes its own children to the enclosing top-level group's menu section rather than collapsing as a unit. Setting `CanCollapseOverride="False"` on a nested group pins its children in place.

```xml
<ToolbarGroup Classes="AreaAware" TargetAreas="Text">
  <ToggleTool Action="{x:Static EditorActions.Bold}" />
  <ToggleTool Action="{x:Static EditorActions.Italic}" />

  <!-- Only while the caret is on an image -->
  <ToolbarGroup Classes="AreaAware" TargetAreas="Image">
    <ImageFlyoutTool />
    <ImageLinkFlyoutTool />
  </ToolbarGroup>
</ToolbarGroup>
```

### Applying the `AreaAware` class

`ToolbarGroup` does not react to the editor's active context by default. To enable contextual awareness, add the `AreaAware` class. `TargetAreas` defaults to `CaretAreas`—see [Toolbar target areas](#toolbar-target-areas) for which areas are included.

<Image light={AreaAware} position="center" maxWidth={250} cornerRadius="true" alt="Animation showing toolbar groups appearing and disappearing as the caret moves between body text, a list, and a table."/>
<br />

```xml
<!-- Text formatting group: Only visible when editing text -->
<ToolbarGroup Classes="AreaAware" TargetAreas="Text">
  <ToggleTool Action="{x:Static EditorActions.Bold}" />
  <ToggleTool Action="{x:Static EditorActions.Italic}" />
  <ToggleTool Action="{x:Static EditorActions.Underline}" />
</ToolbarGroup>

<!-- Table actions group: Only visible inside a table -->
<ToolbarGroup Classes="AreaAware" TargetAreas="Table">
  <ButtonTool Action="{x:Static EditorActions.InsertRowAfter}" />
  <ButtonTool Action="{x:Static EditorActions.DeleteRow}" />
</ToolbarGroup>

<!-- Always visible -->
<ToolbarGroup>
  <ButtonTool Action="{x:Static EditorActions.Undo}" />
  <ButtonTool Action="{x:Static EditorActions.Redo}" />
</ToolbarGroup>
```

## Toolbar target areas

`ToolbarTargetAreas` is a `[Flags]` enum in `Avalonia.Controls.Documents.Primitives.Adorners` describing the contexts in which a tool, a menu entry or a block adorner applies. `EditorToolbar` derives the active areas from the selection on every selection and document change and pushes them onto every tool.

| Flag | Caret context |
|---|---|
| `None` | No target area. |
| `Text` | The caret is in any text-editable position. |
| `Block` | The caret is in a block-level context. |
| `Table` | The caret is in a table. |
| `List` | The caret is in a list. |
| `Image` | The caret is on an inline image. |
| `TableCells` | The selection is a set of whole table cells. Driven by the selection shape rather than the caret's ancestry. |
| `PageBand` | The caret is in a header or footer (band). Bands are text, so tools targeting text areas are available. |
| `Footnote` | The caret is in a footnote. |
| `All` | Visible in all areas. |
| `CaretAreas` | Visible in caret-derived areas: `Text`, `Block`, `Table`, `List` and `Image`. Default for `EditorTool.TargetAreas`. |
<br />

`CaretAreas` is deliberately not every flag. `TableCells`, `PageBand` and `Footnote` must be opted into by name.

:::info
`CaretAreas` is new in v12.3. `All` is unchanged. Both are combinations of the other flags, so existing XAML such as `TargetAreas="Text,List"` or `TargetAreas="All"` still binds.
:::

If required, you can combine `ToolbarTargetAreas` to make a tool visible in multiple contexts.

```xml
<ToolbarGroup Classes="AreaAware" TargetAreas="Text,List">
```

## Managing the overflow menu

The overflow menu is the "..." button at the end of the toolbar. When the toolbar runs out of horizontal space, `EditorToolbar` collapses tools into this menu, starting from right to left by default.

Collection descends the whole tool tree. A nested `ToolbarGroup` contributes its own children rather than itself, and the menu reads in the same sequence the tools appear on the bar. A tool that is hidden by its target areas is skipped.

### Rules for what collapses

| `CanCollapseOverride` | `OverflowMenuItem` | 结果 |
|-----------------------|--------------------|---------|
| `null` | set | Collapsible (default) |
| `null` | `null` | Not collapsible |
| `true` | set | Collapsible |
| `true` | `null` | Not collapsible (no menu representation) |
| `false` | set | Not collapsible (pinned) |
| `false` | `null` | Not collapsible |

### Declaring overflow representations

Each collapsible tool must have its own `OverflowMenuItem`. In most cases, the menu item can be a simple `EditorMenuItem`.

```xml
<!-- Collapses into a simple menu item with the same icon -->
<ButtonTool Action="{x:Static EditorActions.Cut}">
  <ButtonTool.Icon>
    <ContentPresenter ContentTemplate="{StaticResource EditorIcons.Cut}" />
  </ButtonTool.Icon>
  <ButtonTool.OverflowMenuItem>
    <EditorMenuItem Action="{x:Static EditorActions.Cut}">
      <EditorMenuItem.Icon>
        <ContentPresenter ContentTemplate="{StaticResource EditorIcons.Cut}" />
      </EditorMenuItem.Icon>
    </EditorMenuItem>
  </ButtonTool.OverflowMenuItem>
</ButtonTool>
```

### Overflow for specialized tools

The following specialized subclasses of `EditorMenuItem` are available for tools that may not work well as plain menu items in an overflow menu.

| Source tool | Overflow item | 行为 |
|---|---|---|
| `ComboBoxTool` (fonts) | `FontFamilyMenuItem` | Submenu of fonts, each rendered in its own typeface. |
| `ComboBoxTool` (generic) | `PropertyMenuItem` | Submenu of values auto-populated from the action. |
| `ColorPickerTool` / `ColorSwatchTool` | `ColorMenuItem` | Submenu with color swatches and optional "No Color". |
| `AlignmentFlyoutTool` | `TextAlignmentMenuItem` | Submenu of alignment options. |

#### 示例 {#examples}

```xml
<!-- Font selector submenu -->
<ComboBoxTool Action="{x:Static EditorActions.FontFamily}" Width="170">
  <ComboBoxTool.OverflowMenuItem>
    <FontFamilyMenuItem Action="{x:Static EditorActions.FontFamily}" />
  </ComboBoxTool.OverflowMenuItem>
</ComboBoxTool>

<!-- Color picker submenu -->
<ColorPickerTool Action="{x:Static EditorActions.ForegroundColor}"
                       ToolTipText="Text color">
  <ColorPickerTool.OverflowMenuItem>
    <ColorMenuItem Action="{x:Static EditorActions.ForegroundColor}"
                         Header="Text color" />
  </ColorPickerTool.OverflowMenuItem>
</ColorPickerTool>

<!-- Text alignment submenu -->
<AlignmentFlyoutTool ToolTipText="Text alignment">
  <AlignmentFlyoutTool.OverflowMenuItem>
    <TextAlignmentMenuItem Header="Text alignment" />
  </AlignmentFlyoutTool.OverflowMenuItem>
</AlignmentFlyoutTool>
```

### Pinning important tools

To guarantee a tool always stays in the toolbar, even when horizontal space is tight, omit `OverflowMenuItem`. Undo and Redo are pinned this way in the default toolbar. Use `CanCollapseOverride="False"` only when you want to keep an overflow definition for conditional toggling.

```xml
<!-- Undo can never be collapsed -->
<ButtonTool Action="{x:Static EditorActions.Undo}">
  <ButtonTool.Icon>
    <ContentPresenter ContentTemplate="{StaticResource EditorIcons.Undo}" />
  </ButtonTool.Icon>
</ButtonTool>
```

## Default mini-bar

When the user selects text, a compact floating toolbar appears near the selection. This is the `SelectionFlyout`, an `EditorSelectionFlyout` (a `Flyout` subclass) that hosts a trimmed-down `EditorToolbar`.

<Image light={DefaultMiniBar} position="center" cornerRadius="true" alt="The default selection mini-bar floating above selected text, showing inline formatting, list, and block configuration tools."/>
<br />

The default mini-bar includes:

- **Inline formatting** (`Text`): Bold, Italic, Underline, Strikethrough, Text color, Highlight color
- **List toggles** (`Text`, `List`): Bullet, Numbered (each a `ListToggleTool` whose split half offers marker styles)
- **Block configuration**: Block background, Borders, Text alignment
- **Table cell operations** (`TableCells`): Merge cells, Split cell, Delete row, Delete column
- **Image actions** (`Image`): Align left/center/right, Image size, Replace image, Add or edit link, Delete image

The mini-bar anchors to the block containing the selection, rather than the pointer. Each group declares its own `TargetAreas`, so the table cell and image groups appear only for those selections.

## Replacing the default mini-bar

Within the `<RichTextEditor>` XAML tags, add a `<RichTextEditor.SelectionFlyout>` and specify a custom `EditorSelectionFlyout`. This can be used to host an `EditorToolbar`.

The outer `Border` named `PART_Chrome` is required — `EditorSelectionFlyout` uses it to distinguish the chrome from the surrounding shadow gutter when handling dismiss events.

This example shows a minimal mini-bar that only provides basic text formatting options.

<Image light={CustomMiniBarMinimal} position="center" cornerRadius="true" alt="A custom selection mini-bar with only Bold, Italic, and Underline toggles."/>
<br />

```xml
<RichTextEditor>
  <RichTextEditor.SelectionFlyout>
    <EditorSelectionFlyout Placement="TopEdgeAlignedLeft"
                           OverlayDismissEventPassThrough="True">
      <Border Name="PART_Chrome" Classes="EditorMiniBarChrome">
        <EditorToolbar>

          <ToggleTool Action="{x:Static EditorActions.Bold}">
            <ToggleTool.Icon>
              <ContentPresenter ContentTemplate="{StaticResource EditorIcons.Bold}" />
            </ToggleTool.Icon>
          </ToggleTool>

          <ToggleTool Action="{x:Static EditorActions.Italic}">
            <ToggleTool.Icon>
              <ContentPresenter ContentTemplate="{StaticResource EditorIcons.Italic}" />
            </ToggleTool.Icon>
          </ToggleTool>

          <ToggleTool Action="{x:Static EditorActions.Underline}">
            <ToggleTool.Icon>
              <ContentPresenter ContentTemplate="{StaticResource EditorIcons.Underline}" />
            </ToggleTool.Icon>
          </ToggleTool>

        </EditorToolbar>
      </Border>
    </EditorSelectionFlyout>
  </RichTextEditor.SelectionFlyout>
</RichTextEditor>
```

Some recommendations:

- Apply the `EditorMiniBarChrome` style class to the surrounding `Border` for the default rounded, shadowed appearance.
- Keep the set of tools small. The mini-bar should complement the main toolbar, not duplicate it.

### Disabling the mini-bar

Within the `<RichTextEditor>` XAML tags, set `SelectionFlyout` to `{x:Null}` to turn it off entirely.

```xml
<RichTextEditor SelectionFlyout="{x:Null}" />
```

## Default context menu

The contextual menu that opens when right-clicking within the text editor is the `EditorContextMenu` — a `MenuFlyout` subclass attached to `RichTextEditor.ContextFlyout`.

<Image light={DefaultContextMenu} position="center" maxWidth={250} cornerRadius="true" alt="The default right-click context menu with Cut, Copy, Paste, Select All, and table operations."/>
<br />

The default context menu contains:

- Cut, Copy, Paste
- Select All
- Table operations (Insert/Delete row, Insert/Delete column, Merge cells, Split cell, Delete table), visible only when the caret is inside a table
- Image operations (Replace image, Delete image), visible only on an image
- Page band operations (Insert page number, Insert page count, Return to body), visible only inside a header or footer

`EditorContextMenu` reads `TargetAreas` on each `EditorMenuItem` to hide items that do not apply to the current context. Unused separator lines left by hidden groups are also hidden automatically. Right-clicking moves the caret to the clicked position first before opening the menu. This ensures the menu opens with the correct context.

## Replacing the context menu

Within the `<RichTextEditor>` XAML tags, add a `<RichTextEditor.ContextFlyout>` and specify a custom `EditorContextMenu`. To add actions to the menu, add individual tags for `<EditorMenuItem>`.

<Image light={CustomContextMenu} position="center" maxWidth={250} cornerRadius="true" alt="A custom context menu with clipboard commands and context-sensitive table operations."/>
<br />

```xml
<RichTextEditor>
  <RichTextEditor.ContextFlyout>
    <EditorContextMenu Placement="Pointer">
      <EditorMenuItem Action="{x:Static EditorActions.Cut}" />
      <EditorMenuItem Action="{x:Static EditorActions.Copy}" />
      <EditorMenuItem Action="{x:Static EditorActions.Paste}" />

      <Separator />

      <EditorMenuItem Action="{x:Static EditorActions.SelectAll}" />

      <Separator />

      <!-- Only appears in tables -->
      <EditorMenuItem Action="{x:Static EditorActions.InsertRowAfter}"
                      TargetAreas="Table" />
      <EditorMenuItem Action="{x:Static EditorActions.DeleteRow}"
                      TargetAreas="Table" />
      <EditorMenuItem Action="{x:Static EditorActions.DeleteTable}"
                      TargetAreas="Table" />
    </EditorContextMenu>
  </RichTextEditor.ContextFlyout>
</RichTextEditor>
```

### Adding property submenus

The same [specialized menu items used for overflow](#overflow-for-specialized-tools) also work in the context menu.

<Image light={CustomContextMenuSpecialized} position="center" maxWidth={250} cornerRadius="true" alt="A custom context menu with specialized submenus for font family, text color, and alignment."/>
<br />

```xml
<EditorContextMenu Placement="Pointer">
  <EditorMenuItem Action="{x:Static EditorActions.Cut}" />
  <EditorMenuItem Action="{x:Static EditorActions.Copy}" />
  <EditorMenuItem Action="{x:Static EditorActions.Paste}" />

  <Separator />

  <FontFamilyMenuItem Action="{x:Static EditorActions.FontFamily}"
                            Header="Font" />
  <ColorMenuItem Action="{x:Static EditorActions.ForegroundColor}"
                       Header="Text color" />
  <TextAlignmentMenuItem Header="Alignment" TargetAreas="Text,Block" />
</EditorContextMenu>
```

### Disabling the context menu

Within the `<RichTextEditor>` XAML tags, set `ContextFlyout` to `{x:Null}` to turn it off entirely.

```xml
<RichTextEditor ContextFlyout="{x:Null}" />
```

## Theming and styling

Toolbar visuals are controlled through dynamic resources and style classes. You can override default settings at the application level, the window level, or on an individual `EditorToolbar`.

### Sizing and color resources

| 资源 | 默认值 | 用途 |
|---|---|---|
| `EditorToolbarToolHeight` | 30 | Tool button height. |
| `EditorToolbarToolMinWidth` | 28 | Minimum tool button width. |
| `EditorToolbarToolPadding` | 6,4 | Internal padding of tool buttons. |
| `EditorToolbarButtonCornerRadius` | 6 | Corner radius of tool buttons. |
| `EditorToolbarToolOpacity` | 0.9 | Tool opacity. |
| `EditorToolbarSeparatorHeight` | 18 | Separator line height. |
| `EditorToolbarSubtleBorderBrush` | Theme | Separator and subtle border color. |
| `EditorToolbarPointerOverBackgroundBrush` | Theme | Hover background color. |
| `EditorToolbarCheckedBackgroundBrush` | Theme | Active/checked background color. |
| `EditorToolbarDisabledForegroundBrush` | Theme | Disabled foreground color. |

#### Example

<Image light={CustomThemeToolbar} position="center" cornerRadius="true" alt="A toolbar with overridden theme resources, showing larger buttons, reduced corner radius, and a custom accent color for checked tools."/>
<br />

```xml
<Application.Resources>
  <ResourceDictionary>
    <!-- Make toolbar buttons bigger -->
    <x:Double x:Key="EditorToolbarToolHeight">36</x:Double>
    <x:Double x:Key="EditorToolbarToolMinWidth">36</x:Double>
    <CornerRadius x:Key="EditorToolbarButtonCornerRadius">4</CornerRadius>

    <!-- Use a custom accent for checked tools -->
    <SolidColorBrush x:Key="EditorToolbarCheckedBackgroundBrush"
                     Color="#4CAF50" Opacity="0.25" />
  </ResourceDictionary>
</Application.Resources>
```

### Style classes

| 类 | Applies to | 效果 |
|---|---|---|
| `ToolbarTool` | `Button`, `ToggleButton`, `SplitButton` | Standard toolbar button sizing, transparency, hover/checked/disabled visuals, transitions. Apply when embedding a stock button inside an `EditorToolbar` so it blends with surrounding tools. |
| `AreaAware` | `ToolbarGroup`, `ToggleTool`, `SeparatorTool`, `TablePickerTool`, `AlignmentFlyoutTool`, and other `EditorTool` subclasses | Binds the active target area from the ancestor `EditorToolbar` and optionally drives `IsVisible`. Required on `ToolbarGroup` for contextual visibility to work. |
| `EditorMiniBarChrome` | `Border` | Compact rounded-border, drop-shadow appearance used by the default selection mini-bar. |

#### Example

Add a plain `Button` to the toolbar without it looking out of place.

```xml
<EditorToolbar>
  <ToolbarGroup>
    <Button Classes="ToolbarTool" Click="OnExport_Click">
      <PathIcon Data="{StaticResource ExportGeometry}" />
    </Button>
  </ToolbarGroup>
  <!-- ... -->
</EditorToolbar>
```

### Targeted styles

For precise control, write a style selector that targets a specific element within the toolbar.

```xml
<Style Selector="EditorToolbar > ToolbarGroup > ToggleTool">
  <Setter Property="Margin" Value="2,0" />
</Style>
```

## 另请参阅 {#see-also}

- [RichTextEditor 参考](/controls/input/text-input/richtexteditor)
- [Extension Patterns](/controls/input/text-input/richtexteditor/extension-patterns)
- [Performance Tuning](/controls/input/text-input/richtexteditor/performance-tuning)
- [Troubleshooting RichTextEditor](/troubleshooting/controls/richtexteditor)

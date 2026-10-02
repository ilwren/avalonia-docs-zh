---
id: accessibility
title: 无障碍
description: 借助 AutomationProperties、键盘导航和自定义 automation peer，打造无障碍的 Avalonia 应用。
doc-type: overview
---

Avalonia 通过 automation peer 内置了无障碍支持，把界面暴露给屏幕阅读器之类的辅助技术。本文介绍如何让你的 Avalonia 应用对所有用户都友好可用。

## Avalonia 的无障碍机制 {#how-accessibility-works-in-avalonia}

Avalonia 的无障碍模型基于 **automation peer**，与 WPF、UWP 类似。每个控件都有一个对应的 `AutomationPeer`，向平台的无障碍 API（Windows 上是 UI Automation，macOS 上是 NSAccessibility，Linux 上是 AT-SPI）描述该控件的角色、状态和内容。

大多数内置控件会自动创建自己的 automation peer：`Button` 把自己报告为按钮，`TextBox` 报告为可编辑文本框，`CheckBox` 报告为复选框，依此类推。

## AutomationProperties

`AutomationProperties` 类提供了一组附加属性，用来给控件补充无障碍元数据。这些属性不影响界面的视觉外观，只有辅助技术会读取它们。

### 名称 {#name}

最重要的一个无障碍属性。控件获得焦点时，屏幕阅读器朗读的就是它提供的文本：

```xml
<Button AutomationProperties.Name="Submit order"
        Content="{Binding SubmitIcon}" />
```

如果控件本身就显示文本内容（比如 `Button` 的 `Content` 是字符串、`TextBlock`），automation peer 会自动采用那段文本。遇到下列情况则需要显式设置 `Name`：
- 内容是图片或图标，没有文字
- 可见文字脱离上下文后含义不明（比如页面上有好几个「编辑」按钮）
- 控件没有可见内容

### HelpText

提供额外的描述性文本，通常在控件名称之后朗读：

```xml
<TextBox AutomationProperties.Name="Email"
         AutomationProperties.HelpText="Enter your email address to receive notifications" />
```

### LabeledBy

把控件与某个标签控件关联起来，用标签的文字作为该控件的无障碍名称：

```xml
<TextBlock x:Name="NameLabel" Text="Full Name:" />
<TextBox AutomationProperties.LabeledBy="{Binding #NameLabel}" />
```

### AutomationId

供 UI 自动化测试使用的稳定标识。与 `Name` 不同，它不参与本地化，也不随显示语言变化：

```xml
<Button AutomationProperties.AutomationId="SubmitOrderButton"
        Content="Submit" />
```

### AcceleratorKey 与 AccessKey {#acceleratorkey-and-accesskey}

把键盘快捷键告知辅助技术：

```xml
<Button AutomationProperties.AcceleratorKey="Ctrl+S"
        Content="Save" />

<Button AutomationProperties.AccessKey="Alt+S"
        Content="_Save" />
```

### ControlTypeOverride

覆盖向辅助技术报告的控件类型。当自定义控件需要被播报成某种标准类型时，就用它：

```xml
<Border AutomationProperties.ControlTypeOverride="Button"
        AutomationProperties.Name="Custom button"
        PointerPressed="OnBorderClick">
    <TextBlock Text="Click me" />
</Border>
```

### LandmarkType

把界面上的某个区域标记为导航地标。屏幕阅读器允许用户在地标之间跳转：

```xml
<StackPanel AutomationProperties.LandmarkType="Navigation">
    <!-- Navigation menu -->
</StackPanel>

<ScrollViewer AutomationProperties.LandmarkType="Main">
    <!-- Main content -->
</ScrollViewer>
```

可用的地标类型有：`Banner`、`Complementary`、`ContentInfo`、`Region`、`Form`、`Main`、`Navigation` 和 `Search`。

:::note
在 Windows 上，`AccessibilityView` 至少要设为 `Control`，讲述人才能识别地标并启用地标导航快捷键（讲述人+N）。
:::

### HeadingLevel

把控件标记为指定级别的标题。屏幕阅读器会借助标题来浏览文档。为保证跨平台一致，请使用 1 到 6（macOS 支持 0-6 级，Windows 支持 1-9 级）：

```xml
<TextBlock AutomationProperties.HeadingLevel="1"
           Text="Settings" FontSize="24" />

<TextBlock AutomationProperties.HeadingLevel="2"
           Text="Appearance" FontSize="18" />
```

### LiveSetting

控制屏幕阅读器如何播报动态变化的内容：

```xml
<!-- Polite: announced when the screen reader is idle -->
<TextBlock AutomationProperties.LiveSetting="Polite"
           Text="{Binding StatusMessage}" />

<!-- Assertive: announced immediately, interrupting current speech -->
<TextBlock AutomationProperties.LiveSetting="Assertive"
           Text="{Binding ErrorMessage}" />
```

### ItemStatus

描述元素的当前状态。屏幕阅读器会朗读这段文字，让用户了解元素所处的状态：

```xml
<ListBoxItem AutomationProperties.ItemStatus="Downloading (45%)"
             Content="{Binding FileName}" />
```

### ItemType

用用户能理解的说法描述元素的类型。它在控件类型之外补充了与应用场景相关的信息：

```xml
<ListBoxItem AutomationProperties.ItemType="PDF Document"
             Content="{Binding FileName}" />
```

### AccessibilityView

控制控件是否出现在自动化树中：

```xml
<!-- Remove decorative elements from the accessibility tree -->
<Image Source="decorative-line.png"
       AutomationProperties.AccessibilityView="Raw" />
```

| 值 | 含义 |
|---|---|
| `Default` | 由控件的 automation peer 决定 |
| `Raw` | 仅出现在原始（未过滤）树中 |
| `Control` | 出现在控件视图中 |
| `Content` | 出现在内容视图中 |

## 键盘无障碍 {#keyboard-accessibility}

无障碍的应用必须光靠键盘就能完整操作：

### Tab 键导航 {#tab-navigation}

确保所有可交互控件都能用 Tab 键访问到。给需要参与 Tab 导航的控件设置 `IsTabStop="True"`，并用 `TabIndex` 来安排先后顺序：

```xml
<TextBox TabIndex="1" />
<TextBox TabIndex="2" />
<Button TabIndex="3" Content="Submit" />
```

完整的键盘导航模型——包括 `KeyboardNavigation.TabNavigation` 的各种模式和 `XYFocus` 方向导航——请参阅[焦点](/docs/input-interaction/focus)。

### 键盘快捷键 {#keyboard-shortcuts}

用 `HotKey` 或 `KeyBinding` 为那些只能用指针完成的交互补上键盘等效操作：

```xml
<Button Content="_Save" HotKey="Ctrl+S" Command="{Binding SaveCommand}" />
```

名称前加下划线即可生成访问键（在 Windows/Linux 上为 Alt+S）。详见[键盘与热键](/docs/input-interaction/keyboard-and-hotkeys)。

### 焦点指示 {#focus-indicators}

确保焦点清晰可见。当 `:focus-visible` 处于激活状态时，Avalonia 默认会显示 `FocusAdorner`（在获得焦点的控件周围画一圈边框）。如果你自己写了控件模板，记得确认焦点依然可见：

```xml
<Style Selector="Button.custom:focus-visible">
    <Setter Property="BorderBrush" Value="{DynamicResource SystemAccentColor}" />
    <Setter Property="BorderThickness" Value="2" />
</Style>
```

## 编写自定义 automation peer {#creating-custom-automation-peers}

你自己写的控件，Avalonia 往往没有足够的信息去向辅助技术描述它。重写 `OnCreateAutomationPeer` 即可提供自定义 peer：

```csharp
public class RatingControl : Control
{
    public static readonly StyledProperty<int> ValueProperty =
        AvaloniaProperty.Register<RatingControl, int>(nameof(Value));

    public int Value
    {
        get => GetValue(ValueProperty);
        set => SetValue(ValueProperty, value);
    }

    protected override AutomationPeer OnCreateAutomationPeer()
    {
        return new RatingControlAutomationPeer(this);
    }
}

public class RatingControlAutomationPeer : ControlAutomationPeer
{
    public RatingControlAutomationPeer(RatingControl owner) : base(owner) { }

    protected override AutomationControlType GetAutomationControlTypeCore()
        => AutomationControlType.Slider;

    protected override string? GetNameCore()
        => $"Rating: {((RatingControl)Owner).Value} out of 5";
}
```

### 需要重写的关键方法 {#key-methods-to-override}

| 方法 | 用途 |
|---|---|
| `GetAutomationControlTypeCore()` | 控件的类型（Button、TextBox、Slider 之类） |
| `GetNameCore()` | 屏幕阅读器朗读的无障碍名称 |
| `GetHelpTextCore()` | 额外的描述性文本 |
| `GetAutomationIdCore()` | 供测试使用的稳定标识 |
| `IsContentElementCore()` | 该控件是否出现在内容视图中 |
| `IsControlElementCore()` | 该控件是否出现在控件视图中 |

## 数据校验错误 {#data-validation-errors}

校验错误会自动暴露给辅助技术。当 `TextBox` 这类控件存在校验错误时（来自数据注解、`INotifyDataErrorInfo` 或异常），`DataValidationErrors` 控件会通过它的 automation peer 把错误作为帮助文本报告出去。控件获得焦点时屏幕阅读器便会朗读这些错误，且校验错误文本的优先级高于工具提示文本。

这不需要任何额外配置。只要你的控件用的是 Avalonia 的[数据校验](/docs/data-binding/binding-validation)机制，错误信息默认就是无障碍的。

## 无障碍检查清单 {#accessibility-checklist}

检查你的应用时，可以对照这份清单：

- 所有可交互控件都能用键盘访问到（Tab / Shift+Tab）
- 所有可获得焦点的控件上，焦点指示都清晰可见
- 图片和图标都通过 `AutomationProperties.Name` 提供了无障碍名称
- 表单字段都有标签（通过 `AutomationProperties.Name`、`AutomationProperties.LabeledBy` 或文本内容）
- 动态内容用 `AutomationProperties.LiveSetting` 来播报
- 不单靠颜色传达信息（同时借助形状、文字或图标）
- 文字达到最低对比度要求（常规文字 4.5:1，大号文字 3:1）
- 自定义控件都配有合适的 automation peer
- 纯装饰性元素已排除在自动化树之外

## 平台支持 {#platform-support}

Avalonia 的无障碍支持程度因平台而异：

| 平台 | Accessibility API | 支持情况 |
|---|---|---|
| Windows | UI Automation (UIA) | 完整支持 |
| macOS | NSAccessibility | 完整支持 |
| Linux | [AT-SPI2](/docs/platform-specific-guides/linux#accessibility) | 完整支持 |
| iOS | UIAccessibility | Supported |
| Android | AccessibilityNodeInfo | Supported |
| Browser (WASM) | ARIA 特性 | 部分支持 |

在 Linux 上，只要系统提供 AT-SPI2，Avalonia 就会自动通过 D-Bus 暴露无障碍树。Orca 等屏幕阅读器可以发现并操作所有标准 Avalonia 控件。配置与测试步骤请参阅 [Linux 平台指南](/docs/platform-specific-guides/linux#accessibility)。

## 另请参阅 {#see-also}

- [焦点](/docs/input-interaction/focus)：键盘焦点导航与 Tab 顺序。
- [键盘与热键](/docs/input-interaction/keyboard-and-hotkeys)：键盘快捷键与访问键。
- [自定义控件](/docs/custom-controls)：编写具备良好无障碍支持的自定义控件。
- [桌面 Linux](/docs/platform-specific-guides/linux#accessibility)：在 Linux 上用 Orca 和 Accerciser 测试无障碍。

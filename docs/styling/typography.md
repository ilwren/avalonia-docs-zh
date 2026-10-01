---
id: typography
title: 排版
description: 文本的字号、字重、字形、字宽、字间距、行高、文本装饰与对齐等属性。
doc-type: reference
---

Avalonia 提供了一组属性来掌控应用中文本的外观。这些属性定义在 [`TextElement`](/api/avalonia/controls/documents/textelement) 上，是可继承的附加属性，因此你可以把它们设在任意控件上，经由[属性值继承](/docs/properties/property-value-inheritance)作用于其视觉树中的所有文本。

## TextElement 的附加属性 {#textelement-attached-properties}

下列属性定义在 `TextElement` 上，并由后代控件继承。你既可以直接设在 `TextBlock` 这类文本控件上，也可以设在容器控件上，让其中所有文本一并生效。

| 附加属性 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `TextElement.FontFamily` | [`FontFamily`](/api/avalonia/media/fontfamily) | 平台默认值 | 渲染文本所用的字型。 |
| `TextElement.FontSize` | `double` | `12` | 文本大小，以设备无关像素为单位。 |
| `TextElement.FontWeight` | [`FontWeight`](/api/avalonia/media/fontweight) | `Normal` | 字符笔画的粗细。 |
| `TextElement.FontStyle` | [`FontStyle`](/api/avalonia/media/fontstyle) | `Normal` | 文本是直立、斜体还是倾斜。 |
| `TextElement.FontStretch` | [`FontStretch`](/api/avalonia/media/fontstretch) | `Normal` | 字符相对于常规宽高比的宽度。 |
| `TextElement.FontFeatures` | `FontFeatureCollection` | `null` | 要启用或禁用的 OpenType 字体特性。 |
| `TextElement.Foreground` | `IBrush` | Inherited | 绘制文本所用的画刷。 |
| `TextElement.LetterSpacing` | `double` | `0` | 字符之间额外的间距，以设备无关像素为单位。 |

直接在 `TextBlock` 上设 `FontSize` 这类属性，等同于在该控件上设 `TextElement.FontSize`。

```xml
<!-- Set font properties on a container to apply to all child text -->
<StackPanel TextElement.FontSize="16"
            TextElement.FontWeight="SemiBold"
            TextElement.LetterSpacing="0.5">
    <TextBlock Text="This inherits all three properties." />
    <TextBlock Text="So does this." />
    <TextBlock FontSize="24" Text="This overrides FontSize but inherits the rest." />
</StackPanel>
```

## 字号 {#font-size}

`FontSize` 以设备无关像素指定文本的高度。你可以设在单个控件上，也可以设在容器上以影响其下所有文本。

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui" Margin="20" Spacing="4">
    <TextBlock FontSize="12" Text="12px (default size)" />
    <TextBlock FontSize="16" Text="16px" />
    <TextBlock FontSize="24" Text="24px" />
    <TextBlock FontSize="36" Text="36px" />
</StackPanel>
```

</XamlPreview>

## 字重 {#font-weight}

`FontWeight` 控制字符笔画的粗细。你可以用具名值，也可以用 1 到 999 的数值。

| 具名值 | 数值 | 别名 |
|---|---|---|
| `Thin` | 100 | |
| `ExtraLight` | 200 | `UltraLight` |
| `Light` | 300 | |
| `SemiLight` | 350 | |
| `Normal` | 400 | `Regular` |
| `Medium` | 500 | |
| `SemiBold` | 600 | `DemiBold` |
| `Bold` | 700 | |
| `ExtraBold` | 800 | `UltraBold` |
| `Black` | 900 | `Heavy` |
| `ExtraBlack` | 950 | `UltraBlack` |

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui" Margin="20" Spacing="4">
    <TextBlock FontWeight="Light" Text="Light (300)" />
    <TextBlock FontWeight="Normal" Text="Normal (400)" />
    <TextBlock FontWeight="Medium" Text="Medium (500)" />
    <TextBlock FontWeight="SemiBold" Text="SemiBold (600)" />
    <TextBlock FontWeight="Bold" Text="Bold (700)" />
    <TextBlock FontWeight="ExtraBold" Text="ExtraBold (800)" />
    <TextBlock FontWeight="Black" Text="Black (900)" />
</StackPanel>
```

</XamlPreview>

你也可以在 XAML 中直接写数值，或在代码中强制转换一个整数：

```xml
<TextBlock FontWeight="550" Text="Custom weight 550" />
```

```csharp
myTextBlock.FontWeight = (FontWeight)550;
```

:::note
可用的字重取决于字体。若所请求的字重没有，Avalonia 会挑一个最接近的。有些字体只带寥寥几档（比如 Normal 和 Bold），另一些则提供了完整档位。
:::

## 字形 {#font-style}

`FontStyle` 控制文本渲染成直立、斜体还是倾斜。

| 值 | 说明 |
|---|---|
| `Normal` | 直立文本（默认）。 |
| `Italic` | 使用字体的斜体变体，字形经过专门设计。 |
| `Oblique` | 由算法把文本倾斜。当字体不含真正的斜体变体时采用。 |

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui" Margin="20" Spacing="4">
    <TextBlock FontStyle="Normal" Text="Normal style" />
    <TextBlock FontStyle="Italic" Text="Italic style" />
    <TextBlock FontStyle="Oblique" Text="Oblique style" />
</StackPanel>
```

</XamlPreview>

## 字宽 {#font-stretch}

`FontStretch` 控制字符相对于常规宽高比的宽度。该属性要求字体带有窄体或宽体变体。

| 值 | 说明 |
|---|---|
| `UltraCondensed` | 最窄的字符宽度。 |
| `ExtraCondensed` | 比 `Condensed` 更窄。 |
| `Condensed` | 比 `SemiCondensed` 更窄。 |
| `SemiCondensed` | 比 `Normal` 略窄。 |
| `Normal` | 默认的字符宽度。 |
| `SemiExpanded` | 比 `Normal` 略宽。 |
| `Expanded` | 比 `SemiExpanded` 更宽。 |
| `ExtraExpanded` | 比 `Expanded` 更宽。 |
| `UltraExpanded` | 最宽的字符宽度。 |

```xml
<TextBlock FontStretch="Condensed" Text="Condensed text" />
<TextBlock FontStretch="Normal" Text="Normal text" />
<TextBlock FontStretch="Expanded" Text="Expanded text" />
```

:::note
多数字体只带 `Normal` 宽度的字形。除非字体确有针对所请求字宽设计的字形，否则 `FontStretch` 不会有任何可见效果。
:::

## 字间距 {#letter-spacing}

`LetterSpacing` 在字符之间添加额外空间，以设备无关像素为单位。正值加宽间距，负值收窄间距。

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui" Margin="20" Spacing="4">
    <TextBlock LetterSpacing="-1" Text="Tighter spacing (-1px)" />
    <TextBlock LetterSpacing="0" Text="Default spacing (0px)" />
    <TextBlock LetterSpacing="2" Text="Wider spacing (2px)" />
    <TextBlock LetterSpacing="5" Text="Wide spacing (5px)" />
</StackPanel>
```

</XamlPreview>

由于 `LetterSpacing` 是定义在 `TextElement` 上的可继承附加属性，你可以把它设在容器上，以影响其中所有文本：

```xml
<StackPanel TextElement.LetterSpacing="1.5">
    <TextBlock Text="All text in this panel" />
    <TextBlock Text="has 1.5px extra letter spacing." />
</StackPanel>
```

## 行高与行距 {#line-height-and-line-spacing}

`LineHeight` 和 `LineSpacing` 控制 `TextBlock` 中各行文本之间的垂直距离。

| 属性 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `LineHeight` | `double` | `NaN` | 每一行的总高度。设为 `NaN` 时，由字体度量自动决定行高。 |
| `LineSpacing` | `double` | `0` | 行与行之间额外添加的距离，以设备无关像素为单位，叠加在字体本身的行高之上。 |

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui" Margin="20" Spacing="16" Width="300">
    <TextBlock TextWrapping="Wrap"
               Text="Default line height: this text uses the line height determined by the font metrics. No manual adjustment." />

    <TextBlock TextWrapping="Wrap"
               LineHeight="32"
               Text="LineHeight=32: this text has a fixed line height of 32 pixels, creating consistent vertical spacing." />

    <TextBlock TextWrapping="Wrap"
               LineSpacing="8"
               Text="LineSpacing=8: this text adds 8 extra pixels between each line, on top of the font's natural height." />
</StackPanel>
```

</XamlPreview>

当你需要精确掌控行的尺寸时用 `LineHeight`；若只是想让行与行之间松快些、又不想覆盖字体本身的度量，就用 `LineSpacing`。

## 文本对齐 {#text-alignment}

`TextAlignment` 控制文本在其容器内的水平位置。

| 值 | 说明 |
|---|---|
| `Left` | 文本靠左边缘对齐。 |
| `Center` | 文本水平居中。 |
| `Right` | 文本靠右边缘对齐。 |
| `Start` | 文本靠起始边缘对齐，并遵循 `FlowDirection`。在从左到右的布局中等同于 `Left`。 |
| `End` | 文本靠末端边缘对齐，并遵循 `FlowDirection`。在从左到右的布局中等同于 `Right`。 |
| `Justify` | 文本被拉伸，使每一行（最后一行除外）都铺满整个宽度。需要启用 `TextWrapping`。 |
| `DetectFromContent` | 对齐方式由文本内容的 Unicode 书写方向推断得出。 |

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui" Margin="20" Width="300" Spacing="8">
    <TextBlock TextAlignment="Left" Text="Left-aligned text" />
    <TextBlock TextAlignment="Center" Text="Center-aligned text" />
    <TextBlock TextAlignment="Right" Text="Right-aligned text" />
    <TextBlock TextAlignment="Justify" TextWrapping="Wrap"
               Text="Justified text stretches words evenly across the full width when wrapping is enabled." />
</StackPanel>
```

</XamlPreview>

:::info
若你的应用同时支持从左到右和从右到左的布局，请用 `Start` 和 `End` 而非 `Left` 和 `Right`。这两个取值会自动适配当前的 `FlowDirection`。
:::

## 文本装饰 {#text-decorations}

文本装饰在文字之上或周围画线。Avalonia 通过 [`TextDecorations`](/api/avalonia/media/textdecorations) 类提供了四种预设，并支持用 [`TextDecoration`](/api/avalonia/media/textdecoration) 类完全自定义装饰。

### 预设装饰 {#preset-decorations}

| 值 | 说明 |
|---|---|
| `Underline` | 文本基线下方的一条线。 |
| `Strikethrough` | 穿过文字中部的一条线。 |
| `Overline` | 文本上方的一条线。 |
| `Baseline` | 位于文本基线处的一条线。 |

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui" Margin="20" Spacing="4">
    <TextBlock TextDecorations="Underline" Text="Underlined text" />
    <TextBlock TextDecorations="Strikethrough" Text="Struck-through text" />
    <TextBlock TextDecorations="Overline" Text="Overlined text" />
    <TextBlock TextDecorations="Baseline" Text="Baseline decoration" />
    <TextBlock TextDecorations="Underline Strikethrough" Text="Multiple decorations" />
</StackPanel>
```

</XamlPreview>

你可以把装饰应用到 `TextBlock` 内部的单个 `Run` 元素上：

```xml
<TextBlock>
    <Run Text="Normal text, " />
    <Run TextDecorations="Underline" Text="underlined text, " />
    <Run TextDecorations="Strikethrough" Text="and struck-through text." />
</TextBlock>
```

### 自定义装饰 {#custom-decorations}

若要掌控颜色、粗细、偏移和虚线样式，请直接定义一个 `TextDecoration`。

| 属性 | 类型 | 说明 |
|---|---|---|
| `Location` | [`TextDecorationLocation`](/api/avalonia/media/textdecorationlocation) | 线画在哪里：`Underline`、`Strikethrough`、`Overline` 或 `Baseline`。 |
| `Stroke` | `IBrush` | 绘制装饰线所用的画刷。 |
| `StrokeThickness` | `double` | 装饰线的粗细。 |
| `StrokeThicknessUnit` | [`TextDecorationUnit`](/api/avalonia/media/textdecorationunit) | 粗细的单位：`FontRecommended`（默认）、`FontRenderingEmSize` 或 `Pixel`。 |
| `StrokeOffset` | `double` | 线相对于其默认位置的垂直偏移。 |
| `StrokeOffsetUnit` | `TextDecorationUnit` | 偏移的单位。 |
| `StrokeDashArray` | `AvaloniaList<double>` | 装饰线的虚线样式。 |
| `StrokeLineCap` | `PenLineCap` | 虚线两端的形状：`Flat`、`Round` 或 `Square`。 |

```xml
<TextBlock Text="Custom red dashed underline">
    <TextBlock.TextDecorations>
        <TextDecorationCollection>
            <TextDecoration Location="Underline"
                           Stroke="Red"
                           StrokeThickness="2"
                           StrokeDashArray="2,2" />
        </TextDecorationCollection>
    </TextBlock.TextDecorations>
</TextBlock>
```

## OpenType 字体特性 {#opentype-font-features}

`FontFeatures` 属性用来启用或禁用连字、等宽数字、小型大写字母等 OpenType 特性。特性以逗号分隔的标签形式给出，采用 HarfBuzz 语法。

```xml
<TextBlock Text="0123456789" FontFeatures="+tnum" />
<TextBlock Text="fi fl ffi" FontFeatures="-liga" />
<TextBlock Text="Small Caps" FontFeatures="+smcp" />
```

完整的常用标签清单和用法示例，请见[自定义字体：OpenType 字体特性](/docs/styling/custom-fonts#opentype-font-features)。

## 用样式类搭一套字号体系 {#creating-a-type-scale-with-style-classes}

Avalonia 没有内置 HTML 那样从 `<h1>` 到 `<h6>` 的标题样式。你可以借助[样式类](/docs/styling/style-classes)自建一套字号体系，字号、字重和间距全由你定，恰好贴合应用的设计。

把这些样式定义在 `App.axaml`（或任意共享资源文件）中，这样整个应用都能用上：

```xml title="App.axaml"
<Application.Styles>
    <FluentTheme />

    <Style Selector="TextBlock.h1">
        <Setter Property="FontSize" Value="32" />
        <Setter Property="FontWeight" Value="Bold" />
        <Setter Property="LineHeight" Value="40" />
    </Style>
    <Style Selector="TextBlock.h2">
        <Setter Property="FontSize" Value="24" />
        <Setter Property="FontWeight" Value="SemiBold" />
        <Setter Property="LineHeight" Value="32" />
    </Style>
    <Style Selector="TextBlock.h3">
        <Setter Property="FontSize" Value="20" />
        <Setter Property="FontWeight" Value="SemiBold" />
        <Setter Property="LineHeight" Value="28" />
    </Style>
    <Style Selector="TextBlock.subtitle">
        <Setter Property="FontSize" Value="16" />
        <Setter Property="FontWeight" Value="Medium" />
        <Setter Property="Foreground" Value="{DynamicResource TextFillColorSecondaryBrush}" />
    </Style>
    <Style Selector="TextBlock.body">
        <Setter Property="FontSize" Value="14" />
        <Setter Property="LineHeight" Value="20" />
    </Style>
    <Style Selector="TextBlock.caption">
        <Setter Property="FontSize" Value="12" />
        <Setter Property="Foreground" Value="{DynamicResource TextFillColorTertiaryBrush}" />
    </Style>
</Application.Styles>
```

然后用 `Classes` 属性套上它们：

```xml
<StackPanel Spacing="8">
    <TextBlock Classes="h1" Text="Page title" />
    <TextBlock Classes="subtitle" Text="A short description of the page" />
    <TextBlock Classes="h2" Text="Section heading" />
    <TextBlock Classes="body" TextWrapping="Wrap"
               Text="Body text for the main content of the section." />
    <TextBlock Classes="caption" Text="Last updated March 2026" />
</StackPanel>
```

当某个实例需要与众不同时，可以在样式类之外再做内联覆盖：

```xml
<TextBlock Classes="h1" Foreground="DodgerBlue" Text="Colored heading" />
```

这种做法与在应用中[共享样式](/docs/styling/sharing-styles)配合得很好：字号体系定义一次，之后处处沿用。

## 在代码中设置排版属性 {#setting-typography-from-code}

所有 `TextElement` 附加属性都有对应的静态 `Get` 和 `Set` 方法，可在代码隐藏中使用：

```csharp
TextElement.SetFontSize(myPanel, 18);
TextElement.SetFontWeight(myPanel, FontWeight.Bold);
TextElement.SetLetterSpacing(myPanel, 1.5);
TextElement.SetFontStyle(myPanel, FontStyle.Italic);
```

你也可以直接在文本控件上设置这些属性：

```csharp
myTextBlock.FontSize = 24;
myTextBlock.FontWeight = FontWeight.SemiBold;
myTextBlock.LineHeight = 32;
myTextBlock.TextDecorations = TextDecorations.Underline;
```

## 另请参阅 {#see-also}

- [自定义字体](/docs/styling/custom-fonts)：嵌入并加载自定义字体文件。
- [文本选项](/docs/graphics-animation/text-options)：掌控文本渲染、微调（hinting）与基线对齐。
- [TextBlock](/controls/data-display/text-display/textblock)：显示格式化文本的主力控件。
- [TextTrimming](/controls/data-display/text-display/texttrimming)：文本溢出时如何截断。
- [属性值继承](/docs/properties/property-value-inheritance)：字体属性如何沿视觉树向下传递。
- [`TextElement` API 参考](/api/avalonia/controls/documents/textelement)
- [样式类](/docs/styling/style-classes)：给控件套上具名样式类。
- [`FontWeight` API 参考](/api/avalonia/media/fontweight)

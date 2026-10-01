---
id: colorview
title: ColorView
---

用色谱、调色板和分量滑块呈现一种颜色供用户编辑。

## 常用属性 {#common-properties}

| 属性 | 说明 |
|----------|-------------|
| `Color` | 获取或设置当前选中的颜色，采用 RGB 色彩模型。控件作者请改用 `HsvColor`，以免损失精度、造成颜色漂移。 |
| `ColorModel` | 获取或设置滑块当前采用的色彩模型。该属性只对分量选项卡有效：色谱选项卡必须始终使用 HSV，而调色板选项卡里只有预设颜色。 |
| `ColorSpectrumComponents` | 获取或设置色谱所显示的那两个 HSV 颜色分量。 |
| `ColorSpectrumShape` | 获取或设置色谱显示成什么形状。 |
| `HexInputAlphaPosition` | 获取或设置十六进制输入框中 alpha 分量相对于其他颜色分量的位置。 |
| `HsvColor` | 获取或设置当前选中的颜色，采用 HSV 色彩模型。任何情况下都应优先用它而不是 `Color` 属性。`ColorSpectrum` 内部使用 HSV 色彩模型，用这个属性可以避免精度损失和颜色漂移。 |
| `IsAccentColorsVisible` | 获取或设置一个值，指示是否在预览色旁一并显示强调色。 |
| `IsAlphaEnabled` | 获取或设置一个值，指示是否启用 alpha 分量。停用（设为 false）时，alpha 分量会被固定为最大值，相关编辑控件也会被禁用。 |
| `IsAlphaVisible` | 获取或设置一个值，指示 alpha 分量的编辑控件（滑块和文本框）是否可见。隐藏时，现有的 alpha 分量值保持不变。注意 `IsComponentTextInputVisible` 同样会影响 alpha 分量文本框的可见性。 |
| `IsColorComponentsVisible` | 获取或设置一个值，指示颜色分量这个选项卡/面板/页（子视图）是否可见。 |
| `IsColorModelVisible` | 获取或设置一个值，指示当前色彩模型的指示器/选择器是否可见。 |
| `IsColorPaletteVisible` | 获取或设置一个值，指示调色板这个选项卡/面板/页（子视图）是否可见。 |
| `IsColorPreviewVisible` | 获取或设置一个值，指示颜色预览是否可见。注意强调色的可见性由 `IsAccentColorsVisible` 单独控制。 |
| `IsColorSpectrumVisible` | 获取或设置一个值，指示色谱这个选项卡/面板/页（子视图）是否可见。 |
| `IsColorSpectrumSliderVisible` | 获取或设置一个值，指示色谱的第三分量滑块是否可见。 |
| `IsComponentSliderVisible` | 获取或设置一个值，指示颜色分量滑块是否可见。所有颜色分量都受该属性控制，不过 alpha 还可以用 `IsAlphaVisible` 单独控制。 |
| `IsComponentTextInputVisible` | 获取或设置一个值，指示颜色分量的文本输入框是否可见。所有颜色分量都受该属性控制，不过 alpha 还可以用 `IsAlphaVisible` 单独控制。 |
| `IsHexInputVisible` | 获取或设置一个值，指示十六进制颜色值的文本输入框是否可见。 |
| `MaxHue` | 获取或设置 Hue 分量的最大值，取值范围 0..359。该属性必须大于 `MinHue`。 |
| `MaxSaturation` | 获取或设置 Saturation 分量的最大值，取值范围 0..100。该属性必须大于 `MinSaturation`。 |
| `MaxValue` | 获取或设置 Value 分量的最大值，取值范围 0..100。该属性必须大于 `MinValue`。 |
| `MinHue` | 获取或设置 Hue 分量的最小值，取值范围 0..359。该属性必须小于 `MaxHue`。 |
| `MinSaturation` | 获取或设置 Saturation 分量的最小值，取值范围 0..100。该属性必须小于 `MaxSaturation`。 |
| `MinValue` | 获取或设置 Value 分量的最小值，取值范围 0..100。该属性必须小于 `MaxValue`。 |
| `PaletteColors` | 获取或设置调色板中各个颜色的集合。一般不必手工设置它，而应当给 `Palette` 属性提供一个 `IColorPalette`，让它自动设好。 |
| `PaletteColumnCount` | 获取或设置调色板中每一行（每一节）的颜色数量。在标准调色板中，行表示色阶、列表示颜色。一般不必手工设置它，而应当给 `Palette` 属性提供一个 `IColorPalette`，让它自动设好。 |
| `Palette` | 获取或设置调色板。设置它会自动把 `PaletteColors` 和 `PaletteColumnCount` 一并设好，并覆盖原有的值。 |
| `SelectedIndex` | 获取或设置所选选项卡/面板/页（子视图）的索引。使用默认控件主题时，该属性应与 `ColorViewTab` 枚举配合使用——`ColorViewTab` 枚举定义了三个标准选项卡各自的索引值。用法形如 `SelectedIndex = (int)ColorViewTab.Palette`。 |

:::note
这些表示可见性的属性采用「IsThingVisible」而非「ShowThing」的命名方式，因为界面上有些元素能分别控制「启用」和「可见」两种状态。此处的命名也与 `Control` 保持一致。
:::

## Pseudoclasses

None

## 模板部件 {#template-parts}

| 名称 | 类型 | 说明 |
|------|----- |-------------|
| `PART_HexTextBox` | TextBox | 提供一个输入/输出口，接受控件能够解析的十六进制颜色记法。 |
| `PART_TabControl` | TabControl | 用于在色谱、调色板、分量三个选项卡/面板/页（子视图）之间切换的主控件。这个模板部件是可选的，只有 `SelectedIndex` 的某些校验场景才需要它。 |

## 另请参阅 {#see-also}

- [ColorView API 参考](/api/avalonia/controls/colorview)
- [GitHub 上的 `ColorView.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls.ColorPicker/ColorView/ColorView.cs)

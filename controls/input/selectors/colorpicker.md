---
id: colorpicker
title: ColorPicker
---

import ColorPaletteFluent from '/img/controls/colorpicker/color-palette-fluent.png';
import ColorPaletteFlat from '/img/controls/colorpicker/color-palette-flat.png';
import ColorPaletteFlatHalf from '/img/controls/colorpicker/color-palette-flat-half.png';
import ColorPaletteMaterial from '/img/controls/colorpicker/color-palette-material.png';
import ColorPaletteMaterialHalf from '/img/controls/colorpicker/color-palette-material-half.png';
import ColorPaletteSixteen from '/img/controls/colorpicker/color-palette-sixteen.png';

[`ColorPicker`](/api/avalonia/controls/colorpicker) 是一个高度可定制的通用控件，用户可以用它在 RGB 或 HSV 色彩空间中选取颜色。这套实现既提供了开箱即用的拾色器，也同样看重为开发者提供可用来自行搭建拾色器的基础控件。 

`ColorPicker` 包含一系列控件（组件）：

 * [`ColorSpectrum`](/api/avalonia/controls/primitives/colorspectrum)（基础控件）：用于选色的二维色谱。
 * [`ColorSlider`](/api/avalonia/controls/primitives/colorslider)（基础控件）：背景表示某个颜色分量的滑块。
 * [`ColorPreviewer`](/api/avalonia/controls/primitives/colorpreviewer)（基础控件）：显示预览色，并可附带强调色。
 * [`ColorView`](/api/avalonia/controls/colorview)：用色谱、调色板和分量滑块呈现一种颜色供用户编辑。
 * `ColorPicker`：在下拉浮层中用色谱、调色板和分量滑块呈现一种颜色供用户编辑。只有下拉浮层展开时才能编辑，否则只显示预览色。

每个基础组件都能单独使用，也能彼此混搭。这带来了其他拾色器实现给不了的强大可组合性。举例来说，你可以把 `ColorSpectrum`、`ColorSlider` 和 `ColorPreviewer` 这几个基础控件迅速绑在一起，做出一个全新设计的拾色器。

术语说明：「color picker」通常指这一系列控件，而 `ColorPicker` 特指其中那个具体的控件。

## 这个控件选对了吗？ {#is-this-the-right-control}

这个控件就是拿来直接用的：既对用户友好，又方便开发者定制。既可以用画布式的 `ColorView` 控件，也可以用紧凑的 `ColorPicker` 下拉形式。

若应用有更特殊的需求，每个控件和基础组件都能单独定制，从而拼出一个新的拾色器，而不必把那些复杂的渲染与颜色逻辑重写一遍。要贴合某个应用特定的设计与可用性要求时，这非常有用。

使用这个控件的开发者可以：
 1. 在应用中直接照原样使用 `ColorView` 或 `ColorPicker`
 2. 用自带的属性定制 `ColorView` 或 `ColorPicker`。这些属性能对控件做出不小的改动，比如停用分量滑块、换一套调色板，或者只留下色谱选项卡。
 3. 用现成的基础组件搭一个新的拾色器，以满足某个应用特定的设计与可用性要求。
 4. 给现有组件重做模板，打造一个彻底定制的全新拾色器。

## 在你的应用中使用 {#using-in-your-app}

Avalonia 也会跑在嵌入式设备这类资源受限的环境里。出于这个（以及其他）原因，`ColorPicker` 这类体量较大的控件并未包含在 Avalonia 的主 NuGet 包中。因此，要把 `ColorPicker` 加进你的应用，还得多做一点事：

 1. 把 `Avalonia.Controls.ColorPicker` NuGet 包加进项目。它的版本**必须**与你所用的其他 Avalonia 包一致。
 2. 在 `App.axaml` 中加入下列内容，为所有拾色器控件引入控件主题和样式：
    * Fluent 主题用 `<StyleInclude Source="avares://Avalonia.Controls.ColorPicker/Themes/Fluent/Fluent.xaml" />`，**或者**
    * Simple 主题用 `<StyleInclude Source="avares://Avalonia.Controls.ColorPicker/Themes/Simple/Simple.xaml" />`

:::note
有些主题包（比如 FluentAvalonia）默认就包含全部控件，这一步可以省略。
:::

## 背景 {#background}

这个控件最初是基于 Windows Community Toolkit 的基本设计，对 UWP（后来的 WinUI）中那个控件重新设定样式而来。WinUI 的 `ColorPicker` 在小屏幕上并不好用，整体设计与可用性无论对用户还是开发者来说都有欠缺。

即便功能一应俱全，WinUI 的那个控件仍称不上理想：想重做模板、做定制都得费很大劲（部分原因是各个组件之间高度耦合），而且它用了大量模板部件和代码隐藏。Avalonia 版的控件（完全重写）力图把这些问题统统解决，成为 XAML 拾色器设计的标杆。

从 WinUI 身上学到的几点主要改进是：
 * `ColorPicker` 实现为下拉形式（与其他各类「picker」保持一致）。想要画布式控件（类似 WinUI）的人，还可以用 `ColorView` 控件。
 * Avalonia 的这些控件尽可能把一切都放进 XAML 控件主题里，把代码隐藏压到最少。这大大提升了可组合性，让应用开发者能定制这些控件的每一个部分（多数情况下连基础控件也不例外）。
 * `ColorSlider`、`ColorSpectrum` 这类基础控件完全自成一体，可以单独使用，让应用开发者能自行实现拾色器。
 * Avalonia 本身新增了一个 `HsvColor` 结构（与 `Color`、`HslColor` 并列），现在所有拾色器控件都在用它。这既简化了代码隐藏，也让基础控件与控件之间的颜色属性绑定成为可能。拾色器控件内部一律在 HSV 色彩空间中工作。
 * `HsvColor` 与 `ColorSlider` 双剑合璧，释放出了 WinUI 远不能及的能力（也让重做模板变得轻松）。
 * 新增了许多属性（比 WinUI 还多），用于控制 `ColorView` 各个部分的可见性。每个选项卡都能单独隐藏，大多数子区块也是如此。这样一来，不必重做模板、也不必写复杂的样式选择器，就能做出大量设计上的定制。
 * 通过 `IColorPalette` 接口加入了调色板（与 Windows Community Toolkit 相同）。WinUI 版的这个控件压根不支持调色板。
 * `SelectedIndex`、`ColorModel` 等新属性让你能定制拾色器，并把它置于某个预设状态。比如 WinUI 的 ColorPicker 总是默认 RGB，代码和 XAML 都改不了；这套实现没有这类限制。

## 控件与基础控件 {#controls-and-primitives}

| 控件 | 链接 |
|---------|------|
| `ColorPicker` | |
| `ColorView` | 参见 [`ColorView`](/controls/input/selectors/colorview) 专页。 |
| `ColorSpectrum` | |
| `ColorSlider` | |
| `ColorPreviewer` | |

## 调色板 {#color-palettes}

这里提供了若干实现 `IColorPalette` 接口的预设调色板。它们的实例可以赋给 `ColorView` 或 `ColorPicker` 的 `Palette` 属性。

<table>
  <tr>
    <th>Palette</th>
    <th>说明</th>
  </tr>
  <tr>
    <td>
      <Image light={ColorPaletteFluent} alt="Fluent Color Palette" position="center" maxWidth={400} cornerRadius="true"/>
    </td>
    <td>包含 Windows 10 及更高版本中的 Fluent 调色板。这是默认的调色板。</td>
  </tr>
  <tr>
    <td>
      <Image light={ColorPaletteFlat} alt="Flat UI Color Palette" position="center" maxWidth={400} cornerRadius="true"/>
    </td>
    <td>包含完整的 <a href="https://github.com/designmodo/Flat-UI">Flat UI 调色板</a>.</td>
  </tr>
  <tr>
    <td>
      <Image light={ColorPaletteFlatHalf} alt="Flat UI Half Color Palette" position="center" maxWidth={400} cornerRadius="true"/>
    </td>
    <td>包含一半的 <a href="https://github.com/designmodo/Flat-UI">Flat UI 调色板</a> ，以提升可用性，在移动设备上尤其如此。</td>
  </tr>
  <tr>
    <td>
      <Image light={ColorPaletteMaterial} alt="Material Color Palette" position="center" maxWidth={400} cornerRadius="true"/>
    </td>
    <td>包含大部分 <a href="https://material.io/design/color/the-color-system.html#tools-for-picking-colors">Material Design 调色板</a>。为了让调色板整齐成矩形，这里做了两处改动：1. 排除每种颜色的 A100-A700 色阶——并非所有颜色都有这些色阶（如棕色/灰色）。2. 黑色和白色是独立颜色，也一并排除。</td>
  </tr>
  <tr>
    <td>
      <Image light={ColorPaletteMaterialHalf} alt="Material Half Color Palette" position="center" maxWidth={400} cornerRadius="true"/>
    </td>
    <td>包含一半的 <a href="https://material.io/design/color/the-color-system.html#tools-for-picking-colors">Material Design 调色板</a> （见上文），以提升可用性，在移动设备上尤其如此。</td>
  </tr>
  <tr>
    <td>
      <Image light={ColorPaletteSixteen} alt="Sixteen Color Palette" position="center" maxWidth={400} cornerRadius="true"/>
    </td>
    <td>包含标准的 <a href="https://en.wikipedia.org/wiki/Web_colors#HTML_color_names">十六色调色板</a> ，来自 HTML 4.01 规范。</td>
  </tr>
</table>

## 另请参阅 {#see-also}

- [ColorPicker API 参考](/api/avalonia/controls/colorpicker)
- [GitHub 上的 `ColorPicker.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls.ColorPicker/ColorPicker/ColorPicker.cs)

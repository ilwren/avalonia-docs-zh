---
id: viewbox
title: Viewbox
---

import ViewboxScaleUniformBothScreenshot from '/img/controls/viewbox/viewbox-scale-uniform-both.gif';
import ViewboxScaleUniformFillBothScreenshot from '/img/controls/viewbox/viewbox-scale-uniformtofill-both.gif';
import ViewboxScaleFillBothScreenshot from '/img/controls/viewbox/viewbox-scale-fill-both.gif';
import ViewboxScaleNoneBothScreenshot from '/img/controls/viewbox/viewbox-scale-none-both.gif';
import ViewboxScaleUniformDownOnlyScreenshot from '/img/controls/viewbox/viewbox-uniform-downonly.gif';
import ViewboxScaleUniformUpOnlyScreenshot from '/img/controls/viewbox/viewbox-uniform-uponly.gif';

`Viewbox` 是一个能缩放内容的容器控件。内容以何种方式拉伸、以及何时才拉伸（拉伸方向），都可以自行设定。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性           | 默认值 | 说明                                                  |
| ------------------ | ------- |--------------------------------------------------------------|
| `Stretch`          | Uniform | 决定内容如何适配可用空间。 |
| `StretchDirection` | Both    | 决定何时进行缩放。                          |

`Stretch` 属性的取值如下：

<table><thead><tr><th width="250">Stretch</th><th>说明</th></tr></thead><tbody><tr><td><code>Uniform</code></td><td>（默认值）内容在保持原生宽高比的前提下缩放，以恰好装入容器尺寸。</td></tr><tr><td><code>Fill</code></td><td>内容被拉伸填满容器尺寸，不保持宽高比。</td></tr><tr><td><code>UniformToFill</code></td><td>内容在保持原生宽高比的前提下缩放，直至完全填满容器。若内容的宽高比与分配空间的宽高比不一致，会有一部分内容被遮住。</td></tr></tbody></table>

`StretchDirection` 属性的取值如下：

| Stretch Direction  | 说明                                                                                                                         |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `UpOnly`          | 仅当内容小于可用空间时才放大；内容更大时不作缩小。 |
| `DownOnly`        | 仅当内容大于可用空间时才缩小；内容更小时不作放大。 |
| `Both`            | （默认值）始终按拉伸模式拉伸以适配可用空间。                                                |

### Example

这个简单的例子展示 `Viewbox` 均匀放大一个圆（拉伸模式和拉伸方向都取默认值）。

```xml
<Viewbox Stretch="Uniform" Width="150" Height="150">
   <Ellipse Width="50" Height="50" Fill="CornflowerBlue" />  
</Viewbox>
```

### Demonstrations

下面的演示展示了拉伸模式与拉伸方向各种组合的效果。第一组展示拉伸属性的作用：

<table><thead><tr><th width="275">Stretch Value</th><th>Demonstration</th></tr></thead><tbody><tr><td><code>Uniform</code></td><td><Image light={ViewboxScaleUniformBothScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/></td></tr><tr><td><code>UniformToFill</code></td><td><Image light={ViewboxScaleUniformFillBothScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/></td></tr><tr><td><code>Fill</code></td><td><Image light={ViewboxScaleFillBothScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/></td></tr><tr><td><code>None</code></td><td><Image light={ViewboxScaleNoneBothScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/></td></tr></tbody></table>

这一组演示展示拉伸方向属性的作用：

<table><thead><tr><th width="276">Stretch Direction</th><th>Demonstration</th></tr></thead><tbody><tr><td><code>UpOnly</code></td><td><Image light={ViewboxScaleUniformUpOnlyScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/></td></tr><tr><td><code>DownOnly</code></td><td><Image light={ViewboxScaleUniformDownOnlyScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/></td></tr></tbody></table>

## 另请参阅 {#see-also}

- [Viewbox API 参考](/api/avalonia/controls/viewbox)
- [GitHub 上的 `Viewbox.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Viewbox.cs)

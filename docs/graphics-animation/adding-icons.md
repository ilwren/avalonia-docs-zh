---
id: adding-icons
title: 添加图标
description: 用图片文件、图标字体或路径图标为你的 Avalonia 应用添加图标。
doc-type: how-to
---

图标用形象的图案表达操作或内容，让应用更好用。Avalonia 支持图片文件、图标字体和路径图标三种方式。

## 界面图标 {#ui-icons}

在 Avalonia 中，界面上用好图标既能提升应用的观感，也能让它更易用。图标把操作或内容可视化，用户理解起功能来更轻松。

往 Avalonia 应用中添加图标有好几种办法。本指南介绍三种常见做法：用图片文件、用图标字体、用路径图标。

### 使用图片文件 {#using-image-files}
在 Avalonia 中用图标的办法之一是使用图片文件，PNG、JPG、BMP 等格式都行。下面是把图片文件当图标用的例子：

```xml
<Image Width="16" Height="16" Source="avares://MyApp/Assets/icon.png" />
```

这个例子用 [`Image`](/api/avalonia/controls/image) 控件把应用资源中的一张图片显示成图标。`Image` 控件的 `Source` 属性被设成了指向该图片文件的资源 URI。

### 使用图标字体 {#using-icon-fonts}

在 Avalonia 中用图标的另一种办法是使用图标字体。图标字体提供可缩放的矢量图标，尺寸、颜色和投影都能通过 CSS 定制。下面是在 Avalonia 中使用图标字体的例子：

```xml
<TextBlock FontFamily="avares://MyApp/Assets/#FontAwesome" Text="&#xf030;" />
```

这个例子用 `TextBlock` 控件显示 `FontAwesome` 图标字体中的一个图标。`TextBlock` 控件的 `FontFamily` 属性被设成指向字体文件的资源 URI，Text 属性则设成目标图标的 Unicode 码点。

### 使用路径图标 {#using-path-icons}

路径图标可以用 `Geometry` 来绘制图标，其中也包括取自可缩放矢量图形（SVG）格式的路径，尺寸和颜色均可定制。该控件的用法请参阅[参考文档](/controls/media/pathicon)。

### 实践建议 {#best-practices}

图标用得好能提升应用的易用性，但也要用得明智。使用图标时请记住以下几点：

* 确保图标尺寸合适，并且在背景上清晰可辨。
* 常见操作请使用大家公认的图标，这会让你的应用更符合直觉。

## 菜单图标 {#menu-icons}

`MenuItem.Icon` 属性用于给菜单项设置图标。图标的来源可以多种多样：资源 URI、文件路径或网址都行。下面是给菜单项加图标的例子：

```xml
<Menu>
  <MenuItem Header="File">
    <MenuItem Header="Open" Command="{Binding OpenCommand}">
      <MenuItem.Icon>
        <Image Width="16" Height="16" Source="avares://MyApp/Assets/open_icon.png" />
      </MenuItem.Icon>
    </MenuItem>
  </MenuItem>
</Menu>
```

这个例子把 `MenuItem.Icon` 属性设成了一个 `Image` 控件，用它显示应用资源中的一张图片。`Image` 控件的 `Source` 属性设为表示图片来源的资源 URI，`Width` 和 `Height` 属性则用来控制图片的尺寸。

## 另请参阅 {#see-also}

- [形状与几何](/docs/graphics-animation/shapes-and-geometries)：路径图标可用的几何类型。
- [绘制图形](/docs/graphics-animation/drawing-graphics)：Avalonia 图形系统概览。
---
id: transitioningcontentcontrol
title: TransitioningContentControl
description: 一个内容控件：内容变化时会播放过渡动画，支持交叉淡入淡出、滑动和组合式页面过渡。
doc-type: reference
---

import TransitioningContentControlFadeScreenshot from '/img/controls/transitioningcontentcontrol/transitioningcontentcontrol-fade.webp';
import TransitioningContentControlSlideScreenshot from '/img/controls/transitioningcontentcontrol/transitioningcontentcontrol-slide.webp';

[`TransitioningContentControl`](/api/avalonia/controls/transitioningcontentcontrol) 一次显示一块内容，内容一变就播放一段页面过渡动画。它扩展自 [`ContentControl`](/controls/data-display/contentcontrol)，因此凡是能用普通内容控件的地方都能用它。

一个常见用途是做图片幻灯片，不过在导航场景中用 `TransitioningContentControl` 切换视图同样好使。

## 常用属性 {#common-properties}

下面这些属性你多半会经常用到：

| 属性 | 说明 |
|---|---|
| `Content` | 要在控件中显示的内容。 |
| `ContentTemplate` | 用于显示内容的 `DataTemplate`。 |
| `PageTransition` | 内容变化时所用的页面过渡动画。所套用的主题会提供一个默认过渡动画。把该属性设为 `{x:Null}` 可彻底关闭过渡。 |
| `IsTransitionReversed` | 设为 `true` 时，过渡动画反向播放（比如由滑入变为滑出）。 |

## 内置的页面过渡动画 {#built-in-page-transitions}

Avalonia 自带几种页面过渡动画，都可以用在 `TransitioningContentControl` 上：

| 过渡动画 | 说明 |
|---|---|
| `CrossFade` | 旧内容淡出的同时新内容淡入。 |
| `PageSlide` | 让内容从指定方向滑入，支持 `Horizontal` 和 `Vertical` 两种方向。 |
| `CompositePageTransition` | 把多个过渡动画组合起来同时播放。 |

你也可以实现 `IPageTransition` 来自定义过渡动画。完整说明请参阅[设置页面过渡动画](../../docs/graphics-animation/page-transitions)。

## 示例 {#examples}

### 默认过渡（交叉淡入淡出） {#default-transition-cross-fade}

在下面这个例子中，视图模型里存着一组图片。这段 XAML 采用默认的页面过渡动画：每当绑定的 `SelectedImage` 属性变化，图片就会带动画地切换：

```xml
<TransitioningContentControl Content="{Binding SelectedImage}">
    <TransitioningContentControl.ContentTemplate>
        <DataTemplate DataType="Bitmap">
            <Image Source="{Binding}" />
        </DataTemplate>
    </TransitioningContentControl.ContentTemplate>
</TransitioningContentControl>
```

<Image light={TransitioningContentControlFadeScreenshot} alt="TransitioningContentControl with default cross-fade transition" position="center" maxWidth={400} cornerRadius="true"/>

### 横向滑动过渡 {#horizontal-slide-transition}

设置 `PageTransition` 即可替换默认的过渡动画。这里用 `PageSlide` 让图片横向滑动：

```xml
<TransitioningContentControl Content="{Binding SelectedImage}">
    <TransitioningContentControl.PageTransition>
        <PageSlide Orientation="Horizontal" Duration="0:00:00.500" />
    </TransitioningContentControl.PageTransition>
    <TransitioningContentControl.ContentTemplate>
        <DataTemplate DataType="Bitmap">
            <Image Source="{Binding}" />
        </DataTemplate>
    </TransitioningContentControl.ContentTemplate>
</TransitioningContentControl>
```

<Image light={TransitioningContentControlSlideScreenshot} alt="TransitioningContentControl with horizontal page-slide transition" position="center" maxWidth={400} cornerRadius="true"/>

### 自定义时长的交叉淡入淡出 {#cross-fade-with-a-custom-duration}

```xml
<TransitioningContentControl Content="{Binding CurrentView}">
    <TransitioningContentControl.PageTransition>
        <CrossFade Duration="0:00:00.300" />
    </TransitioningContentControl.PageTransition>
</TransitioningContentControl>
```

### 关闭过渡动画 {#disabling-the-transition}

若希望内容瞬间切换、不带任何动画，把 `PageTransition` 设为 null 即可：

```xml
<TransitioningContentControl Content="{Binding CurrentView}"
                             PageTransition="{x:Null}" />
```

## 配合数据模板切换视图 {#view-switching-with-data-templates}

`TransitioningContentControl` 常用来为视图之间的导航加上动画。把 `Content` 绑定到视图模型的某个属性，再为每种视图模型类型提供一个 `DataTemplate`。属性一变，控件就会解析出对应的模板，并自动过渡到新视图。

```xml
<TransitioningContentControl Content="{Binding CurrentPage}">
    <TransitioningContentControl.PageTransition>
        <PageSlide Duration="0:00:00.300" Orientation="Horizontal" />
    </TransitioningContentControl.PageTransition>
    <TransitioningContentControl.DataTemplates>
        <DataTemplate DataType="vm:HomeViewModel">
            <views:HomeView />
        </DataTemplate>
        <DataTemplate DataType="vm:SettingsViewModel">
            <views:SettingsView />
        </DataTemplate>
    </TransitioningContentControl.DataTemplates>
</TransitioningContentControl>
```

完整的分步演练请参阅[如何搭建基本导航](../../docs/how-to/navigation-how-to)。

## 另请参阅 {#see-also}

- [ContentControl](/controls/data-display/contentcontrol)
- [设置页面过渡动画](../../docs/graphics-animation/page-transitions)
- [如何搭建基本导航](../../docs/how-to/navigation-how-to)
- [Carousel](/controls/data-display/collections/carousel)
- [`TransitioningContentControl` API 参考](https://reference.avaloniaui.net/api/Avalonia.ReactiveUI/TransitioningContentControl/)
- [`TransitioningContentControl` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/TransitioningContentControl.cs)

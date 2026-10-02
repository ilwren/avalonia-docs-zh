---
id: pipspager
title: PipsPager
description: Avalonia PipsPager 控件参考：它用一排可交互的圆点指示分页位置，并可选配上一页/下一页按钮。
doc-type: reference
---

import PipsPagerDefaultScreenshot from '/img/controls/pipspager/pipspager-default.png';
import PipsPagerCarouselScreenshot from '/img/controls/pipspager/pipspager-carousel.png';
import PipsPagerLargeCollectionScreenshot from '/img/controls/pipspager/pipspager-large-collection.png';
import PipsPagerCustomColorsScreenshot from '/img/controls/pipspager/pipspager-custom-colors.png';
import PipsPagerCustomButtonsScreenshot from '/img/controls/pipspager/pipspager-custom-buttons.png';
import PipsPagerPillTemplateScreenshot from '/img/controls/pipspager/pipspager-pill-template.png';

# PipsPager

`PipsPager` 是一个页码指示控件，用一排可交互的圆点（pip）表示分页集合中的各页。用户点击某个圆点，或使用可选的上一页/下一页按钮，即可切换当前页。当页数超过 `MaxVisiblePips` 时，圆点会自动滚动，始终让当前选中的那个保持可见。

`PipsPager` 常与 `Carousel` 或 `CarouselPage` 搭配使用，通过 `SelectedPageIndex` 绑定在一起。

## Useful Properties

下面这些属性你多半会经常用到：

| 属性 | 类型 | 默认值 | 说明 |
| -------- | ---- | ------- | ----------- |
| `NumberOfPages` | `int` | `0` | 圆点所表示的总页数。 |
| `SelectedPageIndex` | `int` | `0` | 当前选中页的索引，从 0 开始，支持双向绑定，取值会被钳制在 `[0, NumberOfPages - 1]` 范围内。 |
| `MaxVisiblePips` | `int` | `5` | 同时可见的圆点数量上限。当 `NumberOfPages` 超过该值时，圆点会自动滚动。最小值为 `1`。 |
| `Orientation` | `Orientation` | `Horizontal` | 圆点的排列方向：`Horizontal` 或 `Vertical`。 |
| `IsPreviousButtonVisible` | `bool` | `true` | 显示或隐藏「上一页」导航按钮。 |
| `IsNextButtonVisible` | `bool` | `true` | 显示或隐藏「下一页」导航按钮。 |
| `PreviousButtonTheme` | `ControlTheme?` | `null` | 作用于「上一页」导航按钮的自定义主题。 |
| `NextButtonTheme` | `ControlTheme?` | `null` | 作用于「下一页」导航按钮的自定义主题。 |

## Pseudo-classes

| 伪类 | 触发条件 |
| ------------ | --------- |
| `:first-page` | `SelectedPageIndex` is `0`. |
| `:last-page` | `SelectedPageIndex` 为 `NumberOfPages - 1` 且 `NumberOfPages > 0`。 |
| `:horizontal` | `Orientation` is `Horizontal`. |
| `:vertical` | `Orientation` is `Vertical`. |

## 事件 {#events}

| 事件 | 参数类型 | 说明 |
| ----- | --------- | ----------- |
| `SelectedIndexChanged` | `PipsPagerSelectedIndexChangedEventArgs` | 选中页发生变化时引发，提供 `OldIndex` 和 `NewIndex`。 |

## Keyboard Navigation

- 左 / 上方向键：切换到上一页。
- 右 / 下方向键：切换到下一页。
- Home：跳到第一页（索引 `0`）。
- End：跳到最后一页（`NumberOfPages - 1`）。

## Styling Resource Keys

在 `PipsPager` 或它的某个祖先上覆盖下列资源键，即可定制圆点指示器的颜色：

| 资源键 | 说明 |
| ------------ | ----------- |
| `PipsPagerSelectionIndicatorForeground` | 圆点的默认颜色。 |
| `PipsPagerSelectionIndicatorForegroundSelected` | 选中圆点的颜色。 |
| `PipsPagerSelectionIndicatorForegroundPointerOver` | 指针悬停时圆点的颜色。 |
| `PipsPagerSelectionIndicatorForegroundPressed` | 按下时圆点的颜色。 |

## 示例 {#examples}

### Basic PipsPager

```xml
<PipsPager NumberOfPages="5" />
```

<Image light={PipsPagerDefaultScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

### 在代码中使用 PipsPager {#pipspager-in-code}

```csharp
var pager = new PipsPager
{
    NumberOfPages = 5,
    MaxVisiblePips = 5
};
```

### Vertical Orientation

```xml
<PipsPager NumberOfPages="5" Orientation="Vertical" />
```

### Without Navigation Buttons

```xml
<PipsPager NumberOfPages="10"
           MaxVisiblePips="5"
           IsPreviousButtonVisible="False"
           IsNextButtonVisible="False" />
```

### 与 Carousel 双向绑定 {#two-way-binding-with-a-carousel}

把 `SelectedPageIndex` 与 `Carousel.SelectedIndex` 绑定起来，让两者的导航保持同步：

```xml
<Grid RowDefinitions="*,Auto">
    <Carousel Name="GalleryCarousel"
              SelectedIndex="{Binding #GalleryPager.SelectedPageIndex, Mode=TwoWay}">
        <Carousel.Items>
            <Border Background="#E3F2FD" CornerRadius="8">
                <TextBlock Text="Page 1" FontSize="30"
                           VerticalAlignment="Center" HorizontalAlignment="Center" />
            </Border>
            <Border Background="#C8E6C9" CornerRadius="8">
                <TextBlock Text="Page 2" FontSize="30"
                           VerticalAlignment="Center" HorizontalAlignment="Center" />
            </Border>
            <Border Background="#FFE0B2" CornerRadius="8">
                <TextBlock Text="Page 3" FontSize="30"
                           VerticalAlignment="Center" HorizontalAlignment="Center" />
            </Border>
        </Carousel.Items>
    </Carousel>

    <PipsPager Name="GalleryPager"
               Grid.Row="1"
               NumberOfPages="3"
               HorizontalAlignment="Center"
               Margin="0,12,0,0" />
</Grid>
```

<Image light={PipsPagerCarouselScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

### 与 CarouselPage 双向绑定 {#two-way-binding-with-a-carouselpage}

```xml
<Grid RowDefinitions="*,Auto">
    <CarouselPage Name="DemoCarousel"
                  SelectedIndex="{Binding #Pager.SelectedPageIndex, Mode=TwoWay}">
        <ContentPage Header="Welcome">
            <TextBlock Text="Welcome" FontSize="28"
                       HorizontalAlignment="Center" VerticalAlignment="Center" />
        </ContentPage>
        <ContentPage Header="Features">
            <TextBlock Text="Features" FontSize="28"
                       HorizontalAlignment="Center" VerticalAlignment="Center" />
        </ContentPage>
        <ContentPage Header="Get Started">
            <TextBlock Text="Get Started" FontSize="28"
                       HorizontalAlignment="Center" VerticalAlignment="Center" />
        </ContentPage>
    </CarouselPage>

    <PipsPager Name="Pager"
               Grid.Row="1"
               NumberOfPages="3"
               HorizontalAlignment="Center"
               Margin="0,12,0,0" />
</Grid>
```

### 大集合与自动滚动的圆点 {#large-collections-with-auto-scrolling-pips}

当 `NumberOfPages` 超过 `MaxVisiblePips` 时，圆点条会自动滚动，始终让当前选中的那个保持可见：

```xml
<PipsPager NumberOfPages="50"
           MaxVisiblePips="7"
           SelectedPageIndex="25" />
```

<Image light={PipsPagerLargeCollectionScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

### 响应选中项变化 {#responding-to-selection-changes}

```csharp
pager.SelectedIndexChanged += (sender, e) =>
{
    Console.WriteLine($"Changed from page {e.OldIndex} to {e.NewIndex}");
};
```

### Custom Pip Colors

在 `PipsPager` 上覆盖指示器的资源键，即可改变圆点颜色：

```xml
<PipsPager NumberOfPages="5" MaxVisiblePips="5">
    <PipsPager.Resources>
        <SolidColorBrush x:Key="PipsPagerSelectionIndicatorForeground" Color="Orange" />
        <SolidColorBrush x:Key="PipsPagerSelectionIndicatorForegroundSelected" Color="Blue" />
        <SolidColorBrush x:Key="PipsPagerSelectionIndicatorForegroundPointerOver" Color="Gold" />
    </PipsPager.Resources>
</PipsPager>
```

<Image light={PipsPagerCustomColorsScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

### Custom Button Themes

用 `PreviousButtonTheme` 和 `NextButtonTheme` 把默认的箭头按钮换成自定义主题的按钮：

```xml
<PipsPager NumberOfPages="5" MaxVisiblePips="5">
    <PipsPager.Resources>
        <ControlTheme x:Key="PrevTheme" TargetType="Button">
            <Setter Property="Content" Value="Prev" />
            <Setter Property="Background" Value="LightGray" />
            <Setter Property="Foreground" Value="Black" />
            <Setter Property="Padding" Value="8,2" />
            <Setter Property="Margin" Value="0,0,8,0" />
            <Setter Property="Template">
                <ControlTemplate>
                    <Border Background="{TemplateBinding Background}" CornerRadius="4">
                        <ContentPresenter Content="{TemplateBinding Content}"
                                          Margin="{TemplateBinding Padding}" />
                    </Border>
                </ControlTemplate>
            </Setter>
        </ControlTheme>
        <ControlTheme x:Key="NextTheme" TargetType="Button">
            <Setter Property="Content" Value="Next" />
            <Setter Property="Background" Value="LightGray" />
            <Setter Property="Foreground" Value="Black" />
            <Setter Property="Padding" Value="8,2" />
            <Setter Property="Margin" Value="8,0,0,0" />
            <Setter Property="Template">
                <ControlTemplate>
                    <Border Background="{TemplateBinding Background}" CornerRadius="4">
                        <ContentPresenter Content="{TemplateBinding Content}"
                                          Margin="{TemplateBinding Padding}" />
                    </Border>
                </ControlTemplate>
            </Setter>
        </ControlTheme>
    </PipsPager.Resources>
    <PipsPager.PreviousButtonTheme>
        <StaticResource ResourceKey="PrevTheme" />
    </PipsPager.PreviousButtonTheme>
    <PipsPager.NextButtonTheme>
        <StaticResource ResourceKey="NextTheme" />
    </PipsPager.NextButtonTheme>
</PipsPager>
```

<Image light={PipsPagerCustomButtonsScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

### 自定义圆点模板（胶囊形指示器） {#custom-pip-templates-pill-shaped-indicator}

用样式选择器定位内部的 `ListBoxItem`，即可替换默认的圆点形状。下面的例子把选中的圆点从圆形变成横向胶囊：

```xml
<PipsPager NumberOfPages="5"
           IsPreviousButtonVisible="False"
           IsNextButtonVisible="False">
    <PipsPager.Styles>
        <Style Selector="PipsPager /template/ ListBox ListBoxItem">
            <Setter Property="Width" Value="24" />
            <Setter Property="Height" Value="24" />
            <Setter Property="Padding" Value="0" />
            <Setter Property="Margin" Value="2,0" />
            <Setter Property="MinWidth" Value="0" />
            <Setter Property="MinHeight" Value="0" />
            <Setter Property="VerticalAlignment" Value="Center" />
            <Setter Property="Template">
                <ControlTemplate>
                    <Grid Background="Transparent">
                        <Border Name="Pip"
                                Width="8" Height="8" CornerRadius="4"
                                HorizontalAlignment="Center" VerticalAlignment="Center"
                                Background="#C0C0C0">
                            <Border.Transitions>
                                <Transitions>
                                    <DoubleTransition Property="Width" Duration="0:0:0.2" Easing="CubicEaseOut" />
                                    <DoubleTransition Property="Height" Duration="0:0:0.2" Easing="CubicEaseOut" />
                                    <CornerRadiusTransition Property="CornerRadius" Duration="0:0:0.2" Easing="CubicEaseOut" />
                                    <BrushTransition Property="Background" Duration="0:0:0.2" />
                                </Transitions>
                            </Border.Transitions>
                        </Border>
                    </Grid>
                </ControlTemplate>
            </Setter>
        </Style>
        <Style Selector="PipsPager /template/ ListBox ListBoxItem:pointerover /template/ Border#Pip">
            <Setter Property="Width" Value="10" />
            <Setter Property="Height" Value="10" />
            <Setter Property="CornerRadius" Value="5" />
            <Setter Property="Background" Value="#909090" />
        </Style>
        <Style Selector="PipsPager /template/ ListBox ListBoxItem:selected /template/ Border#Pip">
            <Setter Property="Width" Value="24" />
            <Setter Property="Height" Value="8" />
            <Setter Property="CornerRadius" Value="4" />
            <Setter Property="Background" Value="#FF6B35" />
        </Style>
        <Style Selector="PipsPager /template/ ListBox ListBoxItem:selected:pointerover /template/ Border#Pip">
            <Setter Property="Width" Value="24" />
            <Setter Property="Height" Value="8" />
            <Setter Property="CornerRadius" Value="4" />
            <Setter Property="Background" Value="#E85A2A" />
        </Style>
    </PipsPager.Styles>
</PipsPager>
```

<Image light={PipsPagerPillTemplateScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

### Programmatic Control

```csharp
// Set page count
pager.NumberOfPages = 20;

// Jump to a specific page
pager.SelectedPageIndex = 10;

// Limit visible pips
pager.MaxVisiblePips = 7;

// Switch to vertical
pager.Orientation = Orientation.Vertical;

// Hide navigation buttons
pager.IsPreviousButtonVisible = false;
pager.IsNextButtonVisible = false;
```

## 另请参阅 {#see-also}

- [API 参考](/api/avalonia/controls/pipspager)
- [源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/PipsPager/PipsPager.cs)

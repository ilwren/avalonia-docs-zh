---
id: control-template-walkthrough
title: 控件模板实战
---

本文从零搭出一个完整的控件模板，并逐块讲解。读完之后，你就能给任何 Avalonia 控件重做模板了。

## 前置条件 {#prerequisites}

- 一个 Avalonia 项目，其中有一个可供你添加样式和控件的 `Window`。
- 对[样式](/docs/styling/styles)和 [XAML](/docs/fundamentals/avalonia-xaml) 基础有所了解。

## 什么是控件模板？ {#what-is-a-control-template}

控件模板定义控件的视觉结构。每个 Avalonia 控件都有一份由主题提供的默认模板。你可以整个儿换掉这份模板，从而在保留控件行为的前提下改变它的样子。

## 第 1 步：做一个基本的按钮模板 {#step-1-create-a-basic-button-template}

先从一个只把内容渲染出来的极简按钮模板开始：

```xml
<Window.Styles>
    <Style Selector="Button.custom">
        <Setter Property="Template">
            <ControlTemplate>
                <Border Background="{TemplateBinding Background}"
                        BorderBrush="{TemplateBinding BorderBrush}"
                        BorderThickness="{TemplateBinding BorderThickness}"
                        CornerRadius="{TemplateBinding CornerRadius}"
                        Padding="{TemplateBinding Padding}">
                    <ContentPresenter Content="{TemplateBinding Content}"
                                      ContentTemplate="{TemplateBinding ContentTemplate}"
                                      HorizontalContentAlignment="{TemplateBinding HorizontalContentAlignment}"
                                      VerticalContentAlignment="{TemplateBinding VerticalContentAlignment}" />
                </Border>
            </ControlTemplate>
        </Setter>
        <Setter Property="Background" Value="#6366F1" />
        <Setter Property="Foreground" Value="White" />
        <Setter Property="BorderThickness" Value="0" />
        <Setter Property="CornerRadius" Value="6" />
        <Setter Property="Padding" Value="16,8" />
        <Setter Property="HorizontalContentAlignment" Value="Center" />
    </Style>
</Window.Styles>

<Button Classes="custom" Content="Click Me" />
```

### 关键概念 {#key-concepts}

- **`ControlTemplate`** 定义取代控件默认外观的视觉树。
- **`TemplateBinding`** 绑定到被模板化父级的属性，比 `{Binding RelativeSource={RelativeSource TemplatedParent}}` 更高效。它默认是 `OneWay` 绑定；若你需要把值写回去，请用 `Mode=TwoWay`。
- **`ContentPresenter`** 负责显示按钮的 `Content` 属性。没有它，按钮的内容就显示不出来。

## 第 2 步：用伪类加上视觉状态 {#step-2-add-visual-states-with-pseudo-classes}

Avalonia 用的是伪类（与 CSS 类似），而不是 WPF 的 VisualStateManager。下面加上几个交互状态：

```xml
<Style Selector="Button.custom">
    <Setter Property="Template">
        <ControlTemplate>
            <Border x:Name="PART_Border"
                    Background="{TemplateBinding Background}"
                    BorderBrush="{TemplateBinding BorderBrush}"
                    BorderThickness="{TemplateBinding BorderThickness}"
                    CornerRadius="{TemplateBinding CornerRadius}"
                    Padding="{TemplateBinding Padding}">
                <ContentPresenter Content="{TemplateBinding Content}"
                                  ContentTemplate="{TemplateBinding ContentTemplate}"
                                  HorizontalContentAlignment="{TemplateBinding HorizontalContentAlignment}"
                                  VerticalContentAlignment="{TemplateBinding VerticalContentAlignment}" />
            </Border>
        </ControlTemplate>
    </Setter>

    <!-- Default state -->
    <Setter Property="Background" Value="#6366F1" />
    <Setter Property="Foreground" Value="White" />
    <Setter Property="BorderThickness" Value="0" />
    <Setter Property="CornerRadius" Value="6" />
    <Setter Property="Padding" Value="16,8" />
    <Setter Property="HorizontalContentAlignment" Value="Center" />
</Style>

<!-- Hover state -->
<Style Selector="Button.custom:pointerover">
    <Setter Property="Background" Value="#818CF8" />
</Style>

<!-- Pressed state -->
<Style Selector="Button.custom:pressed">
    <Setter Property="Background" Value="#4F46E5" />
</Style>

<!-- Disabled state -->
<Style Selector="Button.custom:disabled">
    <Setter Property="Background" Value="#C7D2FE" />
    <Setter Property="Foreground" Value="#9CA3AF" />
</Style>

<!-- Focused state -->
<Style Selector="Button.custom:focus-visible">
    <Setter Property="BorderBrush" Value="White" />
    <Setter Property="BorderThickness" Value="2" />
</Style>
```

### 常用伪类 {#common-pseudo-classes}

| 伪类 | 何时生效 |
|---|---|
| `:pointerover` | 指针悬停在控件上 |
| `:pressed` | 控件正被按下 |
| `:disabled` | 控件被禁用（`IsEnabled="False"`） |
| `:focus` | 控件持有键盘焦点 |
| `:focus-visible` | 控件的键盘焦点来自键盘导航（而非指针点击） |
| `:checked` | ToggleButton/CheckBox/RadioButton 处于选中状态 |
| `:unchecked` | ToggleButton/CheckBox/RadioButton 处于未选中状态 |
| `:selected` | 项被选中（比如 ListBoxItem） |

## 第 3 步：加上动画 {#step-3-add-animations}

用 `Transitions` 属性让状态之间的切换变得平滑：

```xml
<Style Selector="Button.custom">
    <!-- ...template and setters from above... -->
    <Setter Property="Transitions">
        <Transitions>
            <BrushTransition Property="Background" Duration="0:0:0.15" />
            <BrushTransition Property="BorderBrush" Duration="0:0:0.15" />
            <ThicknessTransition Property="BorderThickness" Duration="0:0:0.15" />
        </Transitions>
    </Setter>
</Style>
```

现在，背景色会在悬停、按下和常态之间柔和地渐变了。

## 第 4 步：使用模板部件 {#step-4-use-template-parts}

模板更复杂时，请按 `PART_` 约定给内部元素命名。控件的代码隐藏即可定位这些部件并与之交互：

```xml
<ControlTemplate>
    <Grid>
        <Border x:Name="PART_Background"
                Background="{TemplateBinding Background}"
                CornerRadius="{TemplateBinding CornerRadius}" />

        <Border x:Name="PART_Highlight"
                Background="White" Opacity="0"
                CornerRadius="{TemplateBinding CornerRadius}" />

        <ContentPresenter x:Name="PART_ContentPresenter"
                          Content="{TemplateBinding Content}"
                          Margin="{TemplateBinding Padding}"
                          HorizontalContentAlignment="{TemplateBinding HorizontalContentAlignment}"
                          VerticalContentAlignment="{TemplateBinding VerticalContentAlignment}" />
    </Grid>
</ControlTemplate>
```

之后你就能在伪类样式中圈定这些部件：

```xml
<Style Selector="Button.custom:pointerover /template/ Border#PART_Highlight">
    <Setter Property="Opacity" Value="0.1" />
</Style>

<Style Selector="Button.custom:pressed /template/ Border#PART_Highlight">
    <Setter Property="Opacity" Value="0.2" />
</Style>
```

`/template/` 选择器可以钻进控件的模板视觉树，`#PART_Highlight` 则按名称选取。

## 第 5 步：把它们拼到一起 {#step-5-putting-it-all-together}

下面是一份打磨完整的自定义按钮模板：

```xml
<Window.Styles>
    <Style Selector="Button.pill">
        <Setter Property="Background" Value="#6366F1" />
        <Setter Property="Foreground" Value="White" />
        <Setter Property="BorderThickness" Value="0" />
        <Setter Property="CornerRadius" Value="999" />
        <Setter Property="Padding" Value="20,10" />
        <Setter Property="HorizontalContentAlignment" Value="Center" />
        <Setter Property="Cursor" Value="Hand" />
        <Setter Property="Transitions">
            <Transitions>
                <BrushTransition Property="Background" Duration="0:0:0.2" />
                <TransformOperationsTransition Property="RenderTransform" Duration="0:0:0.1" />
            </Transitions>
        </Setter>
        <Setter Property="RenderTransform" Value="scale(1)" />
        <Setter Property="Template">
            <ControlTemplate>
                <Border Background="{TemplateBinding Background}"
                        CornerRadius="{TemplateBinding CornerRadius}"
                        Padding="{TemplateBinding Padding}"
                        BoxShadow="0 2 4 0 #20000000">
                    <ContentPresenter Content="{TemplateBinding Content}"
                                      ContentTemplate="{TemplateBinding ContentTemplate}"
                                      HorizontalContentAlignment="{TemplateBinding HorizontalContentAlignment}"
                                      VerticalContentAlignment="{TemplateBinding VerticalContentAlignment}" />
                </Border>
            </ControlTemplate>
        </Setter>
    </Style>

    <Style Selector="Button.pill:pointerover">
        <Setter Property="Background" Value="#818CF8" />
    </Style>

    <Style Selector="Button.pill:pressed">
        <Setter Property="Background" Value="#4F46E5" />
        <Setter Property="RenderTransform" Value="scale(0.97)" />
    </Style>

    <Style Selector="Button.pill:disabled">
        <Setter Property="Background" Value="#E5E7EB" />
        <Setter Property="Foreground" Value="#9CA3AF" />
    </Style>
</Window.Styles>

<StackPanel Spacing="12" Margin="20">
    <Button Classes="pill" Content="Primary Action" />
    <Button Classes="pill" Content="Disabled" IsEnabled="False" />
</StackPanel>
```

## 验证效果 {#verify-the-result}

运行应用。你应该看到一个紫色背景的胶囊形按钮：把指针移上去，确认背景变浅；按下去看它变深并略微缩小；再确认禁用状态的按钮呈灰色。若过渡生效了，颜色变化会柔和地动起来，而不是生硬地一跳。

## 自定义模板的小贴士 {#tips-for-custom-templates}

- 务必用 `TemplateBinding` 绑定 `Padding`、`Background`、`BorderBrush`、`BorderThickness` 和 `CornerRadius`，这样模板才会尊重外部设定的属性值。
- 内容控件用 `ContentPresenter`，列表类控件用 `ItemsPresenter`。
- 管理状态时，优先用伪类选择器而不是触发器。
- 给模板部件加上 `PART_` 前缀命名，既清晰也便于代码隐藏取用。
- 用 `Transitions` 让状态变化平滑过渡，而不是生硬的 setter 切换。
- 浅色和深色主题都要试一遍，确保模板在各个主题变体下都站得住。

## 另请参阅 {#see-also}

- [控件主题](/docs/styling/control-themes)：主题如何为所有控件套用模板。
- [样式选择器](/docs/styling/style-selectors)：圈定控件与状态的选择器语法。
- [伪类](/docs/styling/pseudoclasses)：全部可用的伪类。

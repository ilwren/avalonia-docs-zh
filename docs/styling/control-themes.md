---
id: control-themes
title: 控件主题
---

import StylingEllipseButtonScreenshot from '/img/concepts/ui-concepts/styling/ellipse-button.png';

控件主题建立在[样式](/docs/styling/styles)之上，为控件提供可切换的整套外观。普通样式会层层累加、一旦应用便撤不掉；控件主题则可以整个替换。因此，当你要为某个控件实例或界面中的某一块彻底换一副面孔时，控件主题才是正解。

控件主题本身也是样式，但有几处要紧的不同：

- 控件主题没有选择器，取而代之的是 `TargetType` 属性，用来说明它针对哪种控件
- 控件主题存放在 `ResourceDictionary` 中，而非 `Styles` 集合里
- 控件主题通过设置 `Theme` 属性赋给控件，通常借助 `{StaticResource}` 标记扩展

:::tip
由于控件主题以样式为基础，请先弄懂 Avalonia 的[样式系统](/docs/styling/styles)。
:::

:::info
控件主题一般用在[模板化（无外观）](/docs/custom-controls)控件上，但其实任何控件都能用。不过对非模板化控件来说，用普通样式往往更省事。
:::

## 示例：圆形按钮 {#example-round-button}

下面这个简单的 `Button` 主题，会把按钮画成一个椭圆背景，颇有几分 90 年代 Geocities 的味道：

```xml title="App.axaml"
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="AvaloniaApplication.App">
  <Application.Styles>
    <FluentTheme />
  </Application.Styles>

  <Application.Resources>
    // highlight-start
    <ControlTheme x:Key="EllipseButton" TargetType="Button">
      <Setter Property="Background" Value="Blue"/>
      <Setter Property="Foreground" Value="Yellow"/>
      <Setter Property="Padding" Value="8"/>
      <Setter Property="Template">
        <ControlTemplate>
          <Panel>
            <Ellipse Fill="{TemplateBinding Background}"
                     HorizontalAlignment="Stretch"
                     VerticalAlignment="Stretch"/>
            <ContentPresenter x:Name="PART_ContentPresenter"
                              Content="{TemplateBinding Content}"
                              Margin="{TemplateBinding Padding}"/>
          </Panel>
        </ControlTemplate>
      </Setter>
    </ControlTheme>
    // highlight-end
  </Application.Resources>
</Application>
```

```xml title='MainWindow.xaml'
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x='http://schemas.microsoft.com/winfx/2006/xaml'
        x:Class="Sandbox.MainWindow">
  // highlight-start
  <Button Theme="{StaticResource EllipseButton}"
          HorizontalAlignment="Center"
          VerticalAlignment="Center">
    Hello World!
  </Button>
  // highlight-end
</Window>
```

<Image light={StylingEllipseButtonScreenshot} alt="Ellipse button" position="center" maxWidth={400} cornerRadius="true" />

## 控件主题中的交互 {#interaction-in-control-themes}

和普通样式一样，控件主题也支持[嵌套样式](/docs/styling/styles)，可用来添加指针悬停、按下之类的交互状态。

## 示例：圆形按钮的悬停状态 {#example-round-button-hover-state}

借助嵌套样式，我们可以让按钮在指针悬停时变色：

```xml title="App.axaml"
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="AvaloniaApplication.App">
  <Application.Styles>
    <FluentTheme />
  </Application.Styles>

  <Application.Resources>
    <ControlTheme x:Key="EllipseButton" TargetType="Button">
      <Setter Property="Background" Value="Blue"/>
      <Setter Property="Foreground" Value="Yellow"/>
      <Setter Property="Padding" Value="8"/>
      <Setter Property="Template">
        <ControlTemplate>
          <Panel>
            <Ellipse Fill="{TemplateBinding Background}"
                     HorizontalAlignment="Stretch"
                     VerticalAlignment="Stretch"/>
            <ContentPresenter x:Name="PART_ContentPresenter"
                              Content="{TemplateBinding Content}"
                              Margin="{TemplateBinding Padding}"/>
          </Panel>
        </ControlTemplate>
      </Setter>
      
      // highlight-start
      <Style Selector="^:pointerover">
        <Setter Property="Background" Value="Red"/>
        <Setter Property="Foreground" Value="White"/>
      </Style>
      // highlight-end
    </ControlTheme>
  </Application.Resources>
</Application>
```

## 控件主题的查找 {#control-theme-lookup}

控件主题有两种被找到的途径：

- 若控件的 `Theme` 属性已设置，就用那个控件主题；否则
- Avalonia 会沿逻辑树向上搜寻，找一个 `x:Key` 与控件[样式键](/docs/styling/styles)匹配的 `ControlTheme` 资源

:::tip
若 Avalonia 老是找不到你的主题，请确认控件返回的[样式键](/docs/styling/styles)与你控件主题的 `x:Key` 和 `TargetType` 对得上。
:::

实际上这意味着，定义控件主题时你有两种选择：

- **若想让控件主题对该控件的所有实例生效**，就用 `{x:Type}` 作资源键。例如
  `<ControlTheme x:Key="{x:Type Button}" TargetType="Button">`
- **若只想让控件主题作用于部分实例**，就用别的东西作资源键，再用 `{StaticResource}` 取用该资源。这个键通常是个 `string`

:::info
注意，这也意味着同一时刻一个控件上只能应用一个控件主题。
:::

## 示例：让所有按钮都变圆 {#example-make-all-the-buttons-round}

要把该控件主题应用到应用中的所有按钮上，请把控件主题的 `x:Key` 改成与 `Button` 类型匹配。

```xml title="App.axaml"
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="AvaloniaApplication.App">
  <Application.Styles>
    <FluentTheme />
  </Application.Styles>

  <Application.Resources>
      // highlight-next-line
    <ControlTheme x:Key="{x:Type Button}" TargetType="Button">
      <Setter Property="Background" Value="Blue"/>
      <Setter Property="Foreground" Value="Yellow"/>
      <Setter Property="Padding" Value="8"/>
      <Setter Property="Template">
        <ControlTemplate>
          <Panel>
            <Ellipse Fill="{TemplateBinding Background}"
                     HorizontalAlignment="Stretch"
                     VerticalAlignment="Stretch"/>
            <ContentPresenter x:Name="PART_ContentPresenter"
                              Content="{TemplateBinding Content}"
                              Margin="{TemplateBinding Padding}"/>
          </Panel>
        </ControlTemplate>
      </Setter>
      
      <Style Selector="^:pointerover">
        <Setter Property="Background" Value="Red"/>
        <Setter Property="Foreground" Value="White"/>
      </Style>
    </ControlTheme>
  </Application.Resources>
</Application>
```

## TargetType

`ControlTheme.TargetType` 属性指明 setter 中的属性归属于哪个类型。若不指定 `TargetType`，你就必须在 `Setter` 对象里用 `Property="ClassName.Property"` 这种写法为属性加上类名限定。比如不能只写把 `Property` 设为 `FontSize`，而要写成把 `Property` 设为 `TextBlock.FontSize` 或 `Control.FontSize`。

## 另请参阅 {#see-also}

- 带 `WinClassicButtonTheme` 的 [ButtonCustomize](https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/ButtonCustomize) 示例
- Avalonia 内置控件的控件主题：
  - [Simple Theme](https://github.com/AvaloniaUI/Avalonia/tree/master/src/Avalonia.Themes.Simple/Controls)
  - [Fluent Theme](https://github.com/AvaloniaUI/Avalonia/tree/master/src/Avalonia.Themes.Fluent/Controls)
- [Styles](/docs/styling/styles)
- [控件模板实战](/docs/styling/control-template-walkthrough)

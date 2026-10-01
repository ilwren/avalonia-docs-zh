---
id: styling
title: 样式
description: WPF 与 Avalonia 在样式上的关键差异，包括选择器、样式类和主题。
doc-type: migration
---

从 WPF 迁过来时，样式系统是观念上变化最大的一块。Avalonia 没有沿用 WPF 那套基于资源字典的做法，而是采用了带选择器、样式类和伪类的类 CSS 样式模型。本指南逐一讲清关键差异，并给出各个方面切实可用的迁移套路。

## 声明样式 {#style-declaration}

在 WPF 中，样式定义为资源，按类型或键来引用。在 Avalonia 中，样式放在专门的 [`Styles`](/api/avalonia/styling/styles) 集合里，并用类 CSS 的选择器来圈定目标控件。

**WPF:**

```xml
<Window.Resources>
    <Style TargetType="Button">
        <Setter Property="Background" Value="SteelBlue"/>
        <Setter Property="Foreground" Value="White"/>
    </Style>
</Window.Resources>
```

**Avalonia:**

```xml
<Window.Styles>
    <Style Selector="Button">
        <Setter Property="Background" Value="SteelBlue"/>
        <Setter Property="Foreground" Value="White"/>
    </Style>
</Window.Styles>
```

关键差异：

| 方面 | WPF | Avalonia |
|---|---|---|
| 存放位置 | `Resources` dictionary | `Styles` collection |
| 圈定目标的方式 | `TargetType` attribute | `Selector` 特性（类 CSS） |
| Scope | 作用于该资源以下的视觉树 | 作用于 `Styles` 所属控件以下的视觉树 |
| 继承模型 | 资源查找沿树向上进行 | 样式按选择器的具体程度自上而下匹配 |

## 选择器与 TargetType {#selectors-vs-targettype}

WPF 用 `TargetType` 把样式匹配到某个控件类型上。Avalonia 则换成了受 CSS 启发的选择器语法：可以按类型、类、名称、属性状态、嵌套关系等等来圈定目标。

**WPF（圈定所有 TextBlock）：**

```xml
<Style TargetType="TextBlock">
    <Setter Property="Foreground" Value="Gray"/>
</Style>
```

**Avalonia（圈定所有 TextBlock）：**

```xml
<Style Selector="TextBlock">
    <Setter Property="Foreground" Value="Gray"/>
</Style>
```

**Avalonia（圈定 StackPanel 内的 TextBlock）：**

```xml
<Style Selector="StackPanel > TextBlock">
    <Setter Property="Foreground" Value="Gray"/>
</Style>
```

**Avalonia（圈定某个具名控件）：**

```xml
<Style Selector="TextBlock#MyHeader">
    <Setter Property="FontSize" Value="24"/>
</Style>
```

常见的选择器套路：

| 选择器 | 含义 |
|---|---|
| `Button` | 所有 Button 控件 |
| `Button.primary` | 带有 `primary` 样式类的 Button |
| `StackPanel > Button` | 作为 StackPanel 直接子级的 Button |
| `Button:pointerover` | 处于指针悬停状态的 Button |
| `Button:not(:disabled)` | 未被禁用的 Button |
| `TextBlock#title` | 带有 `Name="title"` 的 TextBlock |
| `Button.primary:pointerover` | 处于指针悬停状态的主要按钮 |

完整的选择器参考请见[样式选择器](/docs/styling/style-selectors)。

## 样式类与 x:Key {#style-classes-vs-xkey}

在 WPF 中，同一控件类型的不同样式靠指定 `x:Key`、再用 `Style="{StaticResource MyStyle}"` 引用来区分。Avalonia 改用**样式类**，其行为与 CSS 的 class 一样。

**WPF:**

```xml
<Window.Resources>
    <Style x:Key="PrimaryButton" TargetType="Button">
        <Setter Property="Background" Value="SteelBlue"/>
        <Setter Property="Foreground" Value="White"/>
    </Style>
</Window.Resources>

<Button Style="{StaticResource PrimaryButton}" Content="Save"/>
```

**Avalonia:**

```xml
<Window.Styles>
    <Style Selector="Button.primary">
        <Setter Property="Background" Value="SteelBlue"/>
        <Setter Property="Foreground" Value="White"/>
    </Style>
</Window.Styles>

<Button Classes="primary" Content="Save"/>
```

一个控件可以同时带多个类，而且类还能动态开关：

```xml
<Button Classes="primary large" Content="Save"/>
```

你也可以在代码隐藏中切换类：

```csharp
myButton.Classes.Add("active");
myButton.Classes.Remove("active");
```

这种做法免去了管理资源键的麻烦，组合起来也更灵活。

## 从触发器到伪类 {#triggers-to-pseudo-classes}

WPF 在样式内部使用 `Trigger`、`DataTrigger` 和 `EventTrigger` 元素。Avalonia 把这些统统换成了**伪类**加选择器匹配。

### 属性触发器对应的伪类 {#property-triggers-to-pseudo-classes}

**WPF（属性触发器）：**

```xml
<Style TargetType="Button">
    <Setter Property="Background" Value="Gray"/>
    <Style.Triggers>
        <Trigger Property="IsMouseOver" Value="True">
            <Setter Property="Background" Value="LightBlue"/>
        </Trigger>
        <Trigger Property="IsPressed" Value="True">
            <Setter Property="Background" Value="DarkBlue"/>
        </Trigger>
    </Style.Triggers>
</Style>
```

**Avalonia（伪类）：**

```xml
<Style Selector="Button">
    <Setter Property="Background" Value="Gray"/>
</Style>
<Style Selector="Button:pointerover">
    <Setter Property="Background" Value="LightBlue"/>
</Style>
<Style Selector="Button:pressed">
    <Setter Property="Background" Value="DarkBlue"/>
</Style>
```

常见的 WPF 触发器到伪类的对应关系：

| WPF Trigger Property | Avalonia 伪类 |
|---|---|
| `IsMouseOver` | `:pointerover` |
| `IsPressed` | `:pressed` |
| `IsEnabled="False"` | `:disabled` |
| `IsChecked="True"` | `:checked` |
| `IsFocused` | `:focus` |
| `IsSelected` | `:selected` |
| `IsExpanded` | `:expanded` |

完整清单请见[伪类](/docs/styling/pseudoclasses)。

### DataTrigger 的迁移 {#datatrigger-migration}

WPF 的 `DataTrigger` 会依据绑定值来应用 setter。Avalonia 没有直接对应者，请按场景从下面几种做法中挑一种。

**方案一：配合转换器直接绑定。**

当只有单个属性需要随绑定值变化时，用这个：

```xml
<TextBlock Text="{Binding Status}"
           Foreground="{Binding Status, Converter={StaticResource StatusToColorConverter}}"/>
```

**方案二：用样式类配合选择器。**

若你的 ViewModel 暴露了一个对应某种视觉状态的属性，可以在代码隐藏里设置样式类（或借助 behavior），再用选择器圈定它：

```xml
<Style Selector="Border.error">
    <Setter Property="BorderBrush" Value="Red"/>
    <Setter Property="BorderThickness" Value="2"/>
</Style>
```

**方案三：尺寸相关的触发用容器查询。**

在 WPF 中，常见套路是把 `DataTrigger` 绑定到 `ActualWidth` 或 `ActualHeight`（往往还得过一道转换器），以便在不同尺寸下调整布局。Avalonia 提供了容器查询，正是为替代这套做法而生的。

**WPF（对 ActualWidth 使用 DataTrigger）：**

```xml
<Style TargetType="UniformGrid">
    <Setter Property="Columns" Value="3"/>
    <Style.Triggers>
        <DataTrigger Binding="{Binding ActualWidth,
                     RelativeSource={RelativeSource AncestorType=Border},
                     Converter={StaticResource LessThanConverter},
                     ConverterParameter=600}"
                     Value="True">
            <Setter Property="Columns" Value="1"/>
        </DataTrigger>
    </Style.Triggers>
</Style>
```

**Avalonia（容器查询）：**

```xml
<Border Container.Name="main" Container.Sizing="Width">
    <Border.Styles>
        <Style Selector="UniformGrid#cards">
            <Setter Property="Columns" Value="3"/>
        </Style>
        <ContainerQuery Name="main" Query="max-width:600">
            <Style Selector="UniformGrid#cards">
                <Setter Property="Columns" Value="1"/>
            </Style>
        </ContainerQuery>
    </Border.Styles>

    <UniformGrid x:Name="cards">
        <!-- content -->
    </UniformGrid>
</Border>
```

容器查询省去了转换器和 `RelativeSource` 绑定，还能一次圈定多个属性，并把宽度与高度条件组合起来。完整语法见[容器查询](/docs/styling/container-queries)，构建自适应界面的思路见[响应式布局](/docs/layout/responsive-layouts)。

### 从 EventTrigger 到伪类上的动画 {#eventtrigger-to-animations-on-pseudo-classes}

WPF 的 `EventTrigger` 元素会因路由事件而启动动画。在 Avalonia 中，动画定义在样式里，由伪类或样式类来激活。

**WPF:**

```xml
<Style TargetType="Border">
    <Style.Triggers>
        <EventTrigger RoutedEvent="MouseEnter">
            <BeginStoryboard>
                <Storyboard>
                    <DoubleAnimation Storyboard.TargetProperty="Opacity"
                                     To="1" Duration="0:0:0.3"/>
                </Storyboard>
            </BeginStoryboard>
        </EventTrigger>
    </Style.Triggers>
</Style>
```

**Avalonia:**

```xml
<Style Selector="Border">
    <Setter Property="Opacity" Value="0.5"/>
    <Setter Property="Transitions">
        <Transitions>
            <DoubleTransition Property="Opacity" Duration="0:0:0.3"/>
        </Transitions>
    </Setter>
</Style>
<Style Selector="Border:pointerover">
    <Setter Property="Opacity" Value="1"/>
</Style>
```

Avalonia 用的是 `Transitions` 机制：你声明哪些属性需要动起来以及时长，当属性值因样式或伪类变化而改变时，动画便自动触发。

## ControlTheme 与隐式样式 {#controltheme-vs-implicit-styles}

在 WPF 中，隐式样式（有 `TargetType` 但没有 `x:Key` 的 `Style`）定义了控件的默认外观，其中也包括 `ControlTemplate`。在 Avalonia 中，担此重任的是 [`ControlTheme`](/api/avalonia/styling/controltheme)。

`ControlTheme` 是编写「无外观」控件模板的手段。它存放在 `Resources` 字典中（而非 `Styles` 集合里），按类型查找。

**WPF（带模板的隐式样式）：**

```xml
<Style TargetType="Button">
    <Setter Property="Template">
        <Setter.Value>
            <ControlTemplate TargetType="Button">
                <Border Background="{TemplateBinding Background}"
                        CornerRadius="4"
                        Padding="{TemplateBinding Padding}">
                    <ContentPresenter HorizontalAlignment="Center"
                                      VerticalAlignment="Center"/>
                </Border>
            </ControlTemplate>
        </Setter.Value>
    </Setter>
</Style>
```

**Avalonia (ControlTheme):**

```xml
<ControlTheme x:Key="{x:Type Button}" TargetType="Button">
    <Setter Property="Template">
        <ControlTemplate>
            <Border Background="{TemplateBinding Background}"
                    CornerRadius="4"
                    Padding="{TemplateBinding Padding}">
                <ContentPresenter HorizontalAlignment="Center"
                                  VerticalAlignment="Center"/>
            </Border>
        </ControlTemplate>
    </Setter>

    <Style Selector="^:pointerover">
        <Setter Property="Background" Value="LightBlue"/>
    </Style>
    <Style Selector="^:pressed">
        <Setter Property="Background" Value="DarkBlue"/>
    </Style>
</ControlTheme>
```

关于 `ControlTheme` 的要点：

- 它放在 `Resources` 里，而不是 `Styles` 中。
- 键通常就是 `{x:Type ControlType}`，于是它会自动应用到该类型的所有实例上。
- `ControlTheme` 内部的嵌套样式用 `^` 选择器指代被模板化的控件本身。
- 与类 CSS 的 `Style` 不同，`ControlTheme` **不会**层叠：同一时刻一个控件只会应用一个 `ControlTheme`。

更多细节请见[控件主题](/docs/styling/control-themes)。

## TemplateBinding

WPF 和 Avalonia 都支持用 `TemplateBinding` 把模板内的元素接到被模板化控件的属性上。不过有一处重要区别：

| 方面 | WPF | Avalonia |
|---|---|---|
| 绑定方向 | 默认双向 | **仅单向** |
| 想要双向怎么办 | 无需额外处理 | 改用普通的 `Binding` 配 `RelativeSource={RelativeSource TemplatedParent}` |

若你在 Avalonia 的控件模板里需要双向绑定，请把：

```xml
<!-- OneWay only in Avalonia -->
<TextBox Text="{TemplateBinding SearchText}"/>
```

换成：

```xml
<!-- Two-way binding in a template -->
<TextBox Text="{Binding SearchText, RelativeSource={RelativeSource TemplatedParent}, Mode=TwoWay}"/>
```

## 另请参阅 {#see-also}

- [Styles](/docs/styling/styles)
- [Control Themes](/docs/styling/control-themes)
- [Pseudo-Classes](/docs/styling/pseudoclasses)
- [Style Selectors](/docs/styling/style-selectors)
- [容器查询](/docs/styling/container-queries)：基于尺寸的样式，用来替代 WPF 中对 ActualWidth/ActualHeight 使用 DataTrigger 的套路。
- [响应式布局](/docs/layout/responsive-layouts)：用容器查询和自动重排面板搭出自适应布局。

---
id: container-queries
title: 容器查询
---

容器查询让样式能依据某个充当容器的祖先元素的尺寸，对控件生效。

:::tip
Avalonia 的容器查询与 CSS 的容器查询相仿，只是功能有所收敛，以贴合 Avalonia 支持的平台和设备形态。若把 `TopLevel` 设为容器，它们也能起到媒体查询的作用。
:::

## 运作原理 {#how-it-works}

容器查询要求某个祖先控件被设为容器。容器尺寸一变，就按查询条件激活相应样式。查询可以判断容器的宽度、高度，或两者兼顾。任何控件都能当容器，但被设为容器的控件不会受到挂在它身上的容器查询中那些样式的影响。查询一旦激活，其中所有样式也会按各自的选择器相应生效。

## 查询怎么用 {#how-to-use-queries}

### 声明容器查询 {#declaring-container-queries}
在 XAML 中，容器查询可以写成控件 `Styles` 属性的直接子元素，像这样：

```xml
<StackPanel Orientation="Horizontal">
  <StackPanel.Styles>
    <ContainerQuery Name="container"
                    Query="max-width:400">
      <Style Selector="Button">
        <Setter Property="Background"
                Value="Red"/>
      </Style>
    </ContainerQuery>
  </StackPanel.Styles>
</StackPanel>
```

它们也可以是 `ControlTheme` 中样式的一部分：

```xml
<ControlTheme x:Key="{x:Type ListBox}" TargetType="ListBox">
    ...
  <Setter Property="Template">
    <ControlTemplate>
      <Border Name="border"
              Container.Name="Test"
              Container.Sizing="WidthAndHeight"
              >
        <ScrollViewer Name="PART_ScrollViewer">
            ...
        </ScrollViewer>
      </Border>
    </ControlTemplate>
  </Setter>


  <ContainerQuery Name="Test"
                  Query="max-height:400">
    <Style Selector="ScrollViewer#PART_ScrollViewer">
      <Setter Property="Background"
              Value="Red"/>
    </Style>
  </ContainerQuery>
</ControlTheme>
```
`Name` 属性指明它要挂到哪个名字的容器上。这并非唯一标识符，多个容器查询可以用同一个名字。
`Query` 则定义了激活所需的尺寸条件，见下文的[查询条件](#queries)。

这使得它们很适合用来做面向不同屏幕尺寸的主题，或者依父级可用空间而变换形态的主题。不过也有几条限制。

1. 容器查询不能放在 `Style` 元素里。
   下面的写法是非法的。

```xml
<StackPanel Orientation="Horizontal">
  <StackPanel.Styles>
    <Style Selector="...">
      <ContainerQuery Name="container"
                      Query="max-width:400">
        <Style Selector="Button">
          <Setter Property="Background"
                  Value="Red"/>
        </Style>
      </ContainerQuery>
    </Style>
  </StackPanel.Styles>
</StackPanel>
```

2. 声明在 `ContainerQuery` 中的样式无法影响容器本身及其祖先。这一点与普通 `Styles` 可以影响父控件不同。因为容器查询依赖容器的实际尺寸，若容器反过来被自家查询激活的样式所影响，就可能出现两个及以上查询不停改写容器尺寸的循环。

### 声明容器 {#declaring-containers}
只有当 `ContainerQuery` 宿主的某个后代控件被声明为容器时，容器查询才会起作用。给任意控件设置 `Container.Name` 和 `Container.Sizing` 附加属性，即可把它声明为容器，像这样：

```xml
<Button
  Container.Name="container-name"
  Container.Sizing="container-sizing"
/>
```

`Container.Name` 指定容器的名字。它并非该容器独有，同一作用域内的多个控件可以用同一个容器名，它们会一并受同一批容器查询的影响。

`Container.Sizing` 指定该容器在查询时采用的尺寸策略。容器的最终尺寸取决于它的取值。这是一个枚举，取值如下：

* `Normal`：不查询容器尺寸。这是默认值，控件照常进行测量和排列。
* `Width`：查询容器的宽度。容器会取父级允许的最大宽度，相关容器查询都用这个值。多数情况下，最终宽度就是允许的最大宽度。
* `Height`：与 `Width` 相同，只不过查询的是容器的高度。
* `WidthAndHeight`：容器的宽度和高度都参与查询。

视尺寸策略而定，容器会把可用的最大尺寸当作自己的期望尺寸。

### Queries
可用的查询条件如下。

* `min-width`：等同于 `x >= width`
* `min-height`：等同于 `x >= height`
* `max-width`：等同于 `x <= width`
* `max-height`：等同于 `x <= height`
* `height`：等同于 `x == height`
* `width`：等同于 `x == width`

下面这个例子演示了多个容器查询各用不同条件的写法：

```xml
<ContainerQuery Name="uniformGrid"
                Query="max-width:400">
  <Style Selector="UniformGrid#ContentGrid">
    <Setter Property="Columns"
            Value="1"/>
  </Style>
</ContainerQuery>
<ContainerQuery Name="uniformGrid"
                Query="min-width:400">
  <Style Selector="UniformGrid#ContentGrid">
    <Setter Property="Columns"
            Value="2"/>
  </Style>
</ContainerQuery>
<ContainerQuery Name="uniformGrid"
                Query="min-width:800">
  <Style Selector="UniformGrid#ContentGrid">
    <Setter Property="Columns"
            Value="3"/>
  </Style>
</ContainerQuery>
```
多个条件可以用 `,` 做「或」组合，或用 `and` 做「与」组合。

```xml
<ContainerQuery Name="uniformGrid"
                Query="max-width:400,min-width:300">
  <Style Selector="UniformGrid#ContentGrid">
    <Setter Property="Columns"
            Value="1"/>
  </Style>
</ContainerQuery>
<ContainerQuery Name="uniformGrid"
                Query="min-width:400 and min-width:300">
  <Style Selector="UniformGrid#ContentGrid">
    <Setter Property="Columns"
            Value="2"/>
  </Style>
</ContainerQuery>
```

这样你就能针对某个尺寸区间来写查询了。

## 另请参阅 {#see-also}

- [响应式布局](/docs/layout/responsive-layouts)：用容器查询搭建自适应布局。
- [如何构建响应式布局](/docs/how-to/responsive-layout-how-to)：常见响应式套路的分步实践。
- [Styles](/docs/styling/styles)
- [控件主题](/docs/styling/control-themes)

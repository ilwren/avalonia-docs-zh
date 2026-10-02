---
id: style-selector-syntax
title: 样式选择器语法
---

本页列出样式选择器的 XAML 语法，以及实现同样选取效果的 C# 代码方法。

## 按控件类 {#by-control-class}

```xml
<Style Selector="Button">
<Style Selector="local|Button">
```

```csharp title='C#'
new Style(x => x.OfType<Button>());
new Style(x => x.OfType(typeof(Button)));
```

按类名选取控件。

上面第一个例子选取的是 `Avalonia.Controls.Button` 类。若要在类型中带上 XAML 命名空间，请用 `|` 字符分隔命名空间与类型。

:::caution
该选择器不匹配派生类型。若需要匹配派生类型，请用 [`:is` 选择器](#include-derived-classes)。
:::

:::info
对象的类型由其 `StyleKey` 属性决定。该属性默认返回当前实例的类型；若你希望自己继承自 `Button` 的控件按 `Button` 来套样式，可以在类中重写 `StyleKeyOverride` 属性，让它返回 `typeof(Button)`。
:::

## 按名称 {#by-name}

```xml
<Style Selector="#myButton">
<Style Selector="Button#myButton">
```

```csharp title='C#'
new Style(x => x.Name("myButton"));
new Style(x => x.OfType<Button>().Name("myButton"));
```

按控件的 `Name` 特性选取，前面加上一个 `#`（井号）。

## 按样式类 {#by-style-class}

```xml
<Style Selector="Button.large">
<Style Selector="Button.large.red">
```

```csharp title='C#'
new Style(x => x.OfType<Button>().Class("large"));
new Style(x => x.OfType<Button>().Class("large").Class("red"));
```

选取带有指定样式类的控件。多个类之间用句点分隔。若选择器中写了多个类，控件必须全部具备才算匹配。

## 按伪类 {#by-pseudoclass}

```xml
<Style Selector="Button:focus">
<Style Selector="Button:focus:pointerover">
<Style Selector="Button.large:focus">
```

```csharp title='C#'
new Style(x => x.OfType<Button>().Class(":focus"));
new Style(x => x.OfType<Button>().Class(":focus").Class(":pointerover"));
new Style(x => x.OfType<Button>().Class("large").Class(":focus"));
```

按控件当前的伪类选取。选择器中冒号标志着伪类名的开始。同一个控件上可以同时有多个伪类。

:::info
关于伪类的更多细节，请见[伪类](/docs/styling/pseudoclasses)。
:::

## 连派生类一起匹配 {#include-derived-classes}

```xml
<Style Selector=":is(Button)">
<Style Selector=":is(local|Button)">
```

```csharp title='C#'
new Style(x => x.Is<Button>());
new Style(x => x.Is(typeof(Button)));
```

它与样式类选择器非常相似，只是还会匹配派生类型。

:::info
匹配过程中，Avalonia 通过查看控件的 `StyleKey` 属性来判定其类型。
:::

这让你能写出非常宽泛的、基于类的选择器。由于所有控件都派生自 `Control` 类，只按样式类 `margin2` 选取的选择器可以这样写：

```xml
<Style Selector=":is(Control).margin2">
<Style Selector=":is(local|Control).margin2">
```

```csharp title='C#'
new Style(x => x.Is<Control>().Class("margin2"));
new Style(x => x.Is(typeof(Control)).Class("margin2"));
```

## 子级运算符 {#child-operator}

```xml
<Style Selector="StackPanel > Button">
```

```csharp title='C#'
new Style(x => x.OfType<StackPanel>().Child().OfType<Button>());
```

用 `>` 字符分隔两个选择器即构成子级选择器。它只匹配**逻辑控件树**中的直接子级。

:::info
关于逻辑控件树背后的概念，请见[控件树](/docs/custom-controls/control-trees)。
:::

举例来说，把上面那个选择器用在这段 XAML 上：

```xml
<StackPanel>
   <Button>Save</Button>
   <DockPanel Width="300" Height="300">
       <Button DockPanel.Dock="Top">Top</Button>
       <TextBlock>Some text</TextBlock>
   </DockPanel>
</StackPanel>
```

该选择器会匹配第一个按钮，而不会匹配第二个。因为第二个按钮并不是 StackPanel 的直接子级（它还隔着一层 DockPanel）。

## 任意后代运算符 {#any-descendant-operator}

```xml
<Style Selector="StackPanel Button">
```

```csharp title='C#'
new Style(x => x.OfType<StackPanel>().Descendant().OfType<Button>());
```

两个选择器之间用空格分隔时，它会匹配逻辑树中的任意后代。左边是父级，右边是后代。

所以把上面的选择器用在前面那段 XAML 上，两个按钮都会被选中。

## 按属性匹配 {#by-property-match}

```xml
<Style Selector="Button[IsDefault=true]">
```

```csharp title='C#'
new Style(x => x.OfType<Button>().PropertyEquals(Button.IsDefaultProperty, true));
```

你可以在选择器中加上属性值做进一步限定。属性=值这一对写在方括号里，它会匹配所有指定属性为指定值的控件。

```xml
<StackPanel Orientation="Horizontal">
   <Button IsDefault="True">Save</Button>
   <Button>Cancel</Button>   
</StackPanel>
```

例如在上面那段 XAML 中，第一个按钮会被选中，第二个则不会。

:::info
注意：用附加属性做属性匹配时，属性名必须用圆括号括起来。例如：

```xml
<Style Selector="TextBlock[(Grid.Row)=0]">
```
:::

:::info
使用属性匹配时，属性类型必须支持组件模型的类型转换器，即 `TypeConverter` 类。更多信息请见[微软的 TypeConverter 文档](https://learn.microsoft.com/dotnet/api/system.componentmodel.typeconverter)。
:::

## 按模板 {#by-template}

```xml
<Style Selector="Button /template/ ContentPresenter">
```

```csharp title='C#'
new Style(x => x.OfType<Button>().Template().OfType<ContentPresenter>());
```

上面这种语法用于选取控件模板中的控件。在这个例子里，选择器匹配的是位于 `Button` 模板内的 [`ContentPresenter`](/api/avalonia/controls/presenters/contentpresenter) 控件。

这个选择器与众不同：它能钻进模板里选取，而本页介绍的其他选择器都只作用于逻辑树。

## Not 函数 {#not-function}

```xml
<Style Selector="TextBlock:not(.h1)">
```

```csharp title='C#'
new Style(x => x.OfType<TextBlock>().Not(y => y.Class("h1")));
```

该函数把括号里的选取结果取反。上面的例子会匹配所有**不**带 `h1` 类的 TextBlock 控件。

## 按列表 {#by-list}

```xml
<Style Selector="TextBlock, Button">
```

```csharp title='C#'
new Style(x => Selectors.Or(x.OfType<TextBlock>(), x.OfType<Button>()))
```

你可以用逗号分隔的选择器列表来选取任意匹配项。样式中的 setter 只能改动这些项共有的属性。 

## 按子级位置公式 {#by-child-position-formula}

```xml
<Style Selector="TextBlock:nth-child(2n+3)">
```

```csharp title='C#'
new Style(x => x.OfType<TextBlock>().NthChild(2, 3));
```

你可以按元素在同级中所处的位置来匹配，这与父级（容器）控件是什么类无关。

选取依据是一个形如 `An + B` 的简单公式：其中 **`A`** 控制步长，**`B`** 是相对起点的偏移。在上面的 nth-child 公式里，**`n`** 依次取 0 以及从 0 开始的所有正整数，再把公式结果与子元素从 1 开始计数的位置相比较来判定匹配。

所以，对上面那个选择器而言：

<table><thead><tr><th width="175">Child = 1</th><th width="184">Child = 2</th><th width="201">Child = 3</th><th>Child = 4</th></tr></thead><tbody><tr><td>n=0、n=1</td><td>n=0、n=1</td><td>n=0、n=1</td><td>n=0、n=1</td></tr><tr><td>3, 5</td><td>3, 5</td><td><strong>3</strong>, 5</td><td>3, 5</td></tr><tr><td>No Match</td><td>No Match</td><td>Match</td><td>No Match</td></tr></tbody></table>

若公式算出来小于 1，则忽略——根本不存在那个序号的子元素。

另有一个对应的选择器，其公式从同级的末尾开始数：

```xml
<Style Selector="TextBlock:nth-last-child(2n+3)">
```

```csharp title='C#'
new Style(x => x.OfType<TextBlock>().NthLastChild(2, 3));
```

### 单一子级位置 {#single-child-position}

在 XAML 中，你可以省去公式里的 **A** 和 **n**，只指定一个位置。比如下面这条只选取第 3 个子级：

```xml
<Style Selector="TextBlock:nth-child(3)">
```

```csharp title='C#'
new Style(x => x.OfType<TextBlock>().NthChild(0, 3));
```

### 关键字写法 {#keyword-notation}

你也可以用关键字写法代替公式：`odd` 或 `even`。所以下面这些选择器是等价的：

```xml
<Style Selector="TextBlock:nth-child(2n)">
<Style Selector="TextBlock:nth-child(even)">
```

```xml
<Style Selector="TextBlock:nth-child(2n+1)">
<Style Selector="TextBlock:nth-child(odd)">
```

### 其他公式示例 {#other-formula-examples}

下表列出若干按子级位置选取的例子：

| Formula Example    | 含义                                                                                                                                                                                                  |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `:nth-child(odd)`  | 奇数位元素：**1**、**3**、**5**，以此类推。                                                                                                                                                                     |
| `:nth-child(even)` | 偶数位元素：**2**、**4**、**6**，以此类推。                                                                                                                                                                    |
| `:nth-child(2n+1)` | 奇数位元素：**1**_(2×0+1)_、**3**_(2×1+1)_、**5**_(2×2+1)_，以此类推。等同于 `:nth-child(odd)`                                                                                                          |
| `:nth-child(2n)`   | 偶数位元素：**2**_(2×1)_、**4**_(2×2)_、**6**_(2×3)_，以此类推。等同于 `:nth-child(even)`。注意 **0**_(2×0)_ 虽然是合法写法，但因序号从 1 起算，它匹配不到任何元素。 |
| `:nth-child(7)`    | 第 7 个元素                                                                                                                                                                                                 |
| `:nth-child(n+7)`  | 从第 7 个起的每一个元素：**7**_(0+7)_、**8**_(1+7)_、**9**_(2+7)_，以此类推                                                                                                                                     |
| `:nth-child(3n+4)` | 从第 4 个起每隔 3 个取一个：**4**_(3×0+4)_、**7**_(3×1+4)_、**10**_(3×2+4)_、**13**_(3×3+4)_，以此类推                                                                                                         |
| `:nth-child(-n+3)` | 前 3 个元素：**3**_(-1×0+3)_、**2**_(-1×1+3)_、**1**_(-1×2+3)_。再往后算出的序号都小于 1，匹配不到任何元素。                                                              |

### 在线的子级位置测试器 {#online-child-position-tester}

虽然这是个讲 CSS 的网站，但由于规则相同，它对 Avalonia 的子级位置选择器同样适用。

:::info
你可以用这个网站测试自己的子级位置选择器：\
[https://css-tricks.com/examples/nth-child-tester/](https://css-tricks.com/examples/nth-child-tester/)
:::

## Nesting

```xml
<Style Selector="TextBlock">
    <Setter Property="FontSize" Value="24"/>
    
    <!-- Effectively "TextBlock:pointerover" -->
    <Style Selector="^:pointerover">
        <Setter Property="FontWeight" Value="Bold"/>
    </Style>
</Style>
```

```csharp title='C#'
new Style(x => x.OfType<TextBlock>())
{
    Setters = { new Setter(TextBlock.FontSizeProperty, 24d) },
    Children =
    {
        new Style(x => x.Nesting().Class(":pointerover"))
        {
            Setters = { new Setter(TextBlock.FontWeightProperty, FontWeight.Bold) }
        }
    }
};
```

## 另请参阅 {#see-also}

- [样式选择器](/docs/styling/style-selectors)
- [Pseudoclasses](/docs/styling/pseudoclasses)
- [Styles](/docs/styling/styles)

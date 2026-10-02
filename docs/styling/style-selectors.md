---
id: style-selectors
title: 样式选择器
description: 了解 Avalonia 的样式选择器如何用类 CSS 语法按类型、类、名称和状态匹配控件。
doc-type: explanation
---

Avalonia 用样式选择器来匹配控件，其 XAML 语法自成一套，与 CSS（层叠样式表）颇为相似。选择器决定一个样式作用于哪些控件。

## 选择器速查 {#selector-quick-reference}

| 选择器 | 说明 |
|---|---|
| [`Button`](/api/avalonia/controls/button) | 选取所有 `Button` 控件。 |
| `Button.red` | 选取所有带 `red` 样式类的 `Button` 控件。 |
| `Button.red.large` | 选取同时带 `red` 和 `large` 两个样式类的所有 `Button` 控件。 |
| `Button:focus` | 选取所有激活了 `:focus` 伪类的 `Button` 控件。 |
| `Button.red:focus` | 选取带 `red` 类且处于 `:focus` 伪类状态的所有 `Button` 控件。 |
| `Button#myButton` | 选取 `Name="myButton"` 的那个 `Button`。 |
| `StackPanel Button.xl` | 选取作为 `StackPanel` 后代（任意层级）的 `Button.xl` 控件。 |
| `StackPanel > Button.xl` | 选取作为 `StackPanel` 直接子级的 `Button.xl` 控件。 |
| `Button /template/ ContentPresenter` | 选取 `Button` 控件模板内部的某个指定控件（本例中是 [`ContentPresenter`](/api/avalonia/controls/presenters/contentpresenter)）。 |
| `:is(Button)` | 选取类型为 `Button` 或派生自 `Button` 的控件。 |
| `:not(Button.red)` | 选取不匹配 `Button.red` 的控件。 |
| `Button:nth-child(2n+1)` | 在同级中选取排在奇数位的 `Button` 控件。 |

## 选择器的运作方式 {#how-selectors-work}

样式选择器写在 `Style` 的 `Selector` 特性上：

```xml
<Style Selector="Button.primary:pointerover">
    <Setter Property="Background" Value="DarkBlue" />
</Style>
```

这条选择器圈定的是：带 `primary` 样式类、且指针正悬停其上的所有 `Button` 控件。各个部分自左向右依次组合：

1. `Button` 匹配控件类型
2. `.primary` 匹配样式类
3. `:pointerover` 匹配伪类（状态）

## 选择器的具体程度 {#selector-specificity}

当多个样式匹配同一个控件时，更具体的选择器胜出。具体程度按下列优先顺序判定：

1. 名称选择器（`#name`）最具体
2. 属性与伪类选择器（`:pointerover`、`[IsEnabled=True]`）
3. 样式类选择器（`.primary`）
4. 类型选择器（`Button`）
5. 后代/子级组合符按在树中的位置来裁定

若两个选择器具体程度相同，则写在后面的那个胜出。

## 完整参考 {#full-reference}

所有选择器格式、运算符和组合符的完整说明，请见[样式选择器语法](/docs/styling/style-selector-syntax)参考。

## 另请参阅 {#see-also}

- [样式选择器语法](/docs/styling/style-selector-syntax)
- [Styles](/docs/styling/styles)
- [样式类](/docs/styling/style-classes)
- [Pseudoclasses](/docs/styling/pseudoclasses)

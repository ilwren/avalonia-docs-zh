---
id: avalonia-xaml
title: Avalonia XAML
description: 学习用于定义 Avalonia 用户界面的 XAML 标记语言。
doc-type: explanation
video:
  src: https://youtu.be/kDYULQBg8rI
  title: 吃透 Avalonia XAML —— 命名空间、绑定与代码隐藏
---

Avalonia 用 XAML 来定义用户界面。XAML 是一种基于 XML 的标记语言，很多 UI 框架都在用它。

XAML 虽然是定义 Avalonia 界面最主流的方式，但并非必选项 —— 你完全可以用 C#、F# 或任何 .NET 语言开发 Avalonia 应用。

:::tip
不用 XAML 构建应用的完整指南，请见[纯代码构建界面](/docs/fundamentals/coded-ui)。
:::

:::info
XAML 最初由微软为 WPF 开发，后来被 Silverlight、UWP 等框架沿用。Avalonia 继承了同样的核心概念（声明式标记、对象元素、属性特性、数据绑定、标记扩展），只是换了自己的命名空间和控件库。如果你有 WPF 或 UWP XAML 的底子，这些经验基本可以直接迁移过来。
:::

## AXAML 文件扩展名 {#axaml-file-extension}

XAML 文件在别处的扩展名是 `.xaml`，但由于与 Visual Studio 集成时存在技术问题，Avalonia 启用了自己的 `.axaml` 扩展名 —— 即 “Avalonia XAML”。

## 文件格式 {#file-format}

一个典型的 Avalonia XAML 文件长这样：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        x:Class="AvaloniaApplication1.MainWindow">
</Window>
```

和所有 XML 文件一样，它有一个根元素。根元素标签 `<Window></Window>` 决定了根的类型，这个类型对应某个 Avalonia 控件 —— 上例中就是一个窗口。

上面的示例用到了三个值得一提的特性：

* `xmlns="https://github.com/avaloniaui"` —— Avalonia 自身的 XAML 命名空间声明。这一行必不可少，缺了它文件就不会被识别为 Avalonia XAML 文档。
* `xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"` —— XAML 语言命名空间的声明。
* `x:Class="AvaloniaApplication1.MainWindow"` —— 上述 'x' 声明的扩展，用于告诉 XAML 编译器到哪里找本文件对应的类。该类定义在代码隐藏文件中，通常用 C# 编写。

:::info
关于代码隐藏的概念，请见[代码隐藏](/docs/fundamentals/code-behind)。
:::

## 控件元素 {#control-elements}

往文件里添加代表 Avalonia 控件的 XML 元素，就能拼出应用界面。元素标签名与控件类名完全一致。

:::info
一个界面可以由多种控件组合而成。关于界面组合的概念，详见[界面组合](/docs/fundamentals/ui-composition)。
:::

例如，下面这段 XAML 往窗口内容里放了一个按钮：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <Button>Hello World!</Button>
</Window>
```

:::info
Avalonia 内置控件的完整清单，请见[控件参考](/controls)。
:::

## 控件特性 {#control-attributes}

代表控件的 XML 元素带有一组特性，对应可设置的控件属性。给元素添加一个特性，就等于设置了对应的控件属性。

比如要把按钮背景设成蓝色，加上 `Background` 特性并把值设为 `"Blue"` 即可：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <Button Background="Blue">Hello World!</Button>
</Window>
```

## 控件内容 {#control-content}

你可能注意到了，上例中按钮的内容（'Hello World' 这串文字）是写在开始标签和结束标签之间的。作为替代，也可以直接设置 content 特性：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <Button Content="Hello World!"/>
</Window>
```

这种写法是 Avalonia 控件内容的专属特性。

## 数据绑定 {#data-binding}

你会经常用 Avalonia 的绑定系统，把控件属性和底层对象关联起来。这层关联通过 `{Binding}` 标记扩展声明，例如：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <Button Content="{Binding Greeting}"/>
</Window>
```

:::info
关于数据绑定背后的概念，详见[数据绑定入门](/docs/data-binding/introduction-to-data-binding)。
:::

## 代码隐藏文件 {#code-behind-files}

许多 Avalonia XAML 文件还配有一个代码隐藏文件，通常用 C# 编写，扩展名为 `.axaml.cs`。

:::info
用代码隐藏文件编程的具体指引，请见[代码隐藏](/docs/fundamentals/code-behind)。
:::

## XML 命名空间 {#xml-namespaces}

和任何 XML 格式一样，Avalonia XAML 文件中也可以声明命名空间。XML 命名空间把元素名、特性名与特定 URI 绑定，既避免了命名冲突，也让 XAML 处理器知道去哪里找元素的定义。声明命名空间用 `xmlns` 特性，前缀可选。命名空间声明会从父元素继承到子元素，作用范围从声明处起直到所在元素结束。

用 `xmlns` 特性即可添加命名空间，声明格式如下：

```xml
xmlns:alias="definition"
```

惯例是把要用到的命名空间统统写在根元素上。

一个文件中只能有一个命名空间省略别名部分，其余别名在文件内必须唯一。

命名空间声明的定义部分既可以是一个 URL，也可以是一段代码定义 —— 两者都用于定位文件中各元素的定义。

:::info
关于命名空间声明工作机制的详细说明，请见[自定义控件库](/docs/custom-controls/custom-control-library)。
:::

引用代码时，XAML 命名空间特性的定义部分有两种合法写法：

### using 前缀 {#using-prefix}

无论命名空间位于当前程序集还是被引用的程序集，都可以用 `using:` 前缀为其起别名，两种情况语法一致。例如：

```xml
xmlns:myAlias1="using:AppNameSpace.MyNamespace"
```
### CLR 命名空间前缀 {#clr-namespace-prefix}

Avalonia 同样支持与 WPF 一致的 `clr-namespace:` 前缀。不过它的语法取决于目标命名空间是在当前程序集还是被引用的程序集中。

例如，当命名空间与 XAML 处在同一个程序集时，可以这样写：

```xml
<Window ...
    xmlns:myAlias1="clr-namespace:AppNameSpace.MyNamespace" 
... >
```

如果命名空间位于另一个被引用的程序集（比如某个库）中，就必须补上该程序集的名称：

```xml
<Window ...
    xmlns:myAlias2="clr-namespace:OtherAssembly.MyNameSpace;assembly=OtherAssembly"
 ... >
```

## 另请参阅 {#see-also}

- [纯代码构建界面](/docs/fundamentals/coded-ui)
- [Code-behind](/docs/fundamentals/code-behind)
- [界面组合](/docs/fundamentals/ui-composition)
- [数据绑定入门](/docs/data-binding/introduction-to-data-binding)

---
id: namespaces
title: XAML 命名空间
---

XAML 命名空间告诉 XAML 引擎：到哪里去找你标记里引用的那些类型。每个 Avalonia XAML 文件都至少需要一条命名空间声明才能工作。

## 默认命名空间 {#default-namespaces}

典型的 Avalonia XAML 文件开头会有两条命名空间声明：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
</Window>
```

| 声明 | 用途 |
|---|---|
| `xmlns="https://github.com/avaloniaui"` | Avalonia 的默认命名空间，映射到所有核心 Avalonia CLR 命名空间（`Avalonia`、`Avalonia.Controls`、`Avalonia.Media`、`Avalonia.Animation` 等）。每个 Avalonia XAML 文件都必须有它。 |
| `xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"` | XAML 语言命名空间，提供 `x:Name`、`x:Key`、`x:Class` 等 [x: 指令](/docs/xaml/directives)。 |

## 映射到 Avalonia 默认命名空间的 CLR 命名空间 {#clr-namespaces-mapped-to-the-default-avalonia-namespace}

`https://github.com/avaloniaui` 这个 URI 映射到 Avalonia 各程序集中的许多 CLR 命名空间，其中最常用的有：

- `Avalonia`（基础类型）
- `Avalonia.Controls`（全部标准控件）
- `Avalonia.Controls.Primitives`
- `Avalonia.Controls.Shapes`
- `Avalonia.Controls.Presenters`
- `Avalonia.Controls.Templates`
- `Avalonia.Controls.Documents`
- `Avalonia.Controls.Notifications`
- `Avalonia.Animation`
- `Avalonia.Animation.Easings`
- `Avalonia.Data`（绑定相关类型）
- `Avalonia.Media`（画刷、变换、几何图形）
- `Avalonia.Layout`
- `Avalonia.Styling`
- `Avalonia.Markup.Xaml.MarkupExtensions`
- `Avalonia.Markup.Xaml.Styling`
- `Avalonia.Markup.Xaml.Templates`

## 引用你自己的类型 {#referencing-your-own-types}

要在 XAML 中使用自己写的类，需要声明一个映射到相应 CLR 命名空间的前缀。

### 使用 `using:` 前缀 {#using-the-using-prefix}

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:vm="using:MyApp.ViewModels"
        xmlns:controls="using:MyApp.Controls">

    <controls:MyCustomControl DataContext="{x:Static vm:DesignData.MainViewModel}" />
</Window>
```

`using:` 前缀既适用于当前程序集中的命名空间，也适用于任何被引用程序集中的命名空间。推荐用这种写法。

### 使用 `clr-namespace:` 前缀 {#using-the-clr-namespace-prefix}

WPF 用户熟悉的 `clr-namespace:` 前缀同样受支持：

**同一程序集：**
```xml
xmlns:local="clr-namespace:MyApp.Controls"
```

**不同程序集：**
```xml
xmlns:ext="clr-namespace:ThirdParty.Controls;assembly=ThirdParty.Controls"
```

:::tip
比起 `clr-namespace:`，更推荐 `using:`。`using:` 写法更短，引用其他程序集时也不必再写 `;assembly=` 后缀。
:::

## 自定义 XML 命名空间映射 {#defining-custom-xml-namespace-mappings}

类库作者可以用 `XmlnsDefinition` 程序集特性，把多个 CLR 命名空间映射到同一个 XML 命名空间 URI：

```csharp
// In your library's AssemblyInfo.cs or a Properties file
[assembly: XmlnsDefinition("https://mycompany.com/mylib", "MyLib.Controls")]
[assembly: XmlnsDefinition("https://mycompany.com/mylib", "MyLib.Converters")]
[assembly: XmlnsDefinition("https://mycompany.com/mylib", "MyLib.Panels")]
```

这样类库的使用者只需一条命名空间声明：

```xml
<Window xmlns:mylib="https://mycompany.com/mylib">
    <mylib:FancyButton />
</Window>
```

## 约定俗成的常用命名空间前缀 {#common-namespace-prefixes-by-convention}

下面这些前缀在各个 Avalonia 项目中都很常见：

| 前缀 | Typical Mapping |
|---|---|
| `x` | XAML 语言命名空间 |
| `d` | `http://schemas.microsoft.com/expression/blend/2008` (design-time) |
| `mc` | `http://schemas.openxmlformats.org/markup-compatibility/2006` |
| `local` | 应用的根命名空间 |
| `vm` | ViewModels 命名空间 |
| `conv` | Converters 命名空间 |

### 设计时命名空间 {#design-time-namespaces}

`d:` 和 `mc:` 这两个命名空间用于启用设计时功能：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        mc:Ignorable="d"
        d:DesignWidth="800" d:DesignHeight="450">
</Window>
```

- `d:DesignWidth` 和 `d:DesignHeight` 设置 XAML 设计器中的预览尺寸。
- `d:DataContext` 设置设计时数据上下文，便于预览绑定效果。
- `mc:Ignorable="d"` 告诉运行时忽略所有 `d:` 特性。

## 另请参阅 {#see-also}

- [Avalonia XAML](/docs/fundamentals/avalonia-xaml)：XAML 基础与文件结构。
- [x: 指令](/docs/xaml/directives)：XAML 语言指令。
- [自定义控件库](/docs/custom-controls/custom-control-library)：如何在打包控件时带上命名空间映射。

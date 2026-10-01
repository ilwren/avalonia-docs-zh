---
id: including-assets
title: 资产
description: 在 Avalonia 应用中包含并引用位图、样式和资源字典等资产。
doc-type: reference
---

import AssetFileDiagram from '/img/concepts/ui-concepts/assets/asset-file.png';
import AssetLibraryDiagram from '/img/concepts/ui-concepts/assets/asset-library.png';

很多应用都需要带上位图、样式、资源字典之类的资产。资源字典里装的是可以用 XAML 声明的图形基本元素；样式同样能用 XAML 编写；而位图资产则是 PNG、JPEG 这类二进制文件。

## 把资产包含进来 {#including-assets}

<Image light={AssetFileDiagram} alt="Diagram showing how asset files are included in an Avalonia project" position="center" maxWidth={400} cornerRadius="true"/>

在项目文件中用 `<AvaloniaResource>` 元素即可把资产包含进应用。

举例来说，Avalonia .NET Core MVVM App 解决方案模板会创建一个名为 `Assets` 的文件夹（里面放着 `avalonia-logo.ico` 文件），并在项目文件中添加一个元素，把该目录下的所有文件都包含进来，就像这样：

```xml
<ItemGroup>
  <AvaloniaResource Include="Assets\**"/>
</ItemGroup>
```

在这个 item group 里继续添加 `<AvaloniaResource>` 元素，想包含什么文件都行。

:::tip
这里的元素名 `AvaloniaResource` 只是表示：构建时这些资产会以 .NET 资源的形式内嵌进去。但在 Avalonia 的语境里，我们把这些文件称作「资产（Assets）」，以便和「XAML 资源（resources）」区分开。
:::


### 引用已包含的资产 {#referencing-included-assets}

资产文件一旦包含进来，就可以在定义界面的 XAML 中按需引用。例如下面这些资产是用相对路径引用的：

```xml
<Image Source="icon.png"/>
<Image Source="images/icon.png"/>
<Image Source="../icon.png"/>
```

也可以改用以根目录开头的路径：

```xml
<Image Source="/Assets/icon.png"/>
```

## 来自类库的资产 {#library-assets}

<Image light={AssetLibraryDiagram} alt="Diagram showing how to reference assets from a library assembly" position="center" maxWidth={400} cornerRadius="true"/>

如果资产所在的程序集和 XAML 文件不是同一个，就要用 `avares:` URI 方案。比如资产位于名为 `MyAssembly.dll` 的程序集的 `Assets` 文件夹中，就写成：

```xml
<Image Source="avares://MyAssembly/Assets/icon.png"/>
```

### 资产的类型转换 {#asset-type-conversion}

Avalonia 内置了若干转换器，开箱即可把资产加载为位图、图标和字体。也就是说，一个资产 URI 可以自动转换成下列任意一种：

* Image —— `Image` 类型
* Bitmap —— `Bitmap` 类型
* 窗口图标 —— `WindowIcon` 类型
* 字体 —— `FontFamily` 类型

### 在代码中加载资产 {#loading-assets-in-code}

可以用 `AssetLoader` 静态类编写代码来加载资产。例如：

```csharp title='C#'
var bitmap = new Bitmap(AssetLoader.Open(new Uri(uri)));
```

上面代码中的 `uri` 变量，可以是任何采用 `avares:` 方案的合法 URI（即前文所述的那种）。

Avalonia 不支持 `file://`、`http://` 和 `https://` 这几种方案。要从磁盘或网络加载文件，得你自己实现，或者借助社区的实现。

:::info
社区实现的图片加载器可参考 [AsyncImageLoader.Avalonia](https://github.com/AvaloniaUtils/AsyncImageLoader.Avalonia)。
:::

## 另请参阅 {#see-also}

- [Avalonia XAML](/docs/fundamentals/avalonia-xaml)
- [界面组合](/docs/fundamentals/ui-composition)

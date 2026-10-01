---
id: custom-fonts
title: 自定义字体
---

Avalonia 支持自定义的 TrueType（`.ttf`）和 OpenType（`.otf`）字体。你可以把字体文件嵌进应用并在 XAML 中引用，从此不必仰仗宿主系统装了什么字体。

使用自定义字体有三条路子，各适用于不同场景：

| 办法 | 适用场景 |
|----------|----------|
| [静态资源](#static-resource-fonts) | 通过具名资源键，在特定位置使用某个字体 |
| [嵌入式字体集合](#embedded-font-collections) | 不用资源键，直接按字体族名引用 |
| [预制字体包](#pre-built-font-packages) | 在多个项目间共用同一个字体包 |

## 字体 URI 的格式 {#font-uri-format}

这三条路子都用同一种 URI 格式来定位嵌入的字体文件：

```text
avares://AssemblyName/Path/To/Fonts#Font Family Name
```

- `avares://AssemblyName/Path/To/Fonts` 是字体所在目录或文件的路径，采用 Avalonia 的资产协议。
- `#Font Family Name` 是字体的内部族名（不是文件名）。

:::caution
`#FontFamilyName` 后缀不可省略。少了它，Avalonia 无从判断该加载哪种字型，字体便会悄无声息地退回默认值。族名必须与字体的内部元数据名称一致，而不是磁盘上的文件名。
:::

要让字体文件在运行时可用，项目文件必须把它们作为 `AvaloniaResource` 引入：

```xml title="MyApp.csproj"
<AvaloniaResource Include="Assets\Fonts\*" />
```

## 静态资源字体 {#static-resource-fonts}

你可以把字体声明成 XAML 资源，再用 `StaticResource` 标记扩展按键引用。这条路子让你明确掌控字体用在哪儿。

在应用或窗口资源中定义该字体：

```xml title="App.axaml"
<Application.Resources>
    <FontFamily x:Key="NunitoFont">avares://MyApp/Assets/Fonts#Nunito</FontFamily>
</Application.Resources>
```

然后在任何带 `FontFamily` 属性的控件上引用它：

```xml
<TextBlock FontFamily="{StaticResource NunitoFont}"
           FontSize="24"
           Text="Hello in Nunito" />
```

:::caution
应用级资源牵涉资源字典合并，可能让字体定义悄悄失效。若你在 `<Application.Resources>` 中定义的字体没生效，请把该资源包进一层 `ResourceDictionary.MergedDictionaries` 结构：

```xml title="App.axaml"
<Application.Resources>
    <ResourceDictionary>
        <ResourceDictionary.MergedDictionaries>
            <ResourceDictionary>
                <FontFamily x:Key="NunitoFont">avares://MyApp/Assets/Fonts#Nunito</FontFamily>
            </ResourceDictionary>
        </ResourceDictionary.MergedDictionaries>
    </ResourceDictionary>
</Application.Resources>
```

另一种办法是把字体资源定义在单独的 AXAML 文件里，再用 `ResourceInclude` 引入。定义在 `<Window.Resources>` 作用域的字体不受此问题影响。
:::

## 嵌入式字体集合 {#embedded-font-collections}

[`EmbeddedFontCollection`](/api/avalonia/media/fonts/embeddedfontcollection) 把一个装着字体文件的目录注册到自定义 URI 方案下。这样你就能在 XAML 里直接按字体族名引用，不必为每个字体声明资源键。

该集合把一个自定义 URI（比如 `fonts:MyFonts`）映射到某个资产目录（比如 `avares://MyApp/Assets/Fonts`）。继承 `EmbeddedFontCollection` 即可创建这样的集合：

```csharp
using Avalonia.Media.Fonts;

public sealed class MyFontCollection : EmbeddedFontCollection
{
    public MyFontCollection() : base(
        new Uri("fonts:MyFonts", UriKind.Absolute),
        new Uri("avares://MyApp/Assets/Fonts", UriKind.Absolute))
    {
    }
}
```

在应用配置中注册该集合：

```csharp title="Program.cs"
public static AppBuilder BuildAvaloniaApp() =>
    AppBuilder.Configure<App>()
        .UsePlatformDetect()
        .ConfigureFonts(fontManager =>
        {
            fontManager.AddFontCollection(new MyFontCollection());
        })
        .LogToTrace();
```

之后用 `{scheme}:{collection-key}#{font-family-name}` 这种格式引用集合里的任意字体：

```xml
<TextBlock FontFamily="fonts:MyFonts#Nunito"
           FontSize="24"
           Text="Hello in Nunito" />
```

`EmbeddedFontCollection` 会搜遍指定目录下的每个文件，加载与所请求字体族名相符的那些。一个集合里可以装很多字体族和字体文件。要换用同一集合中的另一款字体，改一改 `#` 后面的名字即可。

## 预制字体包 {#pre-built-font-packages}

字体包把一个 `EmbeddedFontCollection` 打进 NuGet 包，供多个项目共用。[`Avalonia.Fonts.Inter`](https://github.com/AvaloniaUI/Avalonia/tree/master/src/Avalonia.Fonts.Inter) 包就是这种做法的范例。

要使用 Inter 字体，请安装 `Avalonia.Fonts.Inter` NuGet 包，并在应用配置中加上 `.WithInterFont()`：

```csharp title="Program.cs"
public static AppBuilder BuildAvaloniaApp() =>
    AppBuilder.Configure<App>()
        .UsePlatformDetect()
        .WithInterFont()
        .LogToTrace();
```

然后在 XAML 中引用该字体：

```xml
<TextBlock FontFamily="fonts:Inter#Inter"
           FontSize="24"
           Text="Hello in Inter" />
```

## OpenType 字体特性 {#opentype-font-features}

`FontFeatures` 属性控制连字、等宽数字、备用字形等 OpenType 特性。特性以逗号分隔的标签形式给出，采用 [HarfBuzz 语法](https://harfbuzz.github.io/harfbuzz-hb-common.html#hb-feature-from-string)：

```xml
<!-- Disable contextual alternates and enable tabular numbers -->
<TextBlock Text="111111 x64 ->" FontFeatures="-calt,+tnum" />
```

你可以在 `TextBlock` 内部的单个 `Run` 元素上应用字体特性：

```xml
<TextBlock>
    <Run Text="Regular: 12345" />
    <Run Text="Tabular: 12345" FontFeatures="+tnum" />
</TextBlock>
```

也可以用附加属性把它设在某个容器上：

```xml
<StackPanel TextElement.FontFeatures="+tnum">
    <TextBlock Text="12345" />
    <TextBlock Text="67890" />
</StackPanel>
```

常用的 OpenType 特性标签：

| 标签 | 特性 |
|---|---|
| `+tnum` / `-tnum` | 启用/禁用等宽（定宽）数字。 |
| `+liga` / `-liga` | 启用/禁用标准连字。 |
| `+calt` / `-calt` | 启用/禁用上下文替代字形。 |
| `+smcp` | 启用小型大写字母。 |
| `+onum` | 启用旧式（比例）数字。 |

:::info
可用的特性取决于字体本身，并非所有字体都支持全部 OpenType 特性。
:::

## 定制字体匹配 {#customizing-font-matching}

若要更精细地处理字体，你可以重写字体集合上的若干方法，掌控 Avalonia 如何挑选回退字体、如何生成合成字型。

### 自定义字符匹配 {#custom-character-matching}

重写 `TryMatchCharacter`，即可决定当某个字符在所请求的字体族中缺失时改用哪款字体。这适合为应用定制专属的回退链：

```csharp
public sealed class MyFontCollection : EmbeddedFontCollection
{
    public MyFontCollection() : base(
        new Uri("fonts:MyFonts", UriKind.Absolute),
        new Uri("avares://MyApp/Assets/Fonts", UriKind.Absolute))
    {
    }

    public override bool TryMatchCharacter(
        int codepoint,
        FontStyle fontStyle,
        FontWeight fontWeight,
        FontStretch fontStretch,
        CultureInfo? culture,
        out Typeface typeface)
    {
        // Custom logic to match characters to specific fonts
        // Return true if a match was found, false to fall through
        // to the default matching behavior
        return base.TryMatchCharacter(
            codepoint, fontStyle, fontWeight, fontStretch,
            culture, out typeface);
    }
}
```

### 控制合成字型 {#controlling-synthetic-typefaces}

当 Avalonia 找不到与所请求字重或字形完全匹配的字体时，会生成一个合成字型（由算法模拟出样式）。你可以在集合上实现 `IFontCollection2` 并重写合成字型的创建行为，针对特定字体族阻止这种做法。

## 受支持的字体格式 {#supported-font-formats}

多数 TrueType（`.ttf`）和 OpenType（`.otf`、`.ttf`）字体都受支持。可变字体目前尚不支持（见 [Issue #11092](https://github.com/AvaloniaUI/Avalonia/issues/11092)）。

## 排查问题 {#troubleshooting}

### 字体不生效（退回了默认字体） {#font-not-appearing-falls-back-to-default}

若你的自定义字体悄无声息地退回默认字体，请逐一排查下面这些常见原因：

**1. 字体文件没有作为 AvaloniaResource 引入**

项目文件必须显式把字体文件作为 `AvaloniaResource` 引入。否则字体文件压根不会嵌进构建产物，Avalonia 自然找不到。

```xml title="MyApp.csproj"
<AvaloniaResource Include="Assets\Fonts\*" />
```

加好之后重新构建项目。你应该能看到程序集文件变大了，这说明字体确实嵌进去了。

**2. URI 里漏了字体族名**

字体 URI 必须在 `#` 分隔符之后带上字体族名，只给集合路径是不够的。

```xml
<!-- Wrong: missing #FontFamilyName -->
<FontFamily x:Key="MyFont">avares://MyApp/Assets/Fonts</FontFamily>

<!-- Correct: includes the font family name -->
<FontFamily x:Key="MyFont">avares://MyApp/Assets/Fonts#Roboto Mono</FontFamily>
```

同样的规矩也适用于 `EmbeddedFontCollection` URI：

```xml
<!-- Wrong -->
<TextBlock FontFamily="fonts:MyFonts" />

<!-- Correct -->
<TextBlock FontFamily="fonts:MyFonts#Source Code Pro" />
```

`#` 之后的字体族名必须与字体的内部名称一致，而不是文件名。用字体查看器打开字体文件，或查看其元数据，即可找到内部名称。

**3. 字体在 WebAssembly（WASM）中不生效**

浏览器环境访问不到系统字体。若你的字体在桌面上好好的、到了 WASM 却不行，那是浏览器退回去用了一款并不存在的系统字体。

解决办法是用完整的字体集合 URI 语法，而不是指望系统字体回退。比如使用 `Avalonia.Fonts.Inter` 包时：

```xml
<!-- May fail in WASM -->
<TextBlock FontFamily="Inter" />

<!-- Works in all environments -->
<TextBlock FontFamily="fonts:Inter#Inter" />
```

这样能确保 Avalonia 从嵌入的集合中解析字体，而不是去找系统字体。

## 另请参阅 {#see-also}

- [排版](/docs/styling/typography)：字号、字重、字形、字间距、行高与文本装饰。
- [如何添加自定义字体](/docs/how-to/custom-font-how-to)
- [Assets](/docs/fundamentals/including-assets)
- [Styles](/docs/styling/styles)

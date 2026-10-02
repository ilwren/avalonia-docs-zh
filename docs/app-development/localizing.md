---
id: localizing
title: 使用 ResX 本地化
description: 用 ResX 资源文件为 Avalonia 应用做本地化，支持运行时切换语言和 RTL 布局。
doc-type: tutorial
---

要为全球用户打磨体验，本地化是关键一环。在 .NET 中，`ResXResourceReader` 和 `ResXResourceWriter` 类负责以基于 XML 的格式（`.resx`）读写资源。本指南带你用 ResX 为 Avalonia 应用做本地化。


<GitHubSampleLink title="Localization" link="https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/Localization/"/>


## 往项目中添加 ResX 文件 {#add-resx-files-to-the-project}

开始本地化之前，需要为每种要支持的语言准备一个 ResX 文件。举例来说，你可能会在名为 `Lang` 的文件夹里放这样三个文件：

* `Resources.fil-PH.resx` (Filipino)
* `Resources.ja-JP.resx` (Japanese)
* `Resources.resx`（英语，默认语言）

每个 ResX 文件都包含与应用中所用键相对应的译文。本例中这三个 ResX 文件大致长这样：

<Tabs>

<TabItem value="english" label="English (default)">

```xml
<?xml version="1.0" encoding="utf-8"?>
<root>
    <data name="GreetingText">
        <value>Hello!</value>
    </data>
</root>
```

</TabItem>

<TabItem value="filipino" label="Filipino">

```xml
<?xml version="1.0" encoding="utf-8"?>
<root>
    <data name="GreetingText">
        <value>Kumusta!</value>
    </data>
</root>
```

</TabItem>

<TabItem value="japanese" label="Japanese">

```xml
<?xml version="1.0" encoding="utf-8"?>
<root>
    <data name="GreetingText">
        <value>こんにちは！</value>
    </data>
</root>
```

</TabItem>

</Tabs>

:::caution
如果你把 ResX 文件放进 `Assets` 文件夹，记得把它们的「生成操作」改为「嵌入的资源」，否则代码生成可能会失败。
:::

## 设置区域文化 {#set-the-culture}

要让应用使用某种特定语言，需要设置当前区域文化。这件事在 `App.axaml.cs` 文件中完成：加上 `CultureInfo`，并为 `System.Globalization` 补上相应的 `using` 语句。

下面的例子把区域文化设为菲律宾语（`fil-PH`）：

```cs title="App.axaml.cs"
// highlight-next-line
using System.Globalization;

namespace MyApp;

public partial class App : Application
{
    public override void Initialize()
    {
        AvaloniaXamlLoader.Load(this);
    }

    public override void OnFrameworkInitializationCompleted()
    {
        // highlight-start
        Lang.Resources.Culture = new CultureInfo("fil-PH");
        // highlight-end
        if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        {
            desktop.MainWindow = new MainWindow
            {
                DataContext = new MainWindowViewModel(),
            };
        }

        base.OnFrameworkInitializationCompleted();
    }
}
```

请按需把 "fil-PH" 换成其他区域文化代码。

## 在视图中使用本地化文本 {#use-localized-text-in-the-view}

要在视图里使用本地化文本，先声明本地化资源所在的命名空间，然后在 XAML 中以静态方式引用它们。

```xml
<Window xmlns:lang="using:MyApp.Lang">

<TextBlock Text="{x:Static lang:Resources.GreetingText}"/>
```

上面这个示例中，`GreetingText` 是[前面那组 ResX 文件](#add-resx-files-to-the-project)里某个字符串的键。`{x:Static}` 标记扩展用于引用 .NET 类中定义的静态属性——这里指的就是资源文件（`lang:Resources.GreetingText`）。

只要对应的键齐备，把区域文化换成另一种，整个界面就会以所选语言显示。

### 生成 public 的 `Resources` 类 {#generating-a-public-resources-class}

要让 `{x:Static lang:Resources.GreetingText}` 引用生效，`Resources` 类必须是公开可访问的。默认情况下 `ResXFileCodeGenerator` 生成的这个类是 `internal` 的，XAML 够不着它。

你必须确保有一个 `public` 的资源类可用，否则 `{x:Static}` 引用可能会失败（因为 `internal` 的类照样能编译通过）。至于怎么生成 `Resources` 类，取决于你用的工具链：[Visual Studio](#visual-studio) 还是[其他工具](#other-tools-rider-vs-code-cli)。

:::caution
只有默认资源文件（`Resources.resx`）需要生成 `Resources` 类。各区域文化专属的文件（如 `Resources.fil-PH.resx`、`Resources.ja-JP.resx`）只提供译文，不需要各自的类。
:::

#### Visual Studio

在 Visual Studio 中，你可以把生成器工具从 `ResXFileCodeGenerator` 换成 `PublicResXFileCodeGenerator`。做法是在 `.csproj` 文件中加入下面的内容：

```xml
<ItemGroup>
  <EmbeddedResource Update="Lang\Resources.resx">
    <Generator>PublicResXFileCodeGenerator</Generator>
    <LastGenOutput>Resources.Designer.cs</LastGenOutput>
  </EmbeddedResource>
</ItemGroup>

<ItemGroup>
  <Compile Update="Lang\Resources.Designer.cs">
    <DesignTime>True</DesignTime>
    <AutoGen>True</AutoGen>
    <DependentUpon>Resources.resx</DependentUpon>
  </Compile>
</ItemGroup>
```

#### 其他工具（Rider、VS Code、CLI） {#other-tools-rider-vs-code-cli}

不用 Visual Studio 时，推荐改用 MSBuild 资源生成器，它在各平台、各 IDE 下都能运行。把下面的内容加进 `.csproj` 文件：

```xml
<ItemGroup>
  <EmbeddedResource Update="Lang\Resources.resx">
    <Generator>MSBuild:Compile</Generator>
    <StronglyTypedFileName>$(IntermediateOutputPath)Resources.Designer.cs</StronglyTypedFileName>
    <StronglyTypedLanguage>CSharp</StronglyTypedLanguage>
    <StronglyTypedNamespace>MyApp.Lang</StronglyTypedNamespace>
    <StronglyTypedClassName>Resources</StronglyTypedClassName>
    <PublicClass>true</PublicClass>
  </EmbeddedResource>
</ItemGroup>
```

- `MSBuild:Compile` 确保这个类由 MSBuild 在编译过程中生成，而不是交给某个 IDE 的文件生成器。
- `StronglyTypedFileName` 把生成的文件写进中间输出目录（`obj/`），从而不进入版本控制。
- `StronglyTypedNamespace` 必须与 XAML 中期望的命名空间一致。本例中文件放在 `Lang` 文件夹里，于是命名空间就是根命名空间后面加上 `.Lang`。
- `StronglyTypedClassName` 指定类名，这里应当是 `Resources`。
- `PublicClass` 设为 `true` 可让这个类成为 `public`。

## 运行时切换语言 {#runtime-language-switching}

在运行时修改区域文化代码，用户无需重启应用即可切换语言：

```csharp
public void SwitchLanguage(string cultureCode)
{
    Lang.Resources.Culture = new CultureInfo(cultureCode);
    // Raise PropertyChanged for all localized properties
    // or reload the view to pick up new strings
}
```

要注意，区域文化变化时 `x:Static` 绑定并不会自动刷新。因为 `x:Static` 只在加载时解析一次取值，所以在视图被刷新之前，界面不会呈现新语言。可以用下面两种办法绕开：

- **重新加载视图或窗口。**关掉窗口再重建，让所有 `x:Static` 引用按新的区域文化代码重新求值。
- **配合 [`INotifyPropertyChanged`](/docs/data-binding/inotifypropertychanged) 写一个本地化服务。**写一个服务类，把本地化字符串暴露为属性，并在区域文化变化时触发 `PropertyChanged`。然后绑定这些属性，而不是使用 `x:Static`。

## 从右到左（RTL）支持 {#right-to-left-rtl-support}

Avalonia 通过 [`FlowDirection`](/api/avalonia/media/flowdirection) 属性支持 RTL。把 `FlowDirection` 设为 `RightToLeft` 会镜像子控件的布局，这对阿拉伯语、希伯来语、波斯语等语言必不可少。

```xml
<Window FlowDirection="RightToLeft">
    <!-- All child controls mirror their layout -->
</Window>
```

你也可以根据当前区域文化动态设置 `FlowDirection`：

```csharp
var culture = new CultureInfo("ar-SA");
if (culture.TextInfo.IsRightToLeft)
{
    mainWindow.FlowDirection = FlowDirection.RightToLeft;
}
```

有些控件会根据 `FlowDirection` 调整自身布局，例如：

- [`StackPanel`](/controls/layout/panels/stackpanel)（反转水平方向上各项的顺序）
- [`Grid`](/controls/layout/panels/grid)（镜像列的排列顺序）
- [`DockPanel`](/controls/layout/panels/dockpanel)（左右停靠互换）
- [`TextBlock`](/controls/data-display/text-display/textblock)（调整文本对齐方式）

## 区域文化敏感的格式化 {#culture-aware-formatting}

在数据绑定中使用 `StringFormat` 时，格式化会跟随当前线程的区域文化。比如要让名为 `Price` 的值按当地习惯显示货币：

```xml
<TextBlock Text="{Binding Price, StringFormat='{}{0:C}'}" />
```

想指定用哪种区域文化来格式化，就在应用启动时设置 `Thread.CurrentThread.CurrentCulture`。

```csharp
Thread.CurrentThread.CurrentCulture = new CultureInfo("de-DE");
```

在上面的例子中，把区域文化设为 `de-DE` 后，价格 `1234.56` 会显示成 `1.234,56 €` 而不是 `$1,234.56`。

## 平台注意事项 {#platform-considerations}

Avalonia 的本地化功能在所有受支持的平台上表现一致。要检测系统区域设置，在任何受支持的平台上都可以使用 `CultureInfo.CurrentCulture`。

## 另请参阅 {#see-also}

- [资源](/docs/app-development/resources)：应用程序资源。
- [自定义字体](/docs/styling/custom-fonts)：为不同文字系统加载字体。

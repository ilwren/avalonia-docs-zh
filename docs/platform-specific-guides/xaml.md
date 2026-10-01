---
id: xaml
title: 平台专属的 XAML
---

## OnPlatform Markup Extension

### 概述 {#overview}
Avalonia 的 OnPlatform 标记扩展让开发者能按应用运行所在的操作系统，为属性指定不同的值。对于需要依平台调整界面或行为的跨平台应用来说，这尤其好使。

### 标记扩展语法的基本用法 {#basic-usage-in-markup-extension-syntax}

你可以为各平台分别指定值，再给一个默认值，当没有匹配到具体平台时就用它：

```xml
<TextBlock Text="{OnPlatform Default='Unknown', Windows='Im Windows', macOS='Im macOS', Linux='Im Linux'}"/>
```

另一种写法是用构造函数语法直接给出默认值，省去 `Default` 关键字；平台专属的属性仍需照常写明：

```xml
<TextBlock Text="{OnPlatform 'Hello World', Android='Im Android'}"/>
```

这个标记扩展不限于字符串，任何类型都能用：

```xml
<Border Height="{OnPlatform 10, Windows=50.5}"/>
```

### 指定类型参数 {#specifying-type-arguments}

你可以用自定义的 TypeArguments 显式指明这些值的类型：

```xml
<TextBlock Tag="{OnPlatform '0, 0, 0, 0', Windows='10, 10, 10, 10', x:TypeArguments=Thickness}"/>
```

上面这个例子里，`Tag` 属性的类型是 `object`，编译器据此不足以解析输入的字符串。若不指定 TypeArguments，该属性在所有平台上都会是 `string`；而有了 `TypeArguments`，编译器就会把它们解析成 `Thickness` 值。

### 嵌套标记扩展 {#nested-markup-extensions}

OnPlatform 扩展支持在其内部嵌套其他标记扩展：

```xml
<Border Background="{OnPlatform Default={StaticResource DefaultBrush}, Windows={StaticResource WindowsBrush}}"/>
```

### XML 语法 {#xml-syntax}

OnPlatform 也能以 XML 语法来定义属性值：

```xml
<StackPanel>
    <OnPlatform>
        <OnPlatform.Default>
            <ToggleButton Content="Hello World" />
        </OnPlatform.Default>
        <OnPlatform.iOS>
            <ToggleSwitch Content="Hello iOS" />
        </OnPlatform.iOS>
    </OnPlatform>
</StackPanel>
```

请注意，在这个例子里 `OnPlatform` 是 `StackPanel` 的子元素，但运行时只会真正创建一个控件（`ToggleButton` 或 `ToggleSwitch`）并添加到 StackPanel 中。

### 复杂属性的 setter {#complex-property-setters}

与上一个例子类似，OnPlatform 也可以出现在 ResourceDictionary 或其他字典、集合中的复杂属性 setter 里：

```xml
<ResourceDictionary>
    <OnPlatform x:Key="MyBrush">
        <OnPlatform.Default>
            <SolidColorBrush Color="Blue" />
        </OnPlatform.Default>
        <OnPlatform.iOS>
            <SolidColorBrush Color="Yellow" />
        </OnPlatform.iOS>
    </OnPlatform>
</ResourceDictionary>
```

### XML 合并写法 {#xml-combining-syntax}

为避免分支重复，可以在一个分支里写上多个平台。另一个实用的例子是引入平台专属的样式：

```xml
<Application.Styles>
    <!-- Always included -->
    <FluentTheme />

    <!-- Only one branch is executed in runtime -->
    <OnPlatform>
        <!-- if (Android || iOS) -->
        <On Options="Android, iOS">
            <StyleInclude Source="/Styles/Mobile.axaml" />
        </On>
        <!-- else -->
        <On Options="Default">
            <StyleInclude Source="/Styles/Default.axaml" />
        </On>
    </OnPlatform>
</Application.Styles>
```

### 补充说明 {#additional-details}

`OnPlatform` 标记扩展的运作方式类似 C# 里的 switch-case：编译器会为所有可能的取值生成分支，但运行时只会按条件执行其中一个。

还有一点值得记住：若应用是针对特定[运行时标识符](https://learn.microsoft.com/en-us/dotnet/core/rid-catalog)并[启用裁剪](https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/trimming-options)构建的，`OnPlatform` 扩展只会保留可能用到的分支。比如 `OnPlatform` 原本有 Windows 和 macOS 两个分支，但构建时只面向 Windows，那么其余分支会被移除，应用体积也随之减小。


## OnFormFactor Markup Extension

`OnFormFactor` 标记扩展的用法与 `OnPlatform` 相仿，总体语法一致。主要区别在于它不按平台、而是按设备形态（比如桌面和移动）来定义取值：

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <TextBlock Text="{OnFormFactor 'Default value', Mobile='Im Mobile', Desktop='Im Desktop'}"/>
</UserControl>
```

`OnFormFactor` 没有任何编译期裁剪优化，因为设备形态在编译期无从得知。这两个标记扩展都不是动态的：值一旦设定便不会再变。

## 另请参阅 {#see-also}

- [平台相关的 .NET](/docs/platform-specific-guides/dotnet)

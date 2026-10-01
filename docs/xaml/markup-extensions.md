---
id: markup-extensions
title: 标记扩展
---

标记扩展是写在花括号 `{}` 里的特殊表达式，用来在 XAML 中提供动态取值。有了它，你能表达的就不止是简单的字符串字面量了。

## Binding

在控件属性与源属性之间建立数据绑定：

```xml
<TextBlock Text="{Binding UserName}" />
```

### 常用绑定参数 {#common-binding-parameters}

| 参数 | 说明 |
|---|---|
| `Path` | 源对象上的属性路径。它是默认参数。 |
| `Mode` | 绑定方向：`OneWay`、`TwoWay`、`OneTime`、`OneWayToSource`、`Default`。 |
| `Converter` | 用于变换取值的 `IValueConverter`。 |
| `ConverterParameter` | 传给转换器的参数。 |
| `StringFormat` | 应用于绑定值的格式字符串。 |
| `FallbackValue` | 绑定失败时所使用的值。 |
| `TargetNullValue` | 源值为 `null` 时所使用的值。 |
| `Source` | 显式指定的源对象（会覆盖 `DataContext`）。 |
| `ElementName` | 绑定到同一 XAML 作用域内的具名元素。 |
| `RelativeSource` | 绑定到相对位置上的元素（例如 `TemplatedParent`、`Self`）。 |

```xml
<TextBlock Text="{Binding Price, StringFormat='Price: {0:C}'}" />
<TextBox Text="{Binding Name, Mode=TwoWay}" />
<TextBlock Text="{Binding Amount, Converter={StaticResource CurrencyConverter}}" />
<Image Source="{Binding ImageUrl, FallbackValue={x:Null}}" />
```

:::info
绑定语法的完整说明，请见[数据绑定语法](/docs/data-binding/data-binding-syntax)。
:::

## CompiledBinding

一种在编译期校验的绑定。设置了 `x:CompileBindings="True"` 时它与 `{Binding}` 功能等价，但也可以显式使用：

```xml
<TextBlock Text="{CompiledBinding UserName}" />
```

编译绑定要求作用域内设置了 `x:DataType`。它能在编译期检查绑定路径，运行时性能也更好。

## ReflectionBinding

基于反射的绑定，跳过编译期校验。绑定到动态或后期绑定的属性时用它：

```xml
<TextBlock Text="{ReflectionBinding DynamicProperty}" />
```

## StaticResource

按键从当前元素的资源链中查找资源：沿父元素一路向上找到 `Application.Resources` 为止。查找只在加载时发生一次。

```xml
<TextBlock Foreground="{StaticResource PrimaryBrush}" />
```

若找不到该资源，运行时会抛出异常。

### 资源查找顺序 {#resource-lookup-order}

1. 当前元素的 `Resources` 字典。
2. 沿逻辑树向上，各级父元素的 `Resources` 字典。
3. `Application.Resources` 字典。
4. 主题资源。

## DynamicResource

与 `StaticResource` 类似，区别在于资源若在运行时发生变化（例如切换主题），取值会自动更新：

```xml
<TextBlock Foreground="{DynamicResource SystemAccentColor}" />
```

以下情形请用 `DynamicResource`：
- 随主题而变的取值（颜色、画刷、尺寸）
- 运行时会变化的资源（例如用户偏好设置）
- 定义在主题字典中的资源

以下情形请用 `StaticResource`：
- 运行时永不改变的值
- 对性能敏感的场景（静态查找略快一些）

## TemplateBinding

一种轻量绑定，用在 `ControlTemplate` 定义内部，绑定到被模板化的父控件的某个属性：

```xml
<ControlTemplate TargetType="Button">
    <Border Background="{TemplateBinding Background}"
            Padding="{TemplateBinding Padding}"
            CornerRadius="{TemplateBinding CornerRadius}">
        <ContentPresenter Content="{TemplateBinding Content}" />
    </Border>
</ControlTemplate>
```

`TemplateBinding` 等价于 `{Binding RelativeSource={RelativeSource TemplatedParent}}`，但效率更高。

:::info
`TemplateBinding` 支持 `OneWay` 和 `TwoWay` 两种模式，默认是 `OneWay`；需要把值写回时请显式指定 `TwoWay` —— `{TemplateBinding Value, Mode=TwoWay}`。

不支持 `OneTime` 和 `OneWayToSource`。
:::

## OnPlatform

按当前操作系统返回不同的值：

```xml
<TextBlock FontSize="{OnPlatform Default=14, macOS=13, Android=16}" />

<Window Width="{OnPlatform 800, macOS=900}" />
```

支持的平台取值：`Default`、`Windows`、`macOS`、`Linux`、`Android`、`iOS`、`Browser`。

复杂的值请使用嵌套写法：

```xml
<TextBlock>
    <TextBlock.Margin>
        <OnPlatform>
            <On Options="Windows">8,4</On>
            <On Options="macOS">12,6</On>
            <On Options="Default">8,4</On>
        </OnPlatform>
    </TextBlock.Margin>
</TextBlock>
```

## OnFormFactor

按设备的外形规格返回不同的值：

```xml
<TextBlock FontSize="{OnFormFactor Default=14, Desktop=14, Mobile=18}" />
```

支持的取值：`Default`、`Desktop`、`Mobile`。

## RelativeSource

按绑定目标在视觉树或逻辑树中的位置，指定一个相对的绑定源。用在 `{Binding}` 中：

```xml
<!-- Bind to self -->
<Border Tag="{Binding Width, RelativeSource={RelativeSource Self}}" />

<!-- Bind to templated parent -->
<TextBlock Text="{Binding Header, RelativeSource={RelativeSource TemplatedParent}}" />

<!-- Bind to an ancestor by type -->
<TextBlock Text="{Binding DataContext.Title,
    RelativeSource={RelativeSource FindAncestor, AncestorType=Window}}" />
```

## 标记扩展的语法规则 {#markup-extension-syntax-rules}

### 基本语法 {#basic-syntax}

```xml
Property="{ExtensionName}"
Property="{ExtensionName Value}"
Property="{ExtensionName Param1=Value1, Param2=Value2}"
```

### Nesting

标记扩展可以嵌套：

```xml
<TextBlock Text="{Binding Name, Converter={StaticResource UpperCaseConverter}}" />
```

### Escaping

若要把属性设为一个以 `{` 开头的字面字符串，请在前面加一对空花括号：

```xml
<TextBlock Text="{}{This is literal text, not a markup extension}" />
```

## 另请参阅 {#see-also}

- [XAML 参考](/docs/xaml)：XAML 语法总览。
- [x: 指令](/docs/xaml/directives)：XAML 语言指令。
- [数据绑定语法](/docs/data-binding/data-binding-syntax)：绑定语法的完整参考。
- [编译绑定](/docs/data-binding/compiled-bindings)：编译期受校验的绑定。
- [标记扩展（数据绑定）](/docs/data-binding/markup-extensions)：绑定相关标记扩展的细节。

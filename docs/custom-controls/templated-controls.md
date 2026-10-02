---
id: templated-controls
title: 模板化控件
description: 用控件主题、模板部件和伪类打造无外观的模板化控件。
doc-type: how-to
---

模板化控件的控件类里没有任何渲染代码，它的外观由 [`ControlTemplate`](/api/avalonia/markup/xaml/templates/controltemplate) 定义。这把控件的视觉结构与行为分了家，于是开发者和设计师无需改动逻辑就能给控件换装。

熟悉 WPF 的话你会知道，这类控件有时被称作「无外观（lookless）」控件。

Avalonia 许多内置控件都是模板化控件（比如 `Button`、`TextBox` 和 `ListBox`）。你照着同样的路子就能写出自己的。

## 编写一个模板化控件 {#creating-a-templated-control}

要做模板化控件，新建一个继承自 `TemplatedControl` 的控件类，并用 `StyledProperty` 注册你的自定义属性。

下面这个例子是一个带 `LabelText` 属性、但还没有视觉呈现的模板化控件。

```csharp
public class ToggleLabel : TemplatedControl
{
    public static readonly StyledProperty<string> LabelTextProperty =
        AvaloniaProperty.Register<ToggleLabel, string>(nameof(LabelText), "Default");

    public string LabelText
    {
        get => GetValue(LabelTextProperty);
        set => SetValue(LabelTextProperty, value);
    }
}
```

:::caution 不要设置 DataContext = this
千万别在自定义控件的构造函数里给 `DataContext = this` 赋值。这么做会盖掉使用者本指望从父级视觉树继承下来的 `DataContext`。于是设在你控件上的绑定（比如 `<MyControl Items="{Binding SelectedItems}" />`）会去控件类型上找，而不是父级的 `ViewModel`，导致绑定悄无声息地失败。

模板化控件根本不需要自引用的 `DataContext`。在控件模板内部用 [`TemplateBinding`](#templatebinding) 访问控件自身的属性，`DataContext` 则让它从父级自然流下来。
:::

## 定义控件主题 {#defining-the-control-theme}

每个模板化控件都必须有一个包含其 `ControlTemplate` 的默认 `ControlTheme`。这个控件主题通常写在一个主题文件里，再用 `ResourceInclude` 引入 `App.axaml` 中的应用资源。

```xml title="App.axaml"
<Application.Resources>
  <ControlTheme x:Key="{x:Type local:ToggleLabel}" TargetType="local:ToggleLabel">
      <Setter Property="Template">
          <ControlTemplate>
              <Border Background="{TemplateBinding Background}" Padding="8">
                  <TextBlock Text="{TemplateBinding LabelText}" />
              </Border>
          </ControlTemplate>
      </Setter>
  </ControlTheme>
</Application.Resources>
```

几点说明：

- `x:Key="{x:Type local:ToggleLabel}"` 告诉 Avalonia：把这个默认主题套用到 `ToggleLabel` 的所有实例上。
- 若想加一套可供部分实例选用的备选外观，给它加个字符串键，比如 `x:Key="CompactToggleLabel"`。这样个别 `ToggleLabel` 实例只要设置 `Theme="{StaticResource CompactToggleLabel}"` 就能换上这套外观。详见[控件主题查找](/docs/styling/control-themes#control-theme-lookup)。
- `TargetType` 限定了主题的作用类型，好让属性 setter 和模板绑定都针对正确的类型解析。
- 在 `ControlTemplate` 内部，用 [`TemplateBinding`](/api/avalonia/data/templatebinding) 绑定到模板化控件上的属性。

## 模板部件 {#template-parts}

有时模板化控件需要在代码中操作模板里的某些特定元素。把这些元素定义成[`TemplatePart`](/api/avalonia/controls/metadata/templatepartattribute)即可。按惯例，模板部件的名字以 `PART_` 为前缀。

### 声明部件 {#declaring-parts}

给控件类加上 [`TemplatePart`](/api/avalonia/controls/metadata/templatepartattribute) 特性：每个要被识别为独立部件的元素，都写一条 `TemplatePart`。

```csharp
[TemplatePart("PART_Button", typeof(Button), IsRequired = true)]
[TemplatePart("PART_Label", typeof(TextBlock))]
public class ToggleLabel : TemplatedControl
{
    // Templated control behavior and logic
}
```

每条声明包含三项内容：

| 值 | 含义 |
| --- | --- |
| `Name` | 该元素所用的 `x:Name`，必须以 `PART_` 为前缀。 |
| `Type` | 该元素的控件类型，比如 `Button`、`Panel`。 |
| `IsRequired` | 该部件在模板中是否必需，默认为 `false`。 |

:::note
这些声明可以继承，因此派生自 `ToggleLabel` 的控件会继承它的部件声明。
:::

### 在代码中取出部件 {#retrieving-parts-in-code}

重写 `OnApplyTemplate`，在模板套用之后定位各个部件：

- 必需部件用 [`Get<T>`](/api/avalonia/controls/namescopeextensions)
- 可选部件用 [`Find<T>`](/api/avalonia/controls/namescopeextensions)

目标部件缺失时，`Get` 会抛出 `NotFound` 异常，`Find` 则返回 `null`。若目标部件存在、但与声明的控件 `Type` 不匹配，`Get` 和 `Find` 都会抛出 `InvalidOperation` 异常。

```csharp
private Button? _button;
private TextBlock? _label;

protected override void OnApplyTemplate(TemplateAppliedEventArgs e)
{
    base.OnApplyTemplate(e);

    if (_button is not null)
    {
        _button.Click -= OnButtonClick;
    }

    // Required part: Get throws if the template does not provide it.
    _button = e.NameScope.Get<Button>("PART_Button");
    _button.Click += OnButtonClick;

    // Optional part: Find returns null if the template does not provide it.
    _label = e.NameScope.Find<TextBlock>("PART_Label");
}
```

:::tip
`Get<T>` 和 `Find<T>` 的用法示例，可参考 [`ToggleSwitch` 源码](https://github.com/AvaloniaUI/Avalonia/blob/main/src/Avalonia.Controls/ToggleSwitch.cs)。
:::

## `TemplateBinding`

如果你在写控件模板、且想绑定到模板化父级，就用 `TemplateBinding`。

```xml
<TextBlock Name="tb" Text="{TemplateBinding Caption}"/>

<!-- Which is the same as -->
<TextBlock Name="tb" Text="{Binding Caption, RelativeSource={RelativeSource TemplatedParent}}"/>
```

这两种写法多数情况下等价，但有四点差别：

1.  `TemplateBinding` 只接受单个属性，不接受属性路径。若要按属性路径绑定，就得写成更长的那种形式：

    ```xml
    <!-- This WON'T work -->
    <TextBlock Name="tb" Text="{TemplateBinding Caption.Length}"/>

    <!-- Instead, use this syntax for the property path -->
    <TextBlock Name="tb" Text="{Binding Caption.Length, RelativeSource={RelativeSource TemplatedParent}}"/>
    ```

2.  `TemplateBinding` 支持 `OneWay` 和 `TwoWay` 两种模式，不支持 `OneTime` 和 `OneWayToSource`，默认是 `OneWay`。若需要把值写回模板化父级，请显式指定 `TwoWay`。（**注意：**这与 WPF 不同，在 WPF 中 [`TemplateBinding` 只能是 `OneWay`](https://docs.microsoft.com/en-us/dotnet/desktop/wpf/advanced/templatebinding-markup-extension#remarks)。）

    ```xml
    <!-- Writes the slider's value back to the templated parent -->
    <Slider Value="{TemplateBinding Value, Mode=TwoWay}"/>
    ```

3. `TemplateBinding` 只能用在 `StyledElement` 上。（**警告：**若用在非 `StyledElement` 的属性上，绑定会失败且不记录任何错误，该属性仍保持默认值。）

    ```xml
    <!-- This WON'T work because GeometryDrawing is not a StyledElement -->
    <GeometryDrawing Brush="{TemplateBinding AccentBrush}"/>
    
    <!-- Instead, use the longer syntax -->
    <GeometryDrawing Brush="{Binding AccentBrush, RelativeSource={RelativeSource TemplatedParent}}"/>
    ```

## Pseudoclasses

模板化控件可以通过[伪类](/api/avalonia/controls/metadata/pseudoclassesattribute)把自己的视觉状态暴露出来。于是主题作者无需接触代码隐藏，就能按控件状态分别设样式。

### 声明伪类 {#declaring-pseudoclasses}

给控件类加上 [`PseudoClasses`](/api/avalonia/controls/metadata/pseudoclassesattribute)，声明你的控件会用到哪些伪类。伪类名必须带上开头的 `:`。

```csharp
[PseudoClasses(":active", ":dragging")]
public class ToggleLabel : TemplatedControl
{
    // Templated control behavior and logic
}
```

### 在代码中设置伪类 {#setting-pseudoclasses-in-code}

在控件逻辑中设置伪类的状态。

```csharp
PseudoClasses.Set(":active", isActive);
```

然后在控件主题中选中这个伪类。把 `Style` 嵌在 `ControlTheme` 内部，`^` 才会解析成该控件。

```xml
<ControlTheme x:Key="{x:Type local:ToggleLabel}" TargetType="local:ToggleLabel">
    <Setter Property="Template">
        <!-- ControlTemplate as above -->
    </Setter>

    <Style Selector="^:active">
        <Setter Property="Background" Value="Blue" />
    </Style>
</ControlTheme>
```

## 另请参阅 {#see-also}

- [定义属性](/docs/custom-controls/defining-properties)：为自定义控件添加样式化属性、直接属性和附加属性。
- [定义事件](/docs/custom-controls/defining-events)：给自定义控件添加路由事件。
- [控件主题](/docs/styling/control-themes)：控件主题如何定义模板化控件的外观。
- [控件模板演练](/docs/styling/control-template-walkthrough)：一个完整的控件模板实例。
- [伪类](/docs/styling/pseudoclasses)：伪类如何把控件状态暴露给样式。
- [创建自定义控件](/docs/custom-controls)：各类自定义控件概览。
- [`TemplatePartAttribute`](/api/avalonia/controls/metadata/templatepartattribute)：声明模板部件的 API 参考。
- [`PseudoClassesAttribute`](/api/avalonia/controls/metadata/pseudoclassesattribute)：声明伪类的 API 参考。

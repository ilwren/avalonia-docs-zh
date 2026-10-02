---
id: data-validation
title: 数据校验
description: 在 Avalonia 中用 DataAnnotationsValidationPlugin 校验用户输入。
doc-type: overview
---

本文介绍如何用 Avalonia 校验用户输入的数据。

## 数据注解校验插件 {#data-annotations-validation-plugin}

Avalonia 的数据注解校验支持让你能够校验与 `ViewModel` 的 `Properties` 相关联的任何 [`Validation-Attributes`](https://learn.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations.validationattribute)。

可以校验内置的校验特性、[`CustomValidationAttribute`](https://learn.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations.customvalidationattribute)，也可以校验你自己从 `ValidationAttribute` 派生出的特性。

### Enable `DataAnnotationsValidationPlugin`

从 Avalonia v12 起，数据注解校验插件默认是关闭的。启用方法：

1. 打开项目中的 `Program.cs` 文件。
2. 在 `AppBuilder` 里加上这行：

```csharp
.WithDataAnnotationsValidation()
```

如果你要迁移的旧项目里曾用 `BindingPlugins.DataValidators.Remove(plugin);` 之类的写法手动移除数据注解校验插件，现在可以把它删掉了，不再需要。

### 示例：`EMail` 属性为必填，且必须是合法的电子邮件地址 {#example-the-property-email-is-required-and-must-be-a-valid-e-mail-address}

:::note
`RaiseAndSetIfChanged` 是 ReactiveUI 提供的方法，这个示例需要 ReactiveUI 才能运行。
:::

```csharp
[Required]
[EmailAddress]
public string? EMail
{
    get { return _EMail; }
    set { this.RaiseAndSetIfChanged(ref _EMail, value); }
}
```

## 定制校验消息的外观 {#customize-the-appearance-of-the-validation-message}

[`DataValidationErrors class`](/api/avalonia/controls/datavalidationerrors) 用于显示校验错误消息。它可以作为控件放进任何支持数据校验的控件（比如 `TextBox`）的 `ControlTemplate` 中。

在 .axaml 文件中设置 `Style`，即可定制错误消息的外观。

### 示例：自定义数据校验错误消息 {#example-custom-data-validation-error-message}

```xml
<Style Selector="DataValidationErrors">
  <Setter Property="Template">
    <ControlTemplate>
      <DockPanel LastChildFill="True">
        <ContentControl DockPanel.Dock="Right"
                        ContentTemplate="{TemplateBinding ErrorTemplate}"
                        DataContext="{TemplateBinding Owner}"
                        Content="{Binding (DataValidationErrors.Errors)}"
                        IsVisible="{Binding (DataValidationErrors.HasErrors)}"/>
        <ContentPresenter Name="PART_ContentPresenter"
                          Background="{TemplateBinding Background}"
                          BorderBrush="{TemplateBinding BorderBrush}"
                          BorderThickness="{TemplateBinding BorderThickness}"
                          CornerRadius="{TemplateBinding CornerRadius}"
                          ContentTemplate="{TemplateBinding ContentTemplate}"
                          Content="{TemplateBinding Content}"
                          Padding="{TemplateBinding Padding}"/>
      </DockPanel>
    </ControlTemplate>
  </Setter>
  <Setter Property="ErrorTemplate">
    <DataTemplate x:DataType="{x:Type x:Object}">
      <Canvas Width="14" Height="14" Margin="4 0 1 0" 
              Background="Transparent">
        <Canvas.Styles>
          <Style Selector="ToolTip">
            <Setter Property="Background" Value="LightRed"/>
            <Setter Property="BorderBrush" Value="Red"/>
          </Style>
        </Canvas.Styles>
        <ToolTip.Tip>
          <ItemsControl ItemsSource="{Binding}"/>
        </ToolTip.Tip>
        <Path Data="M14,7 A7,7 0 0,0 0,7 M0,7 A7,7 0 1,0 14,7 M7,3l0,5 M7,9l0,2" 
              Stroke="Red" 
              StrokeThickness="2"/>
      </Canvas>
    </DataTemplate>
  </Setter>
</Style>
```

## 另请参阅 {#see-also}

- [数据绑定](/docs/data-binding/introduction-to-data-binding)：把数据绑定到控件。
- [Community Toolkit MVVM](https://learn.microsoft.com/en-us/windows/communitytoolkit/mvvm/observablevalidator)：用 `ObservableValidator` 做校验。

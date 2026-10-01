---
id: binding-validation
title: 数据绑定中的校验
description: 用 DataAnnotations、INotifyDataErrorInfo 或基于异常的方式校验绑定数据。
doc-type: how-to
---

Avalonia 通过标准的 .NET 校验机制支持数据校验。当绑定的属性校验不通过时，控件会显示错误标识和对应的提示信息。

## 用数据注解做校验 {#validation-with-data-annotations}

最简单的办法是在视图模型属性上加 `System.ComponentModel.DataAnnotations` 特性。它可以配合 CommunityToolkit.Mvvm 的 `ObservableValidator` 基类使用：

```csharp
using System.ComponentModel.DataAnnotations;
using CommunityToolkit.Mvvm.ComponentModel;

public partial class RegistrationViewModel : ObservableValidator
{
    [ObservableProperty]
    [NotifyDataErrorInfo]
    [Required(ErrorMessage = "Name is required")]
    [MinLength(2, ErrorMessage = "Name must be at least 2 characters")]
    private string _name = "";

    [ObservableProperty]
    [NotifyDataErrorInfo]
    [Required(ErrorMessage = "Email is required")]
    [EmailAddress(ErrorMessage = "Invalid email address")]
    private string _email = "";

    [ObservableProperty]
    [NotifyDataErrorInfo]
    [Range(18, 120, ErrorMessage = "Age must be between 18 and 120")]
    private int _age;
}
```

有了 `[NotifyDataErrorInfo]` 特性，CommunityToolkit.Mvvm 会在属性变化时触发校验，并引发相应的 `INotifyDataErrorInfo` 事件。

绑定时使用 `TwoWay` 模式：

```xml
<StackPanel Spacing="8">
    <TextBox Text="{Binding Name}" PlaceholderText="Name" />
    <TextBox Text="{Binding Email}" PlaceholderText="Email" />
    <NumericUpDown Value="{Binding Age}" Watermark="Age" />
</StackPanel>
```

校验失败时，控件默认会显示红色边框，错误信息则出现在工具提示中。

## INotifyDataErrorInfo

`INotifyDataErrorInfo` 是 .NET 中用于属性级校验的标准接口。只要视图模型实现了它，Avalonia 就会自动接收其中的校验错误：

```csharp
public class LoginViewModel : INotifyPropertyChanged, INotifyDataErrorInfo
{
    private string _username = "";
    private readonly Dictionary<string, List<string>> _errors = new();

    public string Username
    {
        get => _username;
        set
        {
            _username = value;
            ValidateUsername();
            OnPropertyChanged();
        }
    }

    private void ValidateUsername()
    {
        ClearErrors(nameof(Username));

        if (string.IsNullOrWhiteSpace(Username))
            AddError(nameof(Username), "Username is required");
        else if (Username.Length < 3)
            AddError(nameof(Username), "Username must be at least 3 characters");
    }

    // INotifyDataErrorInfo implementation
    public bool HasErrors => _errors.Count > 0;

    public event EventHandler<DataErrorsChangedEventArgs>? ErrorsChanged;

    public IEnumerable GetErrors(string? propertyName)
    {
        if (propertyName is not null && _errors.TryGetValue(propertyName, out var errors))
            return errors;
        return Array.Empty<string>();
    }

    private void AddError(string propertyName, string error)
    {
        if (!_errors.ContainsKey(propertyName))
            _errors[propertyName] = new List<string>();

        _errors[propertyName].Add(error);
        ErrorsChanged?.Invoke(this, new DataErrorsChangedEventArgs(propertyName));
    }

    private void ClearErrors(string propertyName)
    {
        if (_errors.Remove(propertyName))
            ErrorsChanged?.Invoke(this, new DataErrorsChangedEventArgs(propertyName));
    }

    // INotifyPropertyChanged...
    public event PropertyChangedEventHandler? PropertyChanged;
    protected void OnPropertyChanged([CallerMemberName] string? name = null)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
}
```

## 自定义校验特性 {#custom-validation-attributes}

把可复用的校验逻辑封装成自定义校验特性：

```csharp
public class NotEqualToAttribute : ValidationAttribute
{
    private readonly string _otherProperty;

    public NotEqualToAttribute(string otherProperty)
    {
        _otherProperty = otherProperty;
    }

    protected override ValidationResult? IsValid(
        object? value, ValidationContext context)
    {
        var otherValue = context.ObjectType
            .GetProperty(_otherProperty)?
            .GetValue(context.ObjectInstance);

        if (Equals(value, otherValue))
            return new ValidationResult(
                ErrorMessage ?? $"Must not equal {_otherProperty}");

        return ValidationResult.Success;
    }
}
```

在视图模型上这样使用：

```csharp
[ObservableProperty]
[NotifyDataErrorInfo]
[Required]
private string _password = "";

[ObservableProperty]
[NotifyDataErrorInfo]
[Required]
[NotEqualTo(nameof(Password), ErrorMessage = "New password must differ from current")]
private string _newPassword = "";
```

## 校验错误的呈现 {#validation-error-display}

### 默认表现 {#default-behavior}

默认情况下，Avalonia 以这些方式展示校验错误：
- 控件四周出现红色边框
- 鼠标悬停时弹出含错误信息的工具提示
- 控件角上出现一个红色修饰标记

校验错误还会通过 [`DataValidationErrors`](/api/avalonia/controls/datavalidationerrors) 自动化对等体自动暴露给屏幕阅读器等辅助技术，详见[无障碍访问](/docs/app-development/accessibility#data-validation-errors)。

### 自定义错误呈现方式 {#customizing-error-display}

用 `DataValidationErrors` 控件可以自定义错误的展示方式。通过控件主题重写 `DataValidationErrors` 的模板即可：

```xml
<Style Selector="DataValidationErrors">
    <Setter Property="Template">
        <ControlTemplate>
            <DockPanel>
                <ContentControl DockPanel.Dock="Top"
                                ContentTemplate="{TemplateBinding ErrorTemplate}"
                                DataContext="{TemplateBinding Owner}"
                                Content="{Binding (DataValidationErrors.Errors)}"
                                IsVisible="{Binding (DataValidationErrors.HasErrors)}" />
                <ContentPresenter Name="PART_ContentPresenter"
                                  Background="{TemplateBinding Background}"
                                  BorderBrush="{TemplateBinding BorderBrush}"
                                  BorderThickness="{TemplateBinding BorderThickness}"
                                  Padding="{TemplateBinding Padding}"
                                  Content="{TemplateBinding Content}" />
            </DockPanel>
        </ControlTemplate>
    </Setter>
    <Setter Property="ErrorTemplate">
        <DataTemplate>
            <ItemsControl ItemsSource="{Binding}" Margin="0,0,0,4">
                <ItemsControl.ItemTemplate>
                    <DataTemplate>
                        <TextBlock Text="{Binding ErrorContent}"
                                   Foreground="Red" FontSize="12" />
                    </DataTemplate>
                </ItemsControl.ItemTemplate>
            </ItemsControl>
        </DataTemplate>
    </Setter>
</Style>
```

### 把错误信息显示在控件下方 {#showing-errors-below-the-control}

一种常见做法是把错误信息放在输入框下方，而不是塞进工具提示：

```xml
<Style Selector="DataValidationErrors">
    <Setter Property="ErrorTemplate">
        <DataTemplate>
            <TextBlock Foreground="#EF4444" FontSize="12" Margin="0,2,0,0">
                <TextBlock.Text>
                    <MultiBinding StringFormat="{}{0}">
                        <Binding Path="[0].ErrorContent" />
                    </MultiBinding>
                </TextBlock.Text>
            </TextBlock>
        </DataTemplate>
    </Setter>
</Style>
```

## 提交时统一校验 {#validating-on-submit}

当用户点击提交按钮时校验整个表单：

```csharp
public partial class RegistrationViewModel : ObservableValidator
{
    [RelayCommand(CanExecute = nameof(CanSubmit))]
    private void Submit()
    {
        ValidateAllProperties();

        if (HasErrors)
            return;

        // Proceed with submission
    }

    private bool CanSubmit() => !HasErrors;
}
```

`ValidateAllProperties()` 会一次性对所有属性跑完全部校验特性，这样就能把用户还没碰过的字段里的错误也一并查出来。

## 基于异常的校验 {#exception-based-validation}

Avalonia 还会捕获绑定更新过程中抛出的异常，并把它们当作校验错误展示出来。做些简单的类型转换校验时，这招挺顺手：

```csharp
private int _quantity;
public int Quantity
{
    get => _quantity;
    set
    {
        if (value < 0)
            throw new ArgumentException("Quantity cannot be negative");
        _quantity = value;
        OnPropertyChanged();
    }
}
```

这种办法虽然可行，但更推荐 `INotifyDataErrorInfo` —— 它支持同一属性上有多条错误，也支持异步校验。

## 另请参阅 {#see-also}

- [数据绑定语法](/docs/data-binding/data-binding-syntax)：绑定模式与各项参数。
- [INotifyPropertyChanged](/docs/data-binding/inotifypropertychanged)：视图模型的变更通知。
- [MVVM 模式](/docs/fundamentals/the-mvvm-pattern)：视图模型的常见写法与 CommunityToolkit.Mvvm。

---
id: dialogs-how-to
title: "操作指南：使用对话框"
description: 在 Avalonia 中创建并显示模态对话框、返回结果，以及搭建自定义对话框窗口。
doc-type: how-to
---

本指南介绍如何创建并显示模态对话框、返回结果，以及搭建自定义对话框窗口。

## 显示一个对话框窗口 {#showing-a-dialog-window}

创建一个对话框窗口，并用 `ShowDialog<T>` 以模态方式显示：

```csharp
var dialog = new ConfirmDialog();
dialog.DataContext = new ConfirmDialogViewModel("Delete this item?");

// ShowDialog returns a result when the dialog closes
bool? result = await dialog.ShowDialog<bool?>(parentWindow);

if (result == true)
{
    DeleteItem();
}
```

`parentWindow` 参数用来指定所有者。在桌面平台上，对话框会居中显示在所有者窗口之上，并在关闭前阻止与该窗口交互。

## 创建对话框窗口 {#creating-a-dialog-window}

对话框就是一个普通的 `Window`，只是有几项惯用设置：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        x:Class="MyApp.Views.ConfirmDialog"
        Title="Confirm"
        Width="400" Height="200"
        WindowStartupLocation="CenterOwner"
        CanResize="False"
        ShowInTaskbar="False">
    <Grid RowDefinitions="*,Auto" Margin="20">
        <TextBlock Grid.Row="0" Text="{Binding Message}"
                   TextWrapping="Wrap" VerticalAlignment="Center" />

        <StackPanel Grid.Row="1" Orientation="Horizontal"
                    HorizontalAlignment="Right" Spacing="8">
            <Button Content="Cancel" Command="{Binding CancelCommand}" />
            <Button Content="OK" Command="{Binding ConfirmCommand}" />
        </StackPanel>
    </Grid>
</Window>
```

### 关闭并返回结果 {#closing-with-a-result}

用 `Window.Close(result)` 关闭对话框并返回一个值：

```csharp
public partial class ConfirmDialog : Window
{
    public ConfirmDialog()
    {
        InitializeComponent();
    }
}
```

```csharp
public partial class ConfirmDialogViewModel : ObservableObject
{
    private readonly Window _dialog;

    public string Message { get; }

    public ConfirmDialogViewModel(Window dialog, string message)
    {
        _dialog = dialog;
        Message = message;
    }

    [RelayCommand]
    private void Confirm() => _dialog.Close(true);

    [RelayCommand]
    private void Cancel() => _dialog.Close(false);
}
```

准备好对话框及其视图模型：

```csharp
var dialog = new ConfirmDialog();
var vm = new ConfirmDialogViewModel(dialog, "Delete this item?");
dialog.DataContext = vm;

bool? result = await dialog.ShowDialog<bool?>(this);
```

### 另一种做法：在代码隐藏中关闭 {#alternative-close-from-code-behind}

如果你更愿意把关闭逻辑留在视图里：

```csharp
public partial class ConfirmDialog : Window
{
    public ConfirmDialog()
    {
        InitializeComponent();
    }

    private void OnOkClick(object? sender, RoutedEventArgs e)
    {
        Close(true);
    }

    private void OnCancelClick(object? sender, RoutedEventArgs e)
    {
        Close(false);
    }
}
```

## Returning Complex Results

对话框可以返回任意对象：

```csharp
// Dialog that returns a selected color
var dialog = new ColorPickerDialog();
Color? selectedColor = await dialog.ShowDialog<Color?>(parentWindow);

if (selectedColor is not null)
{
    ApplyColor(selectedColor.Value);
}
```

在对话框中：

```csharp
[RelayCommand]
private void Select()
{
    _dialog.Close(SelectedColor);
}

[RelayCommand]
private void Cancel()
{
    _dialog.Close(null);
}
```

## 获取父窗口 {#getting-the-parent-window}

当你在视图模型或 UserControl 中、手头没有父窗口引用时，可以这样弹出对话框：

```csharp
// From a UserControl's code-behind
var window = TopLevel.GetTopLevel(this) as Window;
if (window is not null)
{
    var result = await dialog.ShowDialog<bool?>(window);
}
```

在视图模型中，可以通过服务或参数把窗口传进来：

```csharp
public interface IDialogService
{
    Task<bool> ShowConfirmAsync(string message);
    Task<string?> ShowInputAsync(string prompt);
}

public class DialogService : IDialogService
{
    private readonly Window _mainWindow;

    public DialogService(Window mainWindow)
    {
        _mainWindow = mainWindow;
    }

    public async Task<bool> ShowConfirmAsync(string message)
    {
        var dialog = new ConfirmDialog();
        dialog.DataContext = new ConfirmDialogViewModel(dialog, message);
        var result = await dialog.ShowDialog<bool?>(_mainWindow);
        return result == true;
    }
}
```

## 文件与文件夹对话框 {#file-and-folder-dialogs}

文件和文件夹选择对话框请使用 `IStorageProvider` 服务：

```csharp
var topLevel = TopLevel.GetTopLevel(this);
if (topLevel is null) return;

var storage = topLevel.StorageProvider;

// Open file picker
var files = await storage.OpenFilePickerAsync(new FilePickerOpenOptions
{
    Title = "Select a File",
    AllowMultiple = false,
    FileTypeFilter = new[]
    {
        new FilePickerFileType("Text Files") { Patterns = new[] { "*.txt" } },
        new FilePickerFileType("All Files") { Patterns = new[] { "*" } },
    }
});

if (files.Count > 0)
{
    var file = files[0];
    await using var stream = await file.OpenReadAsync();
    // Read file contents
}
```

```csharp
// Save file picker
var file = await storage.SaveFilePickerAsync(new FilePickerSaveOptions
{
    Title = "Save File",
    SuggestedFileName = "document.txt",
    FileTypeChoices = new[]
    {
        new FilePickerFileType("Text Files") { Patterns = new[] { "*.txt" } },
    }
});

if (file is not null)
{
    await using var stream = await file.OpenWriteAsync();
    // Write file contents
}
```

完整 API 请参阅[存储提供程序](/docs/services/storage/storage-provider)。

## Preventing Dialog Close

处理 `Closing` 事件可以阻止对话框关闭（比如还有未保存的改动时）：

```csharp
dialog.Closing += (sender, e) =>
{
    if (HasUnsavedChanges)
    {
        e.Cancel = true;
        // Optionally show a confirmation
    }
};
```

## 覆盖式对话框（窗口内） {#overlay-dialogs-in-window}

若希望对话框出现在窗口内部、而不是另开一个操作系统窗口，可以用一层覆盖面板：

```xml
<Grid>
    <!-- Main content -->
    <StackPanel Margin="20">
        <Button Content="Show Dialog" Command="{Binding ShowDialogCommand}" />
    </StackPanel>

    <!-- Dialog overlay -->
    <Border Background="#80000000"
            IsVisible="{Binding IsDialogVisible}">
        <Border Background="White" CornerRadius="8"
                HorizontalAlignment="Center" VerticalAlignment="Center"
                Padding="24" MinWidth="300" BoxShadow="0 8 16 0 #40000000">
            <StackPanel Spacing="16">
                <TextBlock Text="Confirm Action" FontWeight="Bold" FontSize="18" />
                <TextBlock Text="Are you sure?" />
                <StackPanel Orientation="Horizontal" Spacing="8"
                            HorizontalAlignment="Right">
                    <Button Content="Cancel" Command="{Binding HideDialogCommand}" />
                    <Button Content="OK" Command="{Binding ConfirmCommand}" />
                </StackPanel>
            </StackPanel>
        </Border>
    </Border>
</Grid>
```

这种做法在所有平台上都能用，包括不支持独立窗口的 WebAssembly。

## See Also

- [窗口管理](/docs/app-development/window-management)：Show、ShowDialog 与窗口生命周期。
- [存储提供程序](/docs/services/storage/storage-provider)：文件与文件夹选择对话框。
- [命令](/docs/input-interaction/commanding)：把按钮绑定到命令。

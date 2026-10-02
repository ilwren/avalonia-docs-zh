---
id: file-dialogs
title: File Dialogs
description: 在 Avalonia 应用中用 StorageProvider API 打开文件选取、文件保存和文件夹选取对话框。
doc-type: reference
---

文件对话框功能通过 [`StorageProvider`](/docs/services/storage/storage-provider) 服务 API 使用，可从 `Window` 或 `TopLevel` 类取得。本页只讲基本用法，关于该 API 的更多信息请访问 StorageProvider 页面。

<GitHubSampleLink title="File Dialog" link="https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/FileOps"/>

## OpenFilePickerAsync

本方法打开文件选取对话框，让用户选择文件。`FilePickerOpenOptions` 用于指定传给系统对话框的各项选项。

```csharp
public class MyView : UserControl
{
    private async void OpenFileButton_Clicked(object sender, RoutedEventArgs args)
    {
        // Get top level from the current control. Alternatively, you can use Window reference instead.
        var topLevel = TopLevel.GetTopLevel(this);

        // Start async operation to open the dialog.
        var files = await topLevel.StorageProvider.OpenFilePickerAsync(new FilePickerOpenOptions
        {
            Title = "Open Text File",
            AllowMultiple = false
        });

        if (files.Count >= 1)
        {
            // Open reading stream from the first file.
            await using var stream = await files[0].OpenReadAsync();
            using var streamReader = new StreamReader(stream);
            // Reads all the content of file as a text.
            var fileContent = await streamReader.ReadToEndAsync();
        }
    }
}
```

---

## SaveFilePickerAsync

本方法打开文件保存对话框，让用户保存文件。`FilePickerSaveOptions` 用于指定传给系统对话框的各项选项。

### Example

```csharp
public class MyView : UserControl
{
    private async void SaveFileButton_Clicked(object sender, RoutedEventArgs args)
    {
        // Get top level from the current control. Alternatively, you can use Window reference instead.
        var topLevel = TopLevel.GetTopLevel(this);

        // Start async operation to open the dialog.
        var file = await topLevel.StorageProvider.SaveFilePickerAsync(new FilePickerSaveOptions
        {
            Title = "Save Text File"
        });

        if (file is not null)
        {
            // Open writing stream from the file.
            await using var stream = await file.OpenWriteAsync();
            using var streamWriter = new StreamWriter(stream);
            // Write some content to the file.
            await streamWriter.WriteLineAsync("Hello World!");
        }
    }
}
```

---

## SaveFilePickerWithResultAsync

本方法与 `SaveFilePickerAsync` 类似，但还会返回用户选中的是哪个文件类型筛选项。当文件扩展名取决于用户的选择时（比如导出成 PNG 还是 JPEG），这就有用了。

### Example

```csharp
public class MyView : UserControl
{
    private async void ExportButton_Clicked(object sender, RoutedEventArgs args)
    {
        var topLevel = TopLevel.GetTopLevel(this);

        var result = await topLevel.StorageProvider.SaveFilePickerWithResultAsync(new FilePickerSaveOptions
        {
            Title = "Export Image",
            FileTypeChoices = new[]
            {
                new FilePickerFileType("PNG Image") { Patterns = new[] { "*.png" } },
                new FilePickerFileType("JPEG Image") { Patterns = new[] { "*.jpg", "*.jpeg" } },
            }
        });

        if (result.StorageFile is not null)
        {
            // result.SelectedFileType contains the filter the user chose
            var format = result.SelectedFileType?.Name; // e.g., "PNG Image"
            await using var stream = await result.StorageFile.OpenWriteAsync();
            // Save in the chosen format...
        }
    }
}
```

返回的 `SaveFilePickerResult` 结构体包含：

| 属性 | 类型 | 说明 |
|---|---|---|
| `StorageFile` | `IStorageFile?` | 保存下来的文件；若用户取消了，则为 `null`。 |
| `SelectedFileType` | `FilePickerFileType?` | 用户在对话框中选中的文件类型筛选项。 |

关于 StorageProvider 服务的更多信息（包括如何保持对所选文件的访问权限、支持哪些选项等），请访问 [`StorageProvider`](/docs/services/storage/storage-provider) 文档页及其子页。

:::note
为便于讲解，这里的示例直接在 ViewModel 里访问 [`StorageProvider`](/docs/services/storage/storage-provider) API。在真实项目中，建议遵循 MVVM 原则，把它封成服务类，再用依赖注入／控制反转（DI/IoC）取用。具体做法可参考 [IoCFileOps](https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/IoCFileOps) 和 DepInject 这两个示例项目。
:::

## 另请参阅 {#see-also}

- [`StorageProvider`](/docs/services/storage/storage-provider)：完整的存储提供程序 API 参考。
- [文件选取器选项](/docs/services/storage/file-picker-options)：配置文件类型筛选和对话框选项。
- [书签](/docs/services/storage/bookmarks)：持久保存对所选文件和文件夹的访问权限。


















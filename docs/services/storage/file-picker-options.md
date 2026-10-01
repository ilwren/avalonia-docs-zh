---
id: file-picker-options
title: File Picker Options
---

## 选取器的通用选项 {#common-picker-options}

### Title

获取或设置选取器标题栏上显示的文字。

### SuggestedStartLocation

获取或设置文件打开选取器的初始位置，即一开始向用户展示哪个目录下的文件。
该值可以取自此前选过的文件夹，也可以用 `StorageProvider.TryGetFolderFromPathAsync` 或 `StorageProvider.TryGetWellKnownFolderAsync` 取得。

:::note
这只是给系统的一个建议：若应用无权访问该文件夹，或该文件夹不存在，系统可以不予理会。
:::
:::note
在 Linux 上，某些 DBus 文件选取器不支持起始位置。要改用 GTK Free Desktop，请在 `X11PlatformOptions` 中关掉 `UseDBusFilePicker`
:::

## FilePickerOpenOptions

### AllowMultiple

获取或设置一个选项，指示打开选取器是否允许用户选中多个文件。

### FileTypeFilter

获取或设置文件打开选取器所显示的文件类型集合。

### SuggestedFileType

获取或设置对话框在文件类型下拉框中默认选中的 `FilePickerFileType`。该值必须是 `FileTypeFilter` 中的某一项。

为文件选取器建立一份文件类型清单：

```csharp
//This can also be applied for SaveFilePicker.
var files = await _target.StorageProvider.OpenFilePickerAsync(new FilePickerOpenOptions()
{
 Title = title,
//You can add either custom or from the built-in file types. See "Defining custom file types" on how to create a custom one.
 FileTypeFilter = new[] { ImageAll, FilePickerFileTypes.TextPlain }
});
```

## FilePickerSaveOptions

### SuggestedFileName

获取或设置文件保存选取器向用户建议的文件名。

### DefaultExtension

获取或设置保存文件时使用的默认扩展名。

### FileTypeChoices

获取或设置用户可为文件选用的有效文件类型集合。

### SuggestedFileType

获取或设置对话框在文件类型下拉框中默认选中的 `FilePickerFileType`。该值必须是 `FileTypeChoices` 中的某一项。

### ShowOverwritePrompt

获取或设置一个值，指示当用户填写的文件名已存在时，文件打开选取器是否给出警告。

## FolderPickerOpenOptions

### AllowMultiple

获取或设置一个选项，指示打开选取器是否允许用户选中多个文件夹。

## 平台兼容性 {#platform-compatibility}

| 特性        | 托管 |  Windows | macOS | Linux | 浏览器 | Android |  iOS |
|---------------|-------|-------|-------|-------|-------|-------|-------|
| `Title` | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ |
| `SuggestedStartLocation` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `AllowMultiple` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `FileTypeFilter` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `SuggestedFileType` | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| `SuggestedFileName` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| `DefaultExtension` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| `FileTypeChoices` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| `ShowOverwritePrompt` | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ |

## 定义自定义文件类型 {#defining-custom-file-types}

Avalonia 内置了一组文件类型：

- FilePickerFileTypes.All——所有文件
- FilePickerFileTypes.TextPlain——txt 文件
- FilePickerFileTypes.ImageAll——所有图片
- FilePickerFileTypes.ImageJpg——jpg 图片
- FilePickerFileTypes.ImagePng——png 图片
- FilePickerFileTypes.ImageWebP——webp 图片
- FilePickerFileTypes.Pdf——pdf 文档

不过你也可以自定义文件类型供选取器使用。

比如内置的 ImageAll 类型就是这样定义的：

```csharp
public static FilePickerFileType ImageAll { get; } = new("All Images")
{
    Patterns = new[] { "*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.webp" },
    AppleUniformTypeIdentifiers = new[] { "public.image" },
    MimeTypes = new[] { "image/*" }
};
```

其中每个文件类型都带有下列提示信息，供不同平台取用：

- `Patterns` 为大多数 Windows、Linux 和浏览器平台所用，是一种可用于匹配类型的基本 GLOB 模式。
- `AppleUniformTypeIdentifiers` 是 Apple 定义的标准标识符，用于 macOS 和 iOS 平台。在 macOS 终端里用 `mdls -name kMDItemContentType yourfile.ext` 即可查出某个文件对应的正确值。
- `MimeTypes` 是文件的 Web 标识符，除 Windows 和 iOS 外的多数平台都会用到。

若这些信息都已知，建议把所有提示都填上。

:::note
若某项提示你并不确定，请不要随便填值或写 "*.*" 通配符，把该集合留空（null）即可。这会告诉平台忽略这一项，转而使用别的提示。
:::

## 选项中对 WebP 的支持 {#webp-inclusion-in-options}

请注意，`FilePickerFileTypes.ImageWebP` 以及把 "*.webp" 并入 "All Images" 模式，都是 11.1 版才引入的。在更早的版本里，你照样可以自定义文件选取器类型来涵盖 WebP 图片。例如，若只想让用户选 WebP 图片，可以这么写：

```csharp
var customWebPFileType = new FilePickerFileType("Only WebP Images")
{
    Patterns = new[] { "*.webp" },
    AppleUniformTypeIdentifiers = new[] { "org.webmproject.webp" },
    MimeTypes = new[] { "image/webp" }
};
```

若你想把 WebP 也算作图片类型之一，照搬上面那个 "ImageAll" 的例子即可。

## 另请参阅 {#see-also}

- [存储提供程序](/docs/services/storage/storage-provider)：完整的存储提供程序 API 参考。
- [文件对话框](/docs/services/file-dialogs)：使用打开、保存和文件夹选取对话框。
- [书签](/docs/services/storage/bookmarks)：持久保存对所选文件和文件夹的访问权限。

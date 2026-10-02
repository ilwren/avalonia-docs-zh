---
id: storage-provider
title: Storage Provider
---

`StorageProvider` 是文件与文件夹管理的核心，它提供了选取文件和文件夹、查询平台能力以及使用已存书签的各项方法。

`StorageProvider` 可通过 `TopLevel` 或 `Window` 的实例取得；关于如何访问 `TopLevel`，更多细节请看 [TopLevel](/docs/fundamentals/top-level) 页。

```csharp
var storage = window.StorageProvider;
```

## 属性 {#properties}

### CanOpen
指示当前平台上能否打开 `open file picker`。

```csharp
bool CanOpen { get; }
```

### CanSave
指示当前平台上能否打开 `save file picker`。

```csharp
bool CanSave { get; }
```

### CanPickFolder
指示当前平台上能否打开 `folder picker`。

```csharp
bool CanPickFolder { get; }
```

## 方法 {#methods}

### OpenFilePickerAsync
打开文件选取对话框。

```csharp
Task<IReadOnlyList<IStorageFile>> OpenFilePickerAsync(FilePickerOpenOptions options);
```
该方法返回所选 `IStorageFile` 实例的数组；若用户取消了对话框，则返回空集合。

### SaveFilePickerAsync
打开文件保存对话框。

```csharp
Task<IStorageFile?> SaveFilePickerAsync(FilePickerSaveOptions options);
```
该方法返回保存下来的 `IStorageFile` 实例；若用户取消了对话框，则返回 null。

### SaveFilePickerWithResultAsync
打开文件保存对话框，并连同文件一并返回用户选中的文件类型筛选项。

```csharp
Task<SaveFilePickerResult> SaveFilePickerWithResultAsync(FilePickerSaveOptions options);
```
该方法返回一个 `SaveFilePickerResult` 结构体，其 `StorageFile` 属性是保存下来的文件（若取消则为 `null`），`SelectedFileType` 则是用户在对话框中选中的 `FilePickerFileType`。

### OpenFolderPickerAsync
打开文件夹选取对话框。

```csharp
Task<IReadOnlyList<IStorageFolder>> OpenFolderPickerAsync(FolderPickerOpenOptions options);
```
该方法返回所选 `IStorageFolder` 实例的数组；若用户取消了对话框，则返回空集合。

### OpenFileBookmarkAsync
凭书签 ID 打开一个 `IStorageBookmarkFile`。

```csharp
Task<IStorageBookmarkFile?> OpenFileBookmarkAsync(string bookmark);
```
该方法返回已加书签的文件；若操作系统拒绝了请求，则返回 null。

### OpenFolderBookmarkAsync
凭书签 ID 打开一个 `IStorageBookmarkFolder`。

```csharp
Task<IStorageBookmarkFolder?> OpenFolderBookmarkAsync(string bookmark);
```
该方法返回已加书签的文件夹；若操作系统拒绝了请求，则返回 null。

### TryGetFileFromPathAsync
尝试按路径从文件系统读取文件。

```csharp
Task<IStorageFile?> TryGetFileFromPathAsync(Uri filePath);
```
该方法返回文件；若不存在则返回 null。filePath 参数应当是带 "file" 方案的绝对路径，不过在 Android 上也可以是带 "content" 方案的 URI。

### TryGetFolderFromPathAsync
尝试按路径从文件系统读取文件夹。

```csharp
Task<IStorageFolder?> TryGetFolderFromPathAsync(Uri folderPath);
```
该方法返回文件夹；若不存在则返回 null。folderPath 参数应当是带 "file" 方案的绝对路径，不过在 Android 上也可以是带 "content" 方案的 URI。

### TryGetWellKnownFolderAsync
尝试按知名文件夹标识符从文件系统读取文件夹。

```csharp
Task<IStorageFolder?> TryGetWellKnownFolderAsync(WellKnownFolder wellKnownFolder);
```
该方法返回文件夹；若不存在则返回 null。

## 扩展方法 {#extension-methods}

### TryGetFileFromPathAsync
尝试按路径从文件系统读取文件。

```csharp
Task<IStorageFile?> TryGetFileFromPathAsync(this IStorageProvider provider, string filePath);
```
该方法返回文件；若不存在则返回 null。
该方法接受不带任何方案的本地文件路径字符串作参数。
仅在具备物理文件路径的操作系统上受支持，主要是桌面端。

### TryGetFolderFromPathAsync
尝试按路径从文件系统读取文件夹。

```csharp
Task<IStorageFolder?> TryGetFolderFromPathAsync(this IStorageProvider provider, string folderPath);
```
该方法返回文件夹；若不存在则返回 null。
该方法接受不带任何方案的本地文件夹路径字符串作参数。
仅在具备物理文件路径的操作系统上受支持，主要是桌面端。

## 平台兼容性 {#platform-compatibility}

| 特性        | 托管 |  Windows | macOS | Linux | 浏览器 | Android |  iOS |
|---------------|-------|-------|-------|-------|-------|-------|-------|
| `OpenFileBookmarkAsync` | ✓* | ✓* | ✓* | ✓* | ✓ | ✓ | ✓ |
| `OpenFolderBookmarkAsync` | ✓* | ✓* | ✓* | ✓* | ✓ | ✓ | ✓ |
| `OpenFilePickerAsync` | ✓** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `SaveFilePickerAsync` | ✓** | ✓ | ✓ | ✓ | ✓*** | ✓ | ✓ |
| `SaveFilePickerWithResultAsync` | ✓** | ✓ | ✓ | ✓ | ✓*** | ✓ | ✓ |
| `OpenFolderPickerAsync` | ✓** | ✓ | ✓ | ✓ | ✓*** | ✓ | ✓ |
| `TryGetFileFromPathAsync` | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| `TryGetFolderFromPathAsync` | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| `TryGetWellKnownFolderAsync` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

\* 桌面平台对书签的支持并不完善，返回的其实是文件路径。macOS 上的支持已列入计划，以便配合沙箱化的 App Store 应用。

** 托管文件选取器只能在可以打开自定义窗口的桌面平台上使用。

*** 只有基于 Chromium 的浏览器才像样地支持文件选取器。

## 另请参阅 {#see-also}

- [文件对话框](/docs/services/file-dialogs)：常见文件对话框的用法示例。
- [文件选取器选项](/docs/services/storage/file-picker-options)：配置文件类型筛选和对话框选项。
- [书签](/docs/services/storage/bookmarks)：持久保存对所选文件和文件夹的访问权限。
- [存储项](/docs/services/storage/storage-item)：使用存储提供程序返回的文件和文件夹。

---
id: launcher
title: Launcher
description: 了解如何用 Avalonia 的 Launcher 服务，以用户的默认应用打开文件、文件夹和 URI。
doc-type: explanation
---

`Launcher` 服务让你能用与某项内容关联的默认应用打开文件、文件夹或 URI。比如用它在用户的默认浏览器中打开网址，或者用注册处理该文件类型的应用打开文档。

你可以通过 `TopLevel` 或 `Window` 的实例取得 `Launcher`。关于如何访问 `TopLevel`，更多细节请看 [TopLevel](/docs/fundamentals/top-level) 页。

```csharp
var launcher = TopLevel.GetTopLevel(control).Launcher;
```

## 方法 {#methods}

### `LaunchUriAsync`

针对指定的 URI，启动与其方案名关联的默认应用。

```csharp
Task<bool> LaunchUriAsync(Uri uri)
```

:::note
传入的 URI 可以是任意方案，包括自定义方案。不过接不接受这次启动请求，要看操作系统的脸色。
:::

**示例：在默认浏览器中打开网址**

```csharp
var success = await launcher.LaunchUriAsync(new Uri("https://avaloniaui.net"));
```

### `LaunchFileAsync`

启动与指定存储文件或文件夹关联的默认应用。

```csharp
Task<bool> LaunchFileAsync(IStorageItem storageItem);
```

:::note
`IStorageItem` 是从 `IStorageProvider` 或 `IClipboard` 这类沙箱 API 取得的文件或文件夹。若你只面向非沙箱的桌面平台，不妨改用接受 `FileInfo` 或 `DirectoryInfo` 的那些扩展方法。
:::

**示例：打开用户选中的文件**

```csharp
var files = await storageProvider.OpenFilePickerAsync(new FilePickerOpenOptions());
if (files.Count > 0)
{
    await launcher.LaunchFileAsync(files[0]);
}
```

## 扩展方法 {#extension-methods}

面向非沙箱桌面平台（Windows、macOS、Linux）时，下面这些扩展方法用起来更顺手。

### `LaunchFileInfoAsync`

启动与指定文件关联的默认应用。

```csharp
Task<bool> LaunchFileInfoAsync(FileInfo fileInfo)
```

**Example**

```csharp
var file = new FileInfo("/path/to/document.pdf");
var success = await launcher.LaunchFileInfoAsync(file);
```

### `LaunchDirectoryInfoAsync`

启动与指定目录（文件夹）关联的默认应用，通常就是在系统文件管理器中打开该文件夹。

```csharp
Task<bool> LaunchDirectoryInfoAsync(DirectoryInfo directoryInfo);
```

**Example**

```csharp
var folder = new DirectoryInfo("/path/to/folder");
var success = await launcher.LaunchDirectoryInfoAsync(folder);
```

## 返回值 {#return-values}

这些方法都返回一个 `bool`，指示操作系统是否受理了该请求。返回 `true` 并不保证真有应用把该项打开了，只说明系统接下了这个请求且没有报错。

## 平台兼容性 {#platform-compatibility}

| 特性        | Windows | macOS | Linux | 浏览器 | Android |  iOS |
|---------------|-------|-------|-------|-------|-------|-------|
| `LaunchUriAsync` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `LaunchFileAsync` | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ |
| `LaunchFileInfoAsync` | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| `LaunchDirectoryInfoAsync` | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |

## 另请参阅 {#see-also}

- [存储提供程序](/docs/services/storage/storage-provider)：文件与文件夹管理 API。
- [剪贴板](/docs/services/clipboard)：读写剪贴板数据。
- [TopLevel](/docs/fundamentals/top-level)：从控件访问平台服务。

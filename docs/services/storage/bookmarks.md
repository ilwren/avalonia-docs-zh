---
id: bookmarks
title: 书签
---

在安全和隐私管控严格的现代操作系统上，书签对维持文件和文件夹的访问权限尤为要紧。比如在 iOS 和较新版 macOS 这类平台上，直接访问文件系统受到重重限制：应用得请用户通过系统提供的文件选取器挑选文件或文件夹，随后操作系统交给应用一个带安全作用域的书签，日后凭它访问该文件或文件夹。

在 Avalonia 的 `StorageProvider` 中，这些书签由 `IStorageBookmarkFile` 和 `IStorageBookmarkFolder` 两个接口表示。

## Avalonia.Platform.Storage
### `IStorageBookmarkItem` interface
`IStorageBookmarkItem` 接口表示一个已加书签的存储项，继承自 IStorageItem 和 IDisposable。该接口不供客户端实现——没有特别许可，你无法编写自己的实现类。

它提供的主要属性和方法如下：

#### 属性： {#properties}

`CanBookmark`：指示该项能否加书签以便日后复用。

`Name`：该项的名称。

`Path`：该项在文件系统中的路径。

#### 方法： {#methods}
`CreateFileAsync(String)`,`CreateFolderAsync(String)`,`DeleteAsync()`,`Dispose()`,`GetBasicPropertiesAsync()`,`GetFileAsync(String)`,`GetFolderAsync(String)`,`GetItemsAsync()`,`GetParentAsync()`,`MoveAsync(IStorageFolder)`,`ReleaseBookmarkAsync()`,`SaveBookmarkAsync()`.

### `IStorageBookmarkFolder` interface

#### 属性： {#properties-1}
同 IStorageBookmarkItem

#### 方法： {#methods-1}
`DeleteAsync()`,`Dispose()`,`GetBasicPropertiesAsync()`,`GetBasicPropertiesAsync()`,`GetParentAsync()`,`MoveAsync(IStorageFolder)`,`OpenReadAsync()`,`OpenWriteAsync()`,`ReleaseBookmarkAsync()`,`SaveBookmarkAsync()`.



## 书签方法怎么用 {#how-to-use-bookmark-methods}
本节给出 `bookmark` 的实用指引。

### 保存与加载书签 {#saving-and-loading-bookmarks}
要取得某个文件夹或文件的书签 ID，请在存储项上调用异步方法 `SaveBookmarkAsync()`。拿到书签 ID 后，你可以把它存进本地数据库以备日后使用，省得每次都要用户重新选一遍文件夹。

`SaveBookmarkAsync()`：用于为选中的文件或文件夹取得 `bookmark ID`，可存下来日后再用。

```csharp
// Example usage
private async Task SaveBookmarksAsync(Control control)
{
    // A folder must be selected first
    if (_lastSelectedFolder == null) return;

    var bookmarkId = await _lastSelectedFolder.SaveBookmarkAsync();

    if (bookmarkId != null)
    {
        // Save the bookmarkId to a local file for later use.
        // ... (code to save bookmarkId)
    }
}
```

你可以用 `OpenFolderBookmarkAsync()` 系列方法，凭 `bookmark ID` 打开已加书签的文件夹。它会返回该文件夹；若操作系统拒绝了请求，则返回 null。

```csharp
// Example usage
private async Task LoadFolderByBookmarkAsync(Control control, string bookmarkId)
{
    if (string.IsNullOrEmpty(bookmarkId)) return;

    var toplevel = TopLevel.GetTopLevel(control);
    if (toplevel?.StorageProvider != null)
    {
        var folder = await toplevel.StorageProvider.OpenFolderBookmarkAsync(bookmarkId);

        if (folder != null)
        {
            // Successfully opened the bookmarked folder.
            // ... (code to save folder as a var)
            LastSelectedFolder = folder;
        }
    }
}
```

`ReleaseBookmarkAsync()`：用于撤销操作系统授予的安全作用域访问权限。当你不再需要访问该书签项时，应当调用它。

```csharp
// Example usage
private async Task ReleaseBookmarkAsync(Control control, string bookmarkId)
{
    if (string.IsNullOrEmpty(bookmarkId)) return;

    // First, try to release the OS bookmark.
    var toplevel = TopLevel.GetTopLevel(control);
    if (toplevel?.StorageProvider != null)
    {
        var folder = await toplevel.StorageProvider.OpenFolderBookmarkAsync(bookmarkId);
        if (folder is IStorageBookmarkItem storageBookmark)
        {
            await storageBookmark.ReleaseBookmarkAsync();
            storageBookmark.Dispose();
        }
    }
        
    // Then, remove the ID from local storage.
    // ... (code to remove bookmarkId from file)

}
```


### 从书签读写文件内容 {#reading-and-writing-file-content-from-a-bookmark}

`OpenFileBookmarkAsync()`：用于凭存下来的 `bookmark ID` 打开已加书签的文件。它会返回该文件；若操作系统拒绝了请求，则返回 null。


用 `OpenFileBookmarkAsync()` 取回已加书签的文件后，你就能用 `OpenReadAsync()` 读取其内容，或用 `OpenWriteAsync()` 修改它。

`OpenReadAsync()`：打开一个流以读取该书签文件。

```csharp
// Example usage
private async Task LoadFileByBookmarkAsync(Control control, string bookmarkId)
{
    if (string.IsNullOrEmpty(bookmarkId)) return;
    var toplevel = TopLevel.GetTopLevel(control);
    if (toplevel?.StorageProvider != null)
    {
        IStorageFile bookmarkedFile = await toplevel.StorageProvider.OpenFileBookmarkAsync(bookmarkId);
        if (bookmarkedFile != null)
        {
            // Read bookmarkedFile content
            // ... (code to use a read stream)
            await using var readStream = await bookmarkedFile.OpenReadAsync();
            using var reader = new StreamReader(readStream, Encoding.UTF8);
            FileContent = await reader.ReadToEndAsync();
        }
    }
}
```

`OpenWriteAsync()`：打开一个流以写入该书签文件。

```csharp
// Example usage
private async Task SaveFileByBookmarkAsync(Control control, string bookmarkId)
{
    if (string.IsNullOrEmpty(bookmarkId)) return;
    var toplevel = TopLevel.GetTopLevel(control);
    if (toplevel?.StorageProvider != null)
    {
        IStorageFile bookmarkedFile = await toplevel.StorageProvider.OpenFileBookmarkAsync(bookmarkId);
        if (bookmarkedFile != null)
        {
            // Write bookmarkedFile content
            // ... (code to use a write stream)
            await using var writeStream = await bookmarkedFile.OpenWriteAsync();
            await using var writer = new StreamWriter(writeStream, Encoding.UTF8);
            await writer.WriteAsync(FileContent);
        }
    }
}
```


### 管理已加书签的文件和文件夹 {#managing-bookmarked-files-and-folders}
书签加载之后，你就能用从 `IStorageItem` 继承来的那些方法操作该文件或文件夹。

`DeleteAsync()`：异步删除当前存储项及其内容。

```csharp
// Example usage
private async Task DeleteFileAsync()
{
    if (SelectedFile != null && LastSelectedFolder != null)
    {
        await SelectedFile.DeleteAsync();
        // Then refresh the UI.
    }
}
```

`MoveAsync(IStorageFolder)`：异步把该书签项移到新位置。

```csharp
IStorageFile bookmarkedFile = ...;
IStorageFolder newDestinationFolder = ...;
await bookmarkedFile.MoveAsync(newDestinationFolder);
```

`GetBasicPropertiesAsync()`：异步取得存储项的基本属性，比如大小和修改日期。

```csharp
// Example usage
IStorageFile bookmarkedFile = ...;
var properties = await bookmarkedFile.GetBasicPropertiesAsync();
long size = properties.Size;
```

`GetParentAsync()`：异步取得当前存储项的父文件夹。

```csharp
// Example usage
IStorageFile bookmarkedFile = ...;
var parentFolder = await bookmarkedFile.GetParentAsync();
string parentName = parentFolder.Name;
```

`TryGetLocalPath()`：这个扩展方法会尝试以字符串形式取得本地文件系统路径，在需要本地路径的平台专属操作中很有用。

```csharp
// This will work on Windows but may return null on other platforms
IStorageFile bookmarkedFile = ...;
string? localPath = bookmarkedFile.TryGetLocalPath();
```

## 各平台上书签的表示形式 {#platform-specific-bookmark-representation}
`bookmark ID` 的表示形式因平台而异：

**Windows**：书签就是一个简单的绝对路径字符串，长得像 `C:\Documents\Avalonia\bookmarks.pdf` 这样

**Android**：不妨把内容提供程序想成一位服务员，应用通过 Content URI 向它点取某个文件/文件夹。URI 的格式形如 `content://[Authority]/[path]/[id]`。举例来说，`com.android.externalstorage.documents` 是访问外部存储提供程序的 `Authority`，于是书签可能长成 `content://com.android.externalstorage.documents/tree/[your folder path]` 这样（参考：[创建内容提供程序 | Android Developers](https://developer.android.com/guide/topics/providers/content-provider-creating)）。

:::note
具体行为和能力取决于各操作系统及其安全策略。比如在某些平台上，用户一旦移动或重命名书签指向的文件或文件夹，该书签就可能失效。
:::

:::note
不建议把书签 ID 存到远程数据库：书签未必能长期有效，而且可能含有敏感的文件路径信息。
:::

## 另请参阅 {#see-also}

- [存储提供程序](/docs/services/storage/storage-provider)：完整的存储提供程序 API 参考。
- [存储项](/docs/services/storage/storage-item)：与文件和文件夹打交道。
- [文件对话框](/docs/services/file-dialogs)：使用打开、保存和文件夹选取对话框。
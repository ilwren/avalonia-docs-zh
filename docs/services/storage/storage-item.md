---
id: storage-item
title: Storage Items
---

## StorageFile 与 StorageFolder 的公共成员 {#common-members-for-storagefile-and-storagefolder}

### 名称 {#name}

获取该项的短名称，若有扩展名则一并包含在内。

### Path

获取该项在文件系统中的路径。

:::note
Android 后端返回的文件路径可能带 "content:" 方案。
浏览器和 iOS 后端返回的可能是相对 URI。
:::

:::caution
请勿用 Path 属性来保住对文件或文件夹的访问权限。如何长久保持对存储项的访问，请见[书签](/docs/services/storage/bookmarks)页。

请勿用 Path 属性按路径直接读文件，这在多数移动端和浏览器平台上行不通。请改用 [OpenReadAsync](#openreadasync) 和 [OpenWriteAsync](#openwriteasync)。
:::

### CanBookmark

若该项能加书签以便日后复用，则返回 true。

### SaveBookmarkAsync

把项保存为书签。
返回书签的标识符；若系统拒绝了请求，可能返回 null。

### GetBasicPropertiesAsync

获取当前项的基本属性。
目前可用的属性有：
- Size
- DateCreated
- DateModified

### GetParentAsync

获取当前存储项的父文件夹。

### DeleteAsync

删除当前存储项及其内容

### MoveAsync

把当前存储项及其内容移动到 `IStorageFolder`

## StorageFile 的成员 {#storagefile-members}

### OpenReadAsync

打开一个流以供读取。

### OpenWriteAsync

打开一个流以写入该文件。

## StorageFolder 的成员 {#storagefolder-members}

### GetItemsAsync

获取当前文件夹中的文件和子文件夹。
该方法成功完成后，会返回当前文件夹中文件和文件夹的列表，列表里的每一项都由一个 IStorageItem 实现对象表示。

:::note
该方法是惰性求值且异步的。
:::

### CreateFileAsync

在当前存储文件夹下，以指定名称创建一个文件；若文件已存在，则清空并覆盖它。

### CreateFolderAsync

在当前存储文件夹下，以指定名称创建一个文件夹（若已存在则不再创建）。

### TryGetSingleFileAsync

按名称从当前存储文件夹中取出单个文件。找到则返回匹配的 `IStorageFile`，若不存在同名文件则返回 null。这是个扩展方法，把「从文件夹里拿某一个文件」这种常见写法简化了一下。

```csharp
IStorageFile? file = await folder.TryGetSingleFileAsync("config.json");
```

### TryGetSingleFolderAsync

按名称从当前存储文件夹中取出单个子文件夹。找到则返回匹配的 `IStorageFolder`，若不存在同名文件夹则返回 null。这是个扩展方法，把「从文件夹里拿某一个子文件夹」这种常见写法简化了一下。

```csharp
IStorageFolder? subFolder = await folder.TryGetSingleFolderAsync("images");
```

## 扩展方法 {#extension-methods}

### TryGetLocalPath

以字符串形式获取该项在本地文件系统中的路径。
Android 平台通常用 "content:" 虚拟文件路径，浏览器平台则是隔离访问、没有完整路径，因此在这两个平台上该方法会返回 null。

:::note
若你想把文件路径存下来日后复用（配合 TryGetFileFromPathAsync），请考虑改用[书签](/docs/services/storage/bookmarks)：它正是为沙箱环境设计的，而在那种环境里用户应用未必能直接访问物理文件系统。
:::

## 另请参阅 {#see-also}

- [存储提供程序](/docs/services/storage/storage-provider)：完整的存储提供程序 API 参考。
- [书签](/docs/services/storage/bookmarks)：持久保存对所选文件和文件夹的访问权限。
- [文件对话框](/docs/services/file-dialogs)：使用打开、保存和文件夹选取对话框。

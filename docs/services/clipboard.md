---
id: clipboard
title: 剪贴板
---

## 数据格式 {#data-formats}

访问剪贴板之前，先弄明白数据格式很要紧，它由 `DataFormat<T>` 类表示。该类描述一项数据的格式（例如文本、HTML、PNG 等），各类剪贴板和拖放 API 都会用到它。

一个数据格式由种类（`Universal`、`Platform` 或 `Application`）、标识符和数据类型三部分构成。

种类与标识符都相同的两个数据格式，视为相等。

### 通用格式 {#universal-formats}

通用格式是 Avalonia 能直接理解的跨平台格式。  
目前有三种通用格式：

| 格式              | 标识符 | 类型           | 说明         |
| --------------------|------------|----------------|---------------------|
| `DataFormat.Text`   | "Text"     | `string`       | 纯文本数据     |
| `DataFormat.File`   | "File"     | [`IStorageItem`](/api/avalonia/platform/storage/istorageitem) | 文件或目录 |
| `DataFormat.Bitmap` | "Bitmap"   | [`Bitmap`](/api/avalonia/media/imaging/bitmap)       | 位图图像      |

### 平台格式 {#platform-formats}

平台格式**只在应用当前运行的平台上**兼容（比如 Windows、Linux、iOS 等），其标识符必须是底层平台认得的名称。只有当你需要与目标平台直接互操作、并且清楚其编码或序列化方式时，才用这种格式。

:::caution
**切勿**想当然地以为某个标识符在所有平台上都管用！  
举例来说，HTML 格式在 Windows 上叫 `HTML format`，在 Linux 和 Android 上叫 `text/html`，在 macOS 和 iOS 上则叫 `public.html`。使用平台专属格式前，请务必先确认目标操作系统。
:::

平台格式可用 `DataFormat.CreateBytesPlatformFormat` 或 `DataFormat.CreateStringPlatformFormat` 定义，分别对应 `byte[]` 和 `string` 类型。Avalonia 不会自动做序列化。

示例：
```csharp
if (OperatingSystem.IsMacOS())
{
    var macOSHtmlFormat = DataFormat.CreateStringPlatformFormat("public.html");
}
```

### 应用格式 {#application-formats}

应用格式是你的应用专用的，在所有允许自定义数据格式的平台上都能用。其标识符只能含 ASCII 字母、数字，外加点和短横（`A`-`Z`、`a`-`z`、`0`-`9`、`.`、`-`）。这个标识符不会直接暴露给底层平台，而是会在内部加上前缀，以免与平台格式冲突。

当你需要把应用专属的数据放上剪贴板时（比如在程序的多个实例之间共享数据），就用这种格式。

应用格式可用 `DataFormat.CreateBytesApplicationFormat` 或 `DataFormat.CreateStringApplicationFormat` 定义，分别对应 `byte[]` 和 `string` 类型。Avalonia 不会自动做序列化。

```csharp
var myFormat = DataFormat.CreateBytesApplicationFormat("mycompany-myapp-myformat");
```

## IClipboard

`IClipboard` 接口让你能与系统剪贴板打交道，读写文本、图像和自定义数据格式。

`IClipboard` 的实例可通过 [`TopLevel`](/docs/fundamentals/top-level) 对象取得：
```csharp
var clipboard = window.Clipboard;
```

### Reading

#### TryGetDataAsync()

读取剪贴板内容的办法是取得一个 [`IAsyncDataTransfer`](/api/avalonia/input/iasyncdatatransfer) 实例。该对象负责按需提供各种格式的数据项（见下文 [`IAsyncDataTransfer`](#iasyncdatatransfer--iasyncdatatransferitem) 一节）。

`TryGetDataAsync` 方法异步取得表示剪贴板内容的 `IAsyncDataTransfer` 对象。若剪贴板为空，则返回 `null`。

```csharp
using var data = await clipboard.TryGetDataAsync();
```

:::caution
由于剪贴板内容随时可能变化，建议尽快使用返回的 `IAsyncDataTransfer` 实例，不要存起来留待日后再用。对该对象的操作做完后，调用方必须将其释放，因此推荐用 `using` 语句。
:::

#### 扩展方法 {#extension-methods}

要按特定格式取数据，可以用几个现成的扩展方法。对于常见格式，用下面这些即可，不必自己调 `TryGetDataAsync()`：

- `TryGetValueAsync(DataFormat<T>)` 从剪贴板返回一个与指定数据格式匹配的 `T` 类型值，若没有则返回 `null`。
- `TryGetValuesAsync(DataFormat<T>)` 从剪贴板返回多个与指定数据格式匹配的 `T` 类型值，若没有则返回空数组。
- `TryGetTextAsync()` 返回一个与 `DataFormat.Text` 格式匹配的 `string` 值，若没有则返回 `null`。
- `TryGetFileAsync()` 返回一个与 `DataFormat.File` 格式匹配的 `IStorageItem` 对象，若没有则返回 `null`。
- `TryGetFilesAsync()` 返回多个与 `DataFormat.File` 格式匹配的 `IStorageItem` 对象，若没有则返回空数组。
- `TryGetBitmapAsync()` 返回一张与 `DataFormat.Bitmap` 格式匹配的 `Bitmap` 图像，若没有则返回 `null`。

调用返回单个值的方法时，若剪贴板上有多个值，取第一个。

示例：

```csharp
var text = await clipboard.TryGetTextAsync();
Console.WriteLine($"Clipboard text: {text}");

var file = await clipboard.TryGetFileAsync();
Console.WriteLine($"Clipboard file: {file?.Path}");

var bitmap = await clipboard.TryGetBitmapAsync();
Console.WriteLine($"Clipboard image: {bitmap?.PixelSize}");
```

:::tip
这些扩展方法底层都会调用 `TryGetDataAsync()`。若你打算一口气连用好几个，不妨改为只调一次 [`TryGetDataAsync()`](#trygetdataasync) 拿到 `IAsyncDataTransfer`，再从该对象上读出想要的各个值。
:::

#### TryGetInProcessDataAsync()

若之前由 `SetDataAsync()` 放上剪贴板的那个 `IAsyncDataTransfer` 实例仍在，本方法就把它原样取回。若剪贴板内容已变、已被刷出，或平台不支持惰性提供的值，则本方法返回 `null`。

调用本方法可以避开底层平台的剪贴板，在需要精细掌控时很有用。不过多数场景下还是优先用 `TryGetDataAsync()`。

本方法在 Windows、macOS 和 X11 上受支持。

### Writing

#### SetDataAsync()

要把数据放上剪贴板，请调用 `IClipboard.SetDataAsync(IAsyncDataTransfer)` 方法。它接受一个 `IAsyncDataTransfer` 的实现，由后者负责按需提供各种格式的数据项（见下文 [`IAsyncDataTransfer`](#iasyncdatatransfer--iasyncdatatransferitem) 一节）。

示例：
```csharp
var data = new DataTransfer();
data.Add(DataTransferItem.CreateText("Copied from Avalonia!"));
await clipboard.SetDataAsync(data);
```

:::note
往剪贴板上放新对象，总会先清掉原有数据。
:::

:::caution
**切勿**对传给 `SetDataAsync()` 的 `IAsyncDataTransfer` 对象调用 `Dispose()`！该实例在剪贴板上期间必须保持有效。Avalonia 会接管其所有权，并在不再使用时自动释放。
:::

#### 扩展方法 {#extension-methods-1}

为方便起见，写入单个特定格式也有几个扩展方法。常见格式可以用下面这些：

- `SetValueAsync(DataFormat<T>, T)` 把一个 `T` 类型值以指定数据格式放上剪贴板。
- `SetValuesAsync(DataFormat<T>, IEnumerable<T>)` 把多个 `T` 类型值以指定数据格式放上剪贴板。
- `SetTextAsync(string)` 把一个 `string` 值以 `DataFormat.Text` 格式放上剪贴板。
- `SetFileAsync(IStorageItem)` 把一个 `IStorageItem` 对象以 `DataFormat.File` 格式放上剪贴板。
- `SetFilesAsync(IEnumerable<IStorageItem>)` 把多个 `IStorageItem` 对象以 `DataFormat.File` 格式放上剪贴板。
- `SetBitmapAsync(Bitmap)` 把一张 `Bitmap` 图像以 `DataFormat.Bitmap` 格式放上剪贴板。

#### ClearAsync()

调用 `ClearAsync()` 方法会清空剪贴板的全部内容。

#### FlushAsync()

在 Windows、macOS 和 X11 上，数据是按需从放上剪贴板的 `IAsyncDataTransfer` 惰性取出的。
若 Avalonia 应用在未刷出数据的情况下退出，这些数据便不再可用。

调用 `FlushAsync()` 会强制系统把所有数据查出来并持久化，这样应用关闭后数据依然可用。该功能在 Windows 和 X11（Linux）上受支持；在不支持刷出的平台上，本方法什么也不做。

## IAsyncDataTransfer & IAsyncDataTransferItem

`IAsyncDataTransfer` 接口表示剪贴板的内容，暴露以下属性：
- `Formats`，返回一个 `DataFormat` 实例列表，表示该对象内含的所有格式。
- `Items`，返回一个 [`IAsyncDataTransferItem`](/api/avalonia/input/iasyncdatatransferitem) 实例列表，表示该对象内含的所有项。

`IAsyncDataTransferItem` 接口表示 `IAsyncDataTransfer` 中的单个项，暴露以下成员：
- `Formats`，返回一个 `DataFormat` 实例列表，表示该对象内含的所有格式。
- `TryGetRawAsync(DataFormat)`，用于异步取得某个数据格式下的单个值。

:::info
同一个项可以有多种格式。  
比如富文本可能同时以 RTF、HTML 和纯文本三种形式存在。
:::

### 取值 {#getting-values}

#### Raw

要从 `IAsyncDataTransferItem` 对象读取值，请调用 `TryGetRawAsync(DataFormat)` 方法并指明所需的数据格式。

:::tip
返回值是无类型的（`object`）。   
若想拿到带类型的结果，不妨用下面介绍的扩展方法。
:::

#### Typed

有几个扩展方法可从 `IAsyncDataTransfer` 和 `IAsyncDataTransferItem` 取得带类型的值：
- `TryGetValueAsync(DataFormat<T>)` 返回一个与指定数据格式匹配的 `T` 类型值，若没有则返回 `null`。
- `TryGetTextAsync()` 返回一个与 `DataFormat.Text` 格式匹配的 `string` 值，若没有则返回 `null`。
- `TryGetFileAsync()` 返回一个与 `DataFormat.File` 格式匹配的 `IStorageItem` 对象，若没有则返回 `null`。
- `TryGetBitmapAsync()` 返回一张与 `DataFormat.Bitmap` 格式匹配的 `Bitmap` 图像，若没有则返回 `null`。

在 `IAsyncDataTransfer` 上调用时，若有多个项匹配所请求的格式，取第一个。

此外，还有几个扩展方法只对 `IAsyncDataTransfer` 适用：
- `TryGetValuesAsync(DataFormat<T>)` 返回多个与指定数据格式匹配的 `T` 类型值，若没有则返回空数组。
- `TryGetFilesAsync()` 返回多个与 `DataFormat.File` 格式匹配的 `IStorageItem` 对象，若没有则返回空数组。

### Implementation

#### DataTransfer & DataTransferItem

要提供写入剪贴板的值，`IAsyncDataTransfer` 和 `IAsyncDataTransferItem` 两者都得实现。

Avalonia 用 `DataTransfer` 和 [`DataTransferItem`](/api/avalonia/input/datatransferitem) 类型分别给出了这两个接口的实现：
- `DataTransfer` 类是一个项的列表，它提供 `Add(DataTransferItem)` 方法用于添加新项。
- `DataTransferItem` 类可以看成一个「格式—值」字典，它提供 `Set<T>(DataFormat, T)` 方法用于为某个格式设定值。

示例：

```csharp
// Creates an item with both text and HTML formats.
var item = new DataTransferItem();
item.Set(DataFormat.Text, "From Avalonia!");
item.Set(DataFormat.CreateStringPlatformFormat("text/html"), "From <b>Avalonia</b>!");

// Adds the item to the DataTransfer.
var data = new DataTransfer();
data.Add(item);
```

`Set<T>` 方法还有一个重载 `Set<T>(DataFormat, Func<T>)`，可以惰性地提供值。

为方便起见，`DataTransferItem` 为常见格式提供了专门的设值方法：
- `SetText(string)` 为 `DataFormat.Text` 格式设定一个 `string` 值。
- `SetFile(IStorageItem)` 为 `DataFormat.File` 格式设定一个 `IStorageItem` 对象。
- `SetBitmap(Bitmap)` 为 `DataFormat.Bitmap` 格式设定一张 `Bitmap` 图像。

另外，还有一些静态工厂方法可创建只含单一格式的项：
- `DataTransferItem.Create<T>(DataFormat<T>, T)`——用于指定格式。
- `DataTransferItem.CreateText(string)`——用于 `DataFormat.Text` 格式。
- `DataTransferItem.CreateFile(IStorageItem)`——用于 `DataFormat.File` 格式。
- `DataTransferItem.CreateBitmap(Bitmap)`——用于 `DataFormat.Bitmap` 格式。

#### Custom

在更复杂的场景下，你可以手写 `IAsyncDataTransfer` 和 `IAsyncDataTransferItem` 的实现。一种用法是为某个项动态提供多种格式。

动手实现之前，请确认：
- [`DataTransfer` 和 `DataTransferItem`](#datatransfer--datatransferitem) 确实满足不了你的需要。
- `IAsyncDataTransfer.Formats` 包含所有项的格式，且没有重复。
- 你清楚 `IAsyncDataTransferItem.TryGetRawAsync()` 可能从任意线程被调用，且不经过 dispatcher。
- 你考虑过一并实现 `IDataTransfer` 和 `IDataTransferItem`，因为有些平台只能同步访问剪贴板。

:::caution
`IAsyncDataTransferItem.TryGetRawAsync()` 是否在 UI 线程上调用，取决于底层平台。**切勿**在其中调用任何需要 UI 线程的东西，包括经由 `Dispatcher.Invoke/InvokeAsync` 调用，否则会死锁！
:::

## 另请参阅 {#see-also}

- [拖放](/docs/input-interaction/drag-and-drop)：使用同类数据格式 API 的拖放数据传输。
- [TopLevel](/docs/fundamentals/top-level)：从控件访问平台服务。
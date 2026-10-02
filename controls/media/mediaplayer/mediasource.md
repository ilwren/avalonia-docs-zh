---
id: mediasource
title: MediaSource 类
tags:
  - avalonia pro
  - avalonia enterprise
---

在 Avalonia Pro MediaControls 中，`MediaSource` 这组类对各类媒体内容源做了抽象，让媒体播放系统能够用统一的接口对接文件、URL、流等不同来源。


:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## MediaSource（抽象基类） {#mediasource-abstract-base-class}

`MediaSource` 是抽象基类，为所有媒体源定义了统一接口。

### 方法 {#methods}

| 方法    | Return Type | 说明                                  |
|-----------|-------------|----------------------------------------------|
| Dispose() | void        | 释放媒体源占用的资源。 |

## UriSource 类 {#urisource-class}

`UriSource` 类表示用 URI 指向的媒体内容，URI 可以指向本地文件，也可以指向网络资源。

### 属性 {#properties}

| 属性 | 类型 | 说明                                    |
|----------|------|------------------------------------------------|
| Source   | Uri  | 获取指向媒体内容的 URI。 |

### 构造函数 {#constructors}

| 构造函数              | 说明                                |
|--------------------------|--------------------------------------------|
| UriSource(Uri source)    | 用指定的 URI 初始化。        |
| UriSource(string source) | 用指定的 URI 字符串初始化。 |

### 方法 {#methods-1}

| 方法                  | Return Type | 说明                                 |
|-------------------------|-------------|---------------------------------------------|
| Equals(UriSource other) | bool        | 判断与另一个 UriSource 是否相等。 |
| Equals(object obj)      | bool        | 判断与某个对象是否相等。         |
| GetHashCode()           | int         | 返回该实例的哈希码。    |
| Dispose()               | void        | 释放资源（通常什么也不做）。     |

### 用法示例 {#usage-examples}

```csharp
// From a string URL
var webSource = new UriSource("https://example.com/video.mp4");

// From a file path
var fileSource = new UriSource("file:///C:/Videos/sample.mp4");

// From a Uri object
var uri = new Uri("rtsp://example.com/stream");
var streamSource = new UriSource(uri);
```

## StreamSource 类 {#streamsource-class}

`StreamSource` 类表示以流的形式提供的媒体内容，让运行时动态生成的内容或内存中的内容也能播放。

### 属性 {#properties-1}

| 属性     | 类型   | 说明                                          |
|--------------|--------|------------------------------------------------------|
| TargetStream | Stream | 获取承载媒体数据的底层流。    |
| IsSeekable   | bool   | 获取底层流是否支持跳转。 |

### 构造函数 {#constructors-1}

| 构造函数                       | 说明                            |
|-----------------------------------|----------------------------------------|
| StreamSource(Stream targetStream) | 用指定的流初始化。 |

### 方法 {#methods-2}

| 方法                     | Return Type | 说明                                          |
|----------------------------|-------------|------------------------------------------------------|
| Equals(StreamSource other) | bool        | 判断与另一个 StreamSource 是否相等。       |
| Dispose()                  | void        | 释放资源，包括底层的流。 |

### 用法示例 {#usage-examples-1}

```csharp
// From a file stream
var fileStream = File.OpenRead("video.mp4");
var fileStreamSource = new StreamSource(fileStream);

// From a memory stream
byte[] videoData = GetVideoData();
var memoryStream = new MemoryStream(videoData);
var memoryStreamSource = new StreamSource(memoryStream);

// From a network stream
var webRequest = WebRequest.Create("https://example.com/video.mp4");
var responseStream = webRequest.GetResponse().GetResponseStream();
var networkStreamSource = new StreamSource(responseStream);
```

## `UriSource` 与 `StreamSource` 的取舍 {#choosing-between-urisource-and-streamsource}

### 何时使用 `UriSource` {#when-to-use-urisource}

- 本地媒体文件。
- 带直链 URL 的网络流。
- 实时协议流（RTSP/RTMP/RDP）。
- 任何能用标准 URI 表示的媒体。

**优点**：

- 开销更低。
- 由媒体后端原生处理。
- 不必操心内存和生存期管理。

### 何时使用 `StreamSource` {#when-to-use-streamsource}

- 内存中的媒体内容。
- 运行时动态生成的内容。
- 从非标准来源加载的内容。
- 播放前需要预处理的内容。

**优点**：

- 对接自定义内容源更灵活。
- 不需要临时文件。
- 可处理加密或受保护的内容。

## 资源管理 {#resource-management}

`UriSource` 和 `StreamSource` 都实现了 `IDisposable`：

- 对 `UriSource` 而言，`Dispose` 方法通常什么也不做。
- 对 `StreamSource` 而言，`Dispose` 方法会释放底层的流。

`MediaPlayer` 会自动管理生命周期：

- 设置新的 Source 时，先前的 Source 会被释放。
- 播放器被释放或反初始化时，当前的 Source 会被释放。

## 实践建议 {#best-practices}

1. **Resource Management**:
    - 交给 `StreamSource` 的流不要自行释放，它已经接管了所有权。

2. **Source Selection**:
    - 文件和网络媒体尽量用 `UriSource`，效率更高。
    - 内存中的内容、或需要预处理的内容则用 `StreamSource`。

3. **Error Handling**:
    - 创建 `UriSource` 之前先校验 URI
    - 创建 `StreamSource` 之前先确认流可读
    - 打开文件或网络资源时注意处理异常

4. **Seeking Considerations**:
    - 查看 `StreamSource.IsSeekable` 可判断是否支持跳转。
    - 若需要跳转，请确保流本身支持（`CanSeek` = true）。

## 另请参阅 {#see-also}

- [MediaPlayer 控件](/controls/media/mediaplayer)
- [MediaPlayer 类](/controls/media/mediaplayer/mediaplayer-class)
- [Implementing MediaPlayer](/controls/media/mediaplayer/media-playback)
- [Installing Avalonia Pro](/tools/installing-avalonia-pro)
- [疑难排查](/troubleshooting/controls/mediaplayer)
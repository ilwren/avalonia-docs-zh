---
id: media-playback
title: 实现媒体播放
sidebar_label: 实现媒体播放
tags:
  - avalonia pro
  - avalonia enterprise
---

这是一份实用指南，介绍如何用 Avalonia Pro 的 [`MediaPlayer`](/controls/media/mediaplayer) 在 Avalonia 应用中实现媒体播放。


:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## 初始化时机 {#initialization-timing}

:::caution
在 Avalonia 界面完全加载之前，`MediaPlayer` 还没准备好接受媒体源。过早设置 `Source` 属性（比如在 Window 或 UserControl 的构造函数里）会悄无声息地失败，因为此时底层平台后端尚未初始化。
:::

请务必等控件的 `Loaded` 事件触发之后再设置 `Source` 属性。有两种做法：

### 做法一：重写 OnLoaded {#option-1-use-the-onloaded-override}

```csharp
public partial class MainView : UserControl
{
    private Model _vm;

    public MainView()
    {
        InitializeComponent();
        _vm = new Model();
        DataContext = _vm;
    }

    protected override void OnLoaded(RoutedEventArgs e)
    {
        base.OnLoaded(e);
        _vm.SetSource(new UriSource("file:///C:/Videos/sample.mp4"));
    }
}
```

### Option 2: Use Dispatcher.UIThread.Post

如果所处的上下文没法重写 `OnLoaded`，可以用 `Dispatcher.UIThread.Post` 把调用推迟到 UI 线程就绪之后：

```csharp
protected override void OnLoaded(RoutedEventArgs e)
{
    base.OnLoaded(e);
    Dispatcher.UIThread.Post(() =>
    {
        mediaPlayer.Source = new UriSource("file:///C:/Videos/sample.mp4");
    });
}
```

:::tip
当 `MediaPlayerControl` 搭配 XAML 绑定使用时（比如 `Source="{Binding MediaSource}"`），时机由绑定系统自动处理，因为绑定是在控件挂入视觉树之后求值的。只有在代码隐藏中设置 `Source` 时，才需要你自己照看时机。
:::

## 加载媒体源 {#loading-media-sources}

### 用 UriSource 从文件或 URL 加载 {#from-files-or-urls-using-urisource}

```csharp
// Local file
mediaPlayer.Source = new UriSource("file:///C:/videos/sample.mp4");
// or 
mediaPlayer.Source = new UriSource(new Uri("file:///C:/videos/sample.mp4"));

// Remote URL
mediaPlayer.Source = new UriSource("https://example.com/video.mp4");
```

**注意**：只要条件允许，请给本地文件 URI 加上 `file://` 协议头，这样播放器才能确认该路径指向本地文件。

### 用 StreamSource 从流加载 {#from-streams-with-streamsource}

```csharp
// From file stream
var fileStream = File.OpenRead("path/to/video.mp4");
mediaPlayer.Source = new StreamSource(fileStream);

// From memory stream
var memoryStream = new MemoryStream(byteArray);
mediaPlayer.Source = new StreamSource(memoryStream);
```

**注意**：传给 `StreamSource` 的流不要自行释放，播放器会照看它的生存期。

### 用 StorageFileSource 配合文件选择器 {#using-file-picker-with-storagefilesource}

```csharp
public async void OpenFile_Click(object sender, RoutedEventArgs e)
{
    var storageProvider = TopLevel.GetTopLevel(this)?.StorageProvider;
    if (storageProvider == null) return;
    
    var files = await storageProvider.OpenFilePickerAsync(new FilePickerOpenOptions
    {
        AllowMultiple = false
    });
    
    if (files.Count != 1) return;
    if (files[0].Path is not { } path) return;
    
    mediaPlayer.Source = new StorageFileSource(files[0]);
}
```

## 常见操作 {#common-operations}

### 播放控制 {#playback-control}

```csharp
// Play/pause
await mediaPlayer.PlayAsync();
await mediaPlayer.PauseAsync();

// Stop
await mediaPlayer.StopAsync();

// Seek to position
mediaPlayer.Position = TimeSpan.FromSeconds(30);

// Change volume (0.0 to 1.0)
mediaPlayer.Volume = 0.75;

// Mute/unmute
mediaPlayer.IsMuted = true;
```

### 媒体信息 {#media-information}

```csharp
// Get duration
TimeSpan? duration = mediaPlayer.Duration;

// Check if media has video
bool hasVideo = mediaPlayer.HasVideo;

// Check if media is seekable
bool isSeekable = mediaPlayer.IsSeekable;

// Get current position
TimeSpan position = mediaPlayer.Position;
```

### 错误处理 {#error-handling}

```csharp
mediaPlayer.ErrorOccurred += (sender, args) =>
{
    Console.WriteLine($"Media error: {args.Message}");
    args.Handled = true; // Prevents the exception from being thrown.
};
```

**注意**：这个回调给了你机会，让 `MediaPlayer` 的状态得以体面地复位。

### 基本示例 {#basic-example}

```xml
<Window xmlns="https://github.com/avaloniaui"
        Width="800" Height="450">

    <Grid RowDefinitions="*, Auto">
        <MediaPlayerControl Name="mediaPlayer" Grid.Row="0" />
        <Button Grid.Row="1" Content="Open File" Click="OpenFile_Click" />
    </Grid>

</Window>
```

```csharp
public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
    }

    public async void OpenFile_Click(object sender, RoutedEventArgs e)
    {
        var storageProvider = TopLevel.GetTopLevel(this)?.StorageProvider;
        if (storageProvider == null) return;
        
        var files = await storageProvider.OpenFilePickerAsync(new FilePickerOpenOptions
        {
            AllowMultiple = false
        });
        
        if (files.Count != 1) return;
        if (files[0].Path is not { } path) return;
        
        mediaPlayer.Source = new StorageFileSource(files[0]);
    }
}
```

## 平台前置条件 {#platform-prerequisites}

`MediaPlayer` 组件在各个受支持平台上都依赖该平台的原生媒体播放框架：

### Windows

`MediaPlayer` 使用 Windows 的 Media Foundation 渲染多媒体内容；只要终端用户的环境支持，就尽量启用 Vulkan 图形 API。

Windows 10/11：

- 无需额外配置。

Windows 10N/11N 或 10KN/11KN：

- 请参阅[疑难排查](/troubleshooting/controls/mediaplayer)。

### macOS/iOS

在 macOS 和 iOS 上，`MediaPlayer` 使用 Apple 的 AVFoundation 渲染多媒体内容。 

需要 macOS 10.15 或 iOS 12.0 及以上版本。 

- 无需额外配置。

### Android

`MediaPlayer` 使用 Android 的 ExoPlayer 组件渲染多媒体内容；若终端设备支持，还会一并启用 Vulkan 图形 API。

需要 Android API 21（Android 5.0）及以上版本。

- 在你的 app builder 中调用 `UseAndroidPlayer`；
```csharp
protected override AppBuilder CustomizeAppBuilder(AppBuilder builder)
{
    return base.CustomizeAppBuilder(builder)
        ...
        .UseAndroidPlayer(this)
        ...
        .LogToTrace();
}
  ```
- 以获得 Vulkan 支持；
```csharp
protected override AppBuilder CustomizeAppBuilder(AppBuilder builder)
{
    return base.CustomizeAppBuilder(builder)
        .UseAndroidPlayer(this)
        .With(new VulkanOptions()
        {
            VulkanDeviceCreationOptions = new VulkanDeviceCreationOptions()
            {
                DeviceExtensions = new[] { "VK_ANDROID_external_memory_android_hardware_buffer", "VK_EXT_queue_family_foreign" }
            }
        })
        ...
        .LogToTrace();
}
```

### Linux

在 Linux 发行版上，`MediaPlayer` 使用系统安装的 LibVLC 库渲染多媒体内容。

需要 LibVLC 3.0.21 或更高版本。

Debian/Ubuntu:

```bash
apt install libvlc
```

Fedora：

```bash
dnf install libvlc
```

### 嵌入式 Linux（direct rendering manager） {#embedded-linux-direct-rendering-manager}

与普通 Linux 的要求类似，在嵌入式 Linux 设备上 `MediaPlayer` 同样使用系统安装的 LibVLC 库渲染多媒体内容。

请按[在 Linux DRM Framebuffer 上搭建 Avalonia 的指南](https://avaloniaui.net/blog/unleashing-net-on-embedded-linux)操作。

之后再按上文所述安装 VLC 依赖。

Linux DRM 环境没有额外的特殊要求，你可以像在普通 Linux 上一样继续使用 `MediaPlayer` 控件。

## 编解码器支持 {#codecs-support}

`MediaPlayer` 支持哪些媒体编解码器，取决于目标平台内置的编解码器和额外安装的插件。

最稳妥的假设是：视频方面，多数平台都支持 `MPEG-4 Part 10 - Advanced Video Coding`（更常见的叫法是 `H.264`），容器格式为 `MPEG-4 Part 14` 或 `MP4`。 

音频方面，可以稳妥假定受支持的编解码器有 `MP3`、`AAC` 和 `WAV`。

各平台支持哪些编解码器，可查阅以下资料：

### Windows

- https://support.microsoft.com/en-us/windows/codecs-in-media-player-d5c2cdcd-83a2-4805-abb0-c6888138e456

### Android

- https://developer.android.com/media/platform/supported-formats

### Linux 

- https://www.videolan.org/vlc/features.html

### macOS 与 iOS {#macos-and-ios}

- 目前还没有找到权威的一手资料说明 macOS/iOS 默认支持哪些编解码器。

## 另请参阅 {#see-also}

- [MediaPlayer 控件](/controls/media/mediaplayer)
- [MediaPlayer 类](/controls/media/mediaplayer/mediaplayer-class)
- [MediaSource 类](/controls/media/mediaplayer/mediasource)
- [Installing Avalonia Pro](/tools/installing-avalonia-pro)
- [疑难排查](/troubleshooting/controls/mediaplayer)
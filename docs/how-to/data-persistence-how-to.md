---
id: data-persistence-how-to
title: "操作指南：保存与加载应用设置"
description: 用 JSON 文件或数据库，跨会话保存用户偏好与应用状态。
doc-type: how-to
---

本指南介绍在 Avalonia 应用中跨会话保存用户偏好和应用状态的几种套路。

## JSON 文件设置 {#json-file-settings}

最简单的办法是把设置以 JSON 文件的形式存到用户的应用数据目录里：

```csharp
using System.Text.Json;

public class AppSettings
{
    public string Theme { get; set; } = "Default";
    public double WindowWidth { get; set; } = 800;
    public double WindowHeight { get; set; } = 600;
    public string LastOpenedFile { get; set; } = "";
    public bool ShowSidebar { get; set; } = true;
}

public class SettingsService
{
    private static readonly string SettingsPath = Path.Combine(
        Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
        "MyApp",
        "settings.json");

    public AppSettings Load()
    {
        if (!File.Exists(SettingsPath))
            return new AppSettings();

        var json = File.ReadAllText(SettingsPath);
        return JsonSerializer.Deserialize<AppSettings>(json) ?? new AppSettings();
    }

    public void Save(AppSettings settings)
    {
        var directory = Path.GetDirectoryName(SettingsPath)!;
        Directory.CreateDirectory(directory);

        var json = JsonSerializer.Serialize(settings, new JsonSerializerOptions
        {
            WriteIndented = true
        });
        File.WriteAllText(SettingsPath, json);
    }
}
```

:::tip
不妨把 `Load` 方法包进 `try`/`catch` 块中。万一 JSON 文件损坏，或者版本更迭导致结构变了，`JsonSerializer.Deserialize` 就会抛异常。在 `catch` 块里返回一个默认的 `AppSettings` 实例，可以避免应用一启动就崩溃。
:::

### 配合视图模型使用 {#using-with-a-view-model}

```csharp
public partial class SettingsViewModel : ObservableObject
{
    private readonly SettingsService _settingsService;
    private readonly AppSettings _settings;

    public SettingsViewModel(SettingsService settingsService)
    {
        _settingsService = settingsService;
        _settings = settingsService.Load();
        _theme = _settings.Theme;
        _showSidebar = _settings.ShowSidebar;
    }

    [ObservableProperty]
    private string _theme;

    [ObservableProperty]
    private bool _showSidebar;

    partial void OnThemeChanged(string value)
    {
        _settings.Theme = value;
        _settingsService.Save(_settings);
    }

    partial void OnShowSidebarChanged(bool value)
    {
        _settings.ShowSidebar = value;
        _settingsService.Save(_settings);
    }
}
```

:::note
每次属性变化就保存固然省事，但设置项一多、变化又频繁，磁盘 I/O 就会过载。面对高频更新，不妨给保存操作加上防抖，或者用定时器把若干改动攒起来、延迟片刻再一并写出。
:::

## 保存窗口的位置与尺寸 {#saving-window-position-and-size}

你可以把窗口的几何信息存下来，下次启动时恢复：

```csharp
public partial class MainWindow : Window
{
    private readonly SettingsService _settings;

    public MainWindow()
    {
        InitializeComponent();
        _settings = new SettingsService();
        RestoreWindowState();
    }

    private void RestoreWindowState()
    {
        var s = _settings.Load();
        if (s.WindowWidth > 0 && s.WindowHeight > 0)
        {
            Width = s.WindowWidth;
            Height = s.WindowHeight;
        }
    }

    protected override void OnClosing(WindowClosingEventArgs e)
    {
        var s = _settings.Load();
        s.WindowWidth = Width;
        s.WindowHeight = Height;
        _settings.Save(s);
        base.OnClosing(e);
    }
}
```

:::warning
恢复窗口位置时，记得校验存下来的坐标在当前的屏幕配置下是否依然有效。用户也许在上次会话之后拔掉了外接显示器，窗口就会跑到屏幕之外。你可以在应用保存的位置值之前，先用 `TopLevel` 上的 `Screens.All` 查一查可用的屏幕范围。
:::

若你不只想保存尺寸、还想保存窗口位置，请给 `AppSettings` 类加上 `WindowX` 和 `WindowY` 属性，并在 `OnClosing` 中赋值：

```csharp
// In AppSettings
public int WindowX { get; set; } = -1;
public int WindowY { get; set; } = -1;

// In RestoreWindowState
if (s.WindowX >= 0 && s.WindowY >= 0)
{
    Position = new PixelPoint(s.WindowX, s.WindowY);
}

// In OnClosing
s.WindowX = Position.X;
s.WindowY = Position.Y;
```

## 最近文件列表 {#recent-files-list}

你可以记录最近打开过的文件，在菜单或欢迎界面中列出来：

```csharp
public class RecentFilesService
{
    private const int MaxRecent = 10;
    private readonly string _path;
    private List<string> _recentFiles = new();

    public RecentFilesService()
    {
        _path = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "MyApp", "recent.json");
        Load();
    }

    public IReadOnlyList<string> RecentFiles => _recentFiles;

    public void AddFile(string filePath)
    {
        _recentFiles.Remove(filePath);
        _recentFiles.Insert(0, filePath);
        if (_recentFiles.Count > MaxRecent)
            _recentFiles.RemoveAt(_recentFiles.Count - 1);
        Save();
    }

    public void RemoveFile(string filePath)
    {
        _recentFiles.Remove(filePath);
        Save();
    }

    private void Load()
    {
        try
        {
            if (File.Exists(_path))
            {
                var json = File.ReadAllText(_path);
                _recentFiles = JsonSerializer.Deserialize<List<string>>(json) ?? new();
            }
        }
        catch (JsonException)
        {
            _recentFiles = new();
        }
    }

    private void Save()
    {
        var dir = Path.GetDirectoryName(_path)!;
        Directory.CreateDirectory(dir);
        File.WriteAllText(_path, JsonSerializer.Serialize(_recentFiles));
    }
}
```

:::tip
展示最近文件列表时，请先确认每个文件是否还在，再显示给用户。文件在上次打开之后可能已被移动、改名或删除。像上面的 `RemoveFile` 方法那样提供一个「从列表中移除」的选项，能让用户在遇到失效条目时体验好不少。
:::

## 各平台的存储路径 {#platform-specific-storage-paths}

每个操作系统都有自己存放应用配置的惯例。
那通常是一个专用的可写文件夹，隶属于当前用户（而非全局共享）。

现代 .NET 把这些差异抽象掉了，一次 `Environment.GetFolderPath` 调用就能解析出配置路径：

```csharp
public static string GetAppDataPath()
{
    // Resolve path to the per-user app data folder.
    // `SpecialFolderOption.Create` is important on Linux, where this folder might not be created by default.
    var localAppData = Environment.GetFolderPath(
        Environment.SpecialFolder.LocalApplicationData,
        Environment.SpecialFolderOption.Create);

    // Define app-specific sub-folder, isolated from other apps. Optionally, you can add company specific subfolder as well.
    var myAppData = Path.Combine(localAppData, "MyApp");

    // Optionally, ensure folder is created before returning path from this method.
    if (!Directory.Exists(myAppData))
        Directory.CreateDirectory(myAppData);

    return myAppData;
}
```

下表列出 .NET 8 中 `SpecialFolder.LocalApplicationData` 解析到的位置：

| 平台 | 典型路径 |
|---|---|
| Windows | `%LOCALAPPDATA%\MyApp\` |
| macOS | `~/Library/Application Support/MyApp/` |
| Linux* | `~/.local/share/MyApp/` |

\* Linux 下的路径会因是否设置了 `XDG_DATA_HOME` 而不同。

:::note
运行时应把应用的安装目录视为只读，只用来放随包分发的默认值和静态资产，不要存放可变的用户数据。
此外，向系统级共享目录写入往往还需要提权。
:::

## 书签式存储（移动端与沙盒） {#bookmarked-storage-mobile-and-sandbox}

在沙盒化的平台上（iOS、Android、WebAssembly），标准文件系统 API 可能无法跨会话访问用户选定的文件。这时请用 Avalonia 的 `IStorageProvider` 书签来保留文件访问权：

```csharp
var storage = TopLevel.GetTopLevel(this)?.StorageProvider;
if (storage is null) return;

// Save a bookmark
var file = (await storage.OpenFilePickerAsync(new FilePickerOpenOptions())).FirstOrDefault();
if (file is not null)
{
    var bookmark = await file.SaveBookmarkAsync();
    // Store the bookmark string in your settings
    settings.LastFileBookmark = bookmark;
}

// Restore from bookmark
if (!string.IsNullOrEmpty(settings.LastFileBookmark))
{
    var restored = await storage.OpenFileBookmarkAsync(settings.LastFileBookmark);
    if (restored is not null)
    {
        await using var stream = await restored.OpenReadAsync();
        // Read file contents
    }
}
```

:::warning
若用户移动或删除了文件，或者操作系统收回了授权，书签就会失效。请务必检查恢复出来的 `IStorageFile` 是否为 `null`，并妥善处理失败的情形。在某些平台上，书签还可能在系统重启后过期。
:::

书签 API 的完整说明请参阅[书签](/docs/services/storage/bookmarks)。

## 另请参阅 {#see-also}

- [存储提供程序](/docs/services/storage/storage-provider)：跨平台访问文件与文件夹。
- [书签](/docs/services/storage/bookmarks)：在沙盒平台上跨会话保留文件访问权。
- [存储项](/docs/services/storage/storage-item)：使用 `IStorageFile` 与 `IStorageFolder` 实例。
- [窗口管理](/docs/app-development/window-management)：窗口的生命周期、定位与状态。
- [依赖注入](/docs/app-development/dependency-injection)：在应用中注册 `SettingsService` 之类的服务。

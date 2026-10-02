---
id: intent-filter
title: 把应用注册为文件打开方式
description: 配置 Android intent filter，让你的 Avalonia 应用能打开文件和自定义 URI 方案。
doc-type: how-to
---

Android 允许应用通过 intent filter 把自己注册为特定文件类型或 URI 方案的处理方。当用户打开匹配的文件或链接时，Android 会拉起你的应用，并通过一个激活事件把数据传进来。本指南带你把 Avalonia 应用注册为纯文本文件的处理方，并用 Avalonia 的存储 API 读取其内容。

## 前置条件 {#prerequisites}

- 一个面向 Android 的 Avalonia 项目
- 一个继承自 `AvaloniaMainActivity` 的 `MainActivity`

## 第 1 步：给 activity 加上 `IntentFilter` 特性 {#step-1-add-the-intentfilter-attribute-to-your-activity}

给你的 `MainActivity` 标注一个 `[IntentFilter]` 特性。构建时，该特性会自动把相应的 `<intent-filter>` 条目合并进 Android 清单文件，你不必手改 XML。

下面的示例把应用注册为纯文本文件（`text/plain`）的处理方，可经由 `file` 或 `content` URI 方案打开：

```csharp
[Activity(
    Label = "Demo.Android",
    Theme = "@style/MyTheme.NoActionBar",
    Icon = "@drawable/icon",
    MainLauncher = true,
    ConfigurationChanges = ConfigChanges.Orientation | ConfigChanges.ScreenSize | ConfigChanges.UiMode)]
[IntentFilter(["android.intent.action.VIEW"],
    Categories = [Intent.CategoryDefault, Intent.CategoryBrowsable],
    DataSchemes = ["file", "content"],
    DataMimeType = "text/plain",
    DataPathPattern = ".*\\.txt")]
public class MainActivity : AvaloniaMainActivity
{
    // See Steps 2 and 3 below.
}
```

### 如何选择 `DataMimeType` 与 `DataPathPattern` {#choosing-datamimetype-and-datapathpattern}

| 属性 | 用途 | 示例 |
|---|---|---|
| `DataMimeType` | 匹配发送方应用声明的 MIME 类型。 | `"text/plain"`, `"application/pdf"` |
| `DataPathPattern` | 匹配文件路径（只对 `file` 方案有效）。 | `".*\\.txt"`, `".*\\.csv"` |

:::tip
若你想处理多种 MIME 类型，请为每种类型各加一个 `[IntentFilter]` 特性。Android 不支持在一个 filter 里写一串 MIME 类型。
:::

## 第 2 步：监听 `Activated` 事件 {#step-2-listen-for-the-activated-event}

在 `MainActivity` 的构造函数中为 `IAvaloniaActivity.Activated` 挂上处理程序。当 Android 激活你的应用去打开文件时，Avalonia 会带着一个含有传入存储项的 `FileActivatedEventArgs` 实例引发该事件。

```csharp
public class MainActivity : AvaloniaMainActivity
{
    public MainActivity()
    {
        ((IAvaloniaActivity)this).Activated += HandleIntent;
    }

    private static void HandleIntent(object? sender, ActivatedEventArgs e)
    {
        if (e is FileActivatedEventArgs fileActivated && Avalonia.Application.Current is App app)
        {
            app.OpenFiles(fileActivated.Files);
        }
    }
}
```

:::note
无论 Android 是新起一个应用实例，还是把已有实例切到前台，`Activated` 事件都会触发。请确保你的处理程序被多次调用也不出岔子。
:::

## 第 3 步：把文件转交给视图模型 {#step-3-forward-files-to-your-view-model}

用静态的 `Avalonia.Application.Current` 属性即可从 activity 拿到你的 `App` 实例。一个顺手的套路是：在 `OnFrameworkInitializationCompleted` 中创建视图模型后把它存进一个字段，再暴露一个供 activity 调用的辅助方法。

### `App.axaml.cs`

```csharp
public partial class App : Application
{
    private MainViewModel? mainViewModel;

    public override void OnFrameworkInitializationCompleted()
    {
        mainViewModel = new MainViewModel();

        if (ApplicationLifetime is ISingleViewApplicationLifetime singleView)
        {
            singleView.MainView = new MainView
            {
                DataContext = mainViewModel
            };
        }

        base.OnFrameworkInitializationCompleted();
    }

    public void OpenFiles(IReadOnlyList<IStorageItem> files)
    {
        mainViewModel?.OpenFiles(files);
    }
}
```

### `MainViewModel.cs`

```csharp
public class MainViewModel
{
    public async void OpenFiles(IReadOnlyList<IStorageItem> files)
    {
        foreach (IStorageItem item in files)
        {
            if (item is IStorageFile file)
            {
                using Stream stream = await file.OpenReadAsync();
                // Read the stream (use StreamReader, etc.)
            }
        }
    }
}
```

## 处理自定义 URI 方案 {#handling-custom-uri-schemes}

调整 `DataSchemes` 数组，即可注册自定义 URI 方案（比如 `myapp://`）：

```csharp
[IntentFilter(["android.intent.action.VIEW"],
    Categories = [Intent.CategoryDefault, Intent.CategoryBrowsable],
    DataSchemes = ["myapp"])]
```

当应用经由自定义方案被激活时，请改查 `ProtocolActivatedEventArgs` 而非 `FileActivatedEventArgs`：

```csharp
private static void HandleIntent(object? sender, ActivatedEventArgs e)
{
    if (e is FileActivatedEventArgs fileActivated && Avalonia.Application.Current is App app)
    {
        app.OpenFiles(fileActivated.Files);
    }
    else if (e is ProtocolActivatedEventArgs protocolActivated)
    {
        // protocolActivated.Uri contains the full URI, e.g. myapp://path?query=value
    }
}
```

## 排查问题 {#troubleshooting}

| 现象 | 可能的原因 |
|---|---|
| 你的应用没出现在 Android 的分享/打开面板里。 | 你 `[IntentFilter]` 中的 MIME 类型与发送方应用提供的对不上。用 `adb shell am start -a android.intent.action.VIEW -t "text/plain" -d "content://..."` 核对一下。 |
| `FileActivatedEventArgs.Files` 是空的。 | 发送方用的 URI 方案不在你的 filter 之列。请确认 `DataSchemes` 中同时列出了 `"file"` 和 `"content"`。 |
| 启动时处理程序触发了两次。 | 你可能在构造函数和 `OnCreate` 重写里各注册了一遍。只在一处注册就好。 |

## 另请参阅 {#see-also}

- [Android 平台指南](/docs/platform-specific-guides/android)
- [在 Android 上部署](/docs/deployment/android)
- [Android intent filter 文档（developer.android.com）](https://developer.android.com/guide/components/intents-filters)

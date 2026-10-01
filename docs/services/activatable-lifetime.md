---
id: activatable-lifetime
title: 可激活生命周期
description: IActivatableLifetime 的 API 参考——该服务暴露应用的激活与停用事件，以及进出后台状态的方法。
doc-type: reference
---

[`IActivatableLifetime`](/api/avalonia/controls/applicationlifetimes/iactivatablelifetime) 服务定义了一组与应用激活、停用生命周期相关的方法和事件。`IActivatableLifetime` 是应用级的全局服务，可从应用实例上用 `TryGetFeature` 方法取得：

```csharp
Application.Current.TryGetFeature<IActivatableLifetime>();
```

## 事件 {#events}

### Activated

当应用因 `ActivationKind` 枚举所描述的各种缘由被 `Activated` 时引发的事件。

### Deactivated

当应用因 `ActivationKind` 枚举所描述的各种缘由被 `Deactivated` 时引发的事件。

## 方法 {#methods}

### TryLeaveBackground

要求应用尝试离开后台状态。

若在当前平台上可行则返回 `true`，否则返回 `false`。

**示例：**macOS 上的 `[NSApp unhide]`。

### TryEnterBackground

要求应用尝试进入后台状态。

若在当前平台上可行则返回 `true`，否则返回 `false`。

**示例：**macOS 上的 `[NSApp hide]`。

## 尽早订阅以捕获启动期事件 {#subscribing-early-for-startup-events}

若要接收应用启动时发生的激活事件（比如用户双击一个关联文件来启动应用），请在 `OnFrameworkInitializationCompleted` 内、任何 `await` 调用之前订阅 `Activated`。处理程序挂得太晚的话，启动激活事件可能早已触发并被错过。

```csharp
public override void OnFrameworkInitializationCompleted()
{
    if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktopLifetime)
    {
        desktopLifetime.MainWindow = new MainWindow();

        if (this.TryGetFeature<IActivatableLifetime>() is { } activatableLifetime)
        {
            activatableLifetime.Activated += (_, e) =>
            {
                if (e is ProtocolActivatedEventArgs protocolArgs)
                {
                    Console.WriteLine($"Protocol: {protocolArgs.Uri}");
                }
                else if (e is FileActivatedEventArgs fileArgs)
                {
                    Console.WriteLine($"File: {fileArgs.Files.FirstOrDefault()?.Path}");
                }
            };
        }
    }

    base.OnFrameworkInitializationCompleted();
}
```

:::caution
请为每种激活类型选用正确的事件参数类型：`ProtocolActivatedEventArgs` 对应 URI/深度链接激活（`ActivationKind.OpenUri`），`FileActivatedEventArgs` 对应文件关联激活（`ActivationKind.File`）。打开文件时若去判断 `ProtocolActivatedEventArgs` 是匹配不上的，看起来就像事件根本没触发。
:::

## 示例 {#examples}

### 进入与退出后台状态 {#entering-and-exiting-background-state}

你或许希望应用在后台时暂停或停掉某些处理，比如暂停多媒体播放，或者关掉周期性的 HTTP 请求。

```csharp
if (Application.Current?.TryGetFeature<IActivatableLifetime>() is { } activatableLifetime)
{
    activatableLifetime.Activated += (sender, args) =>
    {
        if (args.Kind == ActivationKind.Background)
        {
            Console.WriteLine($"App exited background");
        }
    };
    activatableLifetime.Deactivated += (sender, args) =>
    {
        if (args.Kind == ActivationKind.Background)
        {
            Console.WriteLine($"App entered background");
        }
    };
}
```

### 处理 URI 激活 {#handling-uri-activation}

你的应用可能需要支持协议激活，也就是人们常说的深度链接。链接方案必须在系统中注册并与应用关联；注册之后，操作系统便能把这些链接转交给应用。

典型用例是跳转到某个特定页面，或者构造 [OAuth 操作中的重定向 URL](https://www.oauth.com/oauth2-servers/oauth-native-apps/redirect-urls-for-native-apps/)。

```csharp
if (Application.Current?.TryGetFeature<IActivatableLifetime>() is { } activatableLifetime)
{
    activatableLifetime.Activated += (s, a) =>
   {
        if (a is ProtocolActivatedEventArgs protocolArgs && protocolArgs.Kind == ActivationKind.OpenUri)
        {
            Console.WriteLine($"App activated via Uri: {protocolArgs.Uri}");
        }
   };
}
```

:::note
有些平台需要额外改动清单文件才能启用协议处理。

**macOS 与 iOS：**在 `Info.plist` 中添加带 `CFBundleURLSchemes` 段的 `CFBundleURLTypes`。请见[创建应用自定义 URL 方案](https://rderik.com/blog/creating-app-custom-url-scheme/)（Swift 那部分可略过，`IActivatableLifetime` 已替你处理）。

**Android：**在 `AndroidManifest.xml` 中添加带特定 `android:scheme` 的 `intent-filter`。细节请见 [Android 上的深度链接](https://developer.android.com/training/app-links/deep-linking)（Kotlin/Java 那部分可略过，`IActivatableLifetime` 已替你处理）。
:::

### 处理文件激活 {#handling-file-activation}

你的应用可能需要处理文件激活：当操作系统启动你的应用或把它切到前台时（通常是因为用户打开了与之关联的文件）就会发生。与链接方案一样，文件类型关联也必须在系统中注册并与应用挂钩；注册之后，打开关联文件便会通过该事件顺带打开你的应用。

典型用例是打开文档、导入文件，或处理由系统 shell 传来的文件。

```csharp
if (Application.Current?.TryGetFeature<IActivatableLifetime>() is { } activatableLifetime)
{
    activatableLifetime.Activated += (s, a) =>
    {
        if (a is FileActivatedEventArgs fileArgs && fileArgs.Kind == ActivationKind.File)
        {
            foreach (var file in fileArgs.Files)
            {
                Console.WriteLine($"App activated via file: {file.Name}");
            }
        }
    };
}
```

:::note
有些平台需要额外改动清单文件才能启用文件类型关联。

**macOS 与 iOS：**在 `Info.plist` 中添加 `CFBundleDocumentTypes`，声明应用能处理哪些文件类型。细节请见 [Apple 文档](https://developer.apple.com/documentation/bundleresources/information_property_list/cfbundledocumenttypes)。

**Android：**在 `AndroidManifest.xml` 中添加一个带 `action.VIEW` 以及相应 `data` MIME 类型或文件扩展名的 `intent-filter`。细节请见 [Android 文档](https://developer.android.com/training/data-storage/shared/documents-files)（Kotlin/Java 那部分可略过，`IActivatableLifetime` 已替你处理）。
:::

## 平台兼容性 {#platform-compatibility}

| 特性        |  Windows | macOS | Linux | 浏览器 | Android |  iOS |
|---------------|-------|-------|-------|-------|-------|-------|
| `ActivationKind.Background` | ✖ | ✔ | ✖ | ✔ | ✔ | ✔ |
| `ActivationKind.File` | ✖ | ✔ | ✖ | ✖ | ✔ | ✔ |
| `ActivationKind.OpenUri` | ✖ | ✔ | ✖ | ✖ | ✔ | ✔ |
| `ActivationKind.Reopen` | ✖ | ✔ | ✖ | ✖ | ✖ | ✖ |
| `TryLeaveBackground`  | ✖ | ✔ | ✖ | ✖ | ✖ | ✖ |
| `TryEnterBackground` | ✖ | ✔ | ✖ | ✖ | ✔ | ✖ |

## 另请参阅 {#see-also}

- [IActivatableLifetime 的 issue 与讨论（#15316）](https://github.com/AvaloniaUI/Avalonia/issues/15316)

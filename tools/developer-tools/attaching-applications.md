---
id: attaching-applications
title: 挂接应用
doc-type: how-to
tags:
  - avalonia plus
  - avalonia pro
  - avalonia enterprise
---

## 挂接浏览器或移动端应用 {#attaching-browser-or-mobile-applications}

本页假设两端的应用部署在同一局域网或同一台机器上。远程连接请见[挂接到远程工具](/tools/developer-tools/attaching-to-the-remote-tool)。

:::note

各平台都可以把 `AvaloniaUI.DiagnosticsSupport` 包装进共享项目，`this.AttachDeveloperTools()` 代码也可以放在共享的 `Application` 类里。若某个平台需要特别的配置，可以借助 `OperatingSystem.IsPlatform` API。 

:::

## 挂接浏览器应用 {#attaching-browser-application}

1. 初次配置请按[快速上手](/tools/developer-tools/installation)操作。
2. 运行 `Developer Tools` 应用。也可以在命令行中使用 `avdt` 这个 dotnet 工具。
3. 通过 `dotnet run` 运行浏览器应用，或对已发布的项目使用 `dotnet serve`。更多细节请见 [Avalonia WebAssembly 文档](/docs/platform-specific-guides/webassembly)。
4. 浏览器项目默认在启动时挂接到 `Developer Tools`。详见 [DeveloperToolsOptions.ConnectOnStartup](/tools/developer-tools/options)。

![带开发者工具的浏览器](/img/tools/dev-tools/attaching-to-browser.png)

:::note

为避免与 Chrome 开发者工具冲突，Avalonia 工具的快捷键可以从 <kbd>F12</kbd> 改成自定义的组合键。详见 [DeveloperToolsOptions.Gesture](/tools/developer-tools/options)。

:::

## 挂接 iOS 应用 {#attaching-ios-application}


1. 初次配置请按[快速上手](/tools/developer-tools/installation)操作。
2. 运行 `Developer Tools` 应用。也可以在命令行中使用 `avdt` 这个 dotnet 工具。
3. 从你的 IDE 运行 iOS 应用。更多细节请见 [Avalonia iOS 文档](/docs/platform-specific-guides/ios)。
4. 确保浏览器应用处于焦点状态，这样快捷键才能被捕获。按 <kbd>F12</kbd>。

![带开发者工具的 iOS](/img/tools/dev-tools/attaching-to-ios.png)

## 挂接 Android 应用 {#attaching-android-application}

1. 初次配置请按[快速上手](/tools/developer-tools/installation)操作。
2. 重要：Android 默认不允许任何 HTTP 流量：
   1. 创建 `Resources/xml/network_security_config.xml` 文件：
   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <network-security-config>
     <domain-config cleartextTrafficPermitted="true">
       <domain includeSubdomains="true">10.0.2.2</domain> <!-- Debug address -->
     </domain-config>
   </network-security-config>
   ```
   2. 在 AndroidManifest.xml 文件中更新 `<application>` xml 节点：
   ```xml
   <application android:networkSecurityConfig="@xml/network_security_config">
   ```
   3. 更多细节请见 https://devblogs.microsoft.com/xamarin/cleartext-http-android-network-security/
   4. 本仓库中的 `SimpleToDoList.Android` 项目也作了同样的改动，可供参考。
3. 运行 `Developer Tools` 应用。也可以在命令行中使用 `avdt` 这个 dotnet 工具。
4. 从你的 IDE 运行 Android 应用。更多细节请见 [Avalonia Android 文档](/docs/platform-specific-guides/android)。
5. Android 项目默认在启动时挂接到 `Developer Tools`。详见 [DeveloperToolsOptions.ConnectOnStartup](/tools/developer-tools/options)。

![带开发者工具的 Android](/img/tools/dev-tools/attaching-to-android.png)

:::note

在 Android 上默认的 IP 地址是 `10.0.2.2` 而非 `localhost`，模拟器会把它映射到宿主机。要覆盖它，请见 [DeveloperToolsOptions.Protocol](/tools/developer-tools/options)。

:::

## 挂接 WSL2 中的应用 {#attaching-wsl2-application}

WSL2 让你能从 Windows 宿主机调试和运行 Linux 应用。
你当然可以照搬同一套说明，在 WSL2 系统里也装一整套开发者工具，但这样就与 Windows 上的那份重复了。

为图省事、只保留一份安装，推荐把跑在 Linux 上的应用挂接到 Windows 上运行的开发者工具实例。

1. 初次配置和 nuget 包安装请按[快速上手](/tools/developer-tools/installation)操作。
2. WSL2 机器只需配置一次：

    - （推荐）按[镜像模式网络](https://learn.microsoft.com/en-us/windows/wsl/networking#mirrored-mode-networking)文档所述，启用 WSL2 的镜像模式网络。这种模式下 WSL 实例可以直接访问 Windows 的 `localhost`，无需额外配置，也不用改代码。

    - （备选）按 WSL2 文档[从 Linux 访问 Windows 网络应用（宿主机 IP）](https://learn.microsoft.com/en-us/windows/wsl/networking#accessing-windows-networking-apps-from-linux-host-ip)取得 Windows 宿主机的 IP 地址，然后把它用在你的 `AttachDeveloperTools` 选项里：

    ```csharp
    this.AttachDeveloperTools(o =>
    {
        o.Protocol = DeveloperToolsProtocol.CreateHttp(IPAddress.Parse("YOUR_LOCAL_NETWORK_HOST_IP"));
    });
    ```

3. 在 Windows 宿主机上运行 `Developer Tools` 实例，一般是通过 `avdt` 这个 dotnet 工具的命令行。
4. 运行你的 Linux 应用，并用 <kbd>F12</kbd> 挂接到 `Developer Tools`。

![挂接到 WSL2](/img/tools/dev-tools/attaching-wsl.png)
## 另请参阅 {#see-also}

- [挂接到远程工具](/tools/developer-tools/attaching-to-the-remote-tool)
- [安装开发者工具](/tools/developer-tools/installation)

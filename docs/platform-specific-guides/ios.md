---
id: ios
title: iOS
---

import IOSOpenXcodeScreenshot from '/img/guides/platform-specific-guides/ios/ios-open-xcode.png';
import IOSCreateXcodeProjectScreenshot from '/img/guides/platform-specific-guides/ios/ios-create-xcode-project.png';
import IOSSelectProjectOptionsScreenshot from '/img/guides/platform-specific-guides/ios/ios-select-project-options.png';
import IOSSelectAnyDeviceScreenshot from '/img/guides/platform-specific-guides/ios/ios-select-any-device.png';
import IOSAddAdditionalSimulatorsScreenshot from '/img/guides/platform-specific-guides/ios/ios-add-additional-simulators.png';
import IOSProvisionPhoneScreenshot from '/img/guides/platform-specific-guides/ios/ios-provision-phone.png';
import IOSSelectDeviceScreenshot from '/img/guides/platform-specific-guides/ios/ios-select-device.png';
import IOSCertScreenshot from '/img/guides/platform-specific-guides/ios/ios-cert.png';

## 搭建开发环境 {#setting-up-your-developer-environment}

### 前置条件 {#prerequisites}

在 Mac 上，你需要装好最新版的 macOS 和 Xcode。

### 安装 SDK {#install-the-sdk}

首先，装对 [dotnet SDK](https://dotnet.microsoft.com/en-us/download/dotnet/6.0)非常要紧。撰写本文时，可用的最低 SDK 版本是 6.0.200。

### 安装工作负载 {#install-the-workload}

```bash
dotnet workload install ios
```

:::info
这条命令可能需要加 `sudo` 运行\
\
你也许还得先卸掉旧版本。`dotnet workload remove ios`
:::

这样你就能在任意平台上构建 iOS 应用了。不过要测试和运行它们，还是得有装了 Xcode 的真实 macOS 设备。

## 用 Xcode 为设备配置预置描述 {#provisioning-a-device-with-xcode}

要部署到真实的 iPhone 或 iPad，你必须先用 Xcode 为设备做预置：这会生成一份签名证书，并把你的设备关联到开发预置描述文件上。

继续之前，请照着这份[创建免费 Apple 开发者签名证书的指南](https://docs.microsoft.com/en-us/xamarin/ios/get-started/installation/device-provisioning/free-provisioning)操作。

你需要建一个 Xcode 应用项目，其 `bundle identifier` 要与你将在 Avalonia 应用中使用的一致。

1. Open Xcode

<Image light={IOSOpenXcodeScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

2. 选择 Create a new Xcode project

<Image light={IOSCreateXcodeProjectScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

3. 选择 iOS 和 App，点 Next。

<Image light={IOSSelectProjectOptionsScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

4. 填写项目名称和组织名，其余信息保持默认。

5. 选个目录保存项目。这个项目之后用不着，所以存哪儿不必太在意。

6. 点击顶部状态栏里的 "Any device (arm64)"

<Image light={IOSSelectAnyDeviceScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

7. 在列表底部点击 "Add Additional Simulators..."

<Image light={IOSAddAdditionalSimulatorsScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

8. 点击 devices，用 USB 线连上你的 iPhone 或 iPad。Xcode 会开始为设备做开发预置。

<Image light={IOSProvisionPhoneScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

9. 从设备列表中选中你的 iPhone 或 iPad。

<Image light={IOSSelectDeviceScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

10. 点击播放按钮，应用就会被安装到手机上并运行。

若一切顺利，你的设备就完成开发预置了。要找到代码签名密钥，请打开 **Keychain Access** 应用，搜索 "development"。

<Image light={IOSCertScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

选中的开发证书窗口顶部那行粗体文字，就是你的签名密钥值（例如 `Apple Development: dan@walms.co.uk (3L323F7VSS)`）。

## Mac Catalyst

有了 Mac Catalyst，你不必另写一个 macOS 项目，就能让 Avalonia 的 iOS 应用跑在 macOS 上。当你的应用重度依赖 UIKit API，或者想把 Avalonia 嵌进 MAUI 混合应用（其 macOS 桌面支持正是靠 Catalyst）时，这招很有用。

:::note
若是做原生 macOS 开发，仍推荐使用 Avalonia 基于 AppKit 的后端：它不经 Catalyst 转译层，直接用上 macOS 的窗口系统、Metal 渲染和原生菜单。详见 [macOS 平台指南](/docs/platform-specific-guides/macos)。
:::

### 配置 Mac Catalyst {#setting-up-mac-catalyst}

1. 安装 Mac Catalyst 工作负载：

```bash
dotnet workload install maccatalyst
```

2. 把 `net10.0-maccatalyst` 加进 iOS 项目的目标框架：

```xml
<PropertyGroup>
    <TargetFrameworks>net10.0-ios;net10.0-maccatalyst</TargetFrameworks>
</PropertyGroup>
```

3. 面向 Mac Catalyst 构建并运行：

```bash
dotnet build -f net10.0-maccatalyst
dotnet run -f net10.0-maccatalyst
```

应用会借助 Apple 的 Catalyst 转译层以原生 macOS 应用的形式运行：它会出现在程序坞中、支持 macOS 的窗口管理，也可以通过 Mac App Store 分发。

### Mac Catalyst 与默认 macOS 后端该怎么选 {#when-to-use-mac-catalyst-vs-the-default-macos-backend}

对多数 Avalonia 应用来说，默认的 macOS 后端（Avalonia Native）是更好的选择。它用一个轻量的原生库（`libAvaloniaNative.dylib`）提供窗口、输入、渲染、菜单和无障碍支持，不依赖 .NET 的 macOS 或 Catalyst 工作负载。这意味着你在 Windows 或 Linux 上就能构建、打包并签名 macOS 应用，开发全程不需要 Mac。详见 [Avalonia 在 macOS 上如何运行](/docs/platform-specific-guides/macos#how-avalonia-runs-on-macos)。

Mac Catalyst 的适用面要窄一些，主要针对两类场景：与 UIKit API 深度捆绑的应用，以及内嵌在 MAUI 混合项目里的应用（后者的 macOS 目标正是用 Catalyst）。这些情况下，Catalyst 让你直接复用 iOS 项目，而不必再维护一个独立的 macOS 入口。

| 考量点 | 默认 macOS 后端 | Mac Catalyst |
|---|---|---|
| 可在 Windows 或 Linux 上构建 | Yes | 不可（需要 macOS） |
| 需要的 .NET 工作负载 | 无（`net10.0` 就够了） | `maccatalyst` workload |
| 可用的原生 API 范围 | 极简（只覆盖界面必需的部分） | 经 Catalyst 转译的 UIKit 子集 |
| 与 iOS 共用项目 | 否（另有 Desktop 项目） | 是（同一个 iOS 项目） |
| 嵌入 MAUI 混合应用 | No | Yes |
| 新 Avalonia 应用是否推荐 | Yes | No |

## 深度链接与通用链接 {#deep-linking-and-universal-links}

iOS 支持两种从 URL 打开应用的机制：

### 自定义 URL 方案 {#custom-url-schemes}

在 `Info.plist` 中加入 `CFBundleURLTypes`，即可注册自定义 URL 方案（比如 `myapp://`）：

```xml
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleURLName</key>
        <string>MyApp</string>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>myapp</string>
        </array>
    </dict>
</array>
```

### 通用链接 {#universal-links}

通用链接把你的应用与某个 Web 域名关联起来，于是普通的 `https://` URL 也能直接打开应用。配置办法如下：

1. 为应用添加 Associated Domains 权利。新建或修改 `Entitlements.plist`：
   ```xml
   <key>com.apple.developer.associated-domains</key>
   <array>
       <string>applinks:example.com</string>
   </array>
   ```
2. 在你的 Web 服务器上把 `apple-app-site-association` 文件托管到 `https://example.com/.well-known/apple-app-site-association`。

### 处理激活 {#handling-activation}

无论是自定义 URL 方案还是通用链接，都会在 `IActivatableLifetime` 上引发 `Activated` 事件，其 `ActivationKind.OpenUri`：

```csharp
if (Application.Current.TryGetFeature<IActivatableLifetime>() is { } activatableLifetime)
{
    activatableLifetime.Activated += (s, a) =>
    {
        if (a is ProtocolActivatedEventArgs protocolArgs
            && protocolArgs.Kind == ActivationKind.OpenUri)
        {
            // Handle the URI
            var uri = protocolArgs.Uri;
        }
    };
}
```

这套做法适用于 Avalonia 12 采用的基于 scene 的生命周期。完整 API 参考见[可激活生命周期](/docs/services/activatable-lifetime)。

## 另请参阅 {#see-also}

- [在 iOS 上部署](/docs/deployment/ios)（模拟器、真机与发布）
- [macOS 平台指南](/docs/platform-specific-guides/macos)（原生 AppKit 后端）
- [可激活生命周期](/docs/services/activatable-lifetime)——处理 URI、文件和后台激活
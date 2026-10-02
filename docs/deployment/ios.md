---
id: ios
title: iOS
description: 为 iPhone、iPad 和 Mac Catalyst 构建、签名并分发 Avalonia 应用。
doc-type: how-to
---

## 在模拟器上运行 {#running-on-a-simulator}

在 iOS 项目目录下，用这条命令构建并运行：

```bash
dotnet build
dotnet run
```

这会把应用部署到默认的 iOS 模拟器。若你用的是 JetBrains Rider 或 Visual Studio for Mac，可以直接在 IDE 里运行、构建和调试。

:::info
视 .NET 版本和 iOS 模拟器版本而定，Apple Silicon 的 Mac 上可能需要 Rosetta 2。安装方法：

```bash
/usr/sbin/softwareupdate --install-rosetta
```
:::

## 在真机上运行 {#running-on-a-device}

要部署到实体 iPhone 或 iPad，必须先用 Xcode 为设备作预置：创建签名证书，并把设备与开发预置描述文件关联起来。

用 Xcode 预置设备的详细步骤（包括如何创建免费的 Apple 开发者签名证书），请参阅 [iOS 平台配置指南](/docs/platform-specific-guides/ios)。

设备预置完成后，编辑 `.iOS.csproj`，设置运行时标识和代码签名密钥：

```xml
<RuntimeIdentifier>ios-arm64</RuntimeIdentifier>
<CodesignKey>Apple Development: yourname@example.com (XXXXXXXXXX)</CodesignKey>
```

然后照常构建运行，应用就会部署到你连接的设备上。

## 发布 {#publishing}

为 iOS 发布 Avalonia 应用会生成一个 `.ipa` 文件，也就是可供分发的 iOS 应用归档。分发 iOS 应用要求用预置描述文件签名，该文件包含代码签名信息和预期的分发方式。

### 前置条件 {#prerequisites}

- 一台装有 Xcode 的 Mac（iOS 应用必须在 macOS 上构建）
- [Apple Developer Program](https://developer.apple.com/programs/) 会员资格（分发必需）
- 在 Xcode 中配置好的预置描述文件和签名证书

### 分发方式 {#distribution-options}

苹果提供三种分发 iOS 应用的途径：

- **App Store**：通过 [App Store Connect](https://appstoreconnect.apple.com) 提交，应用需经苹果审核通过。这是触达终端用户最常见的方式。
- **Ad-hoc**：分发给至多 100 台已注册设备用于测试，面向 Apple Developer Program 会员开放。
- **企业内部（Enterprise）**：在组织内部分发，需要 [Apple Developer Enterprise Program](https://developer.apple.com/programs/enterprise/) 会员资格。

无论哪种方式，应用都必须用相应的预置描述文件签名。

### 构建并签名你的应用 {#build-and-sign-your-app}

#### 在 macOS 上发布 {#publishing-from-macos}

进入 iOS 项目文件夹，运行 `dotnet publish`：

```bash
dotnet publish -f net9.0-ios -c Release \
  -p:ArchiveOnBuild=true \
  -p:RuntimeIdentifier=ios-arm64 \
  -p:CodesignKey="Apple Distribution: John Smith (AY2GDE9QM7)" \
  -p:CodesignProvision="MyAvaloniaApp"
```

这会完成构建和签名，并在 `bin/Release/net9.0-ios/ios-arm64/publish/` 中生成 `.ipa`。

具体走哪条分发渠道，取决于你预置描述文件里的分发证书（App Store、Ad Hoc 或 Enterprise）。

#### 在 Windows 上发布 {#publishing-from-windows}

在 Windows 上构建 iOS 应用，需要一台网络可达的 Mac 构建主机。把连接信息作为额外参数传入：

```bash
dotnet publish -f net9.0-ios -c Release \
  -p:ArchiveOnBuild=true \
  -p:RuntimeIdentifier=ios-arm64 \
  -p:CodesignKey="Apple Distribution: John Smith (AY2GDE9QM7)" \
  -p:CodesignProvision="MyAvaloniaApp" \
  -p:ServerAddress=192.168.1.100 \
  -p:ServerUser=macuser \
  -p:ServerPassword=mypassword \
  -p:TcpPort=58181 \
  -p:_DotNetRootRemoteDirectory=/Users/macuser/Library/Caches/Xamarin/XMA/SDKs/dotnet/
```

### 构建属性参考 {#build-properties-reference}

下列属性既可以在命令行上用 `-p:` 传入，也可以写在项目文件的 `<PropertyGroup>` 中：

| 属性 | 说明 |
|---|---|
| `ArchiveOnBuild` | 设为 `true` 以产出 `.ipa`。 |
| `RuntimeIdentifier` | 目标运行时，请用 `ios-arm64`。 |
| `CodesignKey` | 代码签名密钥的名称（比如 `Apple Distribution: Name (ID)`）。 |
| `CodesignProvision` | 签名时要用的预置描述文件名称。 |
| `CodesignEntitlements` | entitlements 文件的路径（如有需要）。 |
| `ApplicationTitle` | 应用对用户显示的名称。 |
| `ApplicationId` | 唯一标识，比如 `com.companyname.myapp`。 |
| `ApplicationVersion` | 构建版本号。 |
| `ApplicationDisplayVersion` | 显示用的版本字符串。 |

#### 把属性写进项目文件 {#define-properties-in-your-project-file}

与其把一堆参数都敲在命令行上，不如把它们写进 `.csproj`：

```xml
<PropertyGroup Condition="$(TargetFramework.Contains('-ios')) and '$(Configuration)' == 'Release'">
    <ArchiveOnBuild>true</ArchiveOnBuild>
    <CodesignKey>Apple Distribution: John Smith (AY2GDE9QM7)</CodesignKey>
    <CodesignProvision>MyAvaloniaApp</CodesignProvision>
</PropertyGroup>
```

然后只需这样发布：
```bash
dotnet publish -f net9.0-ios -c Release
```

### 分发应用 {#distribute-the-app}

- **App Store**：用 [Transporter](https://apps.apple.com/us/app/transporter/id1450874784?mt=12) 或 Xcode 上传 `.ipa`。你需要先在 [App Store Connect](https://appstoreconnect.apple.com) 中创建应用记录，并生成一个 [App 专用密码](https://support.apple.com/HT204397)。
- **Ad-hoc**：用 [Apple Configurator](https://apps.apple.com/app/id1037126344) 分发。
- **企业内部**：通过安全网站或移动设备管理（MDM）分发，详见 [Distribute proprietary in-house apps](https://support.apple.com/guide/deployment/depce7cefc4d/web)。

## 部署 Mac Catalyst {#mac-catalyst-deployment}

如果你的 iOS 项目以 Mac Catalyst（`net10.0-maccatalyst`）为目标，那么同一个项目就能构建并发布 macOS 版本。配置方法请参阅 iOS 平台指南中的 [Mac Catalyst](/docs/platform-specific-guides/ios#mac-catalyst)。

发布 Mac Catalyst 应用：

```bash
dotnet publish -f net10.0-maccatalyst -c Release
```

Mac Catalyst 应用既可以通过 Mac App Store 分发，也可以作为已签名的 `.app` 包分发。签名和分发流程与 iOS 如出一辙，同样使用 Apple Developer 证书和预置描述文件。

## 另请参阅 {#see-also}

- [iOS 平台配置](/docs/platform-specific-guides/ios)

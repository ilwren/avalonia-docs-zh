---
id: macos
title: macOS Deployment
description: 如何在 macOS 上发布和部署 XPF 应用，包括应用包结构与代码签名。
---

## 发布 {#publishing}

从命令行把 XPF 应用发布为 macOS 版本：

```bash
dotnet publish -r osx-arm64 -c Release --self-contained
```

面向 Intel Mac：

```bash
dotnet publish -r osx-x64 -c Release --self-contained
```

:::caution
务必从命令行发布。用 Visual Studio 发布可能产出不完整的输出，缺掉原生库。
:::

## 应用包结构 {#app-bundle-structure}

macOS 应用必须打成 `.app` 包才能分发。`.app` 包其实就是一个具有如下结构的目录：

```text
MyApp.app/
  Contents/
    Info.plist
    MacOS/
      MyApp          (executable or launch script)
    Resources/
      MyApp.icns     (application icon)
```

### Info.plist

创建一个写有应用元数据的 `Info.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>MyApp</string>
    <key>CFBundleDisplayName</key>
    <string>My Application</string>
    <key>CFBundleIdentifier</key>
    <string>com.yourcompany.myapp</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleExecutable</key>
    <string>MyApp</string>
    <key>CFBundleIconFile</key>
    <string>MyApp.icns</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
```

## 项目设置 {#project-settings}

下列 `.csproj` 设置对 macOS 部署颇为要紧：

```xml
<PropertyGroup>
    <SelfContained>true</SelfContained>
    <RuntimeIdentifier>osx-arm64</RuntimeIdentifier>
</PropertyGroup>
```

:::danger
**不要**把 `IncludeNativeLibrariesForSelfExtract` 设为 `true`。它与 macOS 不兼容，会让你的应用在运行时报 “Failed to create CoreCLR” 而崩掉。
:::

## 代码签名 {#code-signing}

所有 macOS 应用都必须经过代码签名才能分发。为 XPF 应用签名时：

- **逐个文件签名**，而不是整包一签。不要给 `codesign` 加 `--deep` 标志，那样可能漏掉文件或套上错误的权利。
- 先把所有 `.dylib` 文件和主可执行文件签完，再签 `.app` 包。

```bash
# Sign individual binaries first
find MyApp.app -name "*.dylib" -exec codesign --force --sign "Developer ID Application: Your Name" {} \;
codesign --force --sign "Developer ID Application: Your Name" MyApp.app/Contents/MacOS/MyApp

# Then sign the bundle
codesign --force --sign "Developer ID Application: Your Name" MyApp.app
```

## Notarization

若在 Mac App Store 之外分发，Apple 要求应用经过公证。请使用 `notarytool`：

```bash
# Create a ZIP for notarization
ditto -c -k --keepParent MyApp.app MyApp.zip

# Submit for notarization
xcrun notarytool submit MyApp.zip --apple-id "you@example.com" \
    --team-id "YOUR_TEAM_ID" --password "app-specific-password" --wait

# Staple the notarization ticket
xcrun stapler staple MyApp.app
```

## 生成 DMG {#dmg-creation}

若要以 `.dmg` 磁盘映像的形式分发：

```bash
hdiutil create -volname "MyApp" -srcfolder MyApp.app -ov MyApp.dmg
```

## Parcel (Preview)

Avalonia 的 **Parcel** 工具可以把整套 macOS 打包流程自动化，包括为 XPF 应用生成 `.app` 包、代码签名、公证以及生成 `.dmg`。想试用预览版请联系 Avalonia 团队。

## Dock 中的可见性 {#dock-visibility}

若要控制应用是否出现在 macOS 的 Dock 中，请见 [macOS：Dock 可见性](/xpf/platforms/macos#dock-visibility)。

## 应用名称 {#application-name}

若要设定 macOS 菜单栏中显示的名称（而非 “Avalonia Application”），请见 [macOS：应用名称](/xpf/platforms/macos#application-name)。

## ReadyToRun

启用 ReadyToRun 让启动更快：

```xml
<PropertyGroup>
    <PublishReadyToRun>true</PublishReadyToRun>
</PropertyGroup>
```

细节请见[性能优化](/xpf/configuration/performance#reducing-startup-time-with-readytorun)。

---
id: macos
title: macOS 问题
sidebar_label: macOS
---

## 应用菜单 {#app-menu}

#### 应用菜单里出现 _About Avalonia_ 菜单项 {#app-menu-shows-about-avalonia-menu-item}

这多半说明你的应用没有指定菜单。启动时 Avalonia 会为应用创建默认菜单项，一旦没有配置过菜单，它就会自动补上 _About Avalonia_ 这一项。在你的 `App.xaml` 中加一个菜单即可解决：

```xml
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:local="using:RoadCaptain.App.RouteBuilder"
             x:Class="RoadCaptain.App.RouteBuilder.App">
	<NativeMenu.Menu>
		<NativeMenu>
			<NativeMenuItem Header="About MyApp" Click="AboutMenuItem_OnClick" />
		</NativeMenu>
	</NativeMenu.Menu>
</Application>
```

macOS 其余的默认菜单项仍由 Avalonia 生成。

#### 菜单栏中的应用名对不上 {#application-name-in-menu-bar-does-not-match}

从应用包启动应用时，菜单栏显示的应用名取自包中的 `Info.plist`，而不是 `App.xaml` 中的 `Name` 属性。

若名字对不上，请核对 `CFBundleName`、`CFBundleDisplayName` 和 `Name` 属性三者的值是否一致。

注意 `CFBundleName` 最长只有 15 个字符，若你的应用名更长，就_必须_设置 `CFBundleDisplayName`。

关于 macOS 究竟从哪儿读取应用名，完整说明请见[应用名称与标识](/docs/platform-specific-guides/macos#application-name-and-identity)。

## 打包 {#packaging}

1. 查看 Parcel 的构建日志，从中找出错误信息
2. 对照 [Apple 应用包编程指南](https://developer.apple.com/library/archive/documentation/CoreFoundation/Conceptual/CFBundles/Introduction/Introduction.html)核对应用包的各项要求

## 代码签名 {#code-signing}

### 常见问题 {#common-issues}

#### 创建证书时没有 “Developer ID Application” 这一项 {#developer-id-application-not-available-when-creating-a-certificate}

该选项需要 Apple Developer 账户的团队成员资格，请联系你们团队的账户持有人开通权限。

#### 签名成功了，但在别的机器上跑不起来 {#app-signs-successfully-but-cannot-execute-on-other-machines}

请确认你用的是 “Developer ID Application” 证书。“Apple Development” 证书只适用于开发构建。

### 其他代码签名问题 {#other-code-signing-issues}

若问题不在上述之列：

1. 查看 Parcel 的签名日志，从中找出错误信息
2. 到 Apple Developer 门户核对证书状态

## Notarization

### 常见问题 {#common-issues-1}

#### 公证耗时过长 {#notarization-takes-too-long}

公证通常几分钟就好，但高峰期可能要等上一小时。最糟的情况下，视应用大小可能要等好几个小时。

#### 报错 “Invalid credentials” {#invalid-credentials-error}

- 核对 Apple ID 和 App 专用密码是否正确
- 确认 Team ID 没有填错
- 检查 Apple Developer 账户的状态

#### 报错 “License agreement must be accepted” {#license-agreement-must-be-accepted-error}

- 用浏览器登录 [Apple Developer 账户](https://developer.apple.com/account/)
- 看看有没有待处理的协议或通知
- 把新的许可协议或服务条款都接受掉
- 接受后稍等几分钟再重试
- Apple 开发者计划更新或政策调整之后，这种情况颇为常见

#### 公证在上传阶段失败 {#notarization-fails-during-upload}

- 检查你的网络连接

### 其他公证问题 {#other-notarization-issues}

若问题不在上述之列：

1. 参阅 Apple 的[分发前为 macOS 软件做公证](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution)指南
2. 查看 Parcel 输出中的公证日志
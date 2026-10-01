---
id: versioning
title: XPF 版本管理
description: 了解如何选择和配置 XPF 的包版本，包括稳定版和夜间构建。
doc-type: how-to
---

## 选择版本 {#choosing-a-version}

正式发布请用最新的稳定版，各稳定版的详情可在[发行说明](/xpf/version-info/release-notes)中查到。日常开发中，你或许更愿意跟进最新的夜间构建，好早点用上新功能和缺陷修复。

所有可用版本都可在 [XPF NuGet 服务器](https://xpf-nuget-feed.avaloniaui.net/packages/xpf.sdk)上浏览。

## 访问 NuGet 源 {#accessing-the-nuget-feed}

XPF 的 NuGet 源需要认证。登录网页门户或配置 NuGet 客户端时，请使用以下凭据：

- **Username:** `license`
- **密码：**你的 XPF 许可证密钥

把该源加进 `NuGet.config` 文件时也要填上这组凭据，这样 `dotnet restore` 和 Visual Studio 才能自动拉取包。

## 为夜间构建配置源 {#configuring-feeds-for-nightly-builds}

XPF 的夜间构建可能依赖 Avalonia 的预发布版本。为确保所有依赖都能正确解析，请把下列包源加进你的 `NuGet.config` 文件（完整配置见[快速上手第 2 步](/xpf/getting-started#step-2-add-a-nugetconfig)）：

```xml
<add key="api.nuget.org" value="https://api.nuget.org/v3/index.json" />
<add key="xpf" value="https://xpf-nuget-feed.avaloniaui.net/v3/index.json" />
<add key="avalonia-nightly" value="https://nuget-feed-all.avaloniaui.net/v3/index.json" />
```

只有在使用 XPF 夜间构建时才需要 `avalonia-nightly` 这个源。若你用的是 XPF 稳定版，可以不加它。

## 钉死某个特定版本 {#pinning-a-specific-version}

要把项目锁定到某个 XPF 版本，请在项目文件或 `Directory.Build.props` 中设置 `XpfVersion` 属性：

```xml
<PropertyGroup>
  <XpfVersion>1.6.0</XpfVersion>
</PropertyGroup>
```

钉死版本可以避免意外升级，也能确保团队里每个人构建时用的都是同一批包。

## 另请参阅 {#see-also}

- [发行说明](/xpf/version-info/release-notes)
- [尚未支持的特性](/xpf/version-info/missing-features)
- [快速上手](/xpf/getting-started)

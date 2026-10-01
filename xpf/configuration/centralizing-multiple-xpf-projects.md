---
id: centralizing-multiple-xpf-projects
title: 集中管理多个 XPF 项目
description: 了解如何在单个仓库中集中管理多个项目的 XPF SDK 版本与许可证密钥配置。
doc-type: how-to
---

当你在一个仓库里管着多个 XPF 项目时，要让每个 `.csproj` 文件里的 SDK 版本和许可证密钥都保持同步，既烦琐又容易出错。把这些设置集中起来，既保证了一致性，日后升级也省心。

## 集中管理 XPF SDK 版本 {#centralize-the-xpf-sdk-version}

你可以在仓库根目录放一个 `global.json` 文件，一次性钉死所有项目的 XPF SDK 版本。只要存在针对 `Xpf.Sdk` 的 `global.json` 条目，MSBuild 就会自动解析出该版本，于是你只需在一个地方改版本号。

在仓库根目录创建（或更新）一个 `global.json` 文件：

```json title="global.json"
{
  "msbuild-sdks": {
    "Xpf.Sdk": "1.6.0"
  }
}
```

然后在各个 `.csproj` 文件中引用 `Xpf.Sdk`，**不要**写版本号：

```xml title="MyApp.csproj"
<Project Sdk="Xpf.Sdk">
```

需要升级时，只改 `global.json` 里的版本，仓库中所有项目下次构建时便会用上新版本。

## 许可证密钥 {#license-keys}

把许可证密钥直接写进受版本控制的文件里有安全隐患。更稳妥的做法是在 `NuGet.config` 和 `.csproj` 文件中引用一个环境变量，让真正的密钥值永远不出现在仓库中。

:::tip
环境变量叫什么都行，下面的示例用的是 `XpfLicenseKey`。
:::

### 设置环境变量 {#set-the-environment-variable}

添加一个名为 `XpfLicenseKey` 的环境变量，值就是你的许可证密钥：

- **Windows**：在开始菜单里搜 “环境变量”，通过系统界面添加。
- **macOS**：运行 `launchctl setenv XpfLicenseKey [LICENSE_KEY]`。每次重启后都得重新跑一遍。
- **Linux**：环境变量通常设在 `.bash_profile`、`.bashrc` 或 `/etc/environment` 里。

创建或修改变量之后，请重启所有已打开的终端会话和 IDE，好让它们读到新值。

### Update `nuget.config`

编辑 `nuget.config` 文件的凭据小节，改为引用该环境变量：

```xml title="nuget.config"
<packageSourceCredentials>
  <xpf>
    <add key="Username" value="license" />
    <add key="ClearTextPassword" value="%XpfLicenseKey%" />
  </xpf>
</packageSourceCredentials>
```

### 更新 `.csproj` 文件 {#update-csproj-files}

编辑每个 `.csproj` 文件中的 `RuntimeHostConfigurationOption` 条目，让它从环境变量读取密钥：

```xml title="MyApp.csproj"
<ItemGroup>
  <RuntimeHostConfigurationOption Include="AvaloniaUI.Xpf.LicenseKey"
                                  Value="$(XpfLicenseKey)" />
</ItemGroup>
```

## 另请参阅 {#see-also}

- [XPF 快速上手](/xpf/getting-started)
- [定制初始化](/xpf/configuration/customizing-initialization)
- [性能配置](/xpf/configuration/performance)
- [Versioning](/xpf/version-info/versioning)
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

Storing license keys directly in source-controlled files is a security risk. Instead, you can reference an environment variable in both your `NuGet.config` and `.csproj` files so the actual key value never appears in your repository.

:::tip
You can name the environment variable anything you like. The examples below use `XpfLicenseKey`.
:::

### Set the environment variable

Add an environment variable called `XpfLicenseKey` whose value is your license key:

- **Windows**: search the Start menu for "Environment Variables" and add the variable through the system GUI.
- **macOS**: run `launchctl setenv XpfLicenseKey [LICENSE_KEY]`. You will need to re-run this command after each reboot.
- **Linux**: environment variables are commonly set in `.bash_profile`, `.bashrc`, or `/etc/environment`.

After you create or change the variable, restart any open terminal sessions and IDEs so they pick up the new value.

### Update `nuget.config`

Edit the credentials section of your `nuget.config` file to reference the environment variable:

```xml title="nuget.config"
<packageSourceCredentials>
  <xpf>
    <add key="Username" value="license" />
    <add key="ClearTextPassword" value="%XpfLicenseKey%" />
  </xpf>
</packageSourceCredentials>
```

### Update `.csproj` files

Edit the `RuntimeHostConfigurationOption` entry in each `.csproj` file to read the key from the environment variable:

```xml title="MyApp.csproj"
<ItemGroup>
  <RuntimeHostConfigurationOption Include="AvaloniaUI.Xpf.LicenseKey"
                                  Value="$(XpfLicenseKey)" />
</ItemGroup>
```

## 另请参阅 {#see-also}

- [Getting started with XPF](/xpf/getting-started)
- [Customizing initialization](/xpf/configuration/customizing-initialization)
- [Performance configuration](/xpf/configuration/performance)
- [Versioning](/xpf/version-info/versioning)
---
id: linux
title: Linux Deployment
description: 如何在 Linux 上发布和部署 XPF 应用，包括所需的原生库和运行时依赖。
---

## 发布 {#publishing}

发布 XPF 应用请一律走命令行。用 Visual Studio 发布可能产出不完整的输出，缺掉 `libSkiaSharp.so` 这类原生库。

```bash
dotnet publish -r linux-x64 -c Release
```

自包含部署：

```bash
dotnet publish -r linux-x64 -c Release --self-contained
```

ARM64 设备：

```bash
dotnet publish -r linux-arm64 -c Release --self-contained
```

## 运行时依赖 {#runtime-dependencies}

请确认目标系统上装了下列软件包。

### Debian / Ubuntu

```bash
sudo apt install libice6 libsm6 libfontconfig1 libgdiplus
```

### Fedora

```bash
sudo dnf install libICE libSM fontconfig libgdiplus
```

### RHEL / CentOS / Rocky Linux

```bash
sudo dnf install epel-release
sudo dnf install libICE libSM fontconfig libgdiplus
```

若要支持 WebView，还需装 `libwebkit2gtk-4.1-dev`（Debian/Ubuntu）或 `webkit2gtk4.1-devel`（Fedora/RHEL）。

细节请见 [Linux：其他依赖](/xpf/platforms/linux#other-dependencies)。

## ReadyToRun

ReadyToRun（R2R）编译把程序集预先编译成本机代码，启动时间因此大幅缩短。在嵌入式 Linux 设备上尤其划算。

```xml
<PropertyGroup>
    <PublishReadyToRun>true</PublishReadyToRun>
</PropertyGroup>
```

```bash
dotnet publish -r linux-x64 -c Release --self-contained
```

:::note
ReadyToRun 可能改变原生 `.so` 库的解析方式。细节请见 [Linux：原生库解析](/xpf/platforms/linux#native-library-resolution-with-readytorun)。
:::

## 依赖框架 vs 自包含 {#framework-dependent-vs-self-contained}

**依赖框架**（默认）：要求目标机器上装有 .NET，部署包更小。

**自包含**：把 .NET 运行时一并带上，包更大，但除系统库外别无外部依赖。面向最终用户分发时推荐这种。

```bash
# Framework-dependent
dotnet publish -r linux-x64 -c Release

# Self-contained
dotnet publish -r linux-x64 -c Release --self-contained
```

## 打包格式 {#packaging-formats}

### AppImage

AppImage 把你的应用打成单个可执行文件。可以用 [appimage-builder](https://appimage-builder.readthedocs.io/) 之类的工具，也可以手动把发布输出打进 AppImage。

### Debian 包（.deb） {#debian-package-deb}

面向基于 Debian 的发行版，可制作 `.deb` 包。用 `dpkg-deb` 或 [dotnet-packaging](https://github.com/quamotion/dotnet-packaging) 这类工具均可：

```bash
dotnet tool install --global dotnet-deb
dotnet deb -r linux-x64 -c Release
```

### RPM 包 {#rpm-package}

面向 Fedora 和基于 RHEL 的发行版：

```bash
dotnet tool install --global dotnet-rpm
dotnet rpm -r linux-x64 -c Release
```

### Flatpak 与 snap {#flatpak-and-snap}

XPF 应用也可以打成 Flatpak 或 Snap 包分发。具体怎么把 .NET 应用装进去，请参阅各打包体系自己的文档。

## CI/CD

在 CI/CD 流水线中构建 XPF 应用时：

1. 添加一个带许可证密钥的 `NuGet.config`（密钥值请用 CI secret 保存）
2. 在构建环境中装齐所需依赖
3. 从命令行发布

GitHub Actions 步骤示例：

```yaml
- name: Publish for Linux
  run: dotnet publish -r linux-x64 -c Release --self-contained
  env:
    XpfLicenseKey: ${{ secrets.XPF_LICENSE_KEY }}
```

如何配合环境变量使用许可证密钥，请见[集中管理多个 XPF 项目](/xpf/configuration/centralizing-multiple-xpf-projects#license-keys)。

## 调试远程 Linux 目标 {#debugging-remote-linux-targets}

若要从 Windows 开发机调试跑在 Linux 上的 XPF 应用，请见 [Linux：调试](/xpf/platforms/linux#debugging-on-linux)。

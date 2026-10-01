---
id: command-line-reference
title: Parcel 命令行参考
sidebar_label: 命令行参考
doc-type: reference
---

用 Parcel 命令行工具把 Avalonia 应用打包成 Windows、macOS 和 Linux 的安装包。Parcel 还能为应用和安装包签名。

## 前置条件 {#prerequisites}

动手使用 Parcel 之前，请确认你备齐了这些：

1. **Parcel .NET 工具**——按[配置指南](/tools/parcel/setup)安装。
2. **有效的许可证密钥**——设置 `AVALONIA_TOOLS_LICENSE_KEY` 环境变量或使用 `--license-key` 选项。许可证密钥可在 [Avalonia 门户](https://portal.avaloniaui.net/)获取。

:::note
Parcel CLI 仅对 [Avalonia Plus](https://avaloniaui.net/pricing) 许可证开放。
:::

## 概述 {#overview}

```bash
parcel [command] [options]
```

## Global Options

| 选项 | 说明 |
|--------|-------------|
| `-?, -h, --help` | 显示帮助与用法信息 |
| `--version` | 显示版本信息 |
| `--license-key` | 设置 Parcel 许可证密钥。若省略该选项，Parcel 会先取 `AVALONIA_TOOLS_LICENSE_KEY`，再退回到已有的应用会话 |
| `--verbosity` | 设置详尽级别（quiet、minimal、normal、detailed、diagnostic） |

## Commands

### pack

按指定的设置和参数构建并打包项目。

```bash
parcel pack <project> [options]
```

**Arguments:**

- `<project>`——含配置内容的 Parcel 项目文件

**选项：**

| 选项 | 说明 | 默认值 |
|--------|-------------|---------|
| `-o, --output` | 输出目录 | `<project-dir>\bin\packages` |
| `-r, --runtimes` | 要打包的运行时标识符，该选项可以多次指定。 | 当前平台的运行时 |
| `-p, --packages` | 输出格式：`deb`、`dmg`、`msix`、`nsis`、`pkg`、`rpm` 或 `zip`。该选项可以多次指定。 | 当前平台的安装包 |
| `--no-build` | 不重新构建输入项目。 | `false` |

**Example:**

```bash
# Pack for current platform
parcel pack MyApp.parcel

# Pack for multiple platforms and formats
parcel pack MyApp.parcel -r osx-x64 -r linux-x64 -p dmg -p deb
```

### step

只跑打包流程中的某一步。调试或定制打包流程时用这条命令。

```bash
parcel step [command] <input> <output> [options]
```

**Available Step Commands:**

| 命令 | 说明 | 输入 | 输出 |
|---------|-------------|-------|--------|
| `publish` | 为目标平台和运行时发布 .NET 项目 | 无显式输入。Parcel 从 `.parcel` 文件读取项目信息。 | 发布出的应用目录 |
| `merge-mac` | 把各架构的构建结果合并成一个通用 macOS 应用包 | 含各架构子目录（`osx-x64`、`osx-arm64`）的目录 | 通用应用目录 |
| `bundle-mac` | 把 macOS 应用及其依赖打进一个应用包 | 应用目录 | 应用包（`.app`） |
| `sign-mac` | 用项目设置中的凭据为 macOS 应用包及其组件签名 | 应用包或扁平目录 | 已签名的应用包或目录 |
| `notary-mac` | 把应用提交给 Apple 做公证，若通过则把票据订到应用上 | 压缩后的应用包或 DMG 文件 | 已公证的文件 |
| `sign-win` | 用项目设置中的提供方为 Windows 应用可执行文件签名 | 含有与 `AssemblyName` 匹配的可执行文件的应用目录 | 已签名的可执行文件 |
| `create-zip` | 创建 ZIP 归档，并保留文件权限和符号链接 | 含应用文件的目录或文件 | ZIP 归档（`.zip`） |
| `create-dmg` | 为 macOS 创建 DMG 磁盘映像 | 应用包（.app） | 未签名的 DMG 映像文件 |
| `create-pkg` | 按 Parcel 项目中的设置创建 macOS 安装包 | 应用包（`.app`） | PKG 安装包（`.pkg`） |
| `create-deb` | 为 Linux 创建 Debian 包 | 应用目录 | Debian 包（.deb） |
| `create-rpm` | 为 Linux 创建 RPM 包 | 应用目录 | RPM 包（`.rpm`） |
| `create-nsis` | 创建 Windows NSIS 安装程序 | 应用目录 | 未签名的 NSIS 安装程序（.exe） |
| `create-msix` | 创建 Windows MSIX 包。Parcel 会生成清单，或在项目模板上做修补。 | 应用目录 | MSIX 包（`.msix`） |

**Example:**

各步骤命令彼此独立，没有强制的先后顺序。下面的示例给出各平台上典型的执行顺序。

你也可以把某一步换成自己的脚本，按需定制流程。


<Tabs>
<TabItem value="win" label="Windows" default>

```bash
# `parcel step publish ./publish -r win-x64 -p project.parcel` can be used instead
dotnet publish -r win-x64 -o ./publish

# signing, with parameters populated from .parcel config file
parcel step sign-win ./publish ./signed -p project.parcel

# installer
parcel step create-nsis ./signed ./installer.exe -p project.parcel

# or ZIP archive
parcel step create-zip ./signed ./archive.zip -p project.parcel
```

</TabItem>
<TabItem value="mac" label="macOS">

```bash
mkdir ./publish

# for universal packages, need to publish both archs
dotnet publish -r osx-x64 -o ./publish/osx-x64
dotnet publish -r osx-arm64 -o ./publish/osx-arm64

# merge two archs into a universal one
parcel step merge-mac ./publish ./merged -p project.parcel

# create app bundle
parcel step bundle-mac ./merged ./bundle.app -p project.parcel

# signing, with parameters populated from .parcel config file
parcel step sign-mac ./bundle.app ./signed.app -p project.parcel

# DMG package
parcel step create-dmg ./signed.app ./package.dmg -p project.parcel

# or ZIP archive
parcel step create-zip ./signed.app ./archive.zip -p project.parcel

# notarization (can be applied on either ZIP, DMG or PKG input)
parcel step notary-mac ./archive.zip ./notarized.app -p project.parcel
```

:::note

用通用包可以在 Intel 和 Apple 芯片上都跑出原生性能，代价是通用可执行文件的体积最多可达单架构版本的两倍。

若你不需要通用包，跳过 `merge-mac` 这一步即可。

:::

</TabItem>
<TabItem value="lin" label="Linux">


```bash
# `parcel step publish ./ ./publish -r linux-x64 -p project.parcel` can be used instead
dotnet publish -r linux-x64 -o ./publish 

# installer
parcel step create-deb ./publish ./installer.deb -p project.parcel

# or ZIP archive
parcel step create-zip ./publish ./archive.zip -p project.parcel
```

</TabItem>
</Tabs>

**Common Options:**

- `-p, --project`——含配置内容的 Parcel 项目文件
- `-w, --overwrite`——覆盖已有的输出文件
- `-r, --runtime`——运行时标识符（用于 publish 命令）

### install-tools

下载或更新打包配置所需的工具依赖。

```bash
parcel install-tools [options]
```

**选项：**

| 选项 | 说明 |
|--------|-------------|
| `-r, --runtimes` | 运行时标识符（可指定多个） |
| `-p, --packages` | 包格式：`deb`、`dmg`、`msix`、`nsis`、`pkg`、`rpm`、`zip`（可指定多个） |

**Example:**

```bash
# Install dependencies for specific platforms and package formats
parcel install-tools -r win-x64 -r osx-x64 -p nsis -p dmg
```

这条命令会在 Parcel 真正用到之前，先把 NSIS 和 DMG 工具下载下来。

### mcp

运行一个模型上下文协议（MCP）服务器，让 AI 助手能够执行 Parcel 命令。

```bash
parcel mcp
```

配置与使用说明请见 [Parcel MCP](/tools/parcel/mcp)。

## Environment Variables

### Parcel 与控制台行为 {#parcel-and-console-behavior}

| 变量 | 说明 |
|---|---|
| `AVALONIA_TOOLS_LICENSE_KEY` | 未提供 `--license-key` 时所用的许可证密钥。 |
| `AVALONIA_TOOLS_LOG_LEVEL` | 设置 Parcel 应用和 MCP 的日志级别，比如 `Debug` 或 `Information`。 |

### 工具发现 {#tool-discovery}

| 变量 | 说明 |
|---|---|
| `PARCEL_JAVA_EXE` | 设置跨平台 Windows 签名所用 Java 可执行文件的路径。Parcel 也会读取 `JAVA_HOME`。 |
| `PARCEL_SIGNTOOL_EXE` | 设置 Windows 上 SignTool 的路径。 |
| `PARCEL_WSL_DISTRIBUTION` | 在 Windows 上需要 WSL 的打包步骤所使用的 WSL2 发行版。 |
| `PARCEL_WSL_USER` | 设置所选 WSL2 发行版中使用的用户账户。 |

### 云端签名 {#cloud-signing}

| 变量 | 说明 |
|---|---|
| `AZURE_TENANT_ID` | Azure Artifact Signing 或 Key Vault 所用的 Microsoft Entra 租户。 |
| `AZURE_CLIENT_ID` | Azure 服务主体的客户端 ID。 |
| `AZURE_CLIENT_SECRET` | Azure 服务主体的密钥。 |
| `AWS_ACCESS_KEY_ID` | AWS KMS 签名所用的 AWS 访问密钥。 |
| `AWS_SECRET_ACCESS_KEY` | AWS KMS 签名所用的 AWS 密钥。 |
| `AWS_SESSION_TOKEN` | 可选的 AWS 临时会话令牌。 |

受支持的标量设置可以用自动生成的 `PARCEL_<SECTION>_<SETTING>` 环境变量覆盖。各设置对应的确切变量名请见 [Parcel 配置参考](/tools/parcel/configuration-reference)。

## 注释支持情况 {#notes}

- 所有打包选项、签名凭据和外观设置都定义在 Parcel 项目文件（`.parcel`）中。
- 使用 `--no-build` 时，请确保发布设置与你的 Parcel 配置一致，比如裁剪、AOT 和单文件发布这几项。

## 另请参阅 {#see-also}

- [Parcel 配置准备](/tools/parcel/setup)
- [Parcel 配置参考](/tools/parcel/configuration-reference)
- [为 macOS 打包](/tools/parcel/packaging-for-macos)
- [为 Windows 打包](/tools/parcel/packaging-for-windows)
- [为 Linux 打包](/tools/parcel/packaging-for-linux)

---
id: packaging-for-windows
title: 为 Windows 打包应用
sidebar_label: Windows
doc-type: reference
tags:
  - avalonia plus
  - avalonia pro
  - avalonia enterprise
---

## 打包 {#packaging}

Parcel 能生成 Windows 安装程序和归档包。用 Parcel 打包可以在 Windows、macOS 或 Linux 上进行。

| 格式 | CLI 代号 | 最适合 |
|---|---|---|
| NSIS 安装程序（`.exe`） | `nsis` | 传统的直接分发方式，安装流程可定制，还可附带卸载程序 |
| MSIX 包（`.msix`） | `msix` | 现代 Windows 部署、企业管理以及 Microsoft Store 分发 |
| ZIP 归档（`.zip`） | `zip` | 无需安装和注册的便携式分发 |

各设置的完整名称、类型、默认值和环境变量，请见 [Parcel 配置参考](/tools/parcel/configuration-reference#windows-settings)。

### Package Configuration

#### Common Properties

**Application Name**:

用作应用安装目录、开始菜单项和快捷方式文件名的显示名称。

:::note
目前还不支持本地化。
:::

**Package Name**:

输出的安装程序文件名（不含扩展名）。

### NSIS Installer Properties

Parcel 用 NSIS（Nullsoft Scriptable Install System）生成轻量的自解压安装程序，安装选项相当灵活。

**公司**：

在 Windows 属性、安装程序和系统对话框中显示的发布者名称。启用 **Create Company Folder** 后，还会用它来组织 Program Files 中的应用目录和注册表项。

**Create Company Folder**:

启用后，Parcel 会把应用装进以公司名命名的子目录：
- 管理员安装：`Program Files\[Company]\[Application Name]\`
- 用户安装：`%LocalAppData%\[Company]\[Application Name]\`

它同样影响开始菜单快捷方式的位置，把快捷方式归到 `Start Menu\Programs\[Company]\[Application Name]` 下。

默认：false。

**Installer Icon**:

**ICO** 或 **SVG** 格式的安装程序图标。ICO 文件应涵盖 16x16 到 256x256 的多档分辨率。该图标会出现在资源管理器里的安装程序可执行文件上、安装过程中，以及 Windows 的卸载列表中。

:::note
它与应用图标是两回事。 

应用图标由 .csproj 文件中标准的 .NET `<ApplicationIcon>file.ico</ApplicationIcon>` 属性决定。
:::

**Requires Admin**:

控制安装时是否需要管理员权限。

启用（默认）时，应用装到 `Program Files`，需要用户账户控制（UAC）提权；禁用时，应用装到当前用户的 `%LocalAppData%` 目录，不需要提权。

默认：true。

**随应用一并提供卸载程序**：

启用后，Parcel 会随应用附带一个卸载程序，并在 Windows 设置 > 应用和功能（较老的 Windows 上是控制面板 > 程序和功能）中创建条目。

默认：true。

**License File**:

安装过程中显示的可选许可文件。支持的格式：
- 纯文本（.txt）
- 富文本格式（.rtf）

许可协议会在安装过程中单列一页显示，用户必须接受才能继续。

### MSIX 包 <MinVersion version="1.1" isNewVersion="true" /> {#msix-packages}

MSIX 带来包标识、干净的安装与卸载，以及与 Windows 部署体系的集成。Parcel 在所有受支持的宿主平台上都能生成 MSIX 包，且不需要 Windows SDK。Parcel 会生成包清单，或在项目中对 `.appxmanifest` 模板做修补，并依据共用的应用元数据和**安装程序图标**设置生成视觉资产。

**Publisher** 设置是 MSIX 标识中的可分辨名称，形如 `CN=Contoso`。若包要签名并直接分发，该值必须与签名证书的主题一字不差。Parcel 会尽量从本地签名证书中取这个值，取不到时则退回到**公司**或**应用名称**。

若走直接分发，请用目标设备信任的证书为 MSIX 包签名；若走 Microsoft Store，提交的包由商店来签名。当签名由 Parcel 之后的其他流程完成时，请关掉 **Sign Installer**。请见微软的 [MSIX 签名概述](https://learn.microsoft.com/en-us/windows/msix/package/signing-package-overview)和 [Microsoft Store 发布指南](https://learn.microsoft.com/en-us/windows/apps/publish/get-started)。

### 桌面集成 {#desktop-integration}

**File Associations**:

通过指定文件扩展名（例如 `.myfile`）把应用与特定文件类型关联起来，也可以另外补上 MIME 类型和自定义图标。Parcel 会为此创建注册表项，以便与资源管理器妥善集成。

在 Avalonia 应用中如何处理这些文件，请见[可激活生命周期](/docs/services/activatable-lifetime#handling-uri-activation)。

**URL Schemes**:

定义自定义方案（例如 `myapp://`、`myprotocol://`）即可注册用于深度链接的 URL 方案。Parcel 会创建相应的注册表项，让其他应用和浏览器能带着特定参数启动你的应用。

在 Avalonia 应用中如何处理 URL 方案，请见[可激活生命周期](/docs/services/activatable-lifetime#handling-uri-activation)。

在 **Basics** 下配置这些关联，Parcel 会把它们套用到 NSIS 和 MSIX 包上。请见[文件关联与 URL 方案](/tools/parcel/configuration-reference#file-associations)。

## Code Signing

Parcel 用 Authenticode 证书为 Windows 可执行文件和安装程序签名。Windows、Linux 和 macOS 上都支持跨平台签名。

:::note
本文讲的是如何把各种签名方式接进 Parcel，并不包含申请证书或配置云签名服务的详细步骤。完整的配置说明请参阅各方式所附的链接文档。
:::

### 前置条件 {#prerequisites}

为 Windows 应用签名之前，请确认你备齐了这些：

- **代码签名证书**：来自受信任证书颁发机构的有效 Authenticode 证书
- **Windows SDK**（仅 Windows）：可从 [Visual Studio 下载页](https://visualstudio.microsoft.com/downloads/)随 Visual Studio Build Tools（CI 上）或 Visual Studio（桌面上）一并安装
- **Java 运行时**：跨平台签名操作所必需。

### Signing Methods

视开发环境和工作流而定，Parcel 支持多种证书格式。

#### Local Certificate

用本地证书文件（PFX/P12 格式）签名。这种方式不建议用于正式发布的应用，Windows 通常也不信任它。

**Required Configuration:**
- **本地签名证书文件**：PFX 或 P12 证书文件的路径
- **本地签名证书密码**：保护该证书文件的密码
- **时间戳服务器 URL**（可选）：时间戳颁发机构服务器的 URL（例如 `http://timestamp.digicert.com`）

**Platform Support:**
- **Windows**：能用原生 SignTool 时用它，否则用 JSign
- **Linux/macOS**：使用 [JSign](https://github.com/ebourg/jsign)（需要 Java 运行时）

**Documentation:**
- [New-SelfSignedCertificate](https://learn.microsoft.com/en-us/powershell/module/pki/new-selfsignedcertificate?view=windowsserver2025-ps)

#### Windows Certificate Store

使用装在 Windows 证书存储中的证书，包括硬件安全模块（HSM）和 USB 令牌里的证书。

**Required Configuration:**
- **存储证书名称**：证书的主题名或指纹
- **使用本地计算机证书存储**（可选）：在本地计算机存储而非当前用户存储中查找
- **自动匹配证书**（可选）：自动挑选最匹配的那张证书

**Platform Support:**
- **仅限 Windows**：需要 Windows SDK（SignTool）

**Documentation:**
- [Windows Certificate Store Overview](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/certificate-stores)

#### Azure Artifact Signing（跨平台） {#azure-artifact-signing-cross-platform}

Azure Artifact Signing 是一项云签名服务，旧称 Trusted Signing。用它就不必再操心本地证书，签名密钥由硬件安全模块（HSM）保护。

**Required Configuration:**
- **Azure Artifact Signing 端点**：服务端点 URL，形如 `https://[region].codesigning.azure.net/`
- **Azure Artifact Signing 证书配置文件名**：证书配置文件的名称
- **Azure Artifact Signing 账户名**：签名账户的名称

**认证方式：**
Azure CLI 认证或环境变量：
- `AZURE_TENANT_ID`：Azure Active Directory 租户 ID
- `AZURE_CLIENT_ID`：服务主体客户端 ID
- `AZURE_CLIENT_SECRET`：服务主体客户端密钥

**所需的 Azure 角色**：“Code Signing Certificate Profile Signer”

**Platform Support:**
- **Windows**：能用原生 SignTool 时用它，否则用 JSign
- **Linux/macOS**：使用 [JSign](https://github.com/ebourg/jsign)（需要 Java 运行时）

:::tip
若企业需要立刻获得信任、等不起慢慢积累声誉，Azure Artifact Signing 是推荐方案。
:::

**Documentation:**
- [Azure Artifact Signing 文档](https://learn.microsoft.com/en-us/azure/artifact-signing/)
- [Artifact Signing 快速上手](https://learn.microsoft.com/en-us/azure/artifact-signing/quickstart)

#### Azure Key Vault

把证书和私钥安全地存进 Azure Key Vault，集中管理证书与访问权限。

**Required Configuration:**
- **Azure Key Vault 名称**：Azure Key Vault 实例的名称
- **Azure Key Vault URL**：（可选）完整的保管库 URL，用于主权云或非默认端点
- **Azure Key Vault 证书名称**：存放在保管库中的证书名称

**认证方式：**
Azure CLI 认证或环境变量：
- `AZURE_TENANT_ID`：Azure Active Directory 租户 ID
- `AZURE_CLIENT_ID`：服务主体客户端 ID
- `AZURE_CLIENT_SECRET`：服务主体客户端密钥

**Required Azure Roles:**
- “Key Vault Crypto User”——用于签名操作
- “Key Vault Certificate User”——用于访问证书

**Documentation:**
- [Azure Key Vault Overview](https://learn.microsoft.com/en-us/azure/key-vault/general/overview)

:::note
由 [JSign](https://github.com/ebourg/jsign) 驱动，需要 Java 运行时。
:::

#### AWS KMS

用 AWS Key Management Service 安全地存放私钥，证书则另行管理。

**Required Configuration:**
- **AWS 区域代码**：密钥所在的 AWS 区域（例如 `us-east-1`、`eu-west-1`、`ap-southeast-2`）
- **AWS 签名证书文件**：证书文件的路径（AWS KMS 只存私钥）
- **AWS 签名密钥 ID 或别名**：AWS KMS 密钥标识符或别名

**认证方式：**
AWS 凭据可来自以下任一来源：
- 环境变量：`AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY`、`AWS_SESSION_TOKEN`
- ECS 容器凭据
- EC2 IMDSv2 服务

**Required IAM Permissions:**
- `kms:ListKeys`——用于发现密钥
- `kms:DescribeKey`——用于读取密钥元数据
- `kms:Sign`——用于签名操作

**Documentation:**
- [AWS KMS Overview](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)

:::note
由 [JSign](https://github.com/ebourg/jsign) 驱动，需要 Java 运行时。
:::

#### DigiCert

使用存放在 DigiCert ONE Secure Software Manager（原 DigiCert KeyLocker）中的证书和密钥，无需安装 DigiCert 客户端工具。

**Required Configuration:**
- **DigiCert API 密钥**：用于 DigiCert ONE 认证的 API 密钥（在 DigiCert ONE 门户中获取）
- **DigiCert 密钥库**：含客户端认证证书的 PKCS#12 密钥库文件
- **DigiCert Storepass**：密钥库文件的密码
- **DigiCert 证书名称或 ID**：该证书在 DigiCert ONE 中的标识
- **DigiCert 主机**（可选）：自定义主机 URL（美国区默认为 `https://clientauth.one.digicert.com`）

**Documentation:**
- [DigiCert Software Trust Manager](https://docs.digicert.com/en/software-trust-manager.html)

:::note
由 [JSign](https://github.com/ebourg/jsign) 驱动，需要 Java 运行时。
:::

#### Google Cloud KMS

用 Google Cloud Key Management Service 安全地存放私钥。由于 Google Cloud KMS 只存私钥，证书须另行提供。

**Required Configuration:**
- **Google 访问令牌**：用于认证的 OAuth 2.0 访问令牌
- **Google 签名密钥环**：密钥环路径，形如 `projects/[PROJECT]/locations/[LOCATION]/keyRings/[KEYRING]`
- **Google 签名证书文件**：证书文件的路径
- **Google 签名证书版本**（可选）：指定密钥的具体版本（省略则用最新版本）

**Required IAM Permissions:**
- `cloudkms.cryptoKeyVersions.useToSign`——用于签名操作
- `cloudkms.cryptoKeyVersions.list`——未指定版本时必需
- `cloudkms.cryptoKeys.list`——用于发现密钥

**Documentation:**
- [Google Cloud KMS Overview](https://cloud.google.com/kms/docs)

:::note
由 [JSign](https://github.com/ebourg/jsign) 驱动，需要 Java 运行时。
:::

#### SSL.com eSigner

来自 SSL.com 的云签名服务，证书由硬件安全模块（HSM）托底，另有可选的沙箱环境供测试。

**Required Configuration:**
- **eSigner 用户名**：SSL.com 账户用户名
- **eSigner 密码**：SSL.com 账户密码
- **eSigner 密钥密码**：用于双因素认证的 Base64 编码 TOTP（基于时间的一次性密码）密钥
- **eSigner 凭据 ID**：该证书的凭据标识符（可在 SSL.com 控制台中找到）
- **eSigner 沙箱**（可选）：启用沙箱环境（`https://cs-try.ssl.com`），正式使用前先行试水

**Documentation:**
- [SSL.com eSigner](https://www.ssl.com/esigner/)

:::note
由 [JSign](https://github.com/ebourg/jsign) 驱动，需要 Java 运行时。
:::

## 另请参阅 {#see-also}

- [Parcel 配置准备](/tools/parcel/setup)
- [Parcel 配置参考](/tools/parcel/configuration-reference)
- [Parcel 命令行参考](/tools/parcel/command-line-reference)

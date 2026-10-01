---
id: packaging-for-macos
title: 为 macOS 打包应用
sidebar_label: macOS
doc-type: reference
tags:
  - avalonia plus
  - avalonia pro
  - avalonia enterprise
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## 打包 {#packaging}

Parcel 能生成 macOS 应用包（`.app`）和安装包。用 Parcel 打包可以在 Windows、macOS 或 Linux 上进行。

| 格式 | CLI 代号 | 最适合 |
|---|---|---|
| DMG 映像（`.dmg`） | `dmg` | 带品牌感的拖放式直接分发 |
| PKG 安装包（`.pkg`） | `pkg` | 受管安装、直接分发，以及提交 Mac App Store |
| ZIP 归档（`.zip`） | `zip` | 不带安装程序、直接分发应用包 |

各设置的完整名称、类型、默认值和环境变量，请见 [Parcel 配置参考](/tools/parcel/configuration-reference#macos-settings)。

### Bundle Configuration

#### Common Properties

**Application Name**:

用作应用显示名的名称，即 `CFBundleDisplayName`。

:::note
目前还不支持本地化。
:::

**Package Name**:

用作应用包名和输出 dmg 文件名的包名。

### Bundle Properties

决定应用在 macOS 上如何呈现与行事的关键应用包元数据。

**Bundle Identifier**:

应用的唯一反向 DNS 标识符（例如 `com.Company.AppName`）。它必须遵循 Apple 的反向 DNS 命名规范：除点和连字符外不要用特殊字符，且必须以字母开头。

**Team ID**:

你 Apple Developer 账户的唯一标识符。签名和公证过程中会用到，其余情况可不填。

**App Category**:

用于 macOS 和 App Store 分类的应用类别，对应 Apple 的 `public.app-category.*` 标识符。

**Application Icon**:

可选的 macOS 图标，格式为 **ICNS** 或 **SVG**，会覆盖**应用图标**。ICNS 文件应涵盖 16 x 16 到 1024 x 1024 像素的各档分辨率。Parcel 会根据源文件生成应用包的图标结构。

**权限**：

带自定义用途说明的系统权限。每项权限都需要一段用途说明，它会出现在 macOS 的权限对话框里。

:::note
用途说明是必填的，否则系统可能会拒绝应用访问相应的系统资源。
:::

**File Associations**:

通过指定文件扩展名（例如 `.myfile`）把应用与特定文件类型关联起来，也可以另外补上 MIME 类型。

在 Avalonia 应用中如何处理这些文件，请见[可激活生命周期](/docs/services/activatable-lifetime#handling-uri-activation)。

**URL Schemes**:

定义自定义方案（例如 `myapp://`、`myprotocol://`）即可注册用于深度链接的 URL 方案，其他应用便能带着特定参数启动你的应用。

在 Avalonia 应用中如何处理 URL 方案，请见[可激活生命周期](/docs/services/activatable-lifetime#handling-uri-activation)。

在 **Basics** 下配置这些关联，Parcel 会把它们写进应用包的 `Info.plist` 文件。若关闭了 **Create Bundle**，Parcel 会忽略这些关联。请见[文件关联与 URL 方案](/tools/parcel/configuration-reference#file-associations)。

#### Custom Info.plist Configuration

Parcel 支持自定义 Info.plist 文件，用于更高阶的应用包配置。

1. 在项目根目录下创建一个 `Info.plist` 文件
2. 按 Apple 的文档添加自定义的键和值
3. Parcel 会把自定义属性与自动生成的属性合并
4. 自定义文件中已有的属性优先
5. 缺少的属性会依据项目配置自动补上

### DMG Creation

Parcel 生成的 DMG 安装映像带拖放界面、自定义背景和符号链接。

:::caution
在 Windows 上生成 DMG 需要 [WSL2](https://learn.microsoft.com/en-us/windows/wsl/)。ZIP 包则不需要 WSL2 也能生成。
:::

**DMG Background Image**:

DMG 安装映像的背景图，格式为 TIFF。

Parcel 自带一个可视化的 DMG 布局编辑器。默认布局采用 **660 x 422** 像素的窗口，各项取值如下：

- **应用包图标**：位于坐标 (173, 231)
- **Applications 文件夹**：位于坐标 (485, 231)
- **图标大小**：128px
- **文字大小**：12px

图标坐标是从左上角量到图标中心的。

用这个编辑器可以调整窗口位置、窗口尺寸、图标大小、标签字号、网格和背景色，也可以挪动应用包和 Applications 文件夹的位置，并为所选布局设计背景图。

:::note
Parcel 会把可选的 **DMG 许可文件**放在映像根目录。开启 **Sign DMG** 即可用应用签名凭据为做好的映像签名。
:::

### ZIP Creation

生成 ZIP 时 Parcel 会保留可执行权限。在 macOS 上解压后应用包结构完好无损，应用无需额外操作即可运行。

### PKG 安装包 <MinVersion version="1.1" isNewVersion="true" /> {#pkg-installers}

PKG 包走的是 macOS 原生安装器，在 Parcel 支持的所有宿主平台上都能生成。PKG 包要求开启 **Create Bundle**，默认把应用装到 `/Applications`。

应用和它的安装包必须使用不同的证书。

- 若走直接分发，请用 **Developer ID Application** 证书为应用签名，用 **Developer ID Installer** 证书为 PKG 签名，然后给包做公证。
- 若要发布到 Mac App Store，请见 [App Store Connect](#app-store-connect)。

另见 Apple 的 [Mac 软件打包指南](https://developer.apple.com/documentation/xcode/packaging-mac-software-for-distribution)和 [Developer ID 概述](https://developer.apple.com/support/developer-id/)。

### 排查问题 {#troubleshooting}

请见 [macOS 排查问题页](/troubleshooting/platform-specific-issues/macos#packaging)。

## Code Signing

Parcel 用 Apple Developer 证书为 macOS 应用包签名。Windows、Linux 和 macOS 上都支持跨平台签名。

### 前置条件 {#prerequisites}

为 macOS 应用签名之前，请确认你备齐了这些：

- **Apple Developer 账户**：有效的 [Apple Developer Program](https://developer.apple.com/programs/) 会员资格（99 美元/年）
- **Xcode 命令行工具**（仅 macOS）：可从 [Apple Developer 资源页](https://developer.apple.com/xcode/resources/)获取

### Signing Methods

视开发环境和工作流而定，Parcel 支持多种证书格式。

#### KeyChain Identity (macOS Only)

使用通过证书请求装进 macOS 钥匙串的证书。

若要在 Mac App Store 之外分发，需要一张与你的团队 ID 关联的 “Developer ID Application” 证书。

#### P12 证书（跨平台） {#p12-certificate-cross-platform}

一种同时包含证书和私钥的便携格式。
Apple 不直接提供 P12 证书，但你可以从钥匙串导出，或用 OpenSSL 生成。

在 Windows 和 Linux 机器上，Parcel 用 [rcodesign](https://github.com/indygreg/apple-platform-rs/tree/main/apple-codesign) 为二进制文件和应用包签名。

#### PEM 证书（跨平台） {#pem-certificate-cross-platform}

跨平台签名可以用 PEM 证书。若要打 PKG 包，必须为应用和安装程序分别配置各自的 PEM 证书字段。

### PKG 所需的安装程序证书 {#installer-certificates-for-pkg}

在 **Installer Signing** 分组中配置 PKG 签名。选一个能为安装包签名的钥匙串标识、P12 证书或 PEM 证书。应用证书签不了 PKG 安装包，安装程序证书也签不了应用包。

### Create Developer Certificate

<Tabs>
<TabItem value="keychain" label="Keychain (macOS Only)" default>

初次配置需要一台 macOS 机器。

**用钥匙串创建证书：**

1. 在 macOS 上打开**钥匙串访问**
2. **钥匙串访问** > **证书助理** > **从证书颁发机构请求证书**
3. 在“常用名称”一栏填个名字，CA 电子邮件地址留空
4. 选择**存储到磁盘**，点**继续**生成 `certificate.csr`
5. 进入 [Apple Developer 账户](https://developer.apple.com/account/) > **Certificates, Identifiers & Profiles**
6. 转到 **Certificates** > **All Certificates**
7. 点击 ➕ 新建一张证书
8. 若应用在 App Store 之外分发，选 **Developer ID Application**
9. 按提示上传 `certificate.csr`
10. 下载生成的 `.cer` 文件
11. 把证书导入钥匙串

:::tip
把证书导出为 P12，此后便可跨平台签名，不必再依赖 macOS。
:::

</TabItem>

<TabItem value="openssl" label="OpenSSL (Cross-Platform)">

用 OpenSSL 可以在任意平台上生成证书。

**前置条件：**

- 已安装 OpenSSL（Windows 上推荐用 WSL2）

**用 OpenSSL 创建证书：**

1. 生成私钥：

    ```bash
    openssl genrsa -out private.key 2048
    ```

2. Generate Certificate Signing Request:

    ```bash
    openssl req -new -key private.key -out certificate.csr
    ```

3. 把 CSR 上传到 [Apple Developer 门户](https://developer.apple.com/account/)
    - 进入 **Certificates, Identifiers & Profiles** > **Certificates**
    - 点击 ➕，选 **Developer ID Application**
    - 上传 `certificate.csr`，然后下载 `.cer` 文件

4. 把证书转换成 PEM 格式：

    ```bash
    openssl x509 -in development.cer -inform DER -out certificate.pem -outform PEM
    ```

5. 生成 P12 文件（会用到先前创建的 `private.key` 文件）：

    ```bash
    openssl pkcs12 -export -out certificate.p12 -inkey private.key -in certificate.pem
    ```

    按提示设一个足够安全的密码。

:::tip
生成的 `certificate.p12` 连同密码，便可在任意平台上配合 Parcel 使用。
:::

</TabItem>

</Tabs>

## App Store Connect

要通过 Mac App Store 分发应用，请提交已签名的 PKG，不要提交 DMG 或 ZIP——那两种格式是给直接分发用的。

### 推荐配置 {#recommended-configuration}

1. 在 App Store Connect 中创建 macOS 应用记录，并注册一个明确的 App ID，其 bundle ID 必须与 Parcel 中的 **Bundle Identifier** 一字不差。App Store Connect 会凭 bundle ID 和版本号把上传的包与应用记录对上号。
2. 应用签名用 **Apple Distribution** 证书，PKG 签名另外用 **Mac Installer Distribution** 证书。提交 App Store 时切勿使用 Developer ID 证书，否则会被 Apple 拒收。
3. 为同一个明确的 App ID 和应用签名证书创建并下载一份 **Mac App Store Connect** 描述文件。
4. 把描述文件复制到 Parcel 项目文件所在目录，并按所配置的 .NET 项目重命名。举例来说，若 **.NET Project Path** 指向 `MyApp.csproj`，就命名为 `MyApp.provisionprofile`。Parcel 要求文件名完全吻合。
5. 确认 MacOS 设置中已启用 **Create Bundle** 和 **Enable Sandbox**。提交 App Store Connect 时必须关掉公证——公证只对旁加载有意义。
6. 若应用需要特别的权限，可在项目目录中另行配置一个自定义 `Entitlements.plist` 文件。提交之前，请在沙箱中测一遍文件访问、网络访问、子进程以及随包携带的辅助工具。
7. 用 Apple 的 Transporter 应用、Xcode 工具或 App Store Connect 支持的其他方式上传 PKG，等处理完成，把所有投递警告解决掉，然后为 macOS 版本选中处理好的构建并提交审核。

请参阅 Apple 的文档：[创建 App Store Connect 描述文件](https://developer.apple.com/help/account/provisioning-profiles/create-an-app-store-provisioning-profile)、[各类证书的用途](https://developer.apple.com/help/account/certificates/certificates-overview)和[上传构建](https://developer.apple.com/help/app-store-connect/manage-builds/upload-builds/)。

:::note[不要用 Parcel 给 App Store 构建做公证]
Parcel 公证的是以 Developer ID 在 Mac App Store 之外分发的软件。App Store 的包由 Apple 在上传和提交时自行校验，因此 App Store 构建请关掉 Parcel 的公证。
:::

## Notarization

Apple 公证用于证明应用已经过 Apple 的恶意软件检查。在 macOS 10.15（Catalina）及更高版本上，若在 Mac App Store 之外分发应用，公证是必需的。

这一流程会把应用上传到 Apple 的服务器接受扫描，并把应用包的哈希与开发者账户关联起来。

Mac App Store 的包由 Apple 在提交时校验，不要另行公证。对直接分发的场景，Parcel 可以为使用 Developer ID 证书的 DMG 和 PKG 文件提交公证并订上票据。请见 Apple 的[公证文档](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution)。

### 前置条件 {#prerequisites-1}

给应用做公证之前，请确认你备齐了这些：

- **Apple Developer 账户**：付费的 Apple Developer Program 会员资格（99 美元/年）
- **有效的 Developer ID 证书**：用于为在 Mac App Store 之外分发的应用做代码签名
- （仅 macOS）**Xcode 命令行工具**：可从 [Apple Developer 资源页](https://developer.apple.com/xcode/resources/)获取

### Apple Account Authentication

Parcel 需要通过 Apple 的公证服务认证，可用两种方式提供凭据。

#### App 专用密码（推荐） {#app-specific-password-recommended}

对于公证 API，Apple 要求使用 App 专用密码而非用户密码。请按 Apple 的指南操作：[如何生成 App 专用密码](https://support.apple.com/en-us/102654)。

**在 Parcel 中配置凭据：**

1. 公证凭据方式选 “Apple Account”
2. 填入你的 Apple ID（电子邮件地址）
3. 填入你的 App 专用密码
4. 填入你的 Team ID（可在 [Apple Developer 会员信息](https://developer.apple.com/account/#/membership)页中找到）

:::tip
请用环境变量存放凭据，不要把它们硬写进配置文件。
:::

#### Keychain Profile (macOS Only)

把 Apple 账户凭据存进 macOS 钥匙串，再按配置文件名引用。凭据会加密保存在本地。

**设置钥匙串配置文件：**

1. Open Terminal
2. 运行下面的命令：

    ```bash
    xcrun notarytool store-credentials "MyParcelProfile" --apple-id "your-email@example.com" --team-id "YOUR_TEAM_ID"
    ```

3. 按提示输入 App 专用密码：

    ```text
    App-specific password for your-email@example.com: [enter your app-specific password]
    Credentials saved to Keychain.
    To use them, specify `--keychain-profile "MyParcelProfile"`
    ```

**在 Parcel 中配置钥匙串配置文件：**

1. 公证凭据方式选 “Keychain Profile”
2. 填入配置文件名（例如 “MyParcelProfile”）

:::caution
Apple 钥匙串只在 macOS 上可用。Windows 或 Linux 上请改用 App 专用密码的方式。
:::

### 运行未公证的应用（测试与个人使用） {#running-non-notarized-apps-testing-personal-use}

若只是测试、开发或自用，没有 Apple Developer 账户也行，未公证的应用在用户手动放行后仍可运行。

当 macOS 拦下一个未公证的应用时，用户可以这样绕过警告：

1. 进入**系统偏好设置** → **安全性与隐私** → **通用**标签页
2. 先尝试运行该应用，macOS 会把它拦下来。
3. 几分钟内，“安全性与隐私”中会出现一条关于被拦应用的提示
4. 点击该提示旁边的**“仍要打开”**
5. 在弹出的对话框中点**“打开”**确认

:::note
即便不做公证，只要手头有 Developer ID 证书，也请为应用做代码签名。
:::

### 排查公证问题 {#troubleshooting-notarization-issues}

请见 [macOS 排查问题页](/troubleshooting/platform-specific-issues/macos#notarization)。

## 排查问题 {#troubleshooting-1}

请见 [macOS 排查问题页](/troubleshooting/platform-specific-issues/macos#code-signing)。

## 另请参阅 {#see-also}

- [Parcel 配置准备](/tools/parcel/setup)
- [Parcel 配置参考](/tools/parcel/configuration-reference)
- [Parcel 命令行参考](/tools/parcel/command-line-reference)

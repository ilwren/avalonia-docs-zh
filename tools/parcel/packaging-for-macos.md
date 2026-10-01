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

To handle URL schemes in Avalonia applications, see [Activatable lifetime](/docs/services/activatable-lifetime#handling-uri-activation).

Configure associations under **Basics**. Parcel writes them to the application bundle's `Info.plist` file. Parcel ignores associations when **Create Bundle** is disabled. See [File associations and URL schemes](/tools/parcel/configuration-reference#file-associations).

#### Custom Info.plist Configuration

Parcel supports custom Info.plist files for advanced bundle configuration.

1. Create an `Info.plist` file in the project's root directory
2. Add custom keys and values following Apple's documentation
3. Parcel merges custom properties with generated ones
4. Existing properties in the custom file take precedence
5. Missing properties are automatically added based on project configuration

### DMG Creation

Parcel creates DMG installers with a drag-and-drop interface, custom backgrounds, and symbolic links.

:::caution
[WSL2](https://learn.microsoft.com/en-us/windows/wsl/) is required for DMG creation on Windows. ZIP packages can be created without WSL2.
:::

**DMG Background Image**:

The background image for the DMG installer in TIFF format.

Parcel includes a visual DMG layout editor. The default layout uses a **660 x 422** pixel window with these values:

- **App Bundle icon**: positioned at coordinates (173, 231)
- **Applications folder**: positioned at coordinates (485, 231)
- **Icon size**: 128px
- **Text size**: 12px

Icons are positioned from the top left corner to the icon center.

Use the editor to change the window position, window size, icon size, label size, grid, and background color. You can also change the positions of the application bundle and Applications folder, and design the background image for the selected layout.

:::note
Parcel puts the optional **DMG License File** at the root of the image. Enable **Sign DMG** to sign the completed image with the application-signing credentials.
:::

### ZIP Creation

Parcel maintains executable permissions during ZIP creation. The bundle structure remains intact when extracted on macOS, and applications remain executable without additional steps.

### PKG installers <MinVersion version="1.1" isNewVersion="true" />

PKG packages use the native macOS Installer. You can create them on every host that Parcel supports. PKG packages require **Create Bundle**. They install the application in `/Applications` by default.

You must use different certificates for the application and its installer package.

- For direct distribution, sign the application with a **Developer ID Application** certificate. Sign the PKG with a **Developer ID Installer** certificate. Then, notarize the package.
- For Mac App Store distribution, see [App Store Connect](#app-store-connect).

See also Apple's [Mac software packaging guidance](https://developer.apple.com/documentation/xcode/packaging-mac-software-for-distribution) and [Developer ID overview](https://developer.apple.com/support/developer-id/).

### 排查问题 {#troubleshooting}

See the [macOS troubleshooting page](/troubleshooting/platform-specific-issues/macos#packaging).

## Code Signing

Parcel signs macOS bundles using Apple Developer certificates. Cross-platform signing is supported on Windows, Linux, and macOS platforms.

### 前置条件 {#prerequisites}

Before you sign a macOS application, make sure that you have these items:

- **Apple Developer Account**: Active [Apple Developer Program](https://developer.apple.com/programs/) membership ($99/year)
- **Xcode Command Line Tools** (macOS only): Available on [Apple Developer Resources](https://developer.apple.com/xcode/resources/)

### Signing Methods

Parcel supports multiple certificate formats depending on development environment and workflow.

#### KeyChain Identity (macOS Only)

Uses certificates from the macOS Keychain that are installed via a certificate request.

Requires a "Developer ID Application" certificate linked to your team ID for distribution outside the Mac App Store.

#### P12 Certificate (Cross-Platform)

Portable certificate format containing both the certificate and private key.
Apple doesn't provide P12 certificates directly, but they can be exported from the Keychain or generated with OpenSSL.

Parcel uses [rcodesign](https://github.com/indygreg/apple-platform-rs/tree/main/apple-codesign) to sign binaries and bundles on Windows and Linux machines.

#### PEM Certificate (Cross-platform)

Use a PEM certificate for cross-platform signing. For a PKG package, you must configure separate PEM certificate fields for the application and installer.

### Installer certificates for PKG

Configure PKG signing in the **Installer Signing** group. Select a Keychain identity, P12 certificate, or PEM certificate that can sign installer packages. An application certificate cannot sign a PKG installer. An installer certificate cannot sign the application bundle.

### Create Developer Certificate

<Tabs>
<TabItem value="keychain" label="Keychain (macOS Only)" default>

Requires a macOS machine for initial setup.

**To create a certificate with Keychain:**

1. Open **Keychain Access** on macOS
2. **Keychain Access** > **Certificate Assistant** > **Request a Certificate From a Certificate Authority**
3. Enter a name in the Common Name field, leave CA Email Address empty
4. Choose **Saved to disk**, then click **Continue** to generate `certificate.csr`
5. Go to [Apple Developer Account](https://developer.apple.com/account/) > **Certificates, Identifiers & Profiles**
6. Navigate to **Certificates** > **All Certificates**
7. Click ➕ to create a new certificate
8. Choose **Developer ID Application** for apps distributed outside the App Store
9. Upload `certificate.csr` when prompted
10. Download the resulting `.cer` file
11. Import the certificate into Keychain

:::tip
Export the certificate as P12 to enable cross-platform signing without requiring macOS after this step.
:::

</TabItem>

<TabItem value="openssl" label="OpenSSL (Cross-Platform)">

Generate certificates on any platform using OpenSSL.

**Prerequisites:**

- OpenSSL installed (WSL2 recommended for Windows)

**To create a certificate with OpenSSL:**

1. Create a private key:

    ```bash
    openssl genrsa -out private.key 2048
    ```

2. Generate Certificate Signing Request:

    ```bash
    openssl req -new -key private.key -out certificate.csr
    ```

3. Upload the CSR to [Apple Developer Portal](https://developer.apple.com/account/)
    - Go to **Certificates, Identifiers & Profiles** > **Certificates**
    - Click ➕, choose **Developer ID Application**
    - Upload `certificate.csr`, then download the `.cer` file

4. Convert the certificate to PEM format:

    ```bash
    openssl x509 -in development.cer -inform DER -out certificate.pem -outform PEM
    ```

5. Create a P12 file (you will need the previously created `private.key` file):

    ```bash
    openssl pkcs12 -export -out certificate.p12 -inkey private.key -in certificate.pem
    ```

    Set a secure password when prompted.

:::tip
The resulting `certificate.p12` and password can be used with Parcel on any platform.
:::

</TabItem>

</Tabs>

## App Store Connect

Submit a signed PKG to distribute an application through the Mac App Store. Do not submit a DMG or ZIP file. These formats are for direct distribution.

### Recommended configuration

1. Create the macOS application record in App Store Connect. Register an explicit App ID. Its bundle ID must exactly match **Bundle Identifier** in Parcel. App Store Connect uses the bundle ID and version to associate an upload with the application record.
2. Configure application signing with an **Apple Distribution** certificate. Configure PKG signing separately with a **Mac Installer Distribution** certificate. Do not use Developer ID certificates for an App Store submission, or it will be rejected by Apple.
3. Create and download a **Mac App Store Connect** provisioning profile for the same explicit App ID and application-signing certificate.
4. Copy the provisioning profile to the directory that contains the Parcel project file. Rename the profile to match the configured .NET project. For example, use `MyApp.provisionprofile` if **.NET Project Path** points to `MyApp.csproj`. Parcel requires the file name to match exactly.
5. Make sure that **Create Bundle** and **Enable Sandbox** are enabled in MacOS settings. Notarization must be disabled for App Store Connect. It is only useful for sideloading.
6. Optionally, configure a custom `Entitlements.plist` file in the project directory if the app requires custom permissions. Before submission, test file access, network access, child processes, and bundled helper tools in the sandbox.
7. Upload the PKG with Apple's Transporter application, Xcode tools, or another method that App Store Connect supports. Wait for processing to finish. Resolve all delivery warnings. Select the processed build for the macOS version, and submit it for review.

See Apple's documentation for [creating an App Store Connect provisioning profile](https://developer.apple.com/help/account/provisioning-profiles/create-an-app-store-provisioning-profile), [certificate purposes](https://developer.apple.com/help/account/certificates/certificates-overview), and [uploading builds](https://developer.apple.com/help/app-store-connect/manage-builds/upload-builds/).

:::note[Do not notarize App Store builds with Parcel]
Parcel notarizes software that uses a Developer ID for distribution outside the Mac App Store. Apple validates App Store packages during upload and submission. Disable Parcel notarization for an App Store build.
:::

## Notarization

Apple notarization verifies that applications have been checked by Apple for malicious software. Notarization is required for macOS 10.15 (Catalina) and later when distributing applications outside the Mac App Store.

The process uploads an application to Apple's servers for scanning and associates the bundle hash with the developer account.

Apple validates Mac App Store packages during submission. Do not notarize them separately. For direct distribution, Parcel can submit and staple DMG and PKG files that use Developer ID certificates. See Apple's [notarization documentation](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution).

### 前置条件 {#prerequisites-1}

Before you notarize an application, make sure that you have these items:

- **Apple Developer Account**: Paid Apple Developer Program membership ($99/year)
- **Valid Developer ID Certificate**: For code signing applications distributed outside the Mac App Store
- (macOS only) **Xcode Command Line Tools**: Available on [Apple Developer Resources](https://developer.apple.com/xcode/resources/)

### Apple Account Authentication

Parcel requires authentication with Apple's notary service. Two methods are available for providing credentials.

#### App-Specific Password (Recommended)

Apple requires app-specific passwords instead of user passwords for the Notary API. Follow Apple's guide: [How to generate an app-specific password](https://support.apple.com/en-us/102654).

**To configure credentials in Parcel:**

1. Select "Apple Account" as the notary credentials option
2. Enter your Apple ID (email address)
3. Enter your app-specific password
4. Enter your Team ID (from the [Apple Developer Membership](https://developer.apple.com/account/#/membership) page)

:::tip
Use environment variables to store credentials instead of hardcoding them in configuration files.
:::

#### Keychain Profile (macOS Only)

Store Apple Account credentials in macOS Keychain and reference them by profile name. Credentials are encrypted and stored locally.

**Setting up a keychain profile:**

1. Open Terminal
2. Run the following command:

    ```bash
    xcrun notarytool store-credentials "MyParcelProfile" --apple-id "your-email@example.com" --team-id "YOUR_TEAM_ID"
    ```

3. Enter app-specific password when prompted:

    ```text
    App-specific password for your-email@example.com: [enter your app-specific password]
    Credentials saved to Keychain.
    To use them, specify `--keychain-profile "MyParcelProfile"`
    ```

**To configure the keychain profile in Parcel:**

1. Select "Keychain Profile" as the notary credentials option
2. Enter the profile name (e.g., "MyParcelProfile")

:::caution
Apple Keychain is only available on macOS. Use the App-Specific Password method on Windows or Linux.
:::

### Running Non-Notarized Apps (Testing & Personal Use)

For testing, development, or personal use without an Apple Developer Account, non-notarized apps can run with user intervention.

When macOS blocks a non-notarized app, users can bypass the warning:

1. Go to **System Preferences** → **Security & Privacy** → **General** tab
2. Try to run the application. macOS blocks it.
3. Within a few minutes, a message appears in Security & Privacy about the blocked app
4. Click **"Open Anyway"** next to the blocked app message
5. Confirm by clicking **"Open"** in the dialog

:::note
Code-sign applications with a Developer ID certificate when available, even without notarization.
:::

### Troubleshooting notarization issues

See the [macOS troubleshooting page](/troubleshooting/platform-specific-issues/macos#notarization).

## 排查问题 {#troubleshooting-1}

See the [macOS troubleshooting page](/troubleshooting/platform-specific-issues/macos#code-signing).

## 另请参阅 {#see-also}

- [Parcel 配置准备](/tools/parcel/setup)
- [Parcel 配置参考](/tools/parcel/configuration-reference)
- [Parcel 命令行参考](/tools/parcel/command-line-reference)

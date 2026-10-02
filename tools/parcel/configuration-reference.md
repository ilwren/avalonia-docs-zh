---
id: configuration-reference
title: Parcel 配置参考
description: Avalonia Parcel 项目中通用、.NET、Windows、macOS 和 Linux 各项设置的参考。
sidebar_label: 配置参考
doc-type: reference
tags:
  - avalonia plus
  - avalonia pro
  - avalonia enterprise
---

`.parcel` 文件存放着 Parcel 用来发布、打包和签名应用的各项设置，共有五个顶层小节：`GeneralSettings`、`PublishSettings`、`Win32Settings`、`MacOsSettings` 和 `LinuxSettings`。

Parcel 以 `.parcel` 文件所在位置为基准解析相对路径。若你用了**另存为**或**移动到**，Parcel 会按新的项目位置更新相对路径。

## 设置取值 {#setting-values}

大多数标量设置既可以写字面值，也可以取环境变量或 MSBuild 属性。在图形界面中，可在设置项旁边选择取值来源。密码、访问令牌等机密请用环境变量，切勿直接存进 `.parcel` 文件。

若项目中没有定义某个受支持的设置，Parcel 会去查它对应的自动环境变量。下面的表格给出了确切的变量名。集合类设置和结构化对象设置没有自动环境变量覆盖。

本参考中的默认值描述的是最终的打包行为。有些默认值是 Parcel 创建项目时写入的，另一些则是在打包时发现设置为空才套用的。

## 通用设置 {#general-settings}

这些设置对所有目标平台都生效，位于 **Basics** 页。

| 设置项 | `.parcel` 属性 | 类型或取值 | 默认值 | 环境变量 | 说明 |
|---|---|---|---|---|---|
| Project | `GeneralSettings.NetProjectPath` | Path | Required | — | 应用 `.csproj` 文件的路径。该字段由 Parcel 维护。 |
| Package Name | `GeneralSettings.PackageName` | String | 程序集名称 | `PARCEL_GENERAL_PACKAGE_NAME` | 包标识符和输出文件名。各平台可能会按自己的规则做规范化。 |
| Assembly Name | `GeneralSettings.AssemblyName` | String | 项目文件名 | `PARCEL_GENERAL_ASSEMBLY_NAME` | 可执行程序集的名称。这是个高级字段，通常从 .NET 项目中读取。 |
| Application Name | `GeneralSettings.ApplicationName` | String | 包名称 | `PARCEL_GENERAL_APPLICATION_NAME` | 安装程序、应用包、快捷方式和桌面项中使用的显示名称。 |
| Version | `GeneralSettings.Version` | 版本字符串 | `1.0.0` | `PARCEL_GENERAL_VERSION` | 应用和包的版本。Parcel 会把它转换成各平台要求的格式。 |
| Application Icon | `GeneralSettings.Icon` | 图标路径 | Parcel 默认图标 | `PARCEL_GENERAL_ICON` | 各平台共用的应用图标。若配置了平台专属图标，则以后者为准。 |
| Company | `GeneralSettings.Company` | String | 需要时取包名称 | `PARCEL_GENERAL_COMPANY` | 设置 Windows 的发布者和 Linux 的包维护者，平台设置可覆盖它。最多 255 个字符。 |
| File Associations | `GeneralSettings.FileTypes` | Collection | None | — | 由受支持的安装程序和应用包注册的文件类型。 |
| URL Schemes | `GeneralSettings.UrlTypes` | Collection | None | — | 由受支持的安装程序和应用包注册的 URL 方案。 |

### 文件关联 <MinVersion version="1.1" isNewVersion="true" /> {#file-associations}

`GeneralSettings.FileTypes` 中的每一项都有以下属性：

| 属性 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `GeneralSettings.FileTypes[].Name` | String | Yes | 供人阅读的文件类型名称。 |
| `GeneralSettings.FileTypes[].Extension` | String | 扩展名或 MIME 类型 | 扩展名，带不带前导点都行。规范化之后必须是 1–10 个小写字母或数字。 |
| `GeneralSettings.FileTypes[].MimeType` | String | 扩展名或 MIME 类型 | MIME 类型，比如 `application/x-example`。若 Linux 需要而你又没填，Parcel 会自动生成一个。 |

`GeneralSettings.UrlTypes` 中的每一项都有以下属性：

| 属性 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `GeneralSettings.UrlTypes[].Name` | String | Yes | 供人阅读的 URL 类型名称。 |
| `GeneralSettings.UrlTypes[].Schemes` | String | Yes | 一个或多个不含 `://` 的 RFC 3986 方案，用逗号、分号或空格分隔。 |

Parcel 会把这些关联写进 Windows 上的 NSIS 和 MSIX 包、macOS 上的应用包，以及 Linux 上 DEB 和 RPM 的桌面项。

在 Windows 上，文件关联必须有扩展名；只给 MIME 类型的条目 Windows 注册不了。

在 macOS 上，关联需要 `MacOsSettings.CreateBundle`。

## .NET 发布设置 {#net-publish-settings}

这些设置控制 Parcel 在打包之前执行的 `dotnet publish` 操作。

| 设置项 | `.parcel` 属性 | 类型 | 默认值 | 环境变量 | 说明 |
|---|---|---|---|---|---|
| 配置 | `PublishSettings.Configuration` | String | 以 .NET 项目为准 | `PARCEL_NET_CONFIGURATION` | 构建配置。必须以字母开头，且只能含字母、数字、`_` 或 `-`。 |
| Publish Single File | `PublishSettings.PublishSingleFile` | Boolean | 新建的 Parcel 项目默认启用 | `PARCEL_NET_PUBLISH_SINGLE_FILE` | 把托管程序集发布进单个可执行文件。 |
| Publish Trimmed | `PublishSettings.PublishTrimmed` | Boolean | 以 .NET 项目为准 | `PARCEL_NET_PUBLISH_TRIMMED` | 启用裁剪以减小包体积。建议对裁剪后的应用做一遍测试。 |
| Publish AOT | `PublishSettings.PublishAot` | Boolean | 以 .NET 项目为准 | `PARCEL_NET_PUBLISH_AOT` | 启用 Native AOT 编译。 |
| Publish ReadyToRun | `PublishSettings.PublishReadyToRun` | Boolean | 以 .NET 项目为准 | `PARCEL_NET_PUBLISH_READY_TO_RUN` | 预编译程序集以改善启动性能。 |
| 发布为自包含 | `PublishSettings.PublishSelfContained` | Boolean | `true` | `PARCEL_NET_PUBLISH_SELF_CONTAINED` | 把 .NET 运行时一并打包。这是个高级字段，图形界面中不显示。 |
| MSBuild Properties | `PublishSettings.ExtraBuildProperties` | 字符串字典 | Empty | — | 传给 `dotnet publish` 的额外属性。 |
| Exclude Files | `PublishSettings.ExcludeFilePatterns` | glob 模式列表 | Empty | — | 打包前把发布输出中匹配的文件和目录删掉。 |

:::note
Parcel 会遵循 *.csproj 文件中定义的 .NET 发布属性，不必在 Parcel 配置里再写一遍。
:::

## Windows 设置 {#windows-settings}

### 安装程序与 MSIX {#installer-and-msix}

| 设置项 | `.parcel` 属性 | 类型 | 默认值 | 环境变量 | 说明 |
|---|---|---|---|---|---|
| Installer Icon | `Win32Settings.InstallerIcon` | ICO 或 SVG 的路径 | Application Icon | `PARCEL_WINDOWS_INSTALLER_ICON` | 为 NSIS 安装程序和生成的 MSIX 资产覆盖共用图标。 |
| Create Company Folder | `Win32Settings.CompanyFolder` | Boolean | `false` | `PARCEL_WINDOWS_COMPANY_FOLDER` | 在 NSIS 的安装路径和开始菜单路径中加一层公司目录。 |
| License File | `Win32Settings.InstallerLicense` | TXT 或 RTF 的路径 | None | `PARCEL_WINDOWS_INSTALLER_LICENSE` | 在 NSIS 安装程序中显示许可协议接受页。 |
| Requires Admin | `Win32Settings.InstallerRequiresAdmin` | Boolean | `true` | `PARCEL_WINDOWS_INSTALLER_REQUIRES_ADMIN` | 以提权方式把 NSIS 包装到 Program Files 下。禁用时则为当前用户安装。 |
| 随应用一并提供卸载程序 | `Win32Settings.IncludeUninstaller` | Boolean | `true` | `PARCEL_WINDOWS_INCLUDE_UNINSTALLER` | 附带 NSIS 卸载程序，并把应用注册到 Windows 的已安装应用列表中。 |
| Publisher | `Win32Settings.MsixPublisher` | 可分辨名称 | 公司名或应用名 | `PARCEL_WINDOWS_MSIX_PUBLISHER` | MSIX 发布者标识。对已签名的包，它必须与证书主题一字不差。 |

### Signing

`Win32Settings.SigningType` 接受 `None`、`LocalCertificate`、`WindowsCertificateStore`、`AzureTrustedSigning`、`AzureKeyVault`、`AwsKeyManagementService`、`DigiCert`、`GoogleKeyManagementService` 或 `ESigner`。图形界面中把 `AzureTrustedSigning` 称作 **Azure Artifact Signing**。

| 设置项 | `.parcel` 属性 | 类型 | 默认值 | 环境变量 | 说明 |
|---|---|---|---|---|---|
| Signing Type | `Win32Settings.SigningType` | 签名类型 | `None` | `PARCEL_WINDOWS_SIGNING_TYPE` | 选择 Authenticode 签名提供方。 |
| Sign Installer | `Win32Settings.SignInstaller` | Boolean | `true` | `PARCEL_WINDOWS_SIGN_INSTALLER` | 为生成的 NSIS 或 MSIX 包以及应用文件签名。若由应用商店或后续流水线来签名，请关闭此项。 |
| 附加的签名匹配模式 | `Win32Settings.AdditionalSignPatterns` | glob 模式列表 | Empty | — | 把更多代码文件纳入应用签名范围。 |
| Timestamp Server URL | `Win32Settings.SigningTimestampServer` | URL | None | `PARCEL_WINDOWS_SIGNING_TIMESTAMP_SERVER` | 使用本地证书或 Windows 证书存储时所用的时间戳颁发机构。 |
| Local Signing Certificate File | `Win32Settings.LocalSigningCertificate` | PFX 或 P12 的路径 | 用本地证书时必填 | `PARCEL_WINDOWS_LOCAL_SIGNING_CERTIFICATE` | 本地签名所用的证书与私钥。 |
| Local Signing Certificate Password | `Win32Settings.LocalSigningCertificatePassword` | 机密字符串 | Empty | `PARCEL_WINDOWS_LOCAL_SIGNING_CERTIFICATE_PASSWORD` | 保护本地证书的密码。 |
| Store Certificate Name | `Win32Settings.StoreCertificateName` | String | 用证书存储时必填 | `PARCEL_WINDOWS_STORE_CERTIFICATE_NAME` | Windows 证书存储中的证书主题或指纹。 |
| Use Local Machine Certificate Store | `Win32Settings.UseLocalMachineCertificateStore` | Boolean | `false` | `PARCEL_WINDOWS_USE_LOCAL_MACHINE_CERTIFICATE_STORE` | 搜索本地计算机而非当前用户。仅限 Windows。 |
| 自动匹配证书 | `Win32Settings.AutoDetectMatchingCertificate` | Boolean | `false` | `PARCEL_WINDOWS_AUTO_DETECT_MATCHING_CERTIFICATE` | 允许 SignTool 自行挑选匹配的证书。仅限 Windows。 |
| Azure Artifact Signing Endpoint | `Win32Settings.TrustedSigningEndpoint` | Azure 签名 URL | Required | `PARCEL_WINDOWS_TRUSTED_SIGNING_ENDPOINT` | Azure Artifact Signing 服务端点。 |
| Azure Artifact Signing Certificate Profile Name | `Win32Settings.TrustedSigningCertificateProfileName` | String | Required | `PARCEL_WINDOWS_TRUSTED_SIGNING_CERTIFICATE_PROFILE_NAME` | Azure Artifact Signing 证书配置文件。 |
| Azure Artifact Signing Account Name | `Win32Settings.TrustedSigningCodeSigningAccountName` | String | Required | `PARCEL_WINDOWS_TRUSTED_SIGNING_CODE_SIGNING_ACCOUNT_NAME` | Azure Artifact Signing 账户。 |
| Azure Key Vault Name | `Win32Settings.AzureKeyVaultName` | String | 除非 URL 中已指明，否则必填 | `PARCEL_WINDOWS_AZURE_KEY_VAULT_NAME` | Azure Key Vault 名称。 |
| Azure Key Vault URL | `Win32Settings.AzureKeyVaultUrl` | Absolute HTTP(S) URL | 公有 Azure 端点 | `PARCEL_WINDOWS_AZURE_KEY_VAULT_URL` | 完整的保管库 URL，含主权云端点。 |
| Azure Key Vault Certificate Name | `Win32Settings.AzureKeyVaultCertificateName` | String | Required | `PARCEL_WINDOWS_AZURE_KEY_VAULT_CERTIFICATE_NAME` | 存放在 Azure Key Vault 中的证书。 |
| AWS Region Code | `Win32Settings.AwsSigningRegionCode` | String | Required | `PARCEL_WINDOWS_AWS_SIGNING_REGION_CODE` | 存有签名密钥的 AWS 区域。 |
| AWS Signing Certificate File | `Win32Settings.AwsSigningCertificateFile` | Path | Required | `PARCEL_WINDOWS_AWS_SIGNING_CERTIFICATE_FILE` | 与 AWS KMS 中私钥相对应的证书。 |
| AWS 签名密钥 ID 或别名 | `Win32Settings.AwsSigningKeyIdOrAlias` | String | Required | `PARCEL_WINDOWS_AWS_SIGNING_KEY_ID_OR_ALIAS` | AWS KMS 密钥标识符或别名。 |
| DigiCert API Key | `Win32Settings.DigiCertApiKey` | 机密字符串 | Required | `PARCEL_WINDOWS_DIGI_CERT_API_KEY` | DigiCert ONE API 密钥。 |
| DigiCert Keystore | `Win32Settings.DigiCertKeystore` | PKCS#12 的路径 | Required | `PARCEL_WINDOWS_DIGI_CERT_KEYSTORE` | 客户端认证用的密钥库。 |
| DigiCert Storepass | `Win32Settings.DigiCertStorepass` | 机密字符串 | Required | `PARCEL_WINDOWS_DIGI_CERT_STOREPASS` | DigiCert 密钥库的密码。 |
| DigiCert 证书名称或 ID | `Win32Settings.DigiCertCertificateNameOrId` | String | Required | `PARCEL_WINDOWS_DIGI_CERT_CERTIFICATE_NAME_OR_ID` | DigiCert ONE 中的证书名称或 ID。 |
| DigiCert Host | `Win32Settings.DigiCertHost` | HTTP(S) URL | 美国区 DigiCert ONE 主机 | `PARCEL_WINDOWS_DIGI_CERT_HOST` | 覆盖 DigiCert ONE 的服务主机。 |
| Google Access Token | `Win32Settings.GoogleAccessToken` | 机密字符串 | Required | `PARCEL_WINDOWS_GOOGLE_ACCESS_TOKEN` | Google Cloud KMS 的 OAuth 2.0 访问令牌。 |
| Google Signing Keyring | `Win32Settings.GoogleSigningKeyring` | 密钥环资源路径 | Required | `PARCEL_WINDOWS_GOOGLE_SIGNING_KEYRING` | 贯穿 `projects`、`locations` 和 `keyRings` 的资源路径。 |
| Google Signing Certificate File | `Win32Settings.GoogleSigningCertificateFile` | Path | Required | `PARCEL_WINDOWS_GOOGLE_SIGNING_CERTIFICATE_FILE` | 与 Google Cloud KMS 密钥相对应的证书。 |
| Google Signing Certificate Version | `Win32Settings.GoogleSigningCertificateVersion` | String | Latest | `PARCEL_WINDOWS_GOOGLE_SIGNING_CERTIFICATE_VERSION` | 要使用的具体密钥版本。 |
| eSigner User Name | `Win32Settings.ESignerUserName` | String | Required | `PARCEL_WINDOWS_E_SIGNER_USER_NAME` | SSL.com 账户用户名。 |
| eSigner Password | `Win32Settings.ESignerPassword` | 机密字符串 | Required | `PARCEL_WINDOWS_E_SIGNER_PASSWORD` | SSL.com 账户密码。 |
| eSigner Key Password | `Win32Settings.ESignerKeyPassword` | 机密字符串 | Required | `PARCEL_WINDOWS_E_SIGNER_KEY_PASSWORD` | Base64 编码的 TOTP 密钥。 |
| eSigner Credential ID | `Win32Settings.ESignerCredentialId` | String | Required | `PARCEL_WINDOWS_E_SIGNER_CREDENTIAL_ID` | SSL.com 签名凭据标识符。 |
| eSigner Sandbox | `Win32Settings.ESignerSandbox` | Boolean | `false` | `PARCEL_WINDOWS_E_SIGNER_SANDBOX` | 使用 SSL.com 的沙箱服务。 |

## macOS 设置 {#macos-settings}

### 应用包、DMG 与 PKG {#bundle-dmg-and-pkg}

| 设置项 | `.parcel` 属性 | 类型 | 默认值 | 环境变量 | 说明 |
|---|---|---|---|---|---|
| Create Bundle | `MacOsSettings.CreateBundle` | Boolean | 新项目默认为 `true` | `PARCEL_MACOS_CREATE_BUNDLE` | 生成 macOS 的 `.app` 应用包。DMG、PKG、权限和文件关联都以应用包为前提。 |
| Bundle Identifier | `MacOsSettings.BundleIdentifier` | 反向 DNS 字符串 | 由公司名和包名推导得出 | `PARCEL_MACOS_BUNDLE_IDENTIFIER` | 用于签名和分发的 `CFBundleIdentifier`。 |
| Team ID | `MacOsSettings.TeamId` | 10 位大写字母或数字 | None | `PARCEL_MACOS_TEAM_ID` | 用于签名和公证的 Apple Developer 团队标识符。 |
| App Category | `MacOsSettings.BundleCategory` | Apple 应用包类别 | `Other` | `PARCEL_MACOS_BUNDLE_CATEGORY` | macOS 和 App Store 中的应用类别。 |
| Application Icon | `MacOsSettings.AppIcon` | ICNS 或 SVG 的路径 | Application Icon | `PARCEL_MACOS_APP_ICON` | 为应用包覆盖共用图标。 |
| Permissions | `MacOsSettings.Permissions` | 权限说明字典 | Empty | — | 为相机、麦克风、定位、通讯录、日历、桌面、文稿、下载和网络添加 macOS 用途说明。 |
| 资源文件匹配模式 | `MacOsSettings.BundleResourcePatterns` | glob 模式列表 | Empty | — | 把匹配的文件挪到 `Contents/Resources`，并在原位置放上符号链接。 |
| Automatically Move Bundle Frameworks | `MacOsSettings.AutomaticallyMoveBundleFrameworks` | Boolean | `false` | `PARCEL_MACOS_AUTOMATICALLY_MOVE_BUNDLE_FRAMEWORKS` | 用于重定位 framework 的高级兼容选项。图形界面中不显示。 |
| Automatically Move Bundle Resources | `MacOsSettings.AutomaticallyMoveBundleResources` | Boolean | `false` | `PARCEL_MACOS_AUTOMATICALLY_MOVE_BUNDLE_RESOURCES` | 用于重定位资源的高级兼容选项。图形界面中不显示。 |
| DMG Background Image | `MacOsSettings.DmgBackground` | TIFF 的路径 | None | `PARCEL_MACOS_DMG_BACKGROUND` | DMG 窗口中显示的背景图。 |
| DMG Layout | `MacOsSettings.DmgLayout` | 布局对象 | Parcel 标准布局 | — | 窗口、网格、图标、文字、背景色、应用位置以及 Applications 链接位置等设置。 |
| DMG License File | `MacOsSettings.DmgLicense` | Path | None | `PARCEL_MACOS_DMG_LICENSE` | 嵌入到 DMG 根目录的文件。 |
| Install Location | `MacOsSettings.InstallerLocation` | 绝对路径 | `/Applications` | `PARCEL_MACOS_INSTALLER_LOCATION` | PKG 的安装目录。这是个高级字段，图形界面中不显示。 |
| Install Scripts Directory | `MacOsSettings.InstallerScripts` | 目录路径 | None | `PARCEL_MACOS_INSTALLER_SCRIPTS` | 存放可执行的 `preinstall` 和 `postinstall` 脚本的目录。这是个高级字段，图形界面中不显示。 |
| Package Identifier | `MacOsSettings.InstallerIdentifier` | 反向 DNS 字符串 | 应用包标识符 | `PARCEL_MACOS_INSTALLER_IDENTIFIER` | 由 PKG 安装程序注册的标识符。这是个高级字段，图形界面中不显示。 |

DMG 布局对象支持下列高级属性：

| `.parcel` 属性 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `MacOsSettings.DmgLayout.BackgroundColorRed` | Number | `1` | 窗口背景色的红色分量。 |
| `MacOsSettings.DmgLayout.BackgroundColorGreen` | Number | `1` | 窗口背景色的绿色分量。 |
| `MacOsSettings.DmgLayout.BackgroundColorBlue` | Number | `1` | 窗口背景色的蓝色分量。 |
| `MacOsSettings.DmgLayout.GridOffsetX` | Integer | `0` | 网格的水平偏移。 |
| `MacOsSettings.DmgLayout.GridOffsetY` | Integer | `0` | 网格的垂直偏移。 |
| `MacOsSettings.DmgLayout.GridSpacing` | Integer | `100` | 网格位置之间的间距。 |
| `MacOsSettings.DmgLayout.X` | Integer | `100` | DMG 窗口的水平位置。 |
| `MacOsSettings.DmgLayout.Y` | Integer | `100` | DMG 窗口的垂直位置。 |
| `MacOsSettings.DmgLayout.Width` | Integer | `660` | DMG 窗口宽度。 |
| `MacOsSettings.DmgLayout.Height` | Integer | `422` | DMG 窗口高度。 |
| `MacOsSettings.DmgLayout.IconSize` | Integer | `128` | 图标大小，以像素为单位。 |
| `MacOsSettings.DmgLayout.TextSize` | Integer | `12` | 图标标签的文字大小。 |
| `MacOsSettings.DmgLayout.BundlePositionX` | Integer | `173` | 应用包的水平位置。 |
| `MacOsSettings.DmgLayout.BundlePositionY` | Integer | `231` | 应用包的垂直位置。 |
| `MacOsSettings.DmgLayout.ApplicationsPositionX` | Integer | `485` | Applications 链接的水平位置。 |
| `MacOsSettings.DmgLayout.ApplicationsPositionY` | Integer | `231` | Applications 链接的垂直位置。 |

### 应用签名 {#application-signing}

`MacOsSettings.SigningCredentialsType` 接受 `None`、`AdHoc`、`KeyChainIdentity`、`P12Certificate` 或 `PemCertificate`。

| 设置项 | `.parcel` 属性 | 类型 | 默认值 | 环境变量 | 说明 |
|---|---|---|---|---|---|
| Signing Credentials | `MacOsSettings.SigningCredentialsType` | 凭据类型 | `AdHoc` | `PARCEL_MACOS_SIGNING_CREDENTIALS_TYPE` | 选择应用包、代码以及（可选的）DMG 以何种方式签名。 |
| Enable App Sandbox | `MacOsSettings.EnableSandbox` | Boolean | `false` | `PARCEL_MACOS_ENABLE_SANDBOX` | 让应用跑在 macOS App Sandbox 中，只能访问其权利所涵盖的资源。发布到 Mac App Store 必须开启。 |
| Sign DMG | `MacOsSettings.SignDmg` | Boolean | `true` | `PARCEL_MACOS_SIGN_DMG` | 用应用签名凭据为生成的 DMG 签名。 |
| 附加的签名匹配模式 | `MacOsSettings.AdditionalSignPatterns` | glob 模式列表 | Empty | — | 把更多代码文件纳入应用包签名范围。 |
| Signing Identity | `MacOsSettings.SigningIdentity` | 钥匙串标识 | 用钥匙串时必填 | `PARCEL_MACOS_SIGNING_IDENTITY` | macOS 钥匙串中的应用签名标识。 |
| Signing P12 Certificate | `MacOsSettings.SigningP12Certificate` | P12 的路径 | 用 P12 时必填 | `PARCEL_MACOS_SIGNING_P12_CERTIFICATE` | 便携的应用签名证书与私钥。 |
| Signing Password | `MacOsSettings.SigningP12Password` | 机密字符串 | Empty | `PARCEL_MACOS_SIGNING_P12_PASSWORD` | 保护应用 P12 证书的密码。 |
| Signing PEM Certificate | `MacOsSettings.SigningPemCertificate` | PEM 的路径 | 用 PEM 时必填 | `PARCEL_MACOS_SIGNING_PEM_CERTIFICATE` | PEM 格式的应用签名证书。 |
| Deep Signing | `MacOsSettings.SignDeep` | Boolean | `false` | `PARCEL_MACOS_SIGN_DEEP` | 用于深度签名的高级兼容选项。图形界面中不显示。 |

### 安装程序签名 {#installer-signing}

PKG 安装程序需要一张单独的安装程序证书。`MacOsSettings.InstallerSigningCredentialsType` 接受的凭据类型与[应用签名](#application-signing)相同。临时签名（ad hoc）造不出已签名的 PKG。

| 设置项 | `.parcel` 属性 | 类型 | 默认值 | 环境变量 | 说明 |
|---|---|---|---|---|---|
| Installer Signing Credentials | `MacOsSettings.InstallerSigningCredentialsType` | 凭据类型 | `None` | `PARCEL_MACOS_INSTALLER_SIGNING_CREDENTIALS_TYPE` | 选择用于为 PKG 安装程序签名的证书。 |
| Installer Signing Identity | `MacOsSettings.InstallerSigningIdentity` | 钥匙串标识 | 用钥匙串时必填 | `PARCEL_MACOS_INSTALLER_SIGNING_IDENTITY` | macOS 钥匙串中的安装程序标识。 |
| Installer Signing P12 Certificate | `MacOsSettings.InstallerSigningP12Certificate` | P12 的路径 | 用 P12 时必填 | `PARCEL_MACOS_INSTALLER_SIGNING_P12_CERTIFICATE` | 便携的安装程序证书与私钥。 |
| Installer Signing Password | `MacOsSettings.InstallerSigningP12Password` | 机密字符串 | Empty | `PARCEL_MACOS_INSTALLER_SIGNING_P12_PASSWORD` | 保护安装程序 P12 证书的密码。 |
| Installer Signing PEM Certificate | `MacOsSettings.InstallerSigningPemCertificate` | PEM 的路径 | 用 PEM 时必填 | `PARCEL_MACOS_INSTALLER_SIGNING_PEM_CERTIFICATE` | PEM 格式的安装程序签名证书。 |

### Notarization

`MacOsSettings.NotaryCredentialsType` 接受 `None`、`KeyChainProfile` 或 `AppleAccount`。

| 设置项 | `.parcel` 属性 | 类型 | 默认值 | 环境变量 | 说明 |
|---|---|---|---|---|---|
| Notary Credentials | `MacOsSettings.NotaryCredentialsType` | 凭据类型 | `None` | `PARCEL_MACOS_NOTARY_CREDENTIALS_TYPE` | 选择向 Apple 公证服务认证的方式。 |
| Notary Keychain Profile | `MacOsSettings.NotaryKeychainProfile` | String | 用钥匙串配置文件时必填 | `PARCEL_MACOS_NOTARY_KEYCHAIN_PROFILE` | 存放在 macOS 钥匙串中的 `notarytool` 配置文件。 |
| Notary Apple ID | `MacOsSettings.NotaryAppleId` | 电子邮件地址 | 用 Apple 账户时必填 | `PARCEL_MACOS_NOTARY_APPLE_ID` | 用于公证的 Apple ID。 |
| Notary App Password | `MacOsSettings.NotaryAppPassword` | 机密字符串 | 用 Apple 账户时必填 | `PARCEL_MACOS_NOTARY_APP_PASSWORD` | 公证服务所用的 App 专用密码。 |

## Linux 设置 {#linux-settings}

| 设置项 | `.parcel` 属性 | 类型或取值 | 默认值 | 环境变量 | 说明 |
|---|---|---|---|---|---|
| Install Directory Name | `LinuxSettings.InstallDirName` | 小写的包目录名 | `app-{package-name}` | `PARCEL_LINUX_INSTALL_DIR_NAME` | 在 `/usr/share` 下创建的目录。必须以字母或数字开头和结尾，最多 100 个字符。 |
| Application Icon | `LinuxSettings.AppIcon` | PNG 或 SVG 的路径 | Application Icon | `PARCEL_LINUX_APP_ICON` | 为 DEB 和 RPM 包覆盖共用图标。 |
| Maintainer | `LinuxSettings.Maintainer` | String | 先取公司名，再取包名 | `PARCEL_LINUX_MAINTAINER` | 包维护者，最好写成 `Name <email@example.com>` 格式。最多 255 个字符。 |
| Copyright | `LinuxSettings.CopyrightFile` | Path | None | `PARCEL_LINUX_COPYRIGHT_FILE` | 写进 DEB 和 RPM 元数据的版权文件。 |
| Desktop Category | `LinuxSettings.DesktopCategory` | Linux 桌面类别 | `Application` | `PARCEL_LINUX_DESKTOP_CATEGORY` | 桌面菜单中使用的类别，并会映射到包管理器的元数据。 |
| 创建 `/usr/bin/` 符号链接 | `LinuxSettings.CreateBinSymlink` | Boolean | `true` | `PARCEL_LINUX_CREATE_BIN_SYMLINK` | 为应用的可执行文件创建一个命令行符号链接。 |
| Additional DEB Dependencies | `LinuxSettings.AdditionalDebDependencies` | List | Empty | — | 添加 Debian 包依赖。备选项之间用竖线分隔。 |
| Additional RPM Dependencies | `LinuxSettings.AdditionalRpmDependencies` | List | Empty | — | 添加 RPM 的包名或能力（capability）。 |

你可以使用主要的 [freedesktop 类别](https://specifications.freedesktop.org/menu-spec/latest/category-registry.html)以及常见的附加类别，例如 `Development`、`Education`、`Game`、`Graphics`、`Network`、`Office`、`Science`、`Settings`、`System`、`Utility`、`WebBrowser`、`TextEditor`、`TerminalEmulator`。

## 另请参阅 {#see-also}

- [Parcel 配置准备](/tools/parcel/setup)
- [Parcel 命令行参考](/tools/parcel/command-line-reference)
- [为 Windows 打包](/tools/parcel/packaging-for-windows)
- [为 macOS 打包](/tools/parcel/packaging-for-macos)
- [为 Linux 打包](/tools/parcel/packaging-for-linux)

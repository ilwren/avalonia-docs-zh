---
id: android
title: Android
description: 把 Avalonia 应用构建、签名并发布为面向 Android 设备的 APK 或 AAB。
doc-type: how-to
---

为 Android 发布 Avalonia 应用会生成 Android 安装包（APK）或 Android App Bundle（AAB）文件。APK 用于把应用直接装到 Android 设备上，AAB 则用于发布到 Google Play。

## 在模拟器上运行 {#running-on-an-emulator}

在 Android 项目目录下，用这条命令构建并运行：

```bash
dotnet build
dotnet run
```

这会把应用部署到默认的 Android 模拟器。如果没有模拟器在运行，系统会用 Android SDK 中配置的第一个可用 AVD（Android 虚拟设备）自动启动一个。

## 在真机上运行 {#running-on-a-device}

部署到实体 Android 设备的步骤：

1. 确认设备上的 Android 版本与 `AndroidManifest.xml` 中的受支持版本或目标版本相符。
2. 用 USB 把设备连到开发机上。
3. 在设备的开发者选项中启用 **USB 调试**。
4. 若 USB 默认连接模式是「仅充电」，请切换到 MTP 或其他模式，ADB 才能发现这台设备。

然后运行：

```bash
dotnet run
```

应用就会被部署到所连设备上并启动。

## 发布 {#publishing}

### 创建密钥库文件 {#create-a-keystore-file}

开发阶段，.NET for Android 用调试密钥库给应用签名，这样就能直接部署到模拟器、或部署到允许运行可调试应用的设备上。但这个密钥库不能用于分发应用，发布版构建必须创建并使用自己的私有密钥库来签名。

:::tip
这一步只需做一次。同一个密钥库会用于发布后续更新，也可以给别的应用签名。请妥善备份密钥库和密码——一旦丢失，你就再也无法以同一身份给应用签名了。
:::

用 JDK 自带的 `keytool` 运行下列参数：

```bash
keytool -genkeypair -v -keystore myapp.keystore -alias myapp -keyalg RSA -keysize 2048 -validity 10000
```

系统会提示你设置并确认密码，然后填写姓名和组织信息。这些信息会写进证书，但不会显示在你的应用里。

### 构建并签名你的应用 {#build-and-sign-your-app}

进入 Android 项目文件夹，带上签名参数运行 `dotnet publish`：

```bash
dotnet publish -f net9.0-android -c Release \
  -p:AndroidKeyStore=true \
  -p:AndroidSigningKeyStore=myapp.keystore \
  -p:AndroidSigningKeyAlias=myapp \
  -p:AndroidSigningKeyPass=mypassword \
  -p:AndroidSigningStorePass=mypassword
```

这会构建并签名应用，在 `bin/Release/net9.0-android/publish` 文件夹中生成 AAB 和 APK 文件。已签名的那份文件名里带 **-signed**。

:::caution
在共用环境中，别把密码直接写在命令行上。请改用 `env:` 或 `file:` 前缀（见下文）。
:::

#### 安全地处理密码 {#secure-password-handling}

`AndroidSigningKeyPass` 和 `AndroidSigningStorePass` 都支持 `env:` 和 `file:` 前缀，以免密码出现在构建日志里。

用环境变量：
```bash
dotnet publish -f net9.0-android -c Release \
  -p:AndroidKeyStore=true \
  -p:AndroidSigningKeyStore=myapp.keystore \
  -p:AndroidSigningKeyAlias=myapp \
  -p:AndroidSigningKeyPass=env:ANDROID_SIGNING_PASSWORD \
  -p:AndroidSigningStorePass=env:ANDROID_SIGNING_PASSWORD
```

用文件：
```bash
dotnet publish -f net9.0-android -c Release \
  -p:AndroidKeyStore=true \
  -p:AndroidSigningKeyStore=myapp.keystore \
  -p:AndroidSigningKeyAlias=myapp \
  -p:AndroidSigningKeyPass=file:/path/to/password.txt \
  -p:AndroidSigningStorePass=file:/path/to/password.txt
```

:::note
当 `AndroidPackageFormat` 设为 `aab` 时，不支持 `env:` 前缀。
:::

### 构建属性参考 {#build-properties-reference}

下列属性既可以在命令行上用 `-p:` 传入，也可以写在项目文件的 `<PropertyGroup>` 中：

| 属性 | 说明 |
|---|---|
| `AndroidKeyStore` | 设为 `true` 表示给应用签名。默认值：`false`。 |
| `AndroidPackageFormats` | 以分号分隔。可设为 `aab`、`apk` 或 `aab;apk`。发布版默认：`aab;apk`。 |
| `AndroidSigningKeyAlias` | 密钥库中密钥的别名。 |
| `AndroidSigningKeyPass` | 密钥密码。支持 `env:` 和 `file:` 前缀。 |
| `AndroidSigningKeyStore` | 密钥库文件名。 |
| `AndroidSigningStorePass` | 密钥库密码。支持 `env:` 和 `file:` 前缀。 |
| `ApplicationTitle` | 应用对用户显示的名称。 |
| `ApplicationId` | 唯一标识，比如 `com.companyname.myapp`。 |
| `ApplicationVersion` | 构建版本号。 |
| `ApplicationDisplayVersion` | 显示用的版本字符串。 |
| `PublishTrimmed` | 是否裁剪未使用的代码。发布版默认：`true`。 |

#### 把属性写进项目文件 {#define-properties-in-your-project-file}

与其把一堆参数都敲在命令行上，不如把它们写进 `.csproj`：

```xml
<PropertyGroup Condition="$(TargetFramework.Contains('-android')) and '$(Configuration)' == 'Release'">
    <AndroidKeyStore>true</AndroidKeyStore>
    <AndroidSigningKeyStore>myapp.keystore</AndroidSigningKeyStore>
    <AndroidSigningKeyAlias>myapp</AndroidSigningKeyAlias>
    <AndroidSigningKeyPass>env:ANDROID_SIGNING_PASSWORD</AndroidSigningKeyPass>
    <AndroidSigningStorePass>env:ANDROID_SIGNING_PASSWORD</AndroidSigningStorePass>
</PropertyGroup>
```

然后只需这样发布：
```bash
dotnet publish -f net9.0-android -c Release
```

### 分发应用 {#distribute-the-app}

- **Google Play**：通过 [Google Play Console](https://play.google.com/console) 提交你的 AAB 文件。详见 [Upload your app to the Play Console](https://developer.android.com/studio/publish/upload-bundle)。
- **直接下载**：把 APK 放在网站或文件共享上。用户需要在自己的设备上允许安装来源不明的应用，详见 [User opt-in for unknown apps](https://developer.android.com/studio/publish#publishing-unknown)。

## 另请参阅 {#see-also}

- [Android 平台配置](/docs/platform-specific-guides/android)

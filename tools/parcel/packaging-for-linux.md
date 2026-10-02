---
id: packaging-for-linux
title: 为 Linux 打包应用
description: 用 Parcel 把 Avalonia 应用打包成 Linux 安装包，支持 DEB、RPM 和 ZIP 格式，还能处理依赖管理和桌面集成。
sidebar_label: Linux
doc-type: reference
tags:
  - avalonia plus
  - avalonia pro
  - avalonia enterprise
---

Parcel 能为不同的 Linux 包管理器和分发方式生成安装包。

## Supported Package Formats

| 格式 | CLI 代号 | 最适合 |
|---|---|---|
| DEB 包（`.deb`） | `deb` | Debian、Ubuntu 及其他基于 Debian 的发行版 |
| RPM 包（`.rpm`） | `rpm` | Fedora、RHEL 及其他基于 RPM 的发行版 |
| ZIP 归档（`.zip`） | `zip` | 不与包管理器集成的便携式分发 |

DEB 和 RPM 包会带上 `.desktop` 条目，还能注册图标、文件关联、URL 方案、包依赖，以及一个可选的 `/usr/bin` 符号链接。

各设置的完整名称、类型、默认值和环境变量，请见 [Parcel 配置参考](/tools/parcel/configuration-reference#linux-settings)。

## Dependencies

Parcel 会在包元数据中声明下列运行时依赖。若你的应用或所用发行版还需要别的库，可通过附加依赖设置添加。

### DEB 依赖 {#deb-dependencies}

- `libc6`
- `libgcc1`
- `libgssapi-krb5-2`
- `libstdc++6`
- `zlib1g`
- `libssl1.0.0`、`libssl1.0.2`、`libssl1.1` 或 `libssl3` 其中之一
- `libicu` 或带版本号的 `libicu` 包

### RPM 依赖 {#rpm-dependencies}

- `glibc`
- `libgcc`
- `krb5-libs`
- `libstdc++`
- `zlib`
- `openssl-libs`
- `libicu`

## Bundle Configuration

用 Linux 设置来配置桌面集成和品牌元素。

### Common Properties

**Application Name**:

在应用启动器和桌面菜单中显示的名称。Parcel 会把它写进 `.desktop` 条目。

**Package Name**:

包元数据和输出文件名中使用的包标识符。对 Linux 包，Parcel 会把它规范化为小写。

**Install Directory Name**:

`/usr/share` 下应用目录的名称，默认为 `app-{package-name}`。只能用小写字母、数字、短横线、下划线或点，且必须以字母或数字开头和结尾。

### DEB/RPM Specific Properties

Debian 和 RPM 包的其他配置属性。

**Application Icon**:

可选的 Linux 图标，会覆盖**应用图标**。Parcel 会自动完成这些事：

- 按合适的分辨率生成 hicolor 图标主题条目
- 在 `.desktop` 文件中链接该图标

**支持的格式**：PNG、SVG

**维护者**：

包维护者或公司名称。Parcel 会把它写进包元数据。

:::note
若你没填这一项，Parcel 会取**公司**；若**公司**也为空，则取**包名**。
:::

**Desktop Category**:

桌面菜单和启动器中的类别，决定应用出现在菜单的哪个位置。Parcel 采用 [freedesktop.org 类别注册表](https://specifications.freedesktop.org/menu-spec/latest/category-registry.html)。

**版权**：

版权或许可证文件的路径。Parcel 会把该文件写进 DEB 和 RPM 的包元数据。

**创建 `/usr/bin/` 符号链接**：

为应用的可执行文件创建符号链接，用户便可从终端启动应用。该设置默认开启。

**附加 DEB 依赖**和**附加 RPM 依赖**：

添加 Parcel 默认之外的依赖。DEB 和 RPM 的依赖要分别配置：DEB 的备选包名之间用 `|` 分隔，RPM 则填包名或能力。

### 桌面集成 {#desktop-integration}

在 **Basics** 下配置文件关联和 URL 方案。Parcel 会把相关的 MIME 元数据和启动信息写进 DEB 和 RPM 包。至于在 Avalonia 应用中如何响应这类激活，请见[文件关联与 URL 方案](/tools/parcel/configuration-reference#file-associations)和[可激活生命周期](/docs/services/activatable-lifetime#handling-uri-activation)。

## Installation & Removal

### DEB Packages (Debian/Ubuntu)

**安装**：
```bash
sudo apt install ./my-app.deb
```

**卸载**：
```bash
sudo apt remove my-app
```

### RPM Packages (Fedora/RHEL)

**安装**：
```bash
sudo dnf install ./my-app.rpm
# or
sudo rpm -i ./my-app.rpm
```

**卸载**：
```bash
sudo dnf remove my-app
# or
sudo rpm -e my-app
```

### ZIP Archives

**解压并运行**：
```bash
unzip my-app.zip
cd my-app
./my-awesome-app
```

## 另请参阅 {#see-also}

- [Parcel 配置准备](/tools/parcel/setup)
- [Parcel 配置参考](/tools/parcel/configuration-reference)
- [Parcel 命令行参考](/tools/parcel/command-line-reference)

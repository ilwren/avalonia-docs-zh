---
id: embedded-linux
title: Embedded Linux
description: 用 DRM/KMS 在嵌入式 Linux 设备上发布、传输并运行 Avalonia 应用。
doc-type: how-to
---

把 Avalonia 应用部署到嵌入式 Linux 设备，与桌面部署有几点不同：目标机上（多数情况下）没有包管理器，没有桌面环境可供集成，应用通常是唯一的图形进程。本文讲的是如何在嵌入式 Linux 目标机上发布、传输并运行你的应用。

## 发布 {#publishing}

请把应用发布为自包含的单文件可执行程序，并指定合适的运行时标识（RID）。嵌入式目标机上基本不会预装 .NET 运行时，所以强烈建议采用自包含部署。

选择与你目标硬件相匹配的 RID：

| 目标架构 | RID | 常见设备 |
|---|---|---|
| ARM 32 位 | `linux-arm` | 树莓派（32 位系统）、较老的 ARM 单板机 |
| ARM 64 位 | `linux-arm64` | 树莓派 4/5（64 位系统）、NVIDIA Jetson、BeagleBone AI，以及大多数现代 ARM 单板机 |
| x64 | `linux-x64` | Intel NUC、工业平板电脑、AMD 嵌入式板卡 |

```bash
dotnet publish -c Release -r linux-arm64 --self-contained true \
  -p:PublishSingleFile=true \
  -p:PublishTrimmed=true \
  -p:PublishReadyToRun=true \
  -p:IncludeNativeLibrariesForSelfExtract=true
```

把 `linux-arm64` 换成适合你设备的 RID。

### 发布选项解读 {#publish-options-explained}

| 选项 | 用途 |
|---|---|
| `--self-contained true` | 把 .NET 运行时一并打包，这样目标机上就不必预装。 |
| `-p:PublishSingleFile=true` | 产出单个可执行文件，而不是一整个装满程序集的目录。 |
| `-p:PublishTrimmed=true` | 移除未使用的代码，显著缩小产物体积。 |
| `-p:PublishReadyToRun=true` | 把程序集预编译成原生代码，启动更快。 |
| `-p:IncludeNativeLibrariesForSelfExtract=true` | 把原生库（SkiaSharp、HarfBuzz）嵌进这个单文件里。 |

:::tip
裁剪可能会把你通过反射用到的代码也删掉。若运行时碰到 `MissingMethodException` 之类的错误，请配置[裁剪器根程序集](https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/trimming-options)来保住受影响的类型。
:::

## 传输到设备上 {#transferring-to-the-device}

把发布产物拷到目标设备。常见做法有：

**SCP（走 SSH）：**
```bash
scp -r ./publish/ user@device-hostname:/home/user/myapp/
```

**rsync（增量传输，反复部署时更快）：**
```bash
rsync -avz --progress ./publish/ user@device-hostname:/home/user/myapp/
```

**U 盘：**
把发布目录拷到 U 盘上，在目标机上挂载，再把文件复制过去。

## 运行应用 {#running-the-application}

给可执行文件加上执行权限，并带 `--drm` 参数运行：

```bash
chmod +x /home/user/myapp/MyApp
sudo ./home/user/myapp/MyApp --drm
```

`--drm` 参数告诉应用改用 DRM/KMS 输出，而不是去连 X11 或 Wayland。之所以要加 `sudo`，是因为访问 DRM 设备通常需要 root 权限。

:::tip
想避免以 root 身份运行，把你的用户加入 `video` 和 `input` 组：
```bash
sudo usermod -aG video,input $USER
```
注销再重新登录，组变更才会生效。此后运行应用就不必加 `sudo` 了。
:::

## 开机自启 {#auto-starting-on-boot}

面向自助终端或一体机场景时，可以配置应用在设备启动时自动运行。

### 使用 systemd 服务 {#using-a-systemd-service}

在 `/etc/systemd/system/myapp.service` 创建一个服务文件：

```ini
[Unit]
Description=My Avalonia Application
After=multi-user.target

[Service]
Type=simple
User=appuser
Group=appuser
SupplementaryGroups=video input
ExecStart=/opt/myapp/MyApp --drm
Restart=on-failure
RestartSec=5
Environment=DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1

[Install]
WantedBy=multi-user.target
```

把 `appuser` 换成你设备上的用户账号，并把 `ExecStart` 路径改成实际的部署位置。`/opt/myapp/` 是嵌入式系统上存放应用二进制的常见惯例，当然放哪儿都行。

启用并启动该服务：

```bash
sudo systemctl enable myapp.service
sudo systemctl start myapp.service
```

### 查看日志 {#viewing-logs}

```bash
journalctl -u myapp.service -f
```

## 缩小镜像体积 {#reducing-image-size}

嵌入式系统的存储往往很紧张。有几招可以缩小部署后的应用体积：

- **裁剪**（上面已启用）会移除未使用的 .NET 程序集和方法。
- **Native AOT** 编译产出的二进制更小、完全原生，也没有 .NET 运行时的开销。详见 [Native AOT 发布](/docs/deployment/native-aot)。
- **固定区域性全球化**（`DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1`）可去掉对 ICU 库的依赖，省下约 30 MB。只有当你的应用不需要按区域设置做格式化或排序时才用这招。

## 目标机上必需的库 {#required-libraries-on-the-target}

即便采用自包含部署，目标机上仍需具备若干原生 Linux 库。在基于 Debian 的系统上（Raspberry Pi OS、Armbian、Ubuntu）：

```bash
sudo apt-get install libgbm1 libgl1-mesa-dri libegl1-mesa libinput10
```

其他发行版也有对应的包，只是名字略有出入。

| NuGet 包 | 它提供什么 | Avalonia 为何需要它 |
|---|---|---|
| `libgbm1` | 通用缓冲区管理（GBM）分配器，负责创建 GPU 可访问的缓冲区，供 DRM 扫描输出到显示器。 | 在 DRM 模式下运行时，Avalonia 通过 GBM 分配渲染表面。没有它就创建不出帧缓冲。 |
| `libgl1-mesa-dri` | Mesa 的 DRI（直接渲染基础设施）驱动，也就是把 OpenGL 调用翻译成硬件指令的那些 GPU 专属模块（比如树莓派的 `vc4`、Mali GPU 的 `panfrost`）。 | 它提供真正的 GPU 加速。即便设备没有独立 GPU，软件光栅化器（`llvmpipe`）也在这里面。 |
| `libegl1-mesa` | Mesa 对 EGL 的实现（EGL 最初是 "Embedded-System Graphics Library" 的缩写，如今已是 Khronos 维护的一个独立名称）。EGL 是一套与平台无关的 API，夹在渲染 API（比如 OpenGL ES）和原生显示系统之间，负责创建渲染上下文、把它绑定到绘图表面，并管理缓冲区、同步对象等资源。在用 X11 的桌面 Linux 上，EGL 与 X 服务器打交道；而在嵌入式 DRM 方案中，EGL 则直接对接 GBM 表面。 | Avalonia 用 EGL 创建 OpenGL ES 渲染上下文，并把它绑定到由 DRM 帧缓冲支撑的 GBM 表面上。正是这一步，把 Avalonia 的绘图指令连到了显示器上真实的像素。 |
| `libinput10` | libinput 库。它提供统一的 API，经由内核的 evdev 接口读取键盘、鼠标、触摸板和触摸屏的输入事件。 | 在桌面环境之外运行时，Avalonia 全部的用户输入都经由 libinput 读取。没有它，触摸、鼠标和键盘输入统统失灵。 |

## 另请参阅 {#see-also}

- [嵌入式 Linux 平台集成](/docs/platform-specific-guides/embedded-linux)：帧缓冲与 DRM 的概念
- [在树莓派上运行](/docs/platform-specific-guides/embedded-linux/raspberry-pi)：针对具体硬件的完整演练
- [桌面 Linux 部署](/docs/deployment/linux)：关于 `.deb` 打包
- [Native AOT 发布](/docs/deployment/native-aot)

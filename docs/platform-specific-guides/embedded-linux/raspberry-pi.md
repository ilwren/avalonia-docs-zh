---
id: raspberry-pi
title: 在树莓派上运行 Avalonia
---

import RaspbianLiteDrmKmsCubeScreenshot from '/img/guides/platform-specific-guides/raspberry-pi/raspbian-lite-drm-kmscube.gif';
import RaspbianLiteDrmDesktopScreenshot from '/img/guides/platform-specific-guides/raspberry-pi/raspbian-lite-drm-desktop.jpg';
import RaspbianLiteRaspberryScreenshot from '/img/guides/platform-specific-guides/raspberry-pi/raspbian-lite-drm-run-on-raspberry.jpg';

## 所需硬件 {#required-hardware}

把 Raspbian Stretch（2018-11-13）刷进一张 8GB SD 卡，`balenaEtcher` 是个趁手的工具。

插上卡，启动 `Raspberry Pi`。

你可以照着 [Raspbian 与 .NET Core 配置指南](https://blogs.msdn.microsoft.com/david/2017/07/20/setting_up_raspian_and_dotnet_core_2_0_on_a_raspberry_pi/)来做，下面是步骤摘要。

## 安装所需的软件包 {#installing-required-packages}

* 安装 `curl`、`libunwind8`、`gettext` 和 `apt-transport-https`。`curl` 和 `apt-transport-https` 通常已是最新的。

```bash
sudo apt-get install curl libunwind8 gettext apt-transport-https
```

* 下载 tar 包。

```bash
curl -sSL -o dotnet.tar.gz https://dotnetcli.blob.core.windows.net/dotnet/Runtime/release/2.0.0/dotnet-runtime-latest-linux-arm.tar.gz
```

* 把 tar 包解压到 `/opt/dotnet`。

```bash
sudo mkdir -p /opt/dotnet && sudo tar zxf dotnet.tar.gz -C /opt/dotnet
```

* 链接 `dotnet` 二进制文件。

```bash
sudo ln -s /opt/dotnet/dotnet /usr/local/bin
```

另一种办法：以超级用户身份登录（运行 "sudo su"）

```bash
apt-get -y install curl libunwind8 gettext apt-transport-https
curl -sSL -o dotnet.tar.gz https://dotnetcli.blob.core.windows.net/dotnet/Runtime/release/2.0.0/dotnet-runtime-latest-linux-arm.tar.gz
mkdir -p /opt/dotnet && sudo tar zxf dotnet.tar.gz -C /opt/dotnet
ln -s /opt/dotnet/dotnet /usr/local/bin
```

:::note
注意脚本的换行符，应当用 `LF` 而非 `CR LF`。把脚本存为 `.sh` 文件，在 `Raspberry Pi` 上用 bash `filename.sh` 运行。
:::

## 发布应用 {#publishing-the-app}

* 要在 `Raspberry Pi` 上运行 `Avalonia` 应用，你需要用到这个 NuGet 包：

[SkiaSharp.NativeAssets.Linux](https://www.nuget.org/packages/SkiaSharp.NativeAssets.Linux/)

它内含 `libSkiaSharp.so`。

* 现在用下面的命令发布应用：

```bash
dotnet publish -r linux-arm -f netcoreapp2.0
```

* 把 publish 目录拷到 `Raspberry Pi` 上，用 `dotnet publish/ApplicationName.dll` 运行

## 在 Raspbian Lite 上运行 {#running-with-raspbian-lite}

本教程教你如何通过 [DRM](https://en.wikipedia.org/wiki/Direct\_Rendering\_Manager)，让 Avalonia 应用跑在装有 Raspbian Lite 的树莓派上。

### 第 1 步 —— 配置树莓派 {#step-1-setup-the-raspberry-pi}

第一步是把树莓派配置好。

#### 下载 Raspbian Lite 操作系统镜像。 {#download-the-raspbian-lite-operation-system-image}

你可以从树莓派官网下载 Raspbian Lite 操作系统镜像。\
[树莓派操作系统镜像链接](https://www.raspberrypi.com/software/operating-systems/)

#### 准备刷机 {#prepare-raspberry-for-flashing}

Raspberry Lite 的安装步骤因机型而略有不同。

[**Raspberry Pi 4 b**](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)\
Pi 4 b 需要一张 SD 卡来装操作系统。\
把 SD 卡插进电脑。\
接下来直接进入第 1.2 步即可。

[**Raspberry CM4**](https://www.raspberrypi.com/products/compute-module-4/?variant=raspberry-pi-cm4001000)\
由于 CM4 是为嵌入式应用设计的，你还需要一块 IO 板。官方有 [Compute Module 4 IO 板](https://www.raspberrypi.com/products/compute-module-4-io-board/)，另外也有不少别的选择，比如 [SourceKit PiTray mini](https://sourcekit.cc/#/?id=sourcekit%C2%AE-pitray-mini)。

按这些[步骤](https://www.raspberrypi.com/documentation/computers/compute-module.html#flashing-the-compute-module-emmc)准备好 EMMC 存储以便挂载。

#### 刷写操作系统 {#flashing-the-operating-system}

* [下载](https://etcher.io/)镜像写入工具 Etcher 并安装。
* 打开 Etcher，从硬盘里选中你在第 1.1 步下载的 .zip 文件。
* 选择要写入镜像的大容量存储设备（SD 卡或 CM4 的 EMMC）。
* 确认选项无误后点击 "Flash!" 开始写入数据。刷写完成后，在树莓派的 boot 盘里新建一个名为 **ssh** 的空文件（不带扩展名，例如用 `touch ssh` 创建）。这样树莓派启动后 SSH 守护进程就会开启，你便能通过网络登录了。
* _**仅限 CM4**：在 `/boot/config.txt` 中加入下面这行以启用 USB 2.0 端口_

```conf
dtoverlay=dwc2,dr_mode=host
```

* 启动树莓派并登录。\
  **Raspberry Pi 4 b**：把 SD 卡插进树莓派，接上电源\
  **CM 4**：在 CM4 IO 板上拔掉电源，取下 J2 跳线帽，再重新接上电源

#### 安装缺失的库 {#install-missing-libraries}

在 Raspbian Lite 上经由 DRM 运行 Avalonia 应用，还需要这些库：

```bash
sudo apt update
sudo apt upgrade
sudo reboot
sudo apt-get install libgbm1 libgl1-mesa-dri libegl1-mesa libinput10
```

#### 验证 DRM（可选） {#verify-drm-optional}

你可以用一个简单却好使的小工具 [kmscube](https://gitlab.freedesktop.org/mesa/kmscube) 来测试安装结果。

```bash
sudo apt-get install kmscube
sudo kmscube
```

现在你应该能在树莓派的屏幕上看到那个旋转的立方体了：\
<Image light={RaspbianLiteDrmKmsCubeScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

### 第 2 步 —— 准备 Avalonia 应用 {#step-2-prepare-avalonia-app}

#### 新建一个 Avalonia 应用（Core 或 MVVM 模板） {#create-new-avalonia-app-core-or-mvvm-app}
本教程中我们把它叫作 _AvaloniaRaspbianLiteDrm_。

#### 添加包 [Avalonia.LinuxFrameBuffer](https://www.nuget.org/packages/Avalonia.LinuxFramebuffer) {#add-package-avalonialinuxframebuffer}

```bash
dotnet add package Avalonia.LinuxFramebuffer
```

#### 2.3 Create MainView
经由 FrameBuffer 运行时没有窗口，所以你需要另建一个视图（UserControl）充当顶层控件。这个视图扮演的就是平常窗口的角色。

`MainView` 将作为我们开发界面的基座：

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
             xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
             mc:Ignorable="d"
             d:DesignWidth="800"
             d:DesignHeight="450"
             x:Class="AvaloniaRaspbianLiteDrm.MainView">
    <StackPanel HorizontalAlignment="Center"
                VerticalAlignment="Center"
                Margin="30"
                Spacing="30">
        <TextBlock FontSize="25">
            Welcome to Avalonia! The best XAML framework ever ♥
        </TextBlock>
        <Slider />
    </StackPanel>
</UserControl>
```

现在新建一个名为 `MainSingleView` 的 UserControl，用它承载 `MainView`：

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
             xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
             xmlns:avaloniaRaspbianLiteDrm="clr-namespace:AvaloniaRaspbianLiteDrm"
             mc:Ignorable="d"
             d:DesignWidth="800"
             d:DesignHeight="450"
             x:Class="AvaloniaRaspbianLiteDrm.MainSingleView">
    <avaloniaRaspbianLiteDrm:MainView />
</UserControl>
```

同时修改 `MainWindow.axaml`，让它内部也承载 `MainView`：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        xmlns:avaloniaRaspbianLiteDrm="clr-namespace:AvaloniaRaspbianLiteDrm"
        mc:Ignorable="d"
        d:DesignWidth="800"
        d:DesignHeight="450"
        x:Class="AvaloniaRaspbianLiteDrm.MainWindow"
        Title="AvaloniaRaspbianLiteDrm">
    <avaloniaRaspbianLiteDrm:MainView />
</Window>
```

`MainView` 同时被 `MainSingleView` 和 `MainWindow` 承载。这样开发时既能在桌面上跑应用，也能在树莓派上跑，方便不少。

#### Prepare Program.cs
接着，改造 `Program.cs` 以启用 DRM。\
把 Main 方法改成下面这样：

```csharp
public static int Main(string[] args)
{
    var builder = BuildAvaloniaApp();
    if (args.Contains("--drm"))
    {
        SilenceConsole();
        // By default, Avalonia will try to detect output card automatically.
        // But you can specify one, for example "/dev/dri/card1".
        return builder.StartLinuxDrm(args, card: null, options: new DrmOutputOptions
        {
            Scaling = 1.0,
        });
    }

    return builder.StartWithClassicDesktopLifetime(args);
}

private static void SilenceConsole()
{
    new Thread(() =>
        {
            Console.CursorVisible = false;
            while (true)
                Console.ReadKey(true);
        })
        { IsBackground = true }.Start();
}
```

`SilenceConsole()` 会接管并隐藏控制台输入，否则控制台光标会在屏幕上一闪一闪。

**2.4 Prepare App.axaml.cs**\
接下来，为使用 DRM 设置 `ISingleViewApplicationLifetime` 的 `MainView`。

修改 `App.axaml.cs` 中的 `OnFrameworkInitializationCompleted()`：

```csharp
public override void OnFrameworkInitializationCompleted()
{
    if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        desktop.MainWindow = new MainWindow();
    else if (ApplicationLifetime is ISingleViewApplicationLifetime singleView)
        singleView.MainView = new MainSingleView();

    base.OnFrameworkInitializationCompleted();
}
```

#### 在桌面上运行并测试 {#run-and-test-on-desktop}
现在你可以像平常一样在桌面上运行/调试应用了。\
启动应用后，你应该看到这样的画面：\
<Image light={RaspbianLiteDrmDesktopScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

### 第 3 步 —— 部署到树莓派并运行 {#step-3-deploy-and-run-on-raspberry}

#### 发布应用 {#publish-app}

```bash
dotnet publish -c Release -o publish -r linux-arm -p:PublishReadyToRun=true -p:PublishSingleFile=true -p:PublishTrimmed=true --self-contained true -p:IncludeNativeLibrariesForSelfExtract=true
```

#### 把应用拷到树莓派 {#copy-app-to-raspberry}
把项目 `/publish` 目录下的文件拷到树莓派上。\
你可以用 `scp <source> <destination>`，也可以用 [CyberDuck](https://cyberduck.io) 之类的工具，或者干脆用 U 盘。

#### 在树莓派上运行应用 {#run-app-on-raspberry}
先把权限改成可执行。

```bash
sudo chmod +x /path/to/app/AvaloniaRaspbianLiteDrm
```

然后就能这样运行应用了：

```bash
sudo ./path/to/app/AvaloniaRaspbianLiteDrm --drm
```

现在你应该看到应用在树莓派上跑起来了：

<Image light={RaspbianLiteRaspberryScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

若你装了触摸屏，不妨试着滑一滑那个滑块控件。

## 另请参阅 {#see-also}

- [嵌入式 Linux 概述](/docs/platform-specific-guides/embedded-linux)
- [虚拟键盘](/controls/input/text-input/virtualkeyboard)
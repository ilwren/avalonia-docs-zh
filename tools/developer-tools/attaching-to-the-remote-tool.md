---
id: attaching-to-the-remote-tool
title: 把 DevTools 挂接到远程工具
sidebar_label: 挂接到远程工具
doc-type: how-to
tags:
  - avalonia plus
  - avalonia pro
  - avalonia enterprise
---

`Developer Tools` 可以连到跑在其他机器上的应用。本指南涵盖两种场景：
1. 局域网访问（例如虚拟机或同一 Wi-Fi 下的设备）
2. 通过 VPN 的互联网访问（出于安全考虑推荐这种）

`Developer Tools` 会在 `29414` 端口上跑一个 HTTP 服务器。关键在于确保发起连接的那台机器能访问到这个服务器。

## 局域网访问 {#local-network-access}

1. 取得运行 `Developer Tools` 那台机器的局域网 IP 地址：
- Windows：打开命令提示符并运行 `ipconfig`
- macOS/Linux：打开终端并运行 `ip addr` 或 `ifconfig`
  找出以下列前缀开头的 IPv4 地址：
- `192.168.`（多数家庭网络）

2. Configure your application to use this IP:

```csharp
this.AttachDeveloperTools(o =>
{
    o.Protocol = DeveloperToolsProtocol.CreateHttp(IPAddress.Parse("YOUR_LOCAL_NETWORK_HOST_IP"));
});
```
3. Start `Developer Tools` (via avdt command)
4. In the settings, make sure that `Allow Any IP` is enabled (if not, you would need to restart the app)
5. Launch your application on second machine press <kbd>F12</kbd> to connect.

:::note

Ensure firewalls on both machines allow port 29414

:::

## Internet access via VPN

While it's possible to avoid VPN and set up port forwarding on the public network, it's not recommended. Keeping ports opened is generally considered a bad practice.

Instead, this tutorial will use VPN to setup a limited access between machines, specifically `Tailscale` will be used as one of the simplest options.
Also ensure that `Tailscale CLI` can be used on the machine with developer tools. See [Tailscale CLI](https://tailscale.com/kb/1080/cli) for reference.

1. Please follow the `Tailscale` [Quick Start guide](https://tailscale.com/kb/1017/install) to install it on both machines, and set up access between them. This tutorial specifically focuses on the `MagicDNS` feature.
2. Once `Tailscale` is installed and connected on both devices, it's necessary to serve the `29414` port from the machine with installed `Developer Tools`. Run
   `tailscale serve 29414`
   or
   `/Applications/Tailscale.app/Contents/MacOS/Tailscale serve 29414` on macOS
   CLI will output something similar to:

```bash
Available within your tailnet:

https://machinename.tail.ts.net/
|-- proxy http://127.0.0.1:29414

Press Ctrl+C to exit.
```

Copy the `https://machinename.tail.ts.net/` URL from this output. You need it in the next step.

3. Use URL from the previous step in your `AttachDeveloperTools` options:

```csharp
this.AttachDeveloperTools(o =>
{
    o.Protocol = DeveloperToolsProtocol.CreateHttp(new Uri("https://machinename.tail.ts.net"));
});
```

4. Start `Developer Tools` (via avdt command)
5. Launch your application on second machine press <kbd>F12</kbd> to connect.

![Connected via VPN](/img/tools/dev-tools/remote-connect-via-vpn.png)


## Changing default port

Under some conditions, `29414` default port might not be available.

To change the port, both `Developer Tools` and `AttachDeveloperTools` needs to be adjusted.

On `Developer Tools`, change `HTTP port` parameter on the settings page and restart the app. See [Settings](/tools/developer-tools/settings) for more details.

On `AttachDeveloperTools` side, specify new port in the `DeveloperToolsProtocol.CreateHttp` method as an optional parameter.

## 另请参阅 {#see-also}

- [挂接应用](/tools/developer-tools/attaching-applications)
- [Developer tools settings](/tools/developer-tools/settings)

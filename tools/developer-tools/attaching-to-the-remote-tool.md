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

2. 把你的应用配置成使用这个 IP：

```csharp
this.AttachDeveloperTools(o =>
{
    o.Protocol = DeveloperToolsProtocol.CreateHttp(IPAddress.Parse("YOUR_LOCAL_NETWORK_HOST_IP"));
});
```
3. 启动 `Developer Tools`（通过 avdt 命令）
4. 在设置中确认 `Allow Any IP` 已启用（若没有，你得重启应用）
5. 在第二台机器上启动你的应用，按 <kbd>F12</kbd> 连接。

:::note

确保两台机器的防火墙都放行 29414 端口

:::

## 通过 VPN 的互联网访问 {#internet-access-via-vpn}

虽说不用 VPN、在公网上做端口转发也行得通，但并不推荐——一直开着端口通常都算不上好习惯。

本教程改用 VPN 在两台机器之间建立受限访问，具体选的是最省事的方案之一 `Tailscale`。
另外请确认装了开发者工具的那台机器上能用 `Tailscale CLI`，可参考 [Tailscale CLI](https://tailscale.com/kb/1080/cli)。

1. 请按 `Tailscale` 的[快速上手指南](https://tailscale.com/kb/1017/install)在两台机器上安装它，并打通彼此的访问。本教程着重用到的是 `MagicDNS` 功能。
2. 两台设备都装好 `Tailscale` 并连上之后，需要从装有 `Developer Tools` 的那台机器把 `29414` 端口对外提供出去。请运行
   `tailscale serve 29414`
   或在 macOS 上运行
   `/Applications/Tailscale.app/Contents/MacOS/Tailscale serve 29414`
   CLI 会输出类似这样的内容：

```bash
Available within your tailnet:

https://machinename.tail.ts.net/
|-- proxy http://127.0.0.1:29414

Press Ctrl+C to exit.
```

从输出中复制 `https://machinename.tail.ts.net/` URL，下一步要用。

3. 把上一步得到的 URL 填进你的 `AttachDeveloperTools` 选项：

```csharp
this.AttachDeveloperTools(o =>
{
    o.Protocol = DeveloperToolsProtocol.CreateHttp(new Uri("https://machinename.tail.ts.net"));
});
```

4. 启动 `Developer Tools`（通过 avdt 命令）
5. 在第二台机器上启动你的应用，按 <kbd>F12</kbd> 连接。

![通过 VPN 连接](/img/tools/dev-tools/remote-connect-via-vpn.png)


## 更改默认端口 {#changing-default-port}

某些情况下，`29414` 的默认端口可能被占用。

要改端口，`Developer Tools` 和 `AttachDeveloperTools` 两边都得调整。

在 `Developer Tools` 一侧，到设置页改 `HTTP port` 参数并重启应用。更多细节见[设置](/tools/developer-tools/settings)。

在 `AttachDeveloperTools` 一侧，把新端口作为可选参数传给 `DeveloperToolsProtocol.CreateHttp` 方法。

## 另请参阅 {#see-also}

- [挂接应用](/tools/developer-tools/attaching-applications)
- [开发者工具设置](/tools/developer-tools/settings)

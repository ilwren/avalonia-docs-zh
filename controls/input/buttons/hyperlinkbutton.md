---
id: hyperlinkbutton
title: HyperlinkButton
description: 一个外观像文字超链接的按钮，点击后用平台默认的处理程序打开 URI。
doc-type: reference
---

[`HyperlinkButton`](/api/avalonia/controls/hyperlinkbutton) 是一个外观像文字超链接的按钮，点击它会打开一个 URI。它借助平台默认的机制来启动 URI（打开浏览器、邮件客户端等等）。

## 常用属性 {#useful-properties}

| 属性 | 类型 | 说明 |
|---|---|---|
| `NavigateUri` | `Uri` | 点击按钮时要打开的 URI。 |
| `Content` | `object` | 按钮中显示的内容（通常是文字）。 |
| `IsVisited` | `bool` | 链接是否已访问过。URI 被启动后会自动置为 `true`。 |
| `Command` | `ICommand` | 可选的命令，按钮被点击时执行。 |

## 基本示例 {#basic-example}

```xml
<HyperlinkButton NavigateUri="https://avaloniaui.net"
                 Content="Visit Avalonia" />
```

## 自定义内容 {#custom-content}

和 `Button` 一样，`HyperlinkButton` 也支持任意内容：

```xml
<HyperlinkButton NavigateUri="https://github.com/AvaloniaUI/Avalonia">
    <StackPanel Orientation="Horizontal" Spacing="8">
        <PathIcon Data="{StaticResource github_icon}" />
        <TextBlock Text="View on GitHub" />
    </StackPanel>
</HyperlinkButton>
```

## 绑定 URI {#binding-the-uri}

```xml
<HyperlinkButton NavigateUri="{Binding ProjectUrl}"
                 Content="{Binding ProjectName}" />
```

## 平台行为 {#platform-behavior}

点击 `HyperlinkButton` 时，URI 的启动交由操作系统的默认处理程序负责。究竟打开哪个浏览器或应用，取决于你的平台设置。比如 `https://` 链接会用默认浏览器打开，而 `mailto:` 链接则会用默认邮件客户端打开。

## Pseudoclasses

| 伪类 | 说明 |
|---|---|
| `:visited` | 当 `IsVisited` 为 `true` 时生效。 |
| `:pressed` | 按钮被按下期间生效。 |

## 另请参阅 {#see-also}

- [Button](/controls/input/buttons/button)：标准的按压式按钮。
- [RepeatButton](/controls/input/buttons/repeatbutton)
- [Launcher](/docs/services/launcher)：用代码启动 URI 和文件。

---
id: breakpoints-tool
title: 断点工具
doc-type: reference
---

应用断点工具让你不改代码就能监视和调试 Avalonia 应用中的属性变化与事件。断点可以下在属性和事件上，帮你定位问题、摸清应用的行为。

满足以下条件时，断点即被视为 `Hit`（相应地会让 `Hit Count` 值加一，或挂起执行）：
1. 属性发生变化（属性断点）或事件被触发（事件断点）。
2. 断点处于启用状态。
3. 若断点设了目标，则该目标与属性/事件的来源相符。
4. 命中次数条件得到满足。

断点可能带有 Target，这取决于它是怎么创建的。
举例来说，不带目标的事件断点算是全局断点，_任何_元素触发该事件时它都会命中。

![带选项面板的断点列表](/img/tools/dev-tools/breakpoints-list.png)


## 添加断点 {#adding-breakpoints}

### 添加属性断点 {#adding-a-property-breakpoint}

在[属性](/tools/developer-tools/elements-tool)列表中，每个依赖属性的右键菜单里都有 **Set Breakpoint** 一项。

这样创建的断点会绑定到你下断点的那个元素上。 

![在属性上下断点](/img/tools/dev-tools/breakpoint-set-on-propety.png)

### 添加事件断点 {#adding-an-event-breakpoint}

在[事件](/tools/developer-tools/events-tool)工具中，每个已触发的事件都可以下断点。

选 **On a Source** 会把断点绑定到之前触发该事件的源元素上；选 **Globally** 则创建一个不绑定的断点，任何元素触发该事件时都会命中。 

![在已触发的事件上下断点](/img/tools/dev-tools/breakpoint-set-on-raised-event.png)

你也可以把断点绑定到路由链上的某个特定元素，或者从 “Event Listeners” 浮出菜单里下断点。  

![在链路元素上下断点](/img/tools/dev-tools/breakpoint-set-on-chain-element.png)

## 管理断点 {#managing-breakpoints}

默认情况下，断点命中时只会让 Hit Count 加一。

另外还有几个选项可以启用：

### 挂起执行 {#suspend-execution}

与常规 IDE 中的断点类似：停下执行，并把你带到断点所在位置。

当你需要通过 IDE 里的调用栈看清究竟是什么触发了属性变化或事件时，这个选项特别管用。

被连接的应用必须挂着第三方调试器，否则这类断点会被忽略。

由于 `Developer Tools` 用的是标准的 `Debugger.Break()` 方法，任何带调试器的常规 IDE 都能用：Visual Studio、Rider 或 VSCode。
可惜没有干净的办法覆盖断点的调用栈，因此 IDE 可能会显示来自 `Debugger.Break` 的内部代码。

### 日志消息 {#log-message}

启用后，断点会往[日志](/tools/developer-tools/logs-tool)工具里写一条日志消息。

![断点命中时的日志输出](/img/tools/dev-tools/breakpoints-logs-ouput.png)

### 命中后移除 {#remove-once-hit}

顾名思义，断点一旦命中就会被移除。可与其他选项搭配使用。

## 另请参阅 {#see-also}

- [事件工具](/tools/developer-tools/events-tool)
- [日志工具](/tools/developer-tools/logs-tool)

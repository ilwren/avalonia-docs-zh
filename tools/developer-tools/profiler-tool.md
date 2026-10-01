---
id: profiler-tool
title: 应用性能分析工具
sidebar_label: 性能分析工具
doc-type: reference
---

[指标](/tools/developer-tools/profiler-tool)基本上只有单一维度的信息，适合画成图表；性能分析器采集的数据则丰富得多。一次录制结束后，`Developer Tools` 会把结果汇总并以表格呈现。

## 录制一份性能剖面 {#recording-a-profile}

1. 点击 **Record** 按钮开始一次性能分析会话。
2. 数据在后台采集，应用照常运行，不受影响。
3. 再点一次 **Record** 停止。
4. 结果汇总后分别显示在各个选项卡中，每种分析器一个。

想要结果好看懂，尽量把你要测的那段交互单独拎出来。比如录制时只打开某个特定视图，或只触发某一个界面操作，免得数据被不相干的活动冲淡。

## Style Matching

当控件被创建或加入视觉树时，Avalonia 会评估所有生效的样式选择器，判断哪些适用。样式匹配分析器把这些匹配尝试汇总起来。

各列含义：
- **Selector**：被评估的样式选择器（例如 `TextBlock.h1`、`Button:pointerover > ContentPresenter`）
- **Elapsed**：所有匹配尝试中评估该选择器所花的总时间
- **Fast Reject Count**：该选择器被快速排除、无需完整评估的次数。当控件能靠一次简单的静态检查（比如类型不符或控件名不符）排除时，就算一次快速排除。要紧的是，被快速排除的控件在激活器变化时也不会被重新评估——例如 `TextBox` 永远不会因为 `Button:pointerover` 被重新评估，因为它早在类型这一关就被排除了
- **Match Attempts**：该选择器对控件做匹配测试的总次数
- **Matches**：其中匹配成功的次数

匹配尝试很多、命中却寥寥无几，往往说明选择器范围开得太宽。不妨瞄准具体的控件类型而非基类，以减少控件创建时的无谓匹配。

## Style Activators

样式匹配衡量的是选择器的初次解析，这个分析器则不同，它衡量选择器在运行时被重新评估的频次。当带激活器（如 `:pointerover`、`:focus`、`:pressed`）的条件选择器随用户交互而反复开关时，就会发生重新评估。

各列含义：
- **Selector**：被重新评估的样式选择器
- **Elapsed**：重新评估所花的总时间
- **Evaluations**：该选择器的激活器被重新评估的总次数
- **Active Evaluations**：其中让样式变为生效的次数
- **Activator**：触发重新评估的激活器类型（例如伪类、属性匹配）

若某个选择器的评估次数高得离谱，说明它开关得比预期频繁得多，把这类选择器的范围收窄往往有帮助。

## Resource Lookup

每当控件、样式或绑定按键解析资源（画刷、thickness、模板等）时，Avalonia 都会沿资源层级一路查找，直到命中为止。这个分析器按键汇总这些查找。

各列含义：
- **Key**：被查找的资源键
- **Elapsed**：所有查找中解析该键所花的总时间
- **Total Lookups**：该键被请求的次数
- **Successful**：其中找到了匹配资源的次数
- **Theme Variant**：查找发生时生效的主题变体（Light/Dark）

某个键查找次数很多、成功次数却很少，多半意味着资源定义缺失或键名拼错了。你可以用[资源工具](/tools/developer-tools/resources-tool)查看各作用域下有哪些可用资源。
## 另请参阅 {#see-also}

- [指标工具](/tools/developer-tools/metrics-tool)
- [资源工具](/tools/developer-tools/resources-tool)

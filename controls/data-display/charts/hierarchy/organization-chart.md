---
id: organization-chart
title: 组织结构图
description: 以层级版面呈现组织结构和汇报关系，展示岗位、职责和层级。
doc-type: reference
tags:
  - avalonia pro
---

import chartsHierarchicalOrganization from '/img/controls/charts/charts-hierarchical-organization.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

组织结构图呈现一个组织的架构，把汇报关系、相对层级以及岗位职责交代清楚。

<Image light={chartsHierarchicalOrganization} maxWidth={400} position="center" cornerRadius="true" alt="Organization chart with a top-level CEO node branching down to department heads showing reporting relationships." />

## 适用场景 {#when-to-use}
- **公司通讯录**：呈现企业的汇报结构。
- **项目层级**：理清产品负责人、开发人员和干系人。
- **家谱**：展示亲缘关系与世系传承。

## 代码示例 {#code-example}

### XAML
```xml
<OrganizationChart xmlns="https://github.com/avaloniaui" Name="OrganizationChartSample" Title="Company Structure" Height="350"
                                               ItemsSource="{Binding OrgChartData}" LabelPath="Name" ChildrenPath="Reports" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public class OrgNode
{
    public string Name { get; set; } = string.Empty;
    public string Position { get; set; } = string.Empty;
    public ObservableCollection<OrgNode> Reports { get; set; } = new();
}

public ObservableCollection<OrgNode> OrgChartData { get; } = new()
{
    new OrgNode { Name = "CEO", Reports = {
        new OrgNode { Name = "CTO", Reports = {
            new OrgNode { Name = "Dev Lead" }
        }},
        new OrgNode { Name = "CFO", Reports = {
            new OrgNode { Name = "Accounting" }
        }}
    }}
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 层级数据源（根节点）。 | `null` |
| `LabelPath` | 节点标签所对应的属性名。 | `null` |
| `ChildrenPath` | 指向子节点集合的路径。 | `null` |
| `Orientation` | `Horizontal` 或 `Vertical` 布局。 | `Vertical` |
| `NodeWidth` | 每个节点方框的宽度。 | `120.0` |
| `NodeHeight` | 每个节点方框的高度。 | `50.0` |
| `NodeGap` | 层级之间以及同级节点之间的间隙。 | `30.0` |

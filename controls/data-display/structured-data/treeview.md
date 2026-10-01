---
id: treeview
title: TreeView
---

import TreeViewAnimalHierarchyScreenshot from '/img/controls/treeview/treeview-animal-hierarchy.gif';
import TreeViewEnhancedAnimalHierarchyScreenshot from '/img/controls/treeview/treeview-enhanced-animal-hierarchy.gif';

`TreeView` 控件可以呈现层级数据，并支持选中条目。条目都套用模板，因此外观可由你定制。

这里有两处数据源：一处是控件的主条目源，给出层级数据的根；另一处是条目模板中的条目源，它让控件能列出层级数据的下一层。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

<table>
  <thead>
    <tr>
      <th width="316">Property</th>
      <th>说明</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>ItemsSource</code></td>
      <td>用作该控件数据源的绑定集合。</td>
    </tr>
    <tr>
      <td><code>ItemsControl.ItemTemplate</code></td>
      <td>条目模板中包含一个 DataTemplate，它会套用到每个条目上，用来改变条目的外观。</td>
    </tr>
    <tr>
      <td><code>ItemsControl.ItemsPanel</code></td>
      <td>承载各项的容器面板，默认是 `StackPanel`。自定义 `ItemsPanel` 的方法见[自定义面板](/docs/how-to/itemscontrol-how-to#custom-panel)。</td>
    </tr>
    <tr>
      <td><code>ItemsControl.Styles</code></td>
      <td>应用到 ItemControl 任意子元素上的样式。</td>
    </tr>
  </tbody>
</table>

## Example

下面这个例子采用 MVVM 写法，在视图模型中用一个 C# 节点类保存层级数据。例子里，视图模型的 `Nodes` 集合中只有一个根节点：

```xml
<TreeView ItemsSource="{Binding Nodes}">
  <TreeView.ItemTemplate>
    <TreeDataTemplate ItemsSource="{Binding SubNodes}">
      <TextBlock Text="{Binding Title}"/>
    </TreeDataTemplate>
  </TreeView.ItemTemplate>
</TreeView>
```

```csharp title='C# View Model'
using AvaloniaControls.Models;
using System.Collections.ObjectModel;

namespace AvaloniaControls.ViewModels
{
    public class MainWindowViewModel : ViewModelBase
    {
        public ObservableCollection<Node> Nodes{ get; }

        public MainWindowViewModel()
        {
            Nodes = new ObservableCollection<Node>
            {                
                new Node("Animals", new ObservableCollection<Node>
                {
                    new Node("Mammals", new ObservableCollection<Node>
                    {
                        new Node("Lion"), new Node("Cat"), new Node("Zebra")
                    })
                })
            };
        }
    }
}
```

```csharp title='C# Node Class'
using System.Collections.ObjectModel;

namespace AvaloniaControls.Models
{
    public class Node
    {
        public ObservableCollection<Node>? SubNodes { get; }
        public string Title { get; }
  
        public Node(string title)
        {
            Title = title;
        }

        public Node(string title, ObservableCollection<Node> subNodes)
        {
            Title = title;
            SubNodes = subNodes;
        }
    }
}
```

默认会显示根节点（可以有多个）。用户点击节点旁的箭头即可展开或收起，点击节点标题则选中该项。在触摸和手写笔设备上，选择发生在指针抬起时而非按下时，这样用户就能从某个节点上开始滚动，而不会误改选择。

<Image light={TreeViewAnimalHierarchyScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

下面这个例子在前一个的基础上作了发挥：改用多个根节点、调整了条目模板，并在视图模型代码中预先选中了一项：

```xml
<TreeView Margin="10"
          ItemsSource="{Binding Nodes}" 
          SelectedItems="{Binding SelectedNodes}"
          SelectionMode="Multiple">
  <TreeView.ItemTemplate>
    <TreeDataTemplate ItemsSource="{Binding SubNodes}">
      <Border HorizontalAlignment="Left"
              BorderBrush="Gray" BorderThickness="1"
              CornerRadius="5" Padding="15 3">
        <TextBlock Text="{Binding Title}" />
      </Border>
    </TreeDataTemplate>
  </TreeView.ItemTemplate>
</TreeView>
```

```csharp title='C# View Model'
using AvaloniaControls.Models;
using System.Collections.ObjectModel;
using System.Linq;

namespace AvaloniaControls.ViewModels
{
    public class MainWindowViewModel : ViewModelBase
    {
        public ObservableCollection<Node> Nodes { get; }
        public ObservableCollection<Node> SelectedNodes { get; }

        public MainWindowViewModel()
        {
            SelectedNodes = new ObservableCollection<Node>();
            Nodes = new ObservableCollection<Node>
            {                
                new Node("Animals", new ObservableCollection<Node>
                {
                    new Node("Mammals", new ObservableCollection<Node>
                    {
                        new Node("Lion"), new Node("Cat"), new Node("Zebra")
                    })
                }),
                new Node("Birds", new ObservableCollection<Node>
                {
                    new Node("Robin"), new Node("Condor"), 
                    new Node("Parrot"), new Node("Eagle")
                }),
                new Node("Insects", new ObservableCollection<Node>
                {
                    new Node("Locust"), new Node("House Fly"), 
                    new Node("Butterfly"), new Node("Moth")
                }),
            };

            var moth = Nodes.Last().SubNodes?.Last();
            if (moth!=null) SelectedNodes.Add(moth);    
        }
    }
}
```

```csharp title='C# Node Class'
using System.Collections.ObjectModel;

namespace AvaloniaControls.Models
{
    public class Node
    {
        public ObservableCollection<Node>? SubNodes { get; }
        public string Title { get; }
  
        public Node(string title)
        {
            Title = title;
        }

        public Node(string title, ObservableCollection<Node> subNodes)
        {
            Title = title;
            SubNodes = subNodes;
        }
    }
}
```

树视图会在需要时加上滚动条。按住 Ctrl 键可以扩展选择范围。

<Image light={TreeViewEnhancedAnimalHierarchyScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

## 展开相关事件 {#expansion-events}

条目展开或折叠时，`TreeViewItem` 会触发 `Expanded` 和 `Collapsed` 两个路由事件。它们会向上冒泡，因此你可以在 `TreeView` 这一层统一处理：

```csharp
treeView.AddHandler(TreeViewItem.ExpandedEvent, (sender, args) =>
{
    var item = (TreeViewItem)args.Source!;
    // React to expansion, e.g., load child data on demand
});

treeView.AddHandler(TreeViewItem.CollapsedEvent, (sender, args) =>
{
    var item = (TreeViewItem)args.Source!;
    // React to collapse
});
```

## 另请参阅 {#see-also}

- [TreeView API 参考](/api/avalonia/controls/treeview)
- [GitHub 上的 `TreeView.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/TreeView.cs)

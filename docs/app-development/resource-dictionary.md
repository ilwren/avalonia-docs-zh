---
id: resource-dictionary
title: 创建资源字典
description: 创建、引入并合并资源字典文件，把可复用的 XAML 资源组织起来。
doc-type: how-to
---

import AddNewItemDialog from '/img/gitbook-import/assets/image (8) (1) (2).png';
import ResourceDictionaryInSolution from '/img/gitbook-import/assets/image (1) (4).png';
import MergedResourceDictionaryStructure from '/img/gitbook-import/assets/image (1) (3).png';

在应用中，你常常需要把画刷、颜色等图形基础元素标准化（当然不止这些）。这些资源既可以定义在 Avalonia 应用的各个层级上，也可以写进单独的文件、按需引入。

资源总是定义在资源字典内部，因此每个资源都带有一个 key 特性。

资源字典所处的层级决定了其中资源的作用范围：资源在其定义所在的文件及更下层可用。所以，把资源字典放在哪里，就决定了这些资源能管多宽。

## 声明资源 {#declaring-resources}

举例来说，你可能希望画刷颜色在整个应用中保持统一。这时就在应用的 XAML 文件 **App.axaml** 里声明一个资源字典，像这样：

```xml title="App.axaml"
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="MyApp.App">
    // highlight-start
  <Application.Resources>
    <SolidColorBrush x:Key="Warning">Yellow</SolidColorBrush>
  </Application.Resources>
    // highlight-end
</Application>
```

或者，你希望某组资源只作用于某个窗口或用户控件，那就把资源字典定义在该窗口或用户控件的文件中。例如：

```xml title="MyUserControl.axaml"
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="MyApp.MyUserControl">
    // highlight-start
  <UserControl.Resources>
    <SolidColorBrush x:Key="Warning">LightYellow</SolidColorBrush>
  </UserControl.Resources>
    // highlight-end
</UserControl>
```

需要的话，甚至可以把资源定义在控件级别：

```xml title="MainWindow.axaml"
<Window xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="MyApp.MainWindow">
  <StackPanel>
    // highlight-start
    <StackPanel.Resources>
      <SolidColorBrush x:Key="Warning">PaleGoldenRod</SolidColorBrush>
    </StackPanel.Resources>
    // highlight-end
  </StackPanel>
</Window>
```

你也可以声明只属于某个样式的资源。 

```xml title="MyStyle.axaml"
<Style Selector="TextBlock.warning">
  <Style.Resources>
    <SolidColorBrush x:Key="Warning">Yellow</SolidColorBrush>
  </Style.Resources>
  <Setter ... />
</Style>
```

:::note
请注意，这个资源在该样式块之外是看不见的——也就是说，样式块外那些带 "warning" 类的 TextBlock 并不会认得它。
:::

还可以为特定的主题变体（Dark、Light 或自定义）定义资源。在下面的例子中，`BackgroundBrush` 和 `ForegroundBrush` 会随系统或应用当前设定的主题变体取不同的值。关于主题变体的更多内容，请阅读[主题变体](/docs/styling/theme-variants)页面。

```xml
<ResourceDictionary>
  <ResourceDictionary.ThemeDictionaries>
    <ResourceDictionary x:Key='Light'>
      <SolidColorBrush x:Key='BackgroundBrush'>White</SolidColorBrush>
      <SolidColorBrush x:Key='ForegroundBrush'>Black</SolidColorBrush>
    </ResourceDictionary>
    <ResourceDictionary x:Key='Dark'>
      <SolidColorBrush x:Key='BackgroundBrush'>Black</SolidColorBrush>
      <SolidColorBrush x:Key='ForegroundBrush'>White</SolidColorBrush>
    </ResourceDictionary>
  </ResourceDictionary.ThemeDictionaries>
</ResourceDictionary>
```

## 资源字典文件 {#resource-dictionary-files}

把资源字典写进各自独立的文件，能让 Avalonia 项目的结构更清晰，资源定义也更容易查找和维护。

放在资源字典文件中的资源，整个应用都能访问。

添加资源字典文件的步骤如下：

-  在你想创建新文件的位置右键点击项目。
-  点击 **添加**，再点 **新建项**。
-  在左侧列表中点击 **Avalonia**：

<Image light={AddNewItemDialog} alt="Add New Item dialog showing Avalonia resource dictionary templates" position="center" maxWidth={400} cornerRadius="true" />

-  Click **Resource Dictionary (Avalonia)**.
-  输入你想用的文件名。
-  Click **Add**.

:::note
资源文件创建好之后，还得把它正确地引入应用，参见[引入与合并资源](#include-and-merge-resources)一节。
:::

现在你可以在标出的位置添加要定义的资源了，大致长这样：

```xml
<ResourceDictionary xmlns="https://github.com/avaloniaui"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <!-- Add Resources Here -->
</ResourceDictionary>
```

## 使用资源 {#using-resources}

用 `{DynamicResource}` 标记扩展即可使用作用范围内某个资源字典中的资源。

比如，要直接把资源用在 border 元素的 background 特性上，XAML 这样写：

```xml
<Border Background="{DynamicResource Warning}">
  Look out!
</Border>
```

### 静态资源 {#static-resource}

你也可以改用 `StaticResource` 标记扩展。例如：

```xml
<Border Background="{StaticResource Warning}">
  Look out!
</Border>
```

静态资源的不同之处在于，它不会响应运行时在代码中对资源所做的修改——一旦加载完成，静态资源就改不了了。

用静态资源的好处是它要干的活更少，加载略快一点，内存占用也略小一些。

## 资源的优先级 {#resource-priority}

Avalonia 从 `DynamicResource` 或 `StaticResource` 标记所在的层级出发，沿**逻辑控件树**向上查找资源键，据此决定该用哪个资源。

这意味着同名键的资源，谁离待解析的标记更近谁优先。换句话说，逻辑控件树上层的资源定义，实际上会被更靠近的定义「覆盖」。比如看这段 XAML：

```xml
<UserControl ... >
  <UserControl.Resources>
    <SolidColorBrush x:Key="Warning">Yellow</SolidColorBrush>
  </UserControl.Resources>

  <StackPanel>
    <StackPanel.Resources>
      <SolidColorBrush x:Key="Warning">Orange</SolidColorBrush>
    </StackPanel.Resources>

    <Border Background="{DynamicResource Warning}">
      Look out!
    </Border>
  </StackPanel>
</UserControl>
```

这里 border 控件用的是键为 'Warning' 的资源，而它被定义了两次——一次在外层 stack panel 上，一次在用户控件级别。Avalonia 会判定边框背景为橙色，因为从 border 自身沿逻辑控件树向上找时，先碰到的是它的父级 stack panel。

## 引入与合并资源 {#include-and-merge-resources}

资源可以从资源字典文件中引入，并与另一个文件里定义的资源合并（哪怕那个文件一个资源都没有）。

<Image light={ResourceDictionaryInSolution} alt="Solution Explorer showing resource dictionary file included in a project" position="center" maxWidth={400} cornerRadius="true" />

如果你想在整个应用层面合并资源字典，就在应用 XAML 文件 **App.axaml** 的 **Application.Resources** 小节中声明一个资源字典，像这样：

```xml
<Application.Resources>
  <ResourceDictionary>
    <ResourceDictionary.MergedDictionaries>
      <MergeResourceInclude Source="/Assets/AppResources.axaml" />
    </ResourceDictionary.MergedDictionaries>
  </ResourceDictionary>
</Application.Resources>
```

你也可以合并资源字典，把合并来的资源声明为只属于某个样式。

<Image light={MergedResourceDictionaryStructure} alt="Merged resource dictionary structure in a styles file" position="center" maxWidth={400} cornerRadius="true" />

这样一来，样式可以写在一个文件里，而用到的资源定义在另一个文件里。既保证了样式的一致性，也让解决方案条理分明、易于维护。

要在样式文件中引入某个文件里的资源字典，添加如下 XAML：

```xml
<Styles.Resources>
  <ResourceDictionary>
    <ResourceDictionary.MergedDictionaries>
      <ResourceInclude Source="/Assets/AppResources.axaml"/>
    </ResourceDictionary.MergedDictionaries>
  </ResourceDictionary>
</Styles.Resources>
```

上面的例子中，资源文件 `AppResources.axaml` 位于项目的 `/Assets` 文件夹内。接着你就可以用这些资源来定义样式了，例如：

```xml
<Style Selector="Button.btn-info">
  <Setter Property="Background" Value="{StaticResource InfoColor}"/>
</Style>
```

其中资源 `InfoColor` 在被引入的那个文件里定义为 `SolidColorBrush`。

:::info
注意这里用 `StaticResource` 来引用资源，因为它不该变化——这里的诉求正是保持样式一致。
:::

## 合并资源的优先级 {#merged-resources-priority}

正如前面所说，资源的解析是从标记所在处沿逻辑控件树向上查找，直到找到带所需键的资源为止。

不过，应用各层级上还存在样式和合并字典，于是又多出下面这些优先级规则：

* 控件资源 -> 合并字典
* 样式资源 -> 合并字典
* 应用资源 -> 合并字典

比如在下面这个假想的应用里，为底部 border 控件所用资源展开的查找，会按方括号 `[]` 中标出的顺序进行：

```text
Application
 |- Resources [11]
     |- Merged dictionary [12]
     |- Merged dictionary [13]
 |- Styles
     |- Resources [14]
         |- Merged dictionary [15]
         |- Merged dictionary [16]

Window
 |- Resources [6]
     |- Merged dictionary [7]
 |- Styles
     |- Resources [8]
         |- Merged dictionary [9]
         |- Merged dictionary [10]
 |- StackPanel
     |- Resources [1]
         |- Merged dictionary [2]
         |- Merged dictionary [3]
     |- Styles
         |- Resources [4]
             |- Merged dictionary [5]
     |- Border
```

从 border 出发，最先查的是父级（stack panel）控件上定义的资源。之后再看同一层级上的合并字典——按它们在 XAML 中出现的先后顺序。

接下来查找父级（stack panel）控件中定义的样式，然后是该层级上的合并字典。

查找就这样沿逻辑控件树一路向上，每一层的处理方式都类似，最后到达应用级的资源和样式。

## 在代码中使用资源 {#consuming-resources-from-code}

Avalonia 提供了几种在代码中访问资源的方式。 

:::note

下面示例中的 `ResourceNode` 可以是任何支持 `Resource` 的节点，比如 `Application.Current`、`Window`、`UserControl` 等。 

:::

- **ResourceNode.Resources["TheKey"]**：<br/>
  这会直接访问底层的 `Dictionary`。注意：它不会去扫描合并字典和各级父节点。 
- **ResourceNode.TryGetResource**: <br/>
  该函数会尝试获取指定资源，成功则返回 `true`，否则返回 `false`。它会扫描合并字典，但不会沿逻辑树往上找。 
- **ResourceNode.TryFindResource**:  <br/>
  这个扩展方法会尝试获取指定资源，成功则返回 `true`，否则返回 `false`。它既扫描合并字典，也会沿逻辑树查找。
- **ResourceNode.GetResourceObservable**: <br/>
  它返回一个 [`IObservable`](https://learn.microsoft.com/en-us/dotnet/api/System.IObservable-1)，可用来观察资源的变化，比如绑定到它上面。

```csharp
// In this sample we have defined the resource in App.axaml and we want to look up the value in the MainWindow constructor.
//
//    <Application.Resources>
//         <x:String x:Key="TheKey">HelloWorld</x:String>
//    </Application.Resources>

public MainWindow()
{
    InitializeComponent();

    // found1 = false | result1 = null
    var found1 = this.TryGetResource("TheKey", this.ActualThemeVariant, out var result1);

    // found2 = true | result2 = "Hello World" 
    var found2 = this.TryFindResource("TheKey", this.ActualThemeVariant, out var result2);

    // Bind the resource to a TextBlock from code behind
    myTextBlock.Bind(TextBlock.TextProperty, Resources.GetResourceObservable("TheKey"));

    // This will update myTextBlock.Text via the bound observable
    this.Resources["TheKey"] = "Hello from code behind";
}
```

## 另请参阅 {#see-also}

- [资源概述](/docs/app-development/resources)：了解资源的种类与查找行为。
- [主题变体](/docs/styling/theme-variants)：使用随主题变化的资源。

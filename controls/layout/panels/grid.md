---
id: grid
title: Grid
description: 了解如何用 Avalonia 的 Grid 面板把子控件按行列排布。
doc-type: reference
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import GridSharedSizeGroupScreenshot from '/img/controls/grid/grid-sharedsizegroup.png';
import GridSampleScreenshot from '/img/controls/grid/grid_example.png';

[`Grid`](/api/avalonia/controls/grid) 控件适合把子控件按列和行排布。你可以为 `Grid` 定义绝对、按比例和自适应三种行列尺寸。

`Grid` 中的每个子控件都可以用列、行坐标定位到某个 `Grid` 单元格。坐标从 0 开始，两者默认都是 0。

如果把多个子控件放进同一个单元格，它们会按在 XAML 中出现的顺序依次绘制在该单元格里。除了 `Panel`，这也是实现层叠的一种办法。

:::caution
若不给 `Grid` 的子控件指定列、行坐标，它们都会被画在左上角（column=0，row=0）。
:::

子控件也可以跨越多行、多列，或行列同时跨越。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性               | 说明                                                         |
|------------------------|---------------------------------------------------------------------|
| ColumnDefinitions      | 描述 `Grid` 各列宽度的尺寸定义。    |
| RowDefinitions         | 描述 `Grid` 各行高度的尺寸定义。      |
| ShowGridLines          | 显示单元格之间的网格线（虚线）。                |
| Grid.Column            | 把控件布局到指定的列（从 0 开始计数）。          |
| Grid.Row               | 把控件布局到指定的行（从 0 开始计数）。             |
| Grid.ColumnSpan        | 让控件横跨 1 列或多列。                         |
| Grid.RowSpan           | 让控件纵跨 1 行或多行。                            |
| Grid.IsSharedSizeScope | 把该控件定义为 `SharedSizeGroup` 的作用域容器 |

## 尺寸定义 {#size-definitions}

行和列的尺寸可以定义为：

* 绝对尺寸——以设备无关像素计（整数） 
* 按比例——按 `Grid` 剩余空间的比例分配
* 自动——按所含子控件的大小自适应

尺寸定义既可以写成一串简写代码，也可以用 XAML 元素完整展开。

完整写法还支持额外的约束，比如 `SharedSizeGroup`，以及用绝对尺寸指定最小和最大长度。

### 绝对尺寸定义 {#absolute-size-definitions}

在列表写法中，绝对尺寸定义写成整数。例如：

`ColumnDefinitions="200, 200, 300"`

用完整展开的 XAML 来写，等价于：

```xml
<Grid>
   <Grid.ColumnDefinitions>
       <ColumnDefinition Width="200"></ColumnDefinition>
       <ColumnDefinition Width="200"></ColumnDefinition>
       <ColumnDefinition Width="300"></ColumnDefinition>
   </Grid.ColumnDefinitions>
</Grid>
```

### 按比例的尺寸定义 {#proportional-size-definitions}

按比例的尺寸定义用星号表示占可用 `Grid` 空间的份额。比如要造两个等宽的列，再加一个两倍宽的列：

`ColumnDefinitions="*, *, 2*"`

用完整展开的 XAML 来写，等价于：

```xml
<Grid>
   <Grid.ColumnDefinitions>
       <ColumnDefinition Width="*"></ColumnDefinition>
       <ColumnDefinition Width="*"></ColumnDefinition>
       <ColumnDefinition Width="2*"></ColumnDefinition>
   </Grid.ColumnDefinitions>
</Grid>
```

:::tip
尺寸定义不支持百分比。有个小技巧可以绕过：让所有比例值加起来等于 100，比如 `<Grid ColumnDefinitions="25*, 25*, 50*">` 就表示 3 列分别占剩余可用宽度的 25%、25% 和 50%。
:::

### 自动尺寸定义 {#automatic-size-definitions}

要让某行或某列按其中最大的子控件自动确定尺寸，请使用代码 'Auto'。例如：

`RowDefinitions="Auto, Auto, Auto"`

用完整展开的 XAML 来写，等价于：

```xml
<Grid>
   <Grid.RowDefinitions>
       <RowDefinition Height="Auto"></RowDefinition>
       <RowDefinition Height="Auto"></RowDefinition>
       <RowDefinition Height="Auto"></RowDefinition>
   </Grid.RowDefinitions>
</Grid>
```

:::caution
如果子控件自己显式设置了尺寸，绘制时会以它为准。也就是说，一旦它比所在的网格单元格还大，就会盖到相邻单元格上。
:::

### 混合使用多种尺寸定义 {#mixing-size-definitions}

同一串尺寸定义中，上述几种写法可以随意混用。例如：

`ColumnDefinitions="200, *, 2*"`

用完整展开的 XAML 来写，等价于：

```xml
<Grid>
   <Grid.ColumnDefinitions>
       <ColumnDefinition Width="200"></ColumnDefinition>
       <ColumnDefinition Width="*"></ColumnDefinition>
       <ColumnDefinition Width="2*"></ColumnDefinition>
   </Grid.ColumnDefinitions>
</Grid>
```

## 绘制规则 {#drawing-rules}

计算尺寸时，先算出绝对值和自动值，按比例的列再去瓜分剩下的空间。

自动尺寸的计算以子控件外边距布局区的外沿为准。

:::info
想回顾控件布局区域这个概念，请参阅[布局区域](/docs/layout/#layout-zones)。 
:::

子控件按在 XAML 中出现的顺序，依次画在各自分配到的网格单元格里。这条规则既决定了两个子控件被分到同一单元格时会怎样，也决定了子控件大于所分配单元格时的重叠关系。

当子控件自带尺寸、且小于所分配的单元格时，它会按自身的水平和垂直对齐属性在单元格内对齐绘制（两者默认都是居中）。

## Example

这个例子展示了：

* 列、行定义的简写语法怎么用。
* 绝对列宽与按比例列宽如何混用。
* 如何为子控件指定单元格。
* 如何跨行、跨列。

下面是一个 `Grid` 的例子：3 个等高的行，3 列中第 1 列固定宽度、另外 2 列按比例瓜分剩余空间：

这里先扣掉第 0 列 100 的绝对宽度，剩余宽度中第 1 列占 1.5 份、第 2 列占 4 份。

按钮绘制时填满从单元格（第 1 列、第 1 行）起、向右再跨一列、向下再跨一行的范围。效果如下：

<XamlPreview>

```xml
<Grid xmlns="https://github.com/avaloniaui"
      HorizontalAlignment="Center"
      VerticalAlignment="Center"
      RowSpacing="10"
      ColumnDefinitions="100,1.5*,4*" RowDefinitions="Auto,Auto,Auto"  Margin="4">
  <TextBlock Grid.Row="0" Grid.Column="0"
             Text="Col0Row0:" />
  <TextBlock Grid.Row="1" Grid.Column="0"
             Text="Col0Row1:" />
  <TextBlock Grid.Row="2" Grid.Column="0"
             Text="Col0Row2:" />
  <TextBlock Grid.Row="0" Grid.Column="2"
             Text="Col2Row0" />
  <Button Grid.Row="1" Grid.Column="1"
          Grid.RowSpan="2" Grid.ColumnSpan="2"
          HorizontalAlignment="Stretch"
          Content="SpansCol1-2Row1-2" />
</Grid>
```

</XamlPreview>

## SharedSizeGroup

`SharedSizeGroup` 让多个 `Grid` 控件之间可以共享自动尺寸的行、列定义信息。

下面的例子演示如何用 `SharedSizeGroup` 让 `ListBox` 内外的列保持一致的尺寸。

<Tabs>
<TabItem value="xml" label="XML" default>

```xml
<StackPanel Grid.IsSharedSizeScope="True">
  <StackPanel.Styles>
    <Style Selector="ListBoxItem">
      <Setter Property="Padding" Value="0" />
    </Style>
  </StackPanel.Styles>

  <ListBox ItemsSource="{Binding People}">
    <ListBox.ItemTemplate>
      <DataTemplate>
        <Grid Name="myGrid" RowDefinitions="auto, auto" ShowGridLines="True">
          <Grid.ColumnDefinitions>
            <ColumnDefinition SharedSizeGroup="A" />
            <ColumnDefinition SharedSizeGroup="B" />
            <ColumnDefinition Width="*" />
            <ColumnDefinition SharedSizeGroup="C" />
          </Grid.ColumnDefinitions>

          <TextBlock Grid.Column="0" Margin="6,0" Text="{Binding FirstName}" />
          <TextBlock Grid.Column="1" Margin="6,0" Text="{Binding LastName}" />
          <TextBlock Grid.Column="2" Margin="6,0" Text="{Binding Age}" />
          <TextBlock Grid.Column="3" Margin="6,0" Text="{Binding Occupation}" />
        </Grid>
      </DataTemplate>
    </ListBox.ItemTemplate>
  </ListBox>
    
  <!-- Controls may appear in-between Grids with SharedSizeGroups -->
  <Separator />

  <Grid>
    <Grid.ColumnDefinitions>
      <ColumnDefinition SharedSizeGroup="A" />
      <ColumnDefinition SharedSizeGroup="B" />
      <ColumnDefinition Width="*" />
      <ColumnDefinition SharedSizeGroup="C" />
    </Grid.ColumnDefinitions>

    <Button Content="This is the First Name" HorizontalAlignment="Stretch" Grid.Column="0" />
    <Button Content="Last" HorizontalAlignment="Stretch" Grid.Column="1" />
    <Button Content="Age" HorizontalAlignment="Stretch" Grid.Column="2" />
    <Button Content="Occupation" HorizontalAlignment="Stretch" Grid.Column="3" />
  </Grid>

</StackPanel>
```

</TabItem>
<TabItem value="example" label="C#">

```csharp
public record Person(string FirstName, string LastName, int Age, string Occupation);

public partial class MainWindowViewModel : ViewModelBase
{
    public ObservableCollection<Person> People { get; } = new()
    {
        new("Jim", "Smith", 35, "Printed Circuit Board Drafter"),
        new("Charlotte", "O'Shaughnessy-Alejandro", 30, "Librarian"),
        new("Ryan", "Cullen", 40, "Ceramics Instructor"),
        new("Valentina", "Levine", 38, "Oceanologist")
    };
}
```

</TabItem>
</Tabs>

<Image light={GridSharedSizeGroupScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

注意各列的尺寸是怎么来的：第一列由 `Button` 决定，第二和第四列由 `ListBox` 的内容决定，第三列则占去剩余空间。

## 在代码中定义 grid {#defining-a-grid-in-code}

下面的例子演示如何搭出一个与 Windows 开始菜单中「运行」对话框相似的界面。

<Image light={GridSampleScreenshot} alt="Grid example app" position="center" maxWidth={400} cornerRadius="true" />

<Tabs
  defaultValue="xaml"
  values={[
      { label: 'XAML', value: 'xaml', },
      { label: 'C#', value: 'cs', },
  ]}
>
<TabItem value="xaml">

```xml
<Grid Background="Gainsboro" 
      HorizontalAlignment="Left" 
      VerticalAlignment="Top" 
      Width="425" 
      Height="165"
      ColumnDefinitions="Auto,*,*,*,*"
      RowDefinitions="Auto,Auto,*,Auto">
    
    <Image Grid.Row="0" Grid.Column="0" Source="{Binding runicon}" />
    
    <TextBlock Grid.Row="0" Grid.Column="1" Grid.ColumnSpan="4" 
               Text="Type the name of a program, folder, document, or Internet resource, and Windows will open it for you." 
               TextWrapping="Wrap" />
               
    <TextBlock Grid.Row="1" Grid.Column="0" Text="Open:" />
    
    <TextBox Grid.Row="1" Grid.Column="1" Grid.ColumnSpan="5" />
    
    <Button Grid.Row="3" Grid.Column="2" Content="OK" Margin="10,0,10,15" />
    
    <Button Grid.Row="3" Grid.Column="3" Content="Cancel" Margin="10,0,10,15" />
    
    <Button Grid.Row="3" Grid.Column="4" Content="Browse ..." Margin="10,0,10,15" />
</Grid>

```

</TabItem>
<TabItem value="cs">

```cs
// Create the Grid.
grid1 = new Grid ();
grid1.Background = Brushes.Gainsboro;
grid1.HorizontalAlignment = HorizontalAlignment.Left;
grid1.VerticalAlignment = VerticalAlignment.Top;
grid1.ShowGridLines = true;
grid1.Width = 425;
grid1.Height = 165;

// Define the Columns.
colDef1 = new ColumnDefinition();
colDef1.Width = new GridLength(1, GridUnitType.Auto);
colDef2 = new ColumnDefinition();
colDef2.Width = new GridLength(1, GridUnitType.Star);
colDef3 = new ColumnDefinition();
colDef3.Width = new GridLength(1, GridUnitType.Star);
colDef4 = new ColumnDefinition();
colDef4.Width = new GridLength(1, GridUnitType.Star);
colDef5 = new ColumnDefinition();
colDef5.Width = new GridLength(1, GridUnitType.Star);
grid1.ColumnDefinitions.Add(colDef1);
grid1.ColumnDefinitions.Add(colDef2);
grid1.ColumnDefinitions.Add(colDef3);
grid1.ColumnDefinitions.Add(colDef4);
grid1.ColumnDefinitions.Add(colDef5);

// Define the Rows.
rowDef1 = new RowDefinition();
rowDef1.Height = new GridLength(1, GridUnitType.Auto);
rowDef2 = new RowDefinition();
rowDef2.Height = new GridLength(1, GridUnitType.Auto);
rowDef3 = new RowDefinition();
rowDef3.Height = new GridLength(1, GridUnitType.Star);
rowDef4 = new RowDefinition();
rowDef4.Height = new GridLength(1, GridUnitType.Auto);
grid1.RowDefinitions.Add(rowDef1);
grid1.RowDefinitions.Add(rowDef2);
grid1.RowDefinitions.Add(rowDef3);
grid1.RowDefinitions.Add(rowDef4);

// Add the Image.
img1 = new Image();
img1.Source = runicon;
Grid.SetRow(img1, 0);
Grid.SetColumn(img1, 0);

// Add the main application dialog.
txt1 = new TextBlock();
txt1.Text = "Type the name of a program, folder, document, or Internet resource, and Windows will open it for you.";
txt1.TextWrapping = TextWrapping.Wrap;
Grid.SetColumnSpan(txt1, 4);
Grid.SetRow(txt1, 0);
Grid.SetColumn(txt1, 1);

// Add the second text cell to the Grid.
txt2 = new TextBlock();
txt2.Text = "Open:";
Grid.SetRow(txt2, 1);
Grid.SetColumn(txt2, 0);

// Add the TextBox control.
tb1 = new TextBox();
Grid.SetRow(tb1, 1);
Grid.SetColumn(tb1, 1);
Grid.SetColumnSpan(tb1, 5);

// Add the buttons.
button1 = new Button();
button2 = new Button();
button3 = new Button();
button1.Content = "OK";
button2.Content = "Cancel";
button3.Content = "Browse ...";
Grid.SetRow(button1, 3);
Grid.SetColumn(button1, 2);
button1.Margin = new Thickness(10, 0, 10, 15);
button2.Margin = new Thickness(10, 0, 10, 15);
button3.Margin = new Thickness(10, 0, 10, 15);
Grid.SetRow(button2, 3);
Grid.SetColumn(button2, 3);
Grid.SetRow(button3, 3);
Grid.SetColumn(button3, 4);

grid1.Children.Add(img1);
grid1.Children.Add(txt1);
grid1.Children.Add(txt2);
grid1.Children.Add(tb1);
grid1.Children.Add(button1);
grid1.Children.Add(button2);
grid1.Children.Add(button3);
```
</TabItem>  

</Tabs>

## 另请参阅 {#see-also}

- [Grid API 参考](/api/avalonia/controls/grid)
- [GitHub 上的 `Grid.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Grid.cs)
- [GridSplitter](/controls/layout/panels/gridsplitter)
- [Canvas](/controls/layout/panels/canvas)
- [DockPanel](/controls/layout/panels/dockpanel)
- [Panel](/controls/layout/panels/panel)
- [RelativePanel](/controls/layout/panels/relativepanel)
- [StackPanel](/controls/layout/panels/stackpanel)
- [UniformGrid](/controls/layout/panels/uniformgrid)
- [WrapPanel](/controls/layout/panels/wrappanel)

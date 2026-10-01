---
id: splitbutton
title: SplitButton
---

import SplitButtonPaletteFlyoutScreenshot from '/img/controls/buttons/splitbutton/splitbutton-palette-flyout.png';

[`SplitButton`](/api/avalonia/controls/splitbutton) 的行为像一个 [`Button`](/controls/input/buttons/button)，但分成主、次两部分，可以分别按下。主部分表现得和普通 `Button` 一样，次部分则打开一个装着更多操作的 [`Flyout`](/controls/menus/menuflyout)。

## 这个控件选对了吗？ {#is-this-the-right-control}

`SplitButton` 里只应该放彼此相近的操作。说到底，它是用来把一组常用操作归到一起、且其中某一个明显更重要的场合：最常用的那个作为默认操作，显示在 SplitButton 的主部分；不那么常用的则放进浮层，按下次要的（下拉）部分时才出现。

:::info
无论按下的是主部分还是浮层里的次要操作，用户选定的动作都应当立即执行。所有按下的操作，不分主次，一律即时生效。
:::

## 常用属性 {#common-properties}

| 属性  | 说明                                                    |
| --------- | -------------------------------------------------------------- |
| `Content` | 在主部分中显示的内容                     |
| [`Flyout`](/api/avalonia/controls/flyout)  | 按下次要部分时弹出的 `Flyout` |
| `Command` | 主按钮被点击时要调用的命令     |
| `HotKey`  | 触发主按钮操作的键盘快捷键   |

## Pseudoclasses

| 伪类    | 说明                                                                                                                                                         |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `:pressed`     | 用空格、Enter 等键盘输入按下整个 `SplitButton` 时设置。此状态下不区分主部分和次要部分 |
| `:flyout-open` | `Flyout` 处于打开状态时设置                                                                                                                                       |

## 示例 {#examples}

### 基本示例 {#basic-example}

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             Padding="20">
  <SplitButton Content="Content">
    <SplitButton.Flyout>
        <MenuFlyout Placement="Bottom">
            <MenuItem Header="Item 1">
                <MenuItem Header="Subitem 1" />
                <MenuItem Header="Subitem 2" />
                <MenuItem Header="Subitem 3" />
            </MenuItem>
            <MenuItem Header="Item 2"
                      InputGesture="Ctrl+A" />
            <MenuItem Header="Item 3" />
        </MenuFlyout>
    </SplitButton.Flyout>
  </SplitButton>
</UserControl>
```

</XamlPreview>

### 颜色选择示例 {#color-selection-example}

`SplitButton` 的一个常见用例是在编辑器中给文字上色：按下 `SplitButton` 的主部分，把当前颜色应用到选中的文字；按下次要部分则打开 `Flyout`，供用户另选一种颜色并应用。同样要注意，在 `Flyout` 中选定另一种颜色后，选中文字的颜色会立即改变，当前颜色也随之更新。

<Image light={SplitButtonPaletteFlyoutScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

```xml
<!-- We have the following DataTemplate defined -->
<DataTemplate DataType="Color">
   <Border CornerRadius="4" Width="20" Height="20" BorderBrush="Gray" BorderThickness="1">
    <Border.Background>
       <SolidColorBrush Color="{Binding}" />
   </Border.Background>
  </Border>
</DataTemplate>
```

```xml
<!-- SelectedColor, ChangeColorCommand and AvailableColors are properties of our ViewModel -->
<SplitButton Content="{Binding SelectedColor}" 
             Command="{Binding ChangeColorCommand}">
  <SplitButton.Flyout>
    <Flyout Placement="Bottom">
      <ListBox ItemsSource="{Binding AvailableColors}" 
               SelectedItem="{Binding SelectedColor}" 
               Height="200" Width="200">
        <ListBox.ItemsPanel>
          <ItemsPanelTemplate>
            <WrapPanel />
          </ItemsPanelTemplate>
        </ListBox.ItemsPanel>
      </ListBox>
    </Flyout>
  </SplitButton.Flyout>
</SplitButton>
```

### 导出按钮示例 {#export-button-sample}

`SplitButton` 的另一个常见例子是导出按钮：按下主部分时按默认设置导出数据；按下次要部分则可以指定更多导出选项，比如「导出为 PNG」「导出为 JPG」等等。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             Padding="20">
  <SplitButton Content="Export to PDF"
               Command="{Binding ExportCommand}"
               CommandParameter=".pdf">
     <SplitButton.Flyout>
          <MenuFlyout Placement="RightEdgeAlignedTop">
              <MenuItem Header="Export to PNG"
                        Command="{Binding ExportCommand}"
                        CommandParameter=".png" />
              <MenuItem Header="Export to JPG"
                        Command="{Binding ExportCommand}"
                        CommandParameter=".jpg" />
         </MenuFlyout>
      </SplitButton.Flyout>
  </SplitButton>
</UserControl>
```

</XamlPreview>

## 另请参阅 {#see-also}

- [SplitButton API 参考](/api/avalonia/controls/splitbutton)
- [GitHub 上的 `SplitButton.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/SplitButton/SplitButton.cs)


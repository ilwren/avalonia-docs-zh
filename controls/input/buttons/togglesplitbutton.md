---
id: togglesplitbutton
title: ToggleSplitButton
---

import ToggleSplitButtonTextListScreenshot from '/img/controls/buttons/togglesplitbutton/togglesplitbutton-text-list.png';

[`ToggleSplitButton`](/api/avalonia/controls/togglesplitbutton) 的行为像一个 [`ToggleButton`](/controls/input/buttons/togglebutton)，但分成主、次两部分，可以分别按下。主部分表现得和普通 `ToggleButton` 一样，次部分则打开一个装着更多操作的 [`Flyout`](/controls/menus/menuflyout)。

:::info
`ToggleSplitButton` 只有选中和未选中两个状态，不像标准的 `ToggleButton` 那样支持不确定状态。这是有意为之，既与 WinUI 保持一致，也限定了控件的用途：`ToggleSplitButton` 只应该用来开关某个功能，除此之外的用法，从可用性角度看目前都算不上好做法。
:::

## 这个控件选对了吗？ {#is-this-the-right-control}

`ToggleSplitButton` 是个相当专门的控件，只应该用在从用户角度看确实合适的地方。它的定位是：开关某项功能，同时允许指定一些有别于默认值的额外配置。

和 [`SplitButton`](/controls/input/buttons/splitbutton) 一样，最常用的操作应当作为默认项显示在主部分。但与 `SplitButton` 不同的是，按下主部分是开启或关闭这项功能，而不是执行某个动作。该功能的额外配置应放进 [`Flyout`](/api/avalonia/controls/flyout)，按下次要的（下拉）部分时才出现。

:::info
在 `Flyout` 中选择某个配置，应当要么（1）用选中的配置开启该功能，要么（2）把该功能切换到选中的配置。在 `Flyout` 中选择配置绝不应该关闭功能——关闭只能靠切换主部分来完成。
:::

## 常用属性 {#common-properties}

| 属性    | 说明                                                    |
| ----------- | -------------------------------------------------------------- |
| `Content`   | 在主部分中显示的内容                     |
| `Flyout`    | 按下次要部分时弹出的 `Flyout` |
| `Command`   | 主按钮被点击时要调用的命令     |
| `IsChecked` | 获取或设置 `ToggleSplitButton` 是否被选中             |

## Pseudoclasses

| 伪类    | 说明                                                                                                                                                               |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `:pressed`     | 用空格、Enter 等键盘输入按下整个 `ToggleSplitButton` 时设置。此状态下不区分主部分和次要部分 |
| `:flyout-open` | `Flyout` 处于打开状态时设置                                                                                                                                             |
| `:checked`     | `ToggleSplitButton` 被选中时设置。（`IsChecked="true"`）                                                                                                         |

## 示例 {#examples}

### 基本示例 {#basic-example}

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             Padding="20">
  <ToggleSplitButton Content="Content"
                   IsChecked="{Binding IsChecked}">
    <ToggleSplitButton.Flyout>
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
    </ToggleSplitButton.Flyout>
  </ToggleSplitButton>
</UserControl>
```

</XamlPreview>

### 带编号列表或项目符号列表的文本编辑器 {#text-editor-with-numbered-or-bulleted-list}

<Image light={ToggleSplitButtonTextListScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

接着 `SplitButton` 中那个文本编辑器的例子：`ToggleSplitButton` 的一个常见用例是给文字加项目符号列表或编号列表。本例中，主部分负责开关列表，次要部分则打开 `Flyout`，供用户挑选项目符号或编号的样式。

```xml
<!-- We have the following Icons defined in our Resources -->
<PathGeometry x:Key="IconData.NumberedList"> {{ Path Data }} </PathGeometry>
<PathGeometry x:Key="IconData.BulletedList"> {{ Path Data }} </PathGeometry>
```

```xml
<ToggleSplitButton IsChecked="{Binding TextEditorHasList}">
    <ToggleSplitButton.Content>
        <!-- Note: For this example we keep the content static, but you can use dynamic content -->
        <PathIcon Data="{DynamicResource IconData.BulletedList}" />
    </ToggleSplitButton.Content>
    <ToggleSplitButton.Flyout>
        <Flyout Placement="Bottom">
            <!-- Note: For this example we keep the content static, but you can use dynamic content -->
            <ListBox Height="200" Width="200" >
                <ListBoxItem>
                    <StackPanel Orientation="Horizontal">
                        <PathIcon Data="{DynamicResource IconData.NumberedList}" />
                        <TextBlock Text="Numbered List" />
                    </StackPanel>
                </ListBoxItem>
                <ListBoxItem>
                    <StackPanel Orientation="Horizontal">
                        <PathIcon Data="{DynamicResource IconData.BulletedList}" />
                        <TextBlock Text="Bulleted List" />
                    </StackPanel>
                </ListBoxItem>
            </ListBox>
        </Flyout>
    </ToggleSplitButton.Flyout>
</ToggleSplitButton>
```

## 另请参阅 {#see-also}

- [ToggleSplitButton API 参考](/api/avalonia/controls/togglesplitbutton)
- [GitHub 上的 `ToggleSplitButton.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/SplitButton/ToggleSplitButton.cs)

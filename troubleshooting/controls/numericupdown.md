---
id: numericupdown
title: NumericUpDown 问题
description: 排查 NumericUpDown 选择控件的毛病
doc-type: troubleshooting
sidebar_label: NumericUpDown
---

## 清空 `NumericUpDown` 文本框时抛出无效强制转换异常 {#invalid-cast-exception-when-numericupdown-text-box-is-cleared}

当 `NumericUpDown` 的文本框内容被清空时，控件可能抛出无效强制转换异常，例如 `Invalid cast from string to decimal?`

想避免这类异常，可以试试下面的办法：

- 在你的 `Binding` 上设置 `TargetNullValue` 和 `FallbackValue`（都设为 `0`）。注意要让它们的类型与源属性类型（通常是 `decimal` 或 `int`）明确一致，这样它们才会被当作数字而非 `string`。如此一来，空文本框就不会再被记成一次绑定失败。
- （可选）设置 `UpdateSourceTrigger=LostFocus`，让视图模型在编辑过程中不被更新。这能减少异常出现的次数，但不能彻底根除。

```xml
<NumericUpDown Minimum="0" Maximum="10000000">
  <NumericUpDown.Value>
    <Binding Path="Units">
      <Binding.TargetNullValue><x:Decimal>0</x:Decimal></Binding.TargetNullValue>
      <Binding.FallbackValue><x:Decimal>0</x:Decimal></Binding.FallbackValue>
    </Binding>
  </NumericUpDown.Value>
</NumericUpDown>
```

## 另请参阅 {#see-also}

- [NumericUpDown 控件](/controls/input/selectors/numericupdown)
- [数据绑定语法](/docs/data-binding/data-binding-syntax)
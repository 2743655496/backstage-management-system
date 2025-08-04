<template>
  <div>首页

    <div class="flex-container">Flex Container（独占一行）</div>
<div class="inline-flex-container">Inline-Flex Container（行内排列）</div>
<div class="inline-flex-container">另一个 Inline-Flex</div>
  </div>
</template>

<script>
export default {

}
</script>

<style lang="less" scoped>
.flex-container {
  display: flex; /* 默认 block-level，独占一行 */
  background: #e74c3c;
  padding: 10px;
  margin: 5px;
}

.inline-flex-container {
  display: inline-flex; /* 行内 Flex，不换行 */
  background: #2ecc71;
  padding: 10px;
  margin: 5px;
}
</style>
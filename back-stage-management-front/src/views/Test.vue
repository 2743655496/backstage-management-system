<template>
  <div>
    <h3>单选</h3>
    <tree-select v-model="singleValue" :data="treeData" />
 
    <h3 style="margin-top:20px;">多选</h3>
    <tree-select v-model="multiValue" :data="treeData" multiple />
  </div>
</template>
 
<script>
import TreeSelect from "../components/TreeSelect.vue";
 
export default {
  components: { TreeSelect },
  data() {
    return {
      singleValue: null,
      multiValue: [],
      treeData: [
        {
          id: 1,
          label: "水果",
          children: [
            {
              id: 11,
              label: "苹果",
              children: [
                { id: 111, label: "红富士" },
                { id: 112, label: "奶苹果" }
              ]
            },
            { id: 12, label: "香蕉" }
          ]
        },
        {
          id: 2,
          label: "蔬菜",
          children: [
            { id: 21, label: "西红柿" },
            { id: 22, label: "黄瓜" }
          ]
        }
      ]
    };
  }
};
</script>
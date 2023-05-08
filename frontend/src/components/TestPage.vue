<template>
  <div>
    <div class="demo-progress">
      <el-progress :text-inside="true" :stroke-width="26" :percentage="percentages[0]" :color="'#5f00af'"/>
      <el-progress
        :text-inside="true"
        :stroke-width="24"
        :percentage="percentages[1]"
        status="success"
      />
      <el-progress
        :text-inside="true"
        :stroke-width="22"
        :percentage="percentages[2]"
        status="warning"
      />
      <el-progress
        :text-inside="true"
        :stroke-width="20"
        :percentage="percentages[3]"
        status="exception"
      />
    </div>
    <el-button @click="startIncreasing">开始增加</el-button>
  </div>
</template>

<script>
import { ref, onUnmounted } from 'vue';

export default {
  setup() {
    const percentages = ref([70, 100, 80, 50]);
    let intervalId;

    const increasePercentages = () => {
      percentages.value = percentages.value.map((percentage) => {
        if (percentage + 5 > 95) {
          return 95;
        }
        return percentage + 5;
      });
    };

    const startIncreasing = () => {
      if (!intervalId) {
        intervalId = setInterval(increasePercentages, 1000);
      }
    };

    onUnmounted(() => {
      clearInterval(intervalId);
    });

    return {
      percentages,
      startIncreasing,
    };
  },
};
</script>

<style scoped>
.demo-progress .el-progress--line {
  margin-bottom: 15px;
  width: 350px;
}
</style>

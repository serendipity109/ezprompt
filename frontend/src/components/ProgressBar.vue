<template>
    <div class="progress-bar-container" v-show="show">
      <div class="progress-bar" :style="{ width: progress + '%' }"></div>
    </div>
  </template>
  
  <script>
  import { ref } from "vue";
  
  export default {
    setup() {
      const show = ref(false);
      const progress = ref(0);
  
      const start = () => {
        show.value = true;
        progress.value = 0;
      };
  
      const update = (value) => {
        progress.value = value;
      };
  
      const finish = () => {
        progress.value = 100;
        setTimeout(() => {
          show.value = false;
        }, 500);
      };
  
      return {
        show,
        progress,
        start,
        update,
        finish,
      };
    },
  };
  </script>
  
  <style scoped>
  .progress-bar-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 5px;
    overflow: hidden;
    z-index: 9999;
  }
  
  .progress-bar {
    height: 100%;
    width: 0;
    background-color: #1abc9c;
    transition: width 0.1s;
  }
  </style>
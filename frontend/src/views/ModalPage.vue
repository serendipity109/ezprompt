<template>
  <div>
    <button @click="showModal">Open Modal</button>

    <div v-if="isModalVisible" class="modal">
      <div class="modal-content">
        <slot />
        <button @click="hideModal">Close Modal</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const isModalVisible = ref(false);

    const showModal = () => {
      isModalVisible.value = true;
    };

    const hideModal = () => {
      isModalVisible.value = false;
    };

    return {
      isModalVisible,
      showModal,
      hideModal,
    };
  },
};
</script>

<style>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 4px;
}

button {
  margin-top: 10px;
}
</style>

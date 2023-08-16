<template>
    <div class="container">
        <input type="file" @change="onFileChange" class="file-input">
        <div class="canvas-wrapper">
            <div class="canvas-container">
                <canvas v-if="image" ref="canvas" @mousedown="drawPoint" @contextmenu.prevent></canvas>
            </div>
            <div class="canvas-container empty"></div>
        </div>
        <button class="reset-button" @click="resetPoints">Reset</button>
    </div>
</template>

<script>
import { ref, toRefs } from 'vue';

export default {
  setup() {
    const image = ref(null);
    const pointCount = ref(0);
    const points = ref([]);
    const canvas = ref(null);

    const onFileChange = (event) => {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        image.value = new Image();
        image.value.onload = () => {
          drawImageToCanvas();
        }
        image.value.src = e.target.result;
      }
      reader.readAsDataURL(file);
    };

    const drawImageToCanvas = () => {
      const ctx = canvas.value.getContext('2d');
      const scaleX = 512 / image.value.width;
      const scaleY = 512 / image.value.height;
      const scale = Math.min(scaleX, scaleY);
      
      const width = image.value.width * scale;
      const height = image.value.height * scale;
      const offsetX = (512 - width) / 2;
      const offsetY = (512 - height) / 2;
      
      canvas.value.width = 512;
      canvas.value.height = 512;
      ctx.drawImage(image.value, offsetX, offsetY, width, height);
    };

    const drawPoint = (event) => {
      if (pointCount.value >= 4) return;

      const x = event.offsetX;
      const y = event.offsetY;

      const color = event.button === 0 ? 'black' : (event.button === 2 ? 'red' : null);

      if (!color) return;

      points.value.push({ x, y, color });
      console.log(x, y, color);
      const ctx = canvas.value.getContext('2d');
      ctx.fillStyle = color;
      const radius = 5;

      ctx.beginPath();
      ctx.arc(x, y, radius, 0, 2 * Math.PI);
      ctx.fill();

      pointCount.value++;
    };

    const resetPoints = () => {
      pointCount.value = 0;
      points.value = [];
      drawImageToCanvas();
    };

    return {
      ...toRefs({ image, pointCount, points }),
      canvas,
      onFileChange,
      drawPoint,
      resetPoints
    };
  }
}
</script>


<style scoped>
.container {
    display: flex;
    align-items: center;
    justify-content: center; /* vertically align the container */
    flex-direction: column;
    width: 80%; /* or whatever width you prefer */
    margin: 0 auto; /* horizontally center the container */
}

.canvas-wrapper {
    display: flex;
    align-items: center;
    margin-bottom: 5px; /* space below the canvas-wrapper */
}

.canvas-container {
    width: 512px;
    height: 512px;
    border: 2px solid purple; /* purple border */
    overflow: hidden;
    position: relative;
    box-sizing: border-box; /* ensure the border doesn't increase the container size */
    margin-right: 5px; /* add margin to the right */
}

canvas {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 508px;  /* reduce by 2px * 2 due to border */
    height: 508px; /* reduce by 2px * 2 due to border */
}

.canvas-container.empty {
    border: 2px dashed purple; /* dashed border for the empty container */
    margin-right: 0; /* remove margin from the empty container */
}

.file-input {
    margin-bottom: 5px; /* space above the file input */
}

.reset-button {
    margin-top: 5px;
    background-color: #ff4757;
    border: none;
    border-radius: 25px;
    color: #ffffff;
    cursor: pointer;
    font-size: 16px;
    padding: 10px 20px;
    outline: none;
    transition: background-color 0.3s, transform 0.3s;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.reset-button:hover {
    background-color: #ff6b81;
}

.reset-button:active {
    transform: scale(0.95);
}

.reset-button:focus {
    box-shadow: 0 0 0 2px rgba(255, 71, 87, 0.5);
}
</style>

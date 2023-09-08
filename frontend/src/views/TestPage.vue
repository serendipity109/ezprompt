<template>
    <div>
        <button class="reset-button" @click="dialog_switch">Switch</button>
        <v-dialog v-model="dialog" width="auto">
            <canvas ref="canvasRef" @mousemove="handleMouseMove" @mouseleave="handleMouseLeave" @mousedown="handleMouseDown"></canvas>
        </v-dialog>
    </div>
</template>

<script>
import { ref, computed, reactive, nextTick } from 'vue';

export default {
    name: 'ImageCanvas',
    setup() {
        const dialog = ref(false);
        const canvasRef = ref(null);
        const baseImageUrl = 'http://192.168.3.20:9527/media/adamwang@emotibot.com/input/image.png';

        const initializeCanvas = () => {
            const canvas = canvasRef.value;
            const ctx = canvas.getContext('2d');
            canvas.width = baseImg.width;
            canvas.height = baseImg.height;
            ctx.drawImage(baseImg, 0, 0);
        };

        const dialog_switch = () => {
            console.log("Switch button clicked");
            dialog.value = !dialog.value;
            if (dialog.value) {
                nextTick(() => {
                    initializeCanvas();
                });
            }
        }

        const maskImageConfig = reactive({
            baseUrl: 'http://192.168.3.20:9527/sam/select_mask?user_id=adamwang@emotibot.com',
            x: 0,
            y: 0
        });

        const maskImageUrl = computed(() => {
            return `${maskImageConfig.baseUrl}&x=${maskImageConfig.x}&y=${maskImageConfig.y}`;
        });

        const baseImg = new Image();
        baseImg.crossOrigin = "anonymous";
        baseImg.src = baseImageUrl;

        const handleMouseMove = (event) => {
            const rect = canvasRef.value.getBoundingClientRect();
            maskImageConfig.x = Math.round(event.clientX - rect.left);
            maskImageConfig.y = Math.round(event.clientY - rect.top);

            const ctx = canvasRef.value.getContext('2d');
            const maskImg = new Image();
            maskImg.crossOrigin = "anonymous";
            maskImg.src = maskImageUrl.value;
            maskImg.onload = () => {
                ctx.drawImage(baseImg, 0, 0);  // redraw the base image
                ctx.drawImage(maskImg, 0, 0);  // draw the new mask image
            };
        };
        
        const handleMouseLeave = () => {
            const ctx = canvasRef.value.getContext('2d');

            // Clear the entire canvas
            ctx.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height);

            // Check if baseImg has loaded
            if (baseImg.complete) {
                // Redraw the baseImg
                ctx.drawImage(baseImg, 0, 0);
            }
        };

        return {
            dialog,
            dialog_switch,
            canvasRef,
            handleMouseMove,
            handleMouseLeave
        };
    },
};
</script>

<style scoped>
canvas {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: auto;
    height: auto;
}
</style>

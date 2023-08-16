<template>
    <div>
        <input type="file" @change="onFileChange">
        <canvas v-if="image" ref="canvas" @mousedown="drawPoint" @contextmenu.prevent></canvas>
        <button class="reset-button" @click="resetPoints">Reset</button>
    </div>
 </template>

<script>
export default {
    data() {
        return {
            image: null,
            pointCount: 0,
            points: []
        }
    },
    methods: {
        onFileChange(event) {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.onload = (e) => {
                this.image = new Image();
                this.image.onload = () => {
                    this.drawImageToCanvas();
                }
                this.image.src = e.target.result;
            }
            reader.readAsDataURL(file);
        },
        drawImageToCanvas() {
            const canvas = this.$refs.canvas;
            const ctx = canvas.getContext('2d');
            canvas.width = this.image.width;
            canvas.height = this.image.height;
            ctx.drawImage(this.image, 0, 0);
        },
        drawPoint(event) {
            if (this.pointCount >= 4) return;

            const x = event.offsetX;
            const y = event.offsetY;

            const color = event.button === 0 ? 'red' : (event.button === 2 ? 'black' : null);

            if (!color) return;

            this.points.push({ x, y, color });
            console.log( x, y, color)
            const canvas = this.$refs.canvas;
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = color;
            const radius = 5;

            ctx.beginPath();
            ctx.arc(x, y, radius, 0, 2 * Math.PI);
            ctx.fill();

            this.pointCount++;
    },
        resetPoints() {
            this.pointCount = 0; 
            this.points = [];
            this.drawImageToCanvas(); 
    }
    }
}
</script>


<style scoped>
.reset-button {
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

<template>
    <div>
        <el-dialog v-model="dialog" height="auto" width="70%" top="70px">
            <template #header>
                <h4 style="text-align:center">
                    Click to select unchanged areas in the original image (purple denotes the area, color depth irrelevant)
                </h4>
            </template>
            <div v-loading="loading" element-loading-text="Loading..." class="canvas-container">
                <canvas ref="canvasRef" @mousemove="handleMouseMove" @mouseleave="handleMouseLeave"
                    @mousedown="handleMouseDown"></canvas>
                <el-button-group class="mt-10" size="large">
                    <el-button class="edit-button" :icon="Refresh" @click="resetMask" >Reset</el-button>
                    <el-button class="edit-button" :icon="CircleCheck" @click="done">Done</el-button>
                </el-button-group>
            </div>
        </el-dialog>
    </div>
</template>

  
<script>
import { ref, computed, reactive, nextTick } from 'vue';
import axios from 'axios';
import {
  Refresh,
  CircleCheck
} from '@element-plus/icons-vue'

export default {
    name: 'ImageCanvas',
    props: {
        username: String
    },
    setup(props, context) {
        const dialog = ref(false);
        const loading = ref(false);
        const filename = ref(null);
        const canvasRef = ref(null);
        const baseImageUrl = computed(() => {
            return `http://192.168.3.20:9527/media/${props.username}/input/${filename.value}`;
        });

        let selectedMaskImg = new Image(); 

        const initializeCanvas = () => {
            const canvas = canvasRef.value;
            const ctx = canvas.getContext('2d');
            canvas.width = baseImg.width;
            canvas.height = baseImg.height;
            ctx.drawImage(baseImg, 0, 0);
        };

        const resetMask = async () => {
            try {
                await axios.post(`http://192.168.3.20:9527/sam/reset_mask?user_id=${props.username}`, {
                    user_id: props.username
                });
                console.log('Reset successful');
                
                const ctx = canvasRef.value.getContext('2d');

                // Update the src of selectedMaskImg
                selectedMaskImg.src = `${selectedMaskImgUrl.value}?t=${new Date().getTime()}`;

                selectedMaskImg.onload = () => {
                    // Clear the entire canvas
                    ctx.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height);

                    // Redraw baseImg and selectedMaskImg
                    if (baseImg.complete) {
                        ctx.drawImage(baseImg, 0, 0);
                    }
                    if (selectedMaskImg.complete) {
                        ctx.drawImage(selectedMaskImg, 0, 0);
                    }
                };
            } catch (error) {
                console.error('Failed to reset mask', error);
            }
        };

        const dialog_switch = async (newFilename) => {
            dialog.value = !dialog.value;
            filename.value = newFilename._value;
            if (dialog.value) {
                // Set the onload event before setting the src
                baseImg.onload = async () => {
                    await nextTick();
                    initializeCanvas();
                    await edit();
                };
                // Now set the src to trigger the loading
                baseImg.src = baseImageUrl.value;  
            }
        };

        const edit = async () => {
            loading.value = true;
            try {
                const response = await axios.post('http://192.168.3.20:9527/sam/edit', null, {
                    params: {
                        user_id: props.username,
                        img: filename.value
                    }
                });
                console.log(response.data);
            } catch (error) {
                console.error('Error making the request:', error);
            }
            loading.value = false;
        }

        const done = async () => {
            try {
                const response = await axios.post('http://192.168.3.20:9527/sam/done', null, {
                    params: {
                        user_id: props.username,
                        img: filename.value
                    }
                });
                console.log(response.data);
                sendUrl(response.data.data);
                dialog.value = !dialog.value;
            } catch (error) {
                console.error('Error making the request:', error);
            }
            loading.value = false;
        };      
        
        const sendUrl = (url) => {
            context.emit('blend-url', url);
        };

        const maskImageConfig = reactive({
            baseUrl: `http://192.168.3.20:9527/sam/select_mask?user_id=${props.username}`,
            x: 0,
            y: 0,
        });

        const maskImageUrl = computed(() => {
            return `${maskImageConfig.baseUrl}&x=${maskImageConfig.x}&y=${maskImageConfig.y}`;
        });

        const selectedMaskImgUrl = computed(() => {
            return `http://192.168.3.20:9527/sam/media/${props.username}/selected_mask`;
        });

        const baseImg = new Image();
        baseImg.crossOrigin = 'anonymous';
        baseImg.src = baseImageUrl;

        const handleMouseMove = (event) => {
            const rect = canvasRef.value.getBoundingClientRect();
            maskImageConfig.x = Math.round(event.clientX - rect.left);
            maskImageConfig.y = Math.round(event.clientY - rect.top);

            const ctx = canvasRef.value.getContext('2d');
            const maskImg = new Image();
            maskImg.crossOrigin = 'anonymous';
            maskImg.src = maskImageUrl.value;

            maskImg.onload = () => {
                ctx.drawImage(baseImg, 0, 0); // redraw the base image
                ctx.drawImage(maskImg, 0, 0); // draw the new mask image
                if (selectedMaskImg.complete) {  // Check if the image has loaded
                    ctx.drawImage(selectedMaskImg, 0, 0);  // Draw the selected mask image
                }
            };
        };

        const handleMouseDown = async (event) => {
            if (event.button !== 0) return; // 如果不是左鍵，直接返回

            try {
                // 執行 Axios POST 請求
                await axios.post(`http://192.168.3.20:9527/sam/mix_mask?user_id=${props.username}`, null, {
                    responseType: 'blob', // 設置 responseType 為 'blob'
                });
                
                const ctx = canvasRef.value.getContext('2d');
                selectedMaskImg.crossOrigin = 'anonymous';
                
                // Add a timestamp to the URL to avoid caching
                selectedMaskImg.src = `${selectedMaskImgUrl.value}?t=${new Date().getTime()}`;
                        
                // Set the onload event before setting the src
                selectedMaskImg.onload = () => {
                    ctx.drawImage(baseImg, 0, 0); // redraw the base image
                    ctx.drawImage(selectedMaskImg, 0, 0); // draw the new mask image on top
                };
            } catch (error) {
                console.error('POST 請求失敗', error);
            }
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
            if (selectedMaskImg.complete) {
                ctx.drawImage(selectedMaskImg, 0, 0);  // Draw the selected mask image
            }
        };

        return {
            dialog,
            loading,
            edit,
            done,
            sendUrl,
            Refresh,
            CircleCheck,
            dialog_switch,
            resetMask,
            canvasRef,
            handleMouseMove,
            handleMouseDown,
            handleMouseLeave,
        };
    },
};
</script>
  
<style scoped>
.canvas-container {
    display: flex;
    flex-direction: column;
    align-items: center; /* Center the children horizontally */
}
.switch-button {
    margin-top: 5px;
    background-color: #141515;
    border: none;
    border-radius: 25px;
    color: #ffffff;
    cursor: pointer;
    font-size: 28px;  /* Increase from 16px to 32px */
    outline: none;
    transition: background-color 0.3s, transform 0.3s;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.edit-button {
    margin-top: 5px;
    background-color: #141515;
    border: none;
    border-radius: 25px;
    color: #ffffff;
    cursor: pointer;
    font-size: 28px;  /* Increase from 16px to 32px */
    outline: none;
    transition: background-color 0.3s, transform 0.3s;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
  
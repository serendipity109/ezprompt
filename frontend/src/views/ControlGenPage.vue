<template>
    <div>
        <nav-bar page="generate" :closePanel="closePanel"/>
        <div class="container min-w-screen" style="margin-top: 8ch;">
            <input type="file" @change="onFileChange" class="file-input">
            <div class="canvas-wrapper">
                <div class="canvas-container">
                    <canvas v-if="image" ref="canvas" @mousedown="drawPoint" @contextmenu.prevent></canvas>
                </div>
                <div v-loading="loading" element-loading-text="Loading..." class="canvas-container empty flex items-center justify-center">
                    <div v-if="msk_type===0" class="flex overflow-x-auto align-center justify-start thin-scrollbar h-auto pb-2"
                        style="height:fit-content; overscroll-behavior-x:contain; white-space: nowrap;">
                        <div v-for="(img_url, index) in img_res" :key="index" style="display: inline-block; margin-right: 5px;">
                            <img v-bind:src="img_url" v-on:click="showViewer([img_url])"
                            style="object-fit:contain; width:100%; max-height: 80%; display: block;" />
                            <input type="checkbox" style="position: relative;" class="image-checkbox" @change="handleCheckboxChange(index, $event)">
                        </div>
                    </div>
                    <div v-if="msk_type===1" class="canvas-container empty flex items-center justify-center">
                        <canvas ref="maskCanvas" v-show="msk_type===1"></canvas>
                    </div>
                </div>
            </div>
            <div class="button-line">
                <button class="reset-button" @click="resetPoints">Reset</button>
                <button class="sam-button" @click="() => sam(blacks, reds)">SAM</button>
                <button class="sm-button" @click="() => select_mask()">Select Mask</button>
            </div>
        </div>
        <div class="model container min-w-screen" style="margin-top: 5ch;">
            <h2 style="font-size: 2em; margin-bottom: 1ch;">Model Selection</h2>
            <el-cascader placeholder="Gender Selection" :options="options" @change="handleChange" />
            <div v-if="gender===0" class="selection-wrapper" style="margin-top: 3ch;">
                <div v-for="(model, index) in models" :key="index" class="selection-item">
                    <el-radio v-model="radio_m" :label="index.toString()" size="large">{{ model }}</el-radio>
                    <img :src="md0_urls[index]" style="width: 151px; height: 151px; margin-right: 5ch;">
                </div>
            </div>
            <div v-if="gender===1" class="selection-wrapper" style="margin-top: 3ch;">
                <div v-for="(model, index) in models" :key="index" class="selection-item">
                    <el-radio v-model="radio_m" :label="index.toString()" size="large">{{ model }}</el-radio>
                    <img :src="md1_urls[index]" style="width: 151px; height: 151px; margin-right: 5ch;">
                </div>
            </div>
        </div>
        <div class="loc container" style="margin-top: 3ch; margin-bottom: 5ch;">
            <h2 style="font-size: 2em; margin-bottom: 1ch;">Location Selection</h2>
            <div class="selection-wrapper">
                <div v-for="(location, index) in locations" :key="index" class="selection-item">
                    <el-radio v-model="radio_l" :label="index.toString()" size="large">{{ location }}</el-radio>
                    <img :src="loc_urls[index]" style="width: 151px; height: 151px; margin-right: 5ch;">
                </div>
            </div>
        </div>
        <div class="generate container" style="margin-top: 3ch; margin-bottom: 3ch;">
            <button class="gen-button" @click="generate">Generate</button>
            <div class="generate image" style="margin-top: 3ch;">
                <div v-loading="loading2" element-loading-text="Loading..." class="res-canvas-container">
                    <canvas ref="resCanvas" v-on:click="showViewer([res_url])"></canvas>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, reactive, computed } from 'vue';
import { api as viewerApi } from 'v-viewer'
import axios from "axios";
import { ElMessage } from 'element-plus'
import NavBar from '@/components/NavBar.vue';
import { GET_USERNAME } from "@/store/storeconstants";
import { useStore } from 'vuex'

export default {
    components: {
        NavBar
    },
    setup() {
        const state = reactive({
        image: null,
        pointCount: 0,
        points: [],
        });
        let img = ref(null);
        const mask = ref(null);
        const image = ref(null);
        const image_url = ref(null);
        const mask_url = ref(null);
        const canvas = ref(null);
        const maskCanvas = ref(null);
        const resCanvas = ref(null);
        const img_res = ref([]);
        const models = ref(["A", "B", "C", "D"]);
        const md0_urls = ref(["http://192.168.3.16:9527/media/mock/0_a.png", "http://192.168.3.16:9527/media/mock/0_b.png", "http://192.168.3.16:9527/media/mock/0_c.png", "http://192.168.3.16:9527/media/mock/0_d.png"])
        const md1_urls = ref(["http://192.168.3.16:9527/media/mock/1_a.png", "http://192.168.3.16:9527/media/mock/1_b.png", "http://192.168.3.16:9527/media/mock/1_c.png", "http://192.168.3.16:9527/media/mock/1_d.png"])
        const locations = ref(["beach", "street", "cafe"]);
        const loc_urls = ref(["https://ai-global-image.weshop.com/ad30c49b-0c28-458b-be06-4b1f73a10965.png_256x256.jpeg", "https://ai-global-image.weshop.com/20c29716-f083-41f1-8c26-db9df6f37135.png_256x256.jpeg", "https://ai-global-image.weshop.com/64207f3d-c144-4197-88b1-df6843359394.png_256x256.jpeg"]);
        const pointCount = ref(0);
        const points = ref([]);
        const blacks = ref([]);
        const reds = ref([]);
        const checkedIndices = ref([]);
        const loading = ref(false);
        const loading2 = ref(false);
        const msk_type = ref(0);
        const gender = ref("0");
        const radio_m = ref("0");
        const radio_l = ref("0");
        const socket = ref(null);
        const LOC = ref("");
        const res_url = ref("");
        const closePanel = ref(true);
        const store = useStore()

        const handleChange = (value) => {
            gender.value = value[0]
        }

        const options = [
        {
            value: 0,
            label: 'Man'
        },
        {
            value: 1,
            label: 'Woman'
        }]

        const username = computed(() => {
            let userName = store.getters[`auth/${GET_USERNAME}`]
            return userName;
        });

        const set_init = async () => {
                closePanel.value = !closePanel.value;
            }
        
        const onFileChange = async (event) => {
            if (username.value == ""){
                ElMessage.error("Please login.")
                return
            }
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.onload = async (e) => {
                image.value = new Image();
                image.value.onload = () => {
                    drawImageToCanvas(image.value, canvas, 512);
                };
                image.value.src = e.target.result;

                const formData = new FormData();
                formData.append('rawfile', file, 'image.png'); // Assuming the name of the file should be 'image.png'

                try {
                    const response = await axios.post(`http://192.168.3.20:9527/upload?user_id=${username.value}`, formData, {
                        headers: {
                            'accept': 'application/json',
                            'Content-Type': 'multipart/form-data'
                        }
                    });
                    image_url.value = response.data.data
                } catch (error) {
                    console.error("Error uploading the image:", error);
                }
            }
            reader.readAsDataURL(file);
            checkedIndices.value = []
        };

        const drawImageToCanvas = (targetImage, targetCanvas, size) => {
            const ctx = targetCanvas.value.getContext('2d');
            ctx.clearRect(0, 0, targetCanvas.width, targetCanvas.height);
            const scaleX = size / targetImage.width;
            const scaleY = size / targetImage.height;
            const scale = Math.min(scaleX, scaleY);
            
            const width = targetImage.width * scale;
            const height = targetImage.height * scale;
            const offsetX = (size - width) / 2;
            const offsetY = (size - height) / 2;
            
            targetCanvas.value.width = size;
            targetCanvas.value.height = size;
            ctx.drawImage(targetImage, offsetX, offsetY, width, height);
        };


        const drawPoint = (event) => {
            if (pointCount.value >= 8) return;

            // Get canvas-relative coordinates
            const xCanvas = event.offsetX;
            const yCanvas = event.offsetY;

            // Calculate the scale used to draw the image
            const scaleX = 512 / image.value.width;
            const scaleY = 512 / image.value.height;
            const scale = Math.min(scaleX, scaleY);

            // Calculate the image's offsets
            const width = image.value.width * scale;
            const height = image.value.height * scale;
            const offsetX = (512 - width) / 2;
            const offsetY = (512 - height) / 2;

            // Convert canvas-relative coordinates to image-relative
            const xImage = Math.round((xCanvas - offsetX) / scale);
            const yImage = Math.round((yCanvas - offsetY) / scale);

            let targetArray = null;
            let color = null;

            if (event.button === 0) {
                color = 'black';
                targetArray = blacks;
            } else if (event.button === 2) {
                color = 'red';
                targetArray = reds;
            }

            if (!color) return;

            targetArray.value.push({ x: xImage, y: yImage });
            const ctx = canvas.value.getContext('2d');
            ctx.fillStyle = color;
            const radius = 5;

            ctx.beginPath();
            ctx.arc(xCanvas, yCanvas, radius, 0, 2 * Math.PI);
            ctx.fill();

            pointCount.value++;
        };


        const resetPoints = () => {
            pointCount.value = 0;
            blacks.value = [];
            reds.value = [];
            drawImageToCanvas(image.value, canvas, 512);
        };

        const sam = async (blacks, reds) => {
            msk_type.value = 0;
            const match = image_url.value.match(/\/media\/(.*?)\/input\/(.*?)$/);
            if (!match) {
                console.error("Invalid image_url format");
                return;
            }
            img = match[2];

            // Construct the URL
            const formatPoints = (points) => {
                return points.map(point => `(${point.x}, ${point.y})`).join(', ');
            };

            const formattedBlacks = encodeURIComponent(`[${formatPoints(blacks)}]`);
            const formattedReds = encodeURIComponent(`[${formatPoints(reds)}]`);

            // Construct the URL
            const url = `http://192.168.3.20:9527/sam?user_id=${encodeURIComponent(username.value)}&img=${encodeURIComponent(img)}&blacks=${formattedBlacks}&reds=${formattedReds}`;

            try {
                const [_, response] = await Promise.all([
                    loading_switch(loading),
                    await axios.post(url, null, {
                        headers: {
                            'accept': 'application/json'
                        }
                    })
                ]);
                console.log(_)
                loading_switch(loading)
                img_res.value = response.data.data;
            } catch (error) {
                console.error("Error in SAM function:", error);
            }
            resetPoints();
        };

        const loading_switch = (loading) => {
            loading.value = !loading.value;
        }
        
        const handleCheckboxChange = (index, event) => {
            if (event.target.checked) {
            // Add the index to the array if it's not already present
                if (!checkedIndices.value.includes(index)) {
                    checkedIndices.value.push(index);
                }
            } else {
                // Remove the index from the array
                checkedIndices.value = checkedIndices.value.filter(i => i !== index);
            }
        };

        const select_mask = async () => {
            const mask_ids = encodeURIComponent(checkedIndices.value.join(","));
        
            // Construct the URL
            const url = `http://192.168.3.20:9527/select_mask/${mask_ids}?user_id=${username.value}`;
            try {
                const response = await axios.post(url, null, {
                    headers: {
                        'accept': 'application/json'
                    }
                });
                mask.value = response.data.data;
                msk_type.value = 1;
                mask_url.value = `http://192.168.3.20:9527/media/${username.value}/input/${mask.value}`;

                // Load mask image and draw it to maskCanvas
                const maskImage = new Image();
                maskImage.onload = () => {
                    drawImageToCanvas(maskImage, maskCanvas, 512);
                };
                maskImage.src = mask_url.value;
            } catch (error) {
                console.error("Error in Select Mask:", error);
            }
        };

        const extractedLora = computed(() => {
            const index = parseInt(radio_m.value, 10);
            let md_urls;
            if (gender.value == 0) {
                md_urls = md0_urls;
            } else {
                md_urls = md1_urls;
            }
            if (index >= 0 && index < md_urls.value.length) {
                const url = md_urls.value[index];
                const parts = url.split('/');
                const filename = parts[parts.length - 1];
                const name = filename.split('.')[0];
                return name;
            }
            return '';  // Return empty string if index is out of bounds
        });

        const generate = async () => {
            if (checkedIndices.value.length === 0){
                ElMessage.error("Please select mask.")
                return
            }
            loading2.value = true;
            if (socket.value && socket.value.readyState !== WebSocket.CLOSED) {
                socket.value.close();
            }
            socket.value = new WebSocket("ws://192.168.3.20:9527/img2img");
            let message;

            switch(radio_l.value) {
                case "0":
                LOC.value = "(on the beach:1.5)";
                break;
                case "1":
                LOC.value = "(on the street:1.5)";
                break;
                case "2":
                LOC.value = "(in a cafe:1.5)";
                break;
            }

            socket.value.onopen = () => {
                message = {
                    "user_id": username.value,
                    "image": img,
                    "mask": mask.value,
                    "prompt":`best quality, masterpiece, (photorealistic:1.4), depth of field, ${LOC.value}`,
                    "nprompt":"(worst quality:2), (low quality:2), (normal quality:2), lowres,watermark, monochrome",
                    "model": extractedLora.value
                };
                console.log(message);
                socket.value.send(JSON.stringify(message));
            };
            ElMessage.info({
                showClose: true,
                message: "Images are generating. Please wait patiently.",
                duration: 5000
            });
            socket.value.onmessage = (event) => {
                const data = JSON.parse(event.data);
                if (data.code === 201 && data.data) {
                    res_url.value = data.data.image;
                    // Load response image and draw it to resCanvas
                    const resImage = new Image();
                    resImage.onload = () => {
                        drawImageToCanvas(resImage, resCanvas, 1024);
                    };
                    resImage.src = data.data.image;
                    loading2.value = false;
                }
            };
        }

        const showViewer = (img_res) => {
        viewerApi({
            options: {
            toolbar: true,
            },
            images: img_res
        })
        }

        return {
            username,
            state, 
            loading,
            loading2,
            image, 
            pointCount, 
            points,
            img_res,
            image_url,
            mask_url,
            models,
            md0_urls,
            md1_urls,
            locations,
            loc_urls,
            canvas,
            maskCanvas,
            resCanvas,
            blacks,
            reds,
            gender,
            msk_type,
            onFileChange,
            drawPoint,
            resetPoints,
            sam,
            select_mask,
            showViewer,
            checkedIndices,
            handleCheckboxChange,
            radio_m,
            radio_l,
            extractedLora,
            generate,
            closePanel,
            set_init,
            res_url,
            handleChange,
            options
        };
    }
}
</script>


<style>
.container {
    display: flex;
    align-items: flex-start;
    justify-content: center; /* vertically align the container */
    flex-direction: column;
    width: 60%; /* or whatever width you prefer */
    margin-left: 410px; /* horizontally center the container */
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

.res-canvas-container {
    width: 728px;
    height: 728px;
    border: 2px solid rgb(52, 92, 132); /* purple border */
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

.image-checkbox {
        display: block;
        margin: 5px auto;
}

.button-line {
        display: flex;
        justify-content: center; /* Horizontally center the buttons */
        gap: 10px; /* Add a gap between the buttons */
        margin-top: 5px;
}

.reset-button {
    margin-top: 5px;
    margin-right: 30px;
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

.sam-button {
    margin-top: 5px;
    margin-right: 330px;
    background-color: #466928;
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

.sam-button:hover {
    background-color: #466928;
}

.sam-button:active {
    transform: scale(0.95);
}

.sam-button:focus {
    box-shadow: 0 0 0 2px rgba(71, 255, 129, 0.5);
}

.sm-button {
    margin-top: 5px;
    background-color: #277071;
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

.sm-button:hover {
    background-color: #284e69;
}

.sm-button:active {
    transform: scale(0.95);
}

.sm-button:focus {
    box-shadow: 0 0 0 2px rgba(71, 197, 255, 0.5);
}

.gen-button {
    margin-top: 5px;
    background-color: #bac04b;
    border: none;
    border-radius: 25px;
    color: #ffffff;
    cursor: pointer;
    font-size: 28px;  /* Increase from 16px to 32px */
    padding: 17px 36px;  /* Increase from 10px 20px to 20px 40px */
    outline: none;
    transition: background-color 0.3s, transform 0.3s;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.gen-button:hover {
    background-color: #919d3e;
}

.gen-button:active {
    transform: scale(0.95);
}

.gen-button:focus {
    box-shadow: 0 0 0 2px #7d863d;
}

.el-radio__input.is-checked+.el-radio__label {
    color: #277b56;
}

.el-radio__input.is-checked .el-radio__inner {
    border-color: #69726e;
    background: #69726e5c;
}

.el-radio.el-radio--large .el-radio__label {
    font-size: 18px;
}

.selection-wrapper {
    display: flex; /* Use Flexbox */
    flex-wrap: wrap; /* If items exceed container width, they will wrap to the next line */
}

.selection-item {
    display: flex; /* Use Flexbox */
    align-items: center; /* Vertically align items in the center */
}
</style>

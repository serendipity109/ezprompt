<template>
    <div>
        <div>
            <nav-bar page="generate" :closePanel="closePanel" />
            <div class="container min-w-screen" style="margin-top: 8ch;">
                <div class="canvas-wrapper">
                    <div class="canvas-container flex items-center justify-center flex-col">
                        <div v-if="image === null" class="upload area  flex items-center justify-center flex-col">
                            <el-upload action="" :on-success="handleSuccess" :on-change="handlechange"
                                :before-upload="beforeUpload" name="rawfile">
                                <div>
                                    <el-icon :size="50">
                                        <Picture />
                                    </el-icon>
                                </div>
                                <div>
                                    <p class="edit header">Upload Image</p>
                                </div>
                            </el-upload>
                            <p class="edit content">Drag and drop file here or upload here</p>
                            <div class="text-xl" style="margin-bottom: 1ch;">（上傳尺寸需小於1024x1024）</div>
                        </div>
                        <canvas v-if="image" ref="canvas" @mousedown="drawPoint" @contextmenu.prevent></canvas>
                    </div>
                    <div class="canvas-container empty flex items-center justify-center flex-col">
                        <canvas v-if="blendurl" ref="blendCanvas"></canvas>
                        <div v-if="blendurl === null" class="flex items-center justify-center flex-col">
                            <el-icon :size="50">
                                <Avatar />
                            </el-icon>
                            <p class="edit header">Edit Area</p>
                            <p class="edit content">Click to edit areas in the original image that do not require any changes
                            </p>
                            <el-button class="edit-button" @click="edit_switch" :icon="EditPen">Edit</el-button>
                            <div v-if="edit">
                                <EditImg ref="editRef" :username="username" :filename="filename" @blend-url="handleblendUrl" />
                            </div>
                        </div>
                    </div>
                </div>
                <div class="button-line">
                    <button class="re-button" @click="reupload">Reupload</button>
                    <button class="re-button" @click="redit" style="margin-left: 41ch;">Redit</button>
                </div>
            </div>
        </div>
        <div class="model container min-w-screen" style="margin-top: 5ch;">
            <h2 style="font-size: 2em; margin-bottom: 1ch;">Model Selection</h2>
            <el-cascader placeholder="Gender Selection" :options="options" @change="handleChange" />
            <div v-if="gender === 0" class="selection-wrapper" style="margin-top: 3ch;">
                <div v-for="(model, index) in models" :key="index" class="selection-item">
                    <el-radio v-model="radio_m" :label="index.toString()" size="large">{{ model }}</el-radio>
                    <img :src="md0_urls[index]" style="width: 151px; height: 151px; margin-right: 5ch;">
                </div>
            </div>
            <div v-if="gender === 1" class="selection-wrapper" style="margin-top: 3ch;">
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
                <div v-loading="loading" element-loading-text="Loading..." class="res-canvas-container">
                    <canvas ref="resCanvas" v-on:click="showViewer([res_url])"></canvas>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue';
import { api as viewerApi } from 'v-viewer'
import axios from "axios";
import { ElMessage } from 'element-plus'
import NavBar from '@/components/NavBar.vue';
import EditImg from '@/components/EditImg.vue';
import {
    Avatar,
    Picture,
    EditPen
} from '@element-plus/icons-vue'

export default {
    components: {
        NavBar,
        EditImg
    },
    setup() {
        const state = reactive({
            image: null,
            pointCount: 0,
            points: [],
        });
        let img = ref(null);
        const filename = ref(null);
        const image = ref(null);
        const mask = ref(null);
        const image_url = ref(null);
        const mask_url = ref(null);
        const blendurl = ref(null);
        const canvas = ref(null);
        const blendCanvas = ref(null);
        const resCanvas = ref(null);
        const img_res = ref([]);
        const models = ref(["A", "B", "C", "D"]);
        const md0_urls = ref(["http://192.168.3.16:9527/media/mock/0_a.png", "http://192.168.3.16:9527/media/mock/0_b.png", "http://192.168.3.16:9527/media/mock/0_c.png", "http://192.168.3.16:9527/media/mock/0_d.png"])
        const md1_urls = ref(["http://192.168.3.16:9527/media/mock/1_a.png", "http://192.168.3.16:9527/media/mock/1_b.png", "http://192.168.3.16:9527/media/mock/1_c.png", "http://192.168.3.16:9527/media/mock/1_d.png"])
        const locations = ref(["beach", "street", "cafe"]);
        const loc_urls = ref(["https://ai-global-image.weshop.com/ad30c49b-0c28-458b-be06-4b1f73a10965.png_256x256.jpeg", "https://ai-global-image.weshop.com/20c29716-f083-41f1-8c26-db9df6f37135.png_256x256.jpeg", "https://ai-global-image.weshop.com/64207f3d-c144-4197-88b1-df6843359394.png_256x256.jpeg"]);
        const checkedIndices = ref([]);
        const loading = ref(false);
        const msk_type = ref(0);
        const gender = ref("0");
        const radio_m = ref("0");
        const radio_l = ref("0");
        const socket = ref(null);
        const LOC = ref("");
        const res_url = ref("");
        const closePanel = ref(true);
        const username = ref("");

        onMounted(() => {
            const sessionUser = sessionStorage.getItem('vuex'); // 'vuex' 是默认的键名
            if (sessionUser) {
                const parsedUser = JSON.parse(sessionUser);
                username.value = parsedUser.user;
            }
        });

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


        const set_init = async () => {
            closePanel.value = !closePanel.value;
        }

        const handlechange = async (file) => {
            const reader = new FileReader();
            reader.onload = async (e) => {
                image.value = new Image();
                image.value.onload = () => {
                    drawImageToCanvas(image.value, canvas, 512);
                };
                image.value.src = e.target.result;

                // 發送POST請求
                const formData = new FormData();
                formData.append('rawfile', file.raw);
                filename.value = file.raw.name;
                try {
                    const response = await axios.post(`http://192.168.3.20:9527/upload?user_id=${username.value}`, formData, {
                        headers: {
                            'accept': 'application/json',
                            'Content-Type': 'multipart/form-data'
                        }
                    });
                    console.log(response.data);
                    // 若需要，你可以在此處處理response
                } catch (error) {
                    console.error("上傳圖片時出錯:", error);
                }
            }
            reader.readAsDataURL(file.raw);
            checkedIndices.value = [];
        };

        const handleSuccess = (response) => {
            console.log(response);
            image_url.value = response.data.data;
        };

        const beforeUpload = (file) => {
            const formData = new FormData();
            formData.append('rawfile', file.raw, 'image.png');  // Assuming the name of the file should be 'image.png'
            return formData;
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

        const edit = ref(false);
        const editRef = ref(null);
        const edit_switch = () => {
            console.log(edit.value);
            edit.value = true;
            if (editRef.value) {
                editRef.value.dialog_switch(filename);
            }
        };

        const handleblendUrl = (url) => {
            blendurl.value = url;
            const blendImage = new Image();
            blendImage.onload = () => {
                drawImageToCanvas(blendImage, blendCanvas, 512);
            };
            blendImage.src = url;
            edit.value = false;
            console.log(edit.value);
        };

        const reupload = () => {
            image.value = null
        };

        const redit = () => {
            blendurl.value = null;
            edit.value = false;
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
            if (checkedIndices.value.length === 0) {
                ElMessage.error("Please select mask.")
                return
            }
            loading.value = true;
            if (socket.value && socket.value.readyState !== WebSocket.CLOSED) {
                socket.value.close();
            }
            socket.value = new WebSocket("ws://192.168.3.20:9527/img2img");
            let message;

            switch (radio_l.value) {
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
                    "prompt": `best quality, masterpiece, (photorealistic:1.4), depth of field, ${LOC.value}`,
                    "nprompt": "(worst quality:2), (low quality:2), (normal quality:2), lowres,watermark, monochrome",
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
                    loading.value = false;
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
            filename,
            state,
            loading,
            Avatar,
            Picture,
            EditPen,
            image,
            img_res,
            image_url,
            mask_url,
            blendurl,
            edit,
            editRef,
            edit_switch,
            models,
            md0_urls,
            md1_urls,
            locations,
            loc_urls,
            canvas,
            blendCanvas,
            resCanvas,
            gender,
            msk_type,
            handlechange,
            handleSuccess,
            beforeUpload,
            reupload,
            redit,
            handleblendUrl,
            showViewer,
            checkedIndices,
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


<style scoped>
.container {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    /* vertically align the container */
    flex-direction: column;
    width: 60%;
    /* or whatever width you prefer */
    margin-left: 410px;
    /* horizontally center the container */
}

.canvas-wrapper {
    display: flex;
    align-items: center;
    margin-bottom: 5px;
    /* space below the canvas-wrapper */
}

.canvas-container {
    width: 512px;
    height: 512px;
    border: 2px solid purple;
    /* purple border */
    overflow: hidden;
    position: relative;
    box-sizing: border-box;
    /* ensure the border doesn't increase the container size */
    margin-right: 5px;
    /* add margin to the right */
    flex-wrap: wrap;
}

.res-canvas-container {
    width: 728px;
    height: 728px;
    border: 2px solid rgb(52, 92, 132);
    /* purple border */
    overflow: hidden;
    position: relative;
    box-sizing: border-box;
    /* ensure the border doesn't increase the container size */
    margin-right: 5px;
    /* add margin to the right */
}

canvas {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 508px;
    /* reduce by 2px * 2 due to border */
    height: 508px;
    /* reduce by 2px * 2 due to border */
}

.canvas-container.empty {
    border: 2px dashed purple;
    /* dashed border for the empty container */
    margin-right: 0;
    /* remove margin from the empty container */
}

.edit.header {
    font-size: 24px;
    text-align: center;
}

.edit.content {
    font-size: 20px;
    text-align: center;
}

.edit-button {
    margin-top: 50px;
    background-color: #141515;
    border: none;
    border-radius: 25px;
    color: #ffffff;
    cursor: pointer;
    font-size: 28px;
    /* Increase from 16px to 32px */
    padding: 20px 30px;
    outline: none;
    transition: background-color 0.3s, transform 0.3s;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}


.button-line {
    display: flex;
    justify-content: center;
    /* Horizontally center the buttons */
    gap: 10px;
    /* Add a gap between the buttons */
    margin-top: 5px;
}

.re-button {
    margin-top: 5px;
    margin-right: 30px;
    background-color: #120e0f;
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

.re-button:hover {
    background-color: #ff6b81;
}

.re-button:active {
    transform: scale(0.95);
}

.re-button:focus {
    box-shadow: 0 0 0 2px rgba(255, 71, 87, 0.5);
}

.gen-button {
    margin-top: 5px;
    background-color: #bac04b;
    border: none;
    border-radius: 25px;
    color: #ffffff;
    cursor: pointer;
    font-size: 28px;
    /* Increase from 16px to 32px */
    padding: 17px 36px;
    /* Increase from 10px 20px to 20px 40px */
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
    display: flex;
    /* Use Flexbox */
    flex-wrap: wrap;
    /* If items exceed container width, they will wrap to the next line */
}

.selection-item {
    display: flex;
    /* Use Flexbox */
    align-items: center;
    /* Vertically align items in the center */
}</style>

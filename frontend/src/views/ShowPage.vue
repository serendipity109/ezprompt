<template>
    <div>
        <nav-bar page="showcase" :closePanel="closePanel"/>
        <div
            class="min-h-screen absolute top-0 bottom-0 left-0 right-0 overflow-x-hidden flex flex-col bg-zinc-800 text-gray-100 text-sm">
            <div class="mb-[56px] sm:mb-0 sm:mt-[56px]">
                <div class="w-screen overflow-x-hidden flex flex-col bg-zinc-800 text-gray-100 text-sm" @click="set_init">
                    <div class="flex flex-col items-center py-4 mt-16">
                        <div class="font-semibold text-3xl text-gray-100">Community Showcase</div>
                        <div class="flex items-center w-1/3 max-w mt-8">
                            <div class="w-full">
                                <div class="w-full flex items-center relative"><svg stroke="currentColor" fill="none"
                                        stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"
                                        class="absolute left-4 pointer-events-none" height="1em" width="1em"
                                        xmlns="http://www.w3.org/2000/svg">
                                        <circle cx="11" cy="11" r="8"></circle>
                                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                                    </svg><input id="main-search" autoComplete="off" v-model="keyword" type="text"
                                        class="bg-zinc-700 flex-1 pl-12 pr-12 rounded-full text-sm px-4 py-2.5 focus:outline-none focus:ring-1 focus:ring-indigo-700"
                                        placeholder="Search your images" />
                                </div>
                            </div>
                        </div>
                        <div class="flex w-full max-w-[600px] md:ml-[48px] px-4 pl-5 md:px-5"></div>
                        <div class=" mb-8 flex flex-col items-center">
                            <div class="flex space-x-2">
                                <button v-if="username" @click="getHistory"
                                    class="w-32 sm:w-36 flex items-center text-xs justify-center text-center  h-9 rounded-full  hover:brightness-110 bg-opacity-0 shadow-sm  mt-4 bg-gradient-to-t from-indigo-900 via-indigo-900 to-indigo-800">Get
                                    History</button>
                                <button v-else @click="getImgs"
                                    class="w-32 sm:w-36 flex items-center text-xs justify-center text-center  h-9 rounded-full  hover:brightness-110 bg-opacity-0 shadow-sm  mt-4 bg-gradient-to-t from-indigo-900 via-indigo-900 to-indigo-800">Search</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div w-full mt-4 px-1 relative>
                    <div role="grid" v-if="flag == 1"
                        class="w-screen overflow-x-hidden flex flex-col bg-zinc-800 text-gray-100 text-sm" tabindex="0"
                        style="position: relative; width: 100%; max-width: 100%;">
                        <div class="image-row" v-for="(row, index) in imageRows" :key="index">
                        <div class="image-container" v-for="(image, index) in row" :key="index">
                            <router-link :to="'/image/' + image.id" :key="index"
                            class="block relative group select-none overflow-hidden m-0.5 border-indigo-600  rounded-xl"
                            style="transition: opacity 500ms ease 0s;">
                            <div
                                class="absolute inset-0 z-10 block text-zinc-100 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none line-clamp px-2 pb-2 text-sm px-2"
                                style="background: linear-gradient(0deg, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0.4) 40%, rgba(0, 0, 0, 0.1) 100%);">
                                <div class="flex-shrink h-full flex items-end">
                                <div class="flex flex-col">
                                    <p class="text-sm mb-1.5 font-medium leading-snug"
                                    style="overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;">
                                    {{ image.view1 }}</p>
                                    <p class="opacity-60 leading-snug text-sm"
                                    style="overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;">
                                    {{ image.view2 }}</p>
                                </div>
                                </div>
                            </div>
                            <div
                                class="top-2 left-0 absolute w-full flex z-10 text-zinc-100 justify-between opacity-0 group-hover:opacity-100 transition-opacity px-2 mb-1 text-sm">
                                <button
                                class=" bg-zinc-900 bg-opacity-50 hover:bg-opacity-100 transition-opacity flex items-center justify-center cursor-pointer text-lg h-10 w-10 rounded-lg">
                                <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round"
                                    stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                                    <circle cx="11" cy="11" r="8"></circle>
                                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                                </svg>
                                </button>
                                <div class="flex flex-col space-y-2">
                                <button
                                    class="  bg-zinc-900 bg-opacity-70 hover:bg-opacity-100 flex items-center justify-center cursor-pointer active:scale-90 transition-all  rounded-lg text-lg h-10 w-10">
                                    <div class="scale-50">
                                    <div class="heart brightness-110"></div>
                                    </div>
                                </button>
                                <button
                                    class="bg-zinc-900 bg-opacity-50 hover:bg-opacity-100 transition-opacity flex items-center justify-center cursor-pointer text-lg h-10 w-10 rounded-lg"><svg
                                    stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 512 512" height="1em"
                                    width="1em" xmlns="http://www.w3.org/2000/svg">
                                    <path
                                        d="M224 96l16-32 32-16-32-16-16-32-16 32-32 16 32 16 16 32zM80 160l26.66-53.33L160 80l-53.34-26.67L80 0 53.34 53.33 0 80l53.34 26.67L80 160zm352 128l-26.66 53.33L352 368l53.34 26.67L432 448l26.66-53.33L512 368l-53.34-26.67L432 288zm70.62-193.77L417.77 9.38C411.53 3.12 403.34 0 395.15 0c-8.19 0-16.38 3.12-22.63 9.38L9.38 372.52c-12.5 12.5-12.5 32.76 0 45.25l84.85 84.85c6.25 6.25 14.44 9.37 22.62 9.37 8.19 0 16.38-3.12 22.63-9.37l363.14-363.15c12.5-12.48 12.5-32.75 0-45.24zM359.45 203.46l-50.91-50.91 86.6-86.6 50.91 50.91-86.6 86.6z">
                                    </path>
                                    </svg></button>
                                </div>
                            </div>
                            <img v-bind:src="image.url" class="img-responsive" alt="Responsive Image">
                            </router-link>
                        </div>
                        </div>
                    </div>
                    <div role="grid" v-else-if="flag == 0"
                        class="w-screen overflow-x-hidden flex flex-col bg-zinc-800 text-gray-100 text-sm" tabindex="0"
                        style="position: relative; width: 100%; max-width: 100%;">
                        <div class="image-row" v-for="(row, index) in imageRows" :key="index">
                            <div class="image-container" v-for="(image, index) in row" :key="index">
                                <router-link :to="'/image/' + image.img" :key="index"
                                    class="block relative group select-none overflow-hidden m-0.5 border-indigo-600  rounded-xl"
                                    style="transition: opacity 500ms ease 0s;">
                                    <div class="absolute inset-0 z-10 block text-zinc-100 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none line-clamp px-2 pb-2 text-sm px-2"
                                        style="background: linear-gradient(0deg, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0.4) 40%, rgba(0, 0, 0, 0.1) 100%);">
                                        <div class="flex-shrink h-full flex items-end">
                                            <div class="flex flex-col">
                                                <p class="text-sm mb-1.5 font-medium leading-snug"
                                                    style="overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;">
                                                    {{ image.view1 }}</p>
                                                <p class="opacity-60 leading-snug text-sm"
                                                    style="overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;">
                                                    {{ image.view2 }}</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div
                                        class="top-2 left-0 absolute w-full flex z-10 text-zinc-100 justify-between opacity-0 group-hover:opacity-100 transition-opacity px-2 mb-1 text-sm">
                                        <button
                                            class=" bg-zinc-900 bg-opacity-50 hover:bg-opacity-100 transition-opacity flex items-center justify-center cursor-pointer text-lg h-10 w-10 rounded-lg">
                                            <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24"
                                                stroke-linecap="round" stroke-linejoin="round" height="1em" width="1em"
                                                xmlns="http://www.w3.org/2000/svg">
                                                <circle cx="11" cy="11" r="8"></circle>
                                                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                                            </svg>
                                        </button>
                                        <div class="flex flex-col space-y-2">
                                            <button
                                                class="  bg-zinc-900 bg-opacity-70 hover:bg-opacity-100 flex items-center justify-center cursor-pointer active:scale-90 transition-all  rounded-lg text-lg h-10 w-10">
                                                <div class="scale-50">
                                                    <div class="heart brightness-110"></div>
                                                </div>
                                            </button>
                                            <button
                                                class="bg-zinc-900 bg-opacity-50 hover:bg-opacity-100 transition-opacity flex items-center justify-center cursor-pointer text-lg h-10 w-10 rounded-lg"><svg
                                                    stroke="currentColor" fill="currentColor" stroke-width="0"
                                                    viewBox="0 0 512 512" height="1em" width="1em"
                                                    xmlns="http://www.w3.org/2000/svg">
                                                    <path
                                                        d="M224 96l16-32 32-16-32-16-16-32-16 32-32 16 32 16 16 32zM80 160l26.66-53.33L160 80l-53.34-26.67L80 0 53.34 53.33 0 80l53.34 26.67L80 160zm352 128l-26.66 53.33L352 368l53.34 26.67L432 448l26.66-53.33L512 368l-53.34-26.67L432 288zm70.62-193.77L417.77 9.38C411.53 3.12 403.34 0 395.15 0c-8.19 0-16.38 3.12-22.63 9.38L9.38 372.52c-12.5 12.5-12.5 32.76 0 45.25l84.85 84.85c6.25 6.25 14.44 9.37 22.62 9.37 8.19 0 16.38-3.12 22.63-9.37l363.14-363.15c12.5-12.48 12.5-32.75 0-45.24zM359.45 203.46l-50.91-50.91 86.6-86.6 50.91 50.91-86.6 86.6z">
                                                    </path>
                                                </svg></button>
                                        </div>
                                    </div>
                                    <img v-bind:src="image.url" class="img-responsive" alt="Responsive Image">
                                </router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
    
<script>
import axios from "axios";
import { defineComponent, ref, onUnmounted, computed } from 'vue'
import 'viewerjs/dist/viewer.css'
import { api as viewerApi } from 'v-viewer'
import NavBar from '@/components/NavBar.vue';
import fileDownload from 'js-file-download';
import { GET_EMAIL } from "@/store/storeconstants";
import { GET_USERNAME } from "@/store/storeconstants";
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

export default defineComponent({
    components: {
        NavBar
    },
    setup() {
        const keyword = ref('');
        const images = ref([]);
        const imageRows = ref([]);
        const datas = ref([]);
        const urls = ref([]);
        const flag = ref(0);
        const showProgress = ref(false);
        const percentage = ref(0);
        const showStyle = ref(false);
        const radio = ref(null);
        const selectedImage = ref({row: -1, col: -1});
        const store = useStore()
        const closePanel = ref(true);
        const router = useRouter()
        let intervalId;

        const username = computed(() => {
            let userName = store.getters[`auth/${GET_USERNAME}`]
            return userName;
        });

        const getHistory = async () => {
            flag.value = 1;
            const response = await axios.get(`http://${process.env.VUE_APP_BACKEND_IP}/history?user_id=${username.value}`);
            if (response.data.code === 200){
                images.value = response.data.data;
                imageRows.value = chunkArray(images.value, 4);
            } else {
                ElMessage.error({showClose: true, message: "User has no record."});
            }
        };

        const getImgs = async () => {
            flag.value = 0;
            const response = await axios.get(`http://${process.env.VUE_APP_BACKEND_IP}/get_images`);
            images.value = response.data;
            console.log(response.data);
            imageRows.value = chunkArray(images.value, 5);
        };

        const chunkArray = (array, size) => {
            const chunkedArray = [];
            for (let i = 0; i < array.length; i += size) {
                chunkedArray.push(array.slice(i, i + size));
            }
            return chunkedArray;
        };

        const showViewer = (urls, index) => {
            viewerApi({
                options: {
                    toolbar: true,
                    initialViewIndex: index
                },
                images: urls,
            });
        };

        const downloadFile = async (urls, index) => {
            let url = urls[index];
            let fileName = url.split('/').pop().split('?')[0];
            await axios.get(url, {
                responseType: 'blob',
            }).then(res => {
                fileDownload(res.data, fileName);
            });
        }

        const email = computed(() => {
            let Email = store.getters[`auth/${GET_EMAIL}`]
            const parts = Email.split('@');
            return parts[0];
        });

        const set_init = async () => {
            closePanel.value = !closePanel.value;
        }

        const goToPage = (pagnition) => {
            router.push(pagnition)
        }

        onUnmounted(() => {
            clearInterval(intervalId);
        });

        return {
            keyword,
            images,
            imageRows,
            datas,
            urls,
            showProgress,
            username,
            flag,
            getHistory,
            getImgs,
            chunkArray,
            showViewer,
            percentage,
            showStyle,
            radio,
            selectedImage,
            downloadFile,
            email,
            closePanel,
            set_init,
            goToPage
        };
    },
});
</script>
  
<style>
.image-gallery {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
}

.image-row {
    display: flex;
    justify-content: center;
    align-items: center;
    padding-bottom: 30px;
}

.image-container {
    margin-top: 0px;
    flex: 1;
    max-width: 20%;
    text-align: center;
}

.img-responsive {
    max-width: 100%;
    height: auto;
}

.selected-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.overlay-button {
    margin: 5px;
}

.overlay-button:hover {
    color: rgb(100, 69, 130);
}

.selected-container.selected {
    padding: 3px;
    background-color: rgb(89, 62, 157);
}

.image-overlay {
    display: flex;
    justify-content: space-around;
    width: 100%;
    height: 0;
    overflow: visible;
}

.el-progress-bar__innerText {
    color: black;
}

.el-progress--line {
    width: 500px;
    margin: 0 auto;
    display: off;
}

.el-radio__input.is-checked .el-radio__inner {
    border-color: #a153e6;
    background: #a153e6;
}

.el-radio__input.is-checked+.el-radio__label {
    color: #a153e6;
}

.el-radio__inner {
    background-color: #ffffff12;
}

.el-radio__label {
    color: #ffffff6e;
}

.radioRow {
    display: flex;
    justify-content: center;
}</style>
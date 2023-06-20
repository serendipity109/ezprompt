<template>
  <div>
    <nav-bar page="home" />
    <div
      class="min-h-screen absolute top-0 bottom-0 left-0 right-0 overflow-x-hidden flex flex-col bg-zinc-800 text-gray-100 text-sm">
      <div class="mb-[56px] sm:mb-0 sm:mt-[56px]">
        <div class="w-screen overflow-x-hidden flex flex-col bg-zinc-800 text-gray-100 text-sm">
          <div class="flex flex-col items-center py-4 mt-16"><a class="font-semibold text-3xl text-gray-100"
              href="/">EZPrompt</a>
            <div class="flex items-center w-full max-w-[600px] md:ml-[48px] mt-8 px-4 pl-5 md:px-5">
              <div class="w-full">
                <div class="w-full flex items-center relative"><svg stroke="currentColor" fill="none" stroke-width="2"
                    viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"
                    class="absolute left-4 pointer-events-none" height="1em" width="1em"
                    xmlns="http://www.w3.org/2000/svg">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                  </svg><input id="main-search" autoComplete="off" v-model="keyword" type="text"
                    class="bg-zinc-700 flex-1 pl-12 pr-12 rounded-full text-sm px-4 py-2.5 focus:outline-none focus:ring-1 focus:ring-indigo-700"
                    placeholder="Give me an EZprompt" />
                  <button
                    class="text-base absolute right-2 hover:bg-zinc-800 h-8 w-8 flex items-center justify-center rounded-full"
                    data-state="closed">
                    <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round"
                      stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                      <circle cx="8.5" cy="8.5" r="1.5"></circle>
                      <polyline points="21 15 16 10 5 21"></polyline>
                    </svg></button>
                </div>
              </div>
              <div class="flex justify-center"><button @click="styleSwitch"
                  class="ml-2 h-10 w-10 rounded-full cursor-pointer flex items-center justify-center  bg-transparent hover:bg-zinc-900"><svg
                    stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round"
                    stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                    <line x1="4" y1="21" x2="4" y2="14"></line>
                    <line x1="4" y1="10" x2="4" y2="3"></line>
                    <line x1="12" y1="21" x2="12" y2="12"></line>
                    <line x1="12" y1="8" x2="12" y2="3"></line>
                    <line x1="20" y1="21" x2="20" y2="16"></line>
                    <line x1="20" y1="12" x2="20" y2="3"></line>
                    <line x1="1" y1="14" x2="7" y2="14"></line>
                    <line x1="9" y1="8" x2="15" y2="8"></line>
                    <line x1="17" y1="16" x2="23" y2="16"></line>
                  </svg></button></div>
            </div>
            <div class="flex w-full max-w-[600px] md:ml-[48px] px-4 pl-5 md:px-5"></div>
            <div v-if="showStyle">
              <div class=" mt-2 flex flex-col items-center">Style Selection</div>
              <div class=" radioRow">
                <el-radio v-model="radio" label="1">漫畫</el-radio>
                <el-radio v-model="radio" label="2">電影</el-radio>
                <el-radio v-model="radio" label="3">水墨畫</el-radio>
              </div>
              <div class=" radioRow">
                <el-radio v-model="radio" label="4">油畫</el-radio>
                <el-radio v-model="radio" label="5">水彩畫</el-radio>
                <el-radio v-model="radio" label="6">鉛筆畫</el-radio>
                <el-radio v-model="radio" label="7">寫實</el-radio>
              </div>
            </div>
            <div class=" mb-8 flex flex-col items-center">
              <div class="flex space-x-2">
                <button @click="ezprompt"
                  class="w-32 sm:w-36 flex items-center text-xs justify-center text-center  h-9 rounded-full  hover:brightness-110 bg-opacity-0 shadow-sm  mt-4 bg-gradient-to-t from-indigo-900 via-indigo-900 to-indigo-800">Generate</button>
                <button @click="getImgs"
                  class="w-32 sm:w-36 flex items-center text-xs justify-center text-center  h-9 rounded-full  hover:brightness-110 bg-opacity-0 shadow-sm  mt-4 border border-gray-700 hover:bg-zinc-700">Search</button>
              </div>
            </div>
            <el-progress v-if="showProgress" :text-inside="true" :stroke-width="20" :percentage="percentage"
              :color="'#5f00ff'" />
          </div>
        </div>
        <div w-full mt-4 px-1 relative>
          <div role="grid" v-if="flag == 1"
            class="w-screen overflow-x-hidden flex flex-col bg-zinc-800 text-gray-100 text-sm" tabindex="0"
            style="position: relative; width: 100%; max-width: 100%;">
            <div class="image-row" v-for="(row, index) in imageRows" :key="index">
              <div class="image-container" v-for="(image, index) in row" :key="index">
                <router-link :to="'/image/' + image.img" :key="index"
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
            style="position: relative; width: 100%; max-width: 100%; ">
            <div class="image-row">
              <div class="image-container" v-for="(url, index) in urls" :key="index"
                :style="{ 'margin-right': index < urls.length - 1 ? '10px' : '0' }" @click="selectedImage = index">
                <div :class="{ 'selected-container': true, 'selected': selectedImage === index }">
                  <img :src="url" style="object-fit: contain; height: 100%; max-height: 50vh"
                    :class="{ 'selected': selectedImage === index }" />
                  <div v-if="selectedImage === index" class="image-overlay">
                    <button class="overlay-button">Share</button>
                    <button class="overlay-button" v-on:click="showViewer(urls, index)">Preview</button>
                    <button class="overlay-button" v-on:click="upscale(urls, index)">Upscale</button>
                  </div>
                </div>
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
import { defineComponent, ref, onMounted, onUnmounted } from 'vue'
import 'viewerjs/dist/viewer.css'
import { api as viewerApi } from 'v-viewer'
import NavBar from '@/components/NavBar.vue';

export default defineComponent({
  components: {
    NavBar
  },
  setup() {
    const message = ref('');
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
    const selectedImage = ref(null);
    const type = ref(null);
    const socket = ref(null);
    let intervalId;

    onMounted(async () => {
      const response = await fetch('http://192.168.3.16:9527/');
      const data = await response.json();
      message.value = data.Model;
    });

    const getImgs = async () => {
      flag.value = 1;
      const response = await axios.get('http://192.168.3.16:9527/get_images');
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

    const ezprompt = async () => {
      flag.value = 0;
      urls.value = [];
      showProgress.value = true;
      percentage.value = 0;

      if (radio.value === '1') {
        type.value = '漫畫';
      } else if (radio.value == '2') {
        type.value = '電影';
      } else if (radio.value == '3') {
        type.value = '水墨畫';
      } else if (radio.value == '4') {
        type.value = '油畫';
      } else if (radio.value == '5') {
        type.value = '水彩畫';
      } else if (radio.value == '6') {
        type.value = '鉛筆畫';
      } else if (radio.value == '7') {
        type.value = '寫實';
      }

      socket.value = new WebSocket("ws://192.168.3.16:9527/dcmj/imagine");

      socket.value.onopen = () => {
        console.log("Connection opened");
        // 在连接打开后发送消息
        const message = {
          "user_id": "adam",
          "prompt": keyword.value,
          ...(type.value ? { "preset": type.value } : {})
        };
        socket.value.send(JSON.stringify(message));
      };

      socket.value.onmessage = (event) => {
        console.log("Received message: ", event.data);
        const data = JSON.parse(event.data);
        if (data.result && data.result.progress) {
          percentage.value = parseInt(data.result.progress);
        }
        if (data.code === 201 && data.data && Array.isArray(data.data.result)) {
          // 如果 code 是 201，输出 result 列表
          data.data.result.slice(1).forEach((item) => {
            urls.value.push(item);
          });
        }
      };

      socket.value.onerror = (error) => {
        console.error("Error occurred: ", error);
        showProgress.value = false;
      };

      socket.value.onclose = () => {
        console.log("Connection closed");
        showProgress.value = false;
      };
    };

    const upscale = async (urls, index) => {
      let url = urls[index];
      let fileName = url.split('/').pop().split('?')[0];
      let filePath = './output/' + fileName;
      showProgress.value = true;
      percentage.value = 0;
      // eslint-disable-next-line no-unused-vars
      const [_, response] = await Promise.all([
        startIncreasing(),
        await axios.post(`http://192.168.3.16:9527/upscale?file_path=${encodeURIComponent(filePath)}`, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
        })
      ]);
      percentage.value = 100;
      showProgress.value = false;
      console.log(response.data);
      urls[index] = response.data.data[0].result;
      showViewer(urls, index);
    }

    const increasePercentage = async () => {
      if (percentage.value + 5 > 95) {
        percentage.value = 95;
      } else {
        percentage.value += 5;
      }
    };

    const startIncreasing = () => {
      if (!intervalId) {
        intervalId = setInterval(increasePercentage, 1000);
      }
    };

    onUnmounted(() => {
      clearInterval(intervalId);
    });

    function styleSwitch() {
      this.showStyle = !this.showStyle
    }

    return {
      message,
      keyword,
      images,
      imageRows,
      datas,
      urls,
      flag,
      showProgress,
      getImgs,
      chunkArray,
      ezprompt,
      showViewer,
      percentage,
      startIncreasing,
      styleSwitch,
      showStyle,
      radio,
      selectedImage,
      upscale
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

;

.el-radio__label {
  color: #ffffff6e;
}

.radioRow {
  display: flex;
  justify-content: center;
}
</style>
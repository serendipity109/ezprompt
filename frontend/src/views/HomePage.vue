<template>
  <div>
    <nav-bar page="home" :closePanel="closePanel"/>
    <div
      class="min-h-screen absolute top-0 bottom-0 left-0 right-0 overflow-x-hidden flex flex-col bg-zinc-800 text-gray-100 text-sm">
      <div class="mb-[56px] sm:mb-0 sm:mt-[56px]">
        <div class="w-screen overflow-x-hidden flex flex-col bg-zinc-800 text-gray-100 text-sm" @click="set_init">
          <div class="flex flex-col items-center py-4 mt-16">
            <div class="font-semibold text-3xl text-gray-100">EZPrompt</div>
            <div class="flex items-center w-full max-w-[600px] mt-8 px-4 pl-5">
              <div class="w-full">
                <div class="w-full flex items-center relative"><svg stroke="currentColor" fill="none" stroke-width="2"
                    viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"
                    class="absolute left-4 pointer-events-none" height="1em" width="1em"
                    xmlns="http://www.w3.org/2000/svg">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                  </svg><input id="main-search" autoComplete="off" v-model="keyword" type="text"
                    class="bg-zinc-700 flex-1 pl-12 pr-12 rounded-full text-sm px-4 py-2.5 focus:outline-none focus:ring-1 focus:ring-indigo-700"
                    placeholder="Give me an EZPrompt" />
                  <upload @fileUpload="handleUrl"
                    class="text-base absolute right-2 hover:bg-zinc-800 h-8 w-8 flex items-center justify-center rounded-full"
                    data-state="closed" />
                </div>
              </div>
            </div>
            <div class="flex flex-col w-full max-w-[300px] items-center mt-4">
              <div class="flex items-center mt-4 mb-4">
                <el-button @click="featureSelect(1)" color="#673794">Style</el-button>
                <el-button @click="featureSelect(2)" color="#66ba81">Size</el-button>
              </div>
              <div v-show="feature == 1">
                <div class=" radioRow">
                  <el-radio v-model="radio" label="0">None</el-radio>
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
              <div v-show="feature == 2" class="w-full">
                <v-slider :ticks="dimLabels" :max="2" step="1" tick-size="3" v-model="dimValue" hide-details></v-slider>
                <input style="display:none" value="4" />
                <div class="flex justify-between w-full  select-none mt-1 text-base">
                  <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16" class="opacity-40"
                    height="1em" width="1em" xmlns="http://www.w3.org/2000/svg" style="transform: scale(1.5);">
                    <path fill-rule="evenodd"
                      d="M14.5 3h-13a.5.5 0 00-.5.5v9a.5.5 0 00.5.5h13a.5.5 0 00.5-.5v-9a.5.5 0 00-.5-.5zm-13-1A1.5 1.5 0 000 3.5v9A1.5 1.5 0 001.5 14h13a1.5 1.5 0 001.5-1.5v-9A1.5 1.5 0 0014.5 2h-13z"
                      clip-rule="evenodd"></path>
                    <path
                      d="M10.648 7.646a.5.5 0 01.577-.093L15.002 9.5V13h-14v-1l2.646-2.354a.5.5 0 01.63-.062l2.66 1.773 3.71-3.71z">
                    </path>
                    <path fill-rule="evenodd" d="M4.502 7a1.5 1.5 0 100-3 1.5 1.5 0 000 3z" clip-rule="evenodd"></path>
                  </svg>
                  <div class="text-s flex items-center transition-all text-zinc-200" style="opacity:1">{{
                    dimLabels[dimValue] }}</div>
                  <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16" class="opacity-40"
                    height="1em" width="1em" xmlns="http://www.w3.org/2000/svg" style="transform: scale(1.5);">
                    <path d="M8.002 5.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z">
                    </path>
                    <path
                      d="M12 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2zM3 2a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v8l-2.083-2.083a.5.5 0 0 0-.76.063L8 11 5.835 9.7a.5.5 0 0 0-.611.076L3 12V2z">
                    </path>
                  </svg>
                </div>
              </div>
            </div>
            <div class="flex flex-col items-center mt-2 mb-8">
              <div class="flex space-x-2">
                <button @click="ezprompt"
                  class="w-32 sm:w-36 flex items-center text-xs justify-center text-center  h-9 rounded-full  hover:brightness-110 bg-opacity-0 shadow-sm  mt-4 bg-gradient-to-t from-indigo-900 via-indigo-900 to-indigo-800">Generate</button>
                <button @click="getImgs"
                  class="w-32 sm:w-36 flex items-center text-xs justify-center text-center  h-9 rounded-full  hover:brightness-110 bg-opacity-0 shadow-sm  mt-4 border border-gray-700 hover:bg-zinc-700">Search</button>
                <button @click="img2img"
                  class="w-32 sm:w-36 flex items-center text-xs justify-center text-center h-9 rounded-full hover:brightness-110 bg-green-700 shadow-sm mt-4 border border-gray-700">img2img</button>
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
                    <button class="overlay-button" v-on:click="downloadFile(urls, index)">Download</button>
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
import Upload from '@/components/UploadImg.vue';
import fileDownload from 'js-file-download';
import { ElMessage } from 'element-plus'
import { useRoute, useRouter } from 'vue-router';
import { getCredits } from '@/utils/account.js';
import { styleSelect } from '@/utils/param.js';

export default defineComponent({
  components: {
    NavBar,
    Upload
  },
  setup() {
    const token = ref('');
    const user_id = ref('');
    const email = ref('');
    const auth = ref('');
    const keyword = ref('');
    const images = ref([]);
    const imageRows = ref([]);
    const datas = ref([]);
    const urls = ref([]);
    const flag = ref(0);
    const showProgress = ref(false);
    const percentage = ref(0);
    const radio = ref("0");
    const selectedImage = ref(null);
    const type = ref(null);
    const socket = ref(null);
    const route = useRoute();
    const router = useRouter();
    const feature = ref(0);
    const dimValue = ref(1);
    const dimLabels = {
      0: '1456 x 816',
      1: '1024 x 1024',
      2: '816 x 1456',
    };
    const sizeLabels = {
      0: "16:9",
      1: "1:1",
      2: "9:16",
    };
    let create_account_token = route.query.token;
    let intervalId;

    const getImgs = async () => {
      flag.value = 1;
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

    const ezprompt = async (image_url = '') => {
      // token = store.getters[`auth/${GET_TOKEN}`]
      if (token.value == "") {
        ElMessage.error({ showClose: true, message: "Please log in." })
        return
      }
      const credits = await getCredits(token.value)
      if (credits < 4) {
        ElMessage.error({ showClose: true, message: "Credits not enough!" })
        return
      }
      if (!keyword.value) {
        ElMessage.error({ showClose: true, message: "Prompt is empty!" })
        return
      }
      flag.value = 0;
      if (urls.value && urls.value.length > 0) {
        urls.value = [];
      }
      showProgress.value = true;
      percentage.value = 0;
      await styleSelect(radio, type)
      console.log(type.value)
      if (socket.value && socket.value.readyState !== WebSocket.CLOSED) {
        socket.value.close();
      }
      socket.value = new WebSocket(`ws://${process.env.VUE_APP_BACKEND_IP}/dcmj/imagine`);
      let message;
      socket.value.onopen = () => {
        message = {
          "user_id": user_id.value,
          "prompt": keyword.value,
          "size": sizeLabels[dimValue.value],
          "mode": "relax",
          ...(typeof image_url === 'string' && image_url !== '' ? { "image_url": image_url } : {}),
          ...(type.value ? { "preset": type.value } : {})
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
    }

    const downloadFile = async (urls, index) => {
      let url = urls[index];
      let fileName = url.split('/').pop().split('?')[0];
      await axios.get(url, {
        responseType: 'blob',
      }).then(res => {
        fileDownload(res.data, fileName);
      });
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

    const handleUrl = (emittedUrl) => {
      flag.value = 0;
      urls.value.push(emittedUrl)
    };

    const img2img = async () => {
      if (keyword.value && urls.value[selectedImage.value]) {
        let image_url = urls.value[selectedImage.value];
        image_url = image_url.replace("192.168.3.16:9527", "61.216.75.236:9528");
        await ezprompt(image_url);
        selectedImage.value = null;
      } else {
        console.error("Selected image is not available in urls.value");
        ElMessage.error({ showClose: true, message: "Image not selected or prompt is empty!" })
      }
    };

    const featureSelect = (type) => {
      feature.value = type;
    }

    const closePanel = ref(true);

    const set_init = async () => {
      closePanel.value = !closePanel.value;
    }

    onMounted(async () => {
      const sessionUser = sessionStorage.getItem('vuex'); // 'vuex' 是默认的键名
          if (sessionUser) {
              const parsedUser = JSON.parse(sessionUser);
              token.value = parsedUser.token;
              user_id.value = parsedUser.user;
              email.value = parsedUser.email;
              auth.value = parsedUser.auth;
          }
      if (create_account_token) {
        const user_res = await axios.post(`http://${process.env.VUE_APP_BACKEND_IP}/user/decode?token=${create_account_token}`)
        const user = user_res.data.user_id
        const pwd = user_res.data.password
        axios.post(`http://${process.env.VUE_APP_BACKEND_IP}/user/create?username=${user}&password=${pwd}`)
          .then(function (response) {
            if (response.data.code === 200) {
              const uid = response.data.data;
              ElMessage.info({
                showClose: true,
                message: `Successfully create account ${uid}`,
                duration: 5000
              });
              ElMessage.info({
                showClose: true,
                message: `Please login.`,
                duration: 5000
              });
            } else if (response.data.code === 400) {
              ElMessage.error({
                showClose: true,
                message: response.data.message,
                duration: 5000
              });
            }
          })
        router.push('/home');
      }
    })

    onUnmounted(() => {
      clearInterval(intervalId);
    });

    return {
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
      feature,
      featureSelect,
      radio,
      selectedImage,
      downloadFile,
      handleUrl,
      img2img,
      closePanel,
      set_init,
      email,
      sizeLabels,
      dimValue,
      dimLabels
    };
  },
});
</script>

<style scoped>
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

.parent :deep(.el-progress-bar__innerText) {
  color: #000;
}

.parent :deep(.el-progress--line) {
  width: 500px;
  margin: 0 auto;
  display: off;
}

.parent :deep(.el-radio__input.is-checked .el-radio__inner) {
  border-color: #a153e6;
  background: #a153e6;
}

.parent :deep(.el-radio__input.is-checked+.el-radio__label) {
  color: #a153e6;
}

.parent :deep(.el-radio__inner) {
  background-color: #ffffff12;
}.parent :deep(.el-radio__label) {
  color: #ffffff6e;
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

.radioRow {
  display: flex;
  justify-content: center;
}
</style>
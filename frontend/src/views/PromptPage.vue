<template>
  <div>
    <nav-bar page="" />
    <div
      class="min-h-screen absolute top-0 bottom-0 left-0 right-0 overflow-x-hidden flex flex-col bg-zinc-800 text-gray-100 text-sm">
      <div class="mb-[56px] sm:mb-0 sm:mt-[56px]">
        <div class="flex w-full h-full self-stretch flex-col md:flex-row pb-0 md:pb-0 md:pt-0 flex-1 ">
          <div class="w-full flex-shrink-0 overflow-hidden text-base px-5 flex flex-col h-auto "
            style="height:fit-content;width:400px">
            <div class="mt-6 px-4 py-3 bg-zinc-700 rounded-xl shadow bg-opacity-50 font-light flex flex-col space-y-5">
              <p><a class="bg-red-500 bg-opacity-0 rounded hover:bg-opacity-40 cursor-pointer " href="/?q=man">{{ pmt
              }}</a></p>
              <div class="flex text-xs font-light">
                <div class="flex flex-1 flex-row space-x-2 mr-2">
                  <div
                    class="text-xs rounded-md sm:text-xs active:scale-95 transition-all transform-gpu whitespace-nowrap flex-1 flex select-none cursor-pointer hover:bg-zinc-600 border border-zinc-600 bg-zinc-700 items-center justify-center  shadow px-2.5 py-2 w-fit-content">
                    <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round"
                      stroke-linejoin="round" class="text-sm mr-2" height="1em" width="1em"
                      xmlns="http://www.w3.org/2000/svg">
                      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    </svg>Copy prompt
                  </div>
                  <div
                    class="text-xs rounded-md sm:text-xs active:scale-95 transition-all transform-gpu whitespace-nowrap flex-1 flex select-none cursor-pointer hover:bg-zinc-600 border border-zinc-600 bg-zinc-700 items-center justify-center  shadow px-2.5 py-2 w-fit-content">
                    <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round"
                      stroke-linejoin="round" class="text-sm mr-2" height="1em" width="1em"
                      xmlns="http://www.w3.org/2000/svg">
                      <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
                      <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
                    </svg>Copy URL
                  </div>
                </div>
              </div>
            </div>
            <div class="flex space-x-2 px-2">
              <div
                class="text-xs rounded-md sm:text-sm group mt-4 whitespace-nowrap flex-1 flex select-none cursor-pointer hover:brightness-110 bg-gradient-to-t from-indigo-900 via-indigo-900 to-indigo-800 drop-shadow items-center justify-center px-2.5 py-2.5 w-fit-content active:scale-95 transition-all">
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 512 512"
                  class="mr-2 text-base transition-all w-3 h-3" height="1em" width="1em"
                  xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M224 96l16-32 32-16-32-16-16-32-16 32-32 16 32 16 16 32zM80 160l26.66-53.33L160 80l-53.34-26.67L80 0 53.34 53.33 0 80l53.34 26.67L80 160zm352 128l-26.66 53.33L352 368l53.34 26.67L432 448l26.66-53.33L512 368l-53.34-26.67L432 288zm70.62-193.77L417.77 9.38C411.53 3.12 403.34 0 395.15 0c-8.19 0-16.38 3.12-22.63 9.38L9.38 372.52c-12.5 12.5-12.5 32.76 0 45.25l84.85 84.85c6.25 6.25 14.44 9.37 22.62 9.37 8.19 0 16.38-3.12 22.63-9.37l363.14-363.15c12.5-12.48 12.5-32.75 0-45.24zM359.45 203.46l-50.91-50.91 86.6-86.6 50.91 50.91-86.6 86.6z">
                  </path>
                </svg>Open in editor
              </div>
              <div
                class="text-xs rounded-md sm:text-sm group mt-4 whitespace-nowrap flex-1 flex select-none cursor-pointer hover:brightness-110 bg-gradient-to-t  from-zinc-700 via-zinc-700 to-zinc-700 drop-shadow items-center justify-center px-2.5 py-2 w-fit-content">
                Explore this style<svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24"
                  stroke-linecap="round" stroke-linejoin="round"
                  class="ml-2 text-base group-hover:translate-x-1 transition-all" height="1em" width="1em"
                  xmlns="http://www.w3.org/2000/svg">
                  <polyline points="9 18 15 12 9 6"></polyline>
                </svg></div>
            </div>
            <div v-if="flag == 0"
              class="md:mt-6 mt-4 opacity-80 ml-2 grid grid-cols-2 gap-2  md:flex  flex-wrap md:flex-col md:space-x-0 md:space-y-1 h-auto pb-16 sm:pb-8">
              <div>
                <div class="text-xs opacity-50">Model</div>
                <div class="text-sm">{{ model }}</div>
              </div>
              <div>
                <div class="text-xs opacity-50">Guidance scale</div>
                <div class="text-sm">{{ CFG }}</div>
              </div>
              <div>
                <div class="text-xs opacity-50">User</div>
                <div class="text-sm">{{ user_id }}</div>
              </div>
              <div>
                <div class="text-xs opacity-50">Dimensions(wxh)</div>
                <div class="text-sm">{{ size }}</div>
              </div>
              <div>
                <div class="text-xs opacity-50">Negative prompt</div>
                <div class="text-sm">{{ npmt }}</div>
              </div>
          </div>
          <div v-if="flag == 1"
            class="md:mt-6 mt-4 opacity-80 ml-2 grid grid-cols-2 gap-2  md:flex  flex-wrap md:flex-col md:space-x-0 md:space-y-1 h-auto pb-16 sm:pb-8">
            <div>
              <div class="text-xs opacity-50">Model</div>
              <div class="text-sm">{{ model }}</div>
            </div>
            <div>
              <div class="text-xs opacity-50">User</div>
              <div class="text-sm">{{ user_id }}</div>
            </div>
            <div>
              <div class="text-xs opacity-50">Dimensions(wxh)</div>
              <div class="text-sm">{{ size }}</div>
            </div>
            <div v-if="source_img">
              <div class="text-xs opacity-50 mb-4">Source Image</div>
              <img v-bind:src="source_img" style="object-fit:contain;height:100%;max-height:40vh" />
            </div> 
          </div>
        </div>
        <div class="flex flex-wrap overflow-hidden flex-1 items-start justify-start thin-scrollbar h-auto pb-2"
          style="height:fit-content;overscroll-behavior-x:contain">
          <div v-for="(img_url, index) in img_res" :key="index">
            <img v-bind:src="img_url" v-on:click="showViewer(img_res)"
              style="object-fit:contain;height:100%;max-height:50vh" />
          </div>
        </div>
      </div>
    </div>
  </div>
</div></template>

<script>
import axios from "axios";
import { defineComponent, ref } from 'vue'
import 'viewerjs/dist/viewer.css'
import { api as viewerApi } from 'v-viewer'
import { useRoute } from 'vue-router'
import NavBar from '@/components/NavBar.vue';

export default defineComponent({
  components: {
    NavBar
  },
  setup() {
    const img_res = ref("");
    const model = ref("");
    const pmt = ref("");
    const npmt = ref("");
    const size = ref("");
    const CFG = ref("");
    const user_id = ref("");
    const source_img = ref(null);
    const page = ref('home');
    const flag = ref(0);
    const route = useRoute();

    const showViewer = (img_res) => {
      viewerApi({
        options: {
          toolbar: true,
        },
        images: img_res
      })
    }

    const fetchImageData = async (id) => {
      const response = await axios.get(`http://${process.env.VUE_APP_BACKEND_IP}/get_hash`,
        {
          params: {
            key: id,
          }
        });
      const res = response.data;
      img_res.value = res.batch;
      model.value = res.model;
      pmt.value = res.prompt;
      size.value = res.size;
      user_id.value = res.user_id;
      if (model.value === "sdxl") {
        flag.value = 0;
        npmt.value = res.nprompt;
        CFG.value = res.CFG;
      } else {
        flag.value = 1;
        if ('source_url' in res) {
          source_img.value = res.source_url
        }
      }
    };

    let id = route.params.id.split('.')[0]
    fetchImageData(id);

    return {
      flag,
      img_res,
      model,
      pmt,
      npmt,
      size,
      CFG,
      user_id,
      source_img,
      page,
      showViewer
    };
  },
});
</script>
<template>
  <div>
    <div
      class="fixed bottom-0 sm:top-0 z-50 flex flex-row items-center justify-between  backdrop-blur bg-opacity-80 border-t  sm:border-t-0 sm:border-b border-opacity-50  text-sm select-none bg-zinc-900 border-t-zinc-700 sm:border-b-zinc-700"
      style="height:56px;width:100vw">
      <div class="hidden sm:flex items-center cursor-pointer px-4 pl-6 left-0 h-full w-32">
        <div class="font-semibold text-3xl text-slate-50 justify-center items-center">SDXL</div>
        <div class="flex relative items-center h-full -mt-1 w-full sm:w-auto">
          <div style="height: 32px; top: 15px; display: absolute" class="absolute rounded bg-zinc-700"></div>
          <a class="flex flex-row items-center cursor-pointer h-full py-1.5 pb-0 px-2 justify-center transition-all flex-1"
            style="width: 80px; z-index: 2; opacity: 1" href="/">
            <div class="relative sm:flex justify-center hidden w-full">
              <div class="absolute w-full" style="border-bottom: 2.5px solid #6366f1; bottom: -17px"></div>
              <span class="text-slate-50">Home</span>
            </div>
            <div class="relative flex items-center justify-center text-xl sm:hidden w-full">
              <div class="absolute w-full" style="border-bottom: 2.5px solid #6366f1; bottom: -17px"></div>
              <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round"
                stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                <polyline points="9 22 9 12 15 12 15 22"></polyline>
              </svg>
            </div>
          </a>
          <a class="flex flex-row items-center cursor-pointer h-full py-1.5 pb-0 px-2 justify-center transition-all flex-1"
            style="width: 80px; z-index: 2; opacity: 0.5" href="/aperture">
            <div class="relative sm:flex justify-center hidden w-full">
              <div class="absolute w-full" style="border-bottom: 2.5px solid transparent; bottom: -17px"></div>
              <span class="text-slate-50">Generate</span>
            </div>
            <div class="relative flex items-center justify-center text-xl sm:hidden w-full">
              <div class="absolute w-full" style="border-bottom: 2.5px solid transparent; bottom: -17px"></div>
              <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round"
                stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="14.31" y1="8" x2="20.05" y2="17.94"></line>
                <line x1="9.69" y1="8" x2="21.17" y2="8"></line>
                <line x1="7.38" y1="12" x2="13.12" y2="2.06"></line>
                <line x1="9.69" y1="16" x2="3.95" y2="6.06"></line>
                <line x1="14.31" y1="16" x2="2.83" y2="16"></line>
                <line x1="16.62" y1="12" x2="10.88" y2="21.94"></line>
              </svg>
            </div>
          </a><a
            class="flex flex-row items-center cursor-pointer h-full py-1.5 pb-0 px-2 justify-center transition-all flex-1"
            style="width: 80px; z-index: 2; opacity: 0.5" href="/history">
            <div class="relative sm:flex justify-center hidden w-full">
              <div class="absolute w-full" style="border-bottom: 2.5px solid transparent; bottom: -17px"></div>
              <span class="text-slate-50">History</span>
            </div>
            <div class="relative flex items-center justify-center text-xl sm:hidden w-full">
              <div class="absolute w-full" style="border-bottom: 2.5px solid transparent; bottom: -17px"></div>
              <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16" height="1em" width="1em"
                xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" clip-rule="evenodd"
                  d="M13.507 12.324a7 7 0 0 0 .065-8.56A7 7 0 0 0 2 4.393V2H1v3.5l.5.5H5V5H2.811a6.008 6.008 0 1 1-.135 5.77l-.887.462a7 7 0 0 0 11.718 1.092zm-3.361-.97l.708-.707L8 7.792V4H7v4l.146.354 3 3z">
                </path>
              </svg>
            </div>
          </a><a
            class="flex flex-row items-center cursor-pointer h-full py-1.5 pb-0 px-2 justify-center transition-all flex-1"
            style="width: 80px; z-index: 2; opacity: 0.5" href="/likes">
            <div class="relative sm:flex justify-center hidden w-full">
              <div class="absolute w-full" style="border-bottom: 2.5px solid transparent; bottom: -17px"></div>
              <span class="text-slate-50">Likes</span>
            </div>
            <div class="relative flex items-center justify-center text-xl sm:hidden w-full">
              <div class="absolute w-full" style="border-bottom: 2.5px solid transparent; bottom: -17px"></div>
              <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round"
                stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z">
                </path>
              </svg>
            </div>
          </a><a
            class="flex flex-row items-center cursor-pointer h-full py-1.5 pb-0 px-2 justify-center transition-all flex-1"
            style="width: 80px; z-index: 2; opacity: 0.5" href="/account">
            <div class="relative sm:flex justify-center hidden w-full">
              <div class="absolute w-full" style="border-bottom: 2.5px solid transparent; bottom: -17px"></div>
              <span class="text-slate-50">Account</span>
            </div>
            <div class="relative flex items-center justify-center text-xl sm:hidden w-full">
              <div class="absolute w-full" style="border-bottom: 2.5px solid transparent; bottom: -17px"></div>
              <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round"
                stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="3"></circle>
                <path
                  d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z">
                </path>
              </svg>
            </div>
          </a>
        </div>
      </div>
    </div>
    <div class="min-h-screen absolute top-0 bottom-0 left-0 right-0 overflow-x-hidden flex flex-col bg-zinc-800 text-gray-100 text-sm">
      <div class="mb-[56px] sm:mb-0 sm:mt-[56px]">    
        <div class="flex w-full h-full self-stretch flex-col md:flex-row pb-0 md:pb-0 md:pt-0 flex-1 ">
          <div class="w-full flex-shrink-0 overflow-hidden text-base px-5 flex flex-col h-auto "
          style="height:fit-content;width:400px">
          <div class="mt-6 px-4 py-3 bg-zinc-700 rounded-xl shadow bg-opacity-50 font-light flex flex-col space-y-5">
            <p><a class="bg-red-500 bg-opacity-0 rounded hover:bg-opacity-40 cursor-pointer "
                href="/?q=man">{{pmt}}</a></p>
            <div class="flex text-xs font-light">
              <div class="flex flex-1 flex-row space-x-2 mr-2">
                <div
                  class="text-xs rounded-md sm:text-xs active:scale-95 transition-all transform-gpu whitespace-nowrap flex-1 flex select-none cursor-pointer hover:bg-zinc-600 border border-zinc-600 bg-zinc-700 items-center justify-center  shadow px-2.5 py-2 w-fit-content">
                  <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round"
                    stroke-linejoin="round" class="text-sm mr-2" height="1em" width="1em"
                    xmlns="http://www.w3.org/2000/svg">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                  </svg>Copy prompt</div>
                <div
                  class="text-xs rounded-md sm:text-xs active:scale-95 transition-all transform-gpu whitespace-nowrap flex-1 flex select-none cursor-pointer hover:bg-zinc-600 border border-zinc-600 bg-zinc-700 items-center justify-center  shadow px-2.5 py-2 w-fit-content">
                  <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round"
                    stroke-linejoin="round" class="text-sm mr-2" height="1em" width="1em"
                    xmlns="http://www.w3.org/2000/svg">
                    <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
                    <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
                  </svg>Copy URL</div>
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
              </svg>Open in editor</div>
            <div
              class="text-xs rounded-md sm:text-sm group mt-4 whitespace-nowrap flex-1 flex select-none cursor-pointer hover:brightness-110 bg-gradient-to-t  from-zinc-700 via-zinc-700 to-zinc-700 drop-shadow items-center justify-center px-2.5 py-2 w-fit-content">
              Explore this style<svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24"
                stroke-linecap="round" stroke-linejoin="round"
                class="ml-2 text-base group-hover:translate-x-1 transition-all" height="1em" width="1em"
                xmlns="http://www.w3.org/2000/svg">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg></div>
          </div>
          <div
            class="md:mt-6 mt-4 opacity-80 ml-2 grid grid-cols-2 gap-2  md:flex  flex-wrap md:flex-col md:space-x-0 md:space-y-1 h-auto pb-16 sm:pb-8">
            <div>
              <div class="text-xs opacity-50">Model</div>
              <div class="text-sm">SDXL</div>
            </div>
            <div>
              <div class="text-xs opacity-50">Guidance scale</div>
              <div class="text-sm">7</div>
            </div>
            <div>
              <div class="text-xs opacity-50">Dimensions</div>
              <div class="text-sm">{{dims}}</div>
            </div>
            <div>
              <div class="text-xs opacity-50">Upscaled</div>
              <div class="text-sm">{{dims}}</div>
            </div>
            <div>
              <div class="text-xs opacity-50">Negative prompt</div>
              <div class="text-sm">{{npmt}}</div>
            </div>
          </div>
        </div>
        <div class="flex flex-wrap overflow-hidden flex-1 items-start justify-start thin-scrollbar h-auto pb-2"
          style="height:fit-content;overscroll-behavior-x:contain">
            <div v-for="(img_url, index) in img_res" :key="index">
              <img v-bind:src="img_url" v-on:click="showViewer(img_res)" style="object-fit:contain;height:100%;max-height:35vh" />
            </div>
          </div>
      </div>
    </div>
  </div>
</div></template>

<script>
import axios from "axios";
import Vue from 'vue'
import Viewer from 'v-viewer'
import 'viewerjs/dist/viewer.css'

export default {
  data() {
    return {
      img_res: "",
      pmt: "",
      npmt: "",
      dims: "",
      CFG: "",
    };
  },
  async created() {
    const response = await axios.get('http://192.168.3.16:8877/get_image',
      {
        params: {
          img: this.$route.params.img,
        }
      });
    const res = response.data;
    this.img_res = res.img_res;
    const pmt_res = res.pmt_res;
    this.pmt = pmt_res.prompt;
    this.npmt = pmt_res.nprompt;
    this.dims = pmt_res.dims;
    this.CFG = pmt_res.CFG;
  },
  mounted() {
    Vue.use(Viewer)
  },
  methods: {
    showViewer(img_res) {
      this.$viewerApi({
          images: img_res,
          options: {
            toolbar: true,
          },
        })
    }
  }
};
</script>

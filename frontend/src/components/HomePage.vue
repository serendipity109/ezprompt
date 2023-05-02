<template>
    <div>
      <div
        class="fixed bottom-0 sm:top-0 z-50 flex flex-row items-center justify-between  backdrop-blur bg-opacity-80 border-t  sm:border-t-0 sm:border-b border-opacity-50  text-sm select-none bg-zinc-900 border-t-zinc-700 sm:border-b-zinc-700"
        style="height:56px;width:100vw">
        <div class="hidden sm:flex items-center cursor-pointer px-4 pl-6 left-0 h-full w-32">
          <div class="font-semibold text-3xl text-slate-50 justify-center items-center">
            {{ message }}
          </div>
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
          <div class="w-screen overflow-x-hidden flex flex-col bg-zinc-800 text-gray-100 text-sm">
            <div class="flex flex-col items-center py-4 mt-16"><a class="font-semibold text-3xl text-gray-100"
                href="/">SDXL</a>
              <div class="flex items-center w-full max-w-[600px] md:ml-[48px] mt-8 px-4 pl-5 md:px-5">
                <div class="w-full">
                  <div class="w-full flex items-center relative"><svg stroke="currentColor" fill="none" stroke-width="2"
                      viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"
                      class="absolute left-4 pointer-events-none" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                      <circle cx="11" cy="11" r="8"></circle>
                      <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg><input id="main-search" autoComplete="off" v-model="keyword" type="text"
                      class="bg-zinc-700 flex-1 pl-12 pr-12 rounded-full text-sm px-4 py-2.5 focus:outline-none focus:ring-1 focus:ring-indigo-700"
                      placeholder="Search for an image" value="" />
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
                <div class="flex justify-center"><button
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
              <div class=" mb-8 flex flex-col items-center">
                <div class="flex space-x-2">
                  <button @click="sendRequest"
                    class="w-32 sm:w-36 flex items-center text-xs justify-center text-center  h-9 rounded-full  hover:brightness-110 bg-opacity-0 shadow-sm  mt-4 bg-gradient-to-t from-indigo-900 via-indigo-900 to-indigo-800">Search</button>
                  <a href="/aperture">
                    <button
                      class="w-32 sm:w-36 flex items-center text-xs justify-center text-center  h-9 rounded-full  hover:brightness-110 bg-opacity-0 shadow-sm  mt-4 border border-gray-700 hover:bg-zinc-700">Generate</button>
                  </a>
                </div>
              </div>
              <div class="mt-2"> </div>
              <div class="w-full mt-4 px-1 relative"></div>
            </div>
          </div>
        <div w-full mt-4 px-1 relative>
          <div role="grid" class="w-screen overflow-x-hidden flex flex-col bg-zinc-800 text-gray-100 text-sm" tabindex="0"
            style="position: relative; width: 100%; max-width: 100%; height: 6053px; max-height: 6053px;">
            <div class="image-row" v-for="(row, index) in imageRows" :key="index">
              <div class="image-container" v-for="(image, index) in row" :key="index">
                <router-link :to="'/image/' + image.img" :key="index" class="block relative group select-none overflow-hidden m-0.5 border-indigo-600  rounded-xl"
                  style="transition: opacity 500ms ease 0s;">
                  <div
                    class="absolute inset-0 z-10 block text-zinc-100 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none line-clamp px-2 pb-2 text-sm px-2"
                    style="background: linear-gradient(0deg, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0.4) 40%, rgba(0, 0, 0, 0.1) 100%);">
                    <div class="flex-shrink h-full flex items-end">
                      <div class="flex flex-col">
                        <p class="text-sm mb-1.5 font-medium leading-snug"
                          style="overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;">
                          {{ image.view1}}</p>
                        <p class="opacity-60 leading-snug text-sm"
                          style="overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;">
                          {{ image.view2}}</p>
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
        </div>
      </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        message: "",
        keyword: "",
        images: [],
        imageRows: [],
      };
    },
    async created() {
      fetch("http://192.168.3.16:8877/")
        .then((response) => response.json())
        .then((data) => {
          this.message = data.Model;
        });
    },
    methods: {
      async sendRequest() {
        const response = await axios.get('http://192.168.3.16:8877/get_images');
        this.images = response.data;
        console.log(response.data);
        this.imageRows = this.chunkArray(this.images, 5);
      },
      chunkArray(array, size) {
        const chunkedArray = [];
        for (let i = 0; i < array.length; i += size) {
          chunkedArray.push(array.slice(i, i + size));
        }
        return chunkedArray;
      }
    },
  };
  </script>
  
  <style>.image-gallery {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
  }
  
  .image-row {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .image-container {
    margin: 0px;
    flex: 1;
    max-width: 20%;
    height: auto;
    text-align: center;
  }
  
  .img-responsive {
    max-width: 100%;
    height: auto;
  }</style>
<template>
    <div>
        <div class="fixed bottom-0 sm:top-0 z-50 flex flex-row items-center justify-between  backdrop-blur bg-opacity-80 border-t  sm:border-t-0 sm:border-b border-opacity-50  text-sm select-none bg-zinc-900 border-t-zinc-700 sm:border-b-zinc-700"
            style="height:56px;width:100vw">
            <div class="hidden sm:flex items-center cursor-pointer px-4 pl-6 left-0 h-full w-32 ">
                <div class="font-semibold text-3xl text-slate-50 justify-center items-center">SDXL</div>
            </div>
            <div class="flex relative items-center h-full -mt-1 w-full sm:w-auto">
                <div style="height:32px;top:15px;display:absolute" class="absolute  rounded bg-zinc-700"></div><a
                    class="flex flex-row items-center cursor-pointer h-full py-1.5 pb-0 px-2 justify-center transition-all flex-1"
                    style="width:80px;z-index:2;opacity:0.5" href="/home">
                    <div class="relative sm:flex justify-center hidden w-full">
                        <div class="absolute w-full" style="border-bottom:2.5px solid transparent;bottom:-17px"></div><span
                            class="text-slate-50">Home</span>
                    </div>
                    <div class="relative flex items-center justify-center text-xl sm:hidden w-full">
                        <div class="absolute w-full" style="border-bottom:2.5px solid transparent;bottom:-17px"></div><svg
                            stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round"
                            stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                            <polyline points="9 22 9 12 15 12 15 22"></polyline>
                        </svg>
                    </div>
                </a><a
                    class="flex flex-row items-center cursor-pointer h-full py-1.5 pb-0 px-2 justify-center transition-all flex-1"
                    style="width:80px;z-index:2;opacity:1" href="/generate">
                    <div class="relative sm:flex justify-center hidden w-full">
                        <div class="absolute w-full" style="border-bottom:2.5px solid #6366f1;bottom:-17px"></div><span
                            class="text-slate-50">Generate</span>
                    </div>
                    <div class="relative flex items-center justify-center text-xl sm:hidden w-full">
                        <div class="absolute w-full" style="border-bottom:2.5px solid #6366f1;bottom:-17px"></div><svg
                            stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round"
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
                    style="width:80px;z-index:2;opacity:0.5" href="/history">
                    <div class="relative sm:flex justify-center hidden w-full">
                        <div class="absolute w-full" style="border-bottom:2.5px solid transparent;bottom:-17px"></div><span
                            class="text-slate-50">History</span>
                    </div>
                    <div class="relative flex items-center justify-center text-xl sm:hidden w-full">
                        <div class="absolute w-full" style="border-bottom:2.5px solid transparent;bottom:-17px"></div><svg
                            stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16" height="1em"
                            width="1em" xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" clip-rule="evenodd"
                                d="M13.507 12.324a7 7 0 0 0 .065-8.56A7 7 0 0 0 2 4.393V2H1v3.5l.5.5H5V5H2.811a6.008 6.008 0 1 1-.135 5.77l-.887.462a7 7 0 0 0 11.718 1.092zm-3.361-.97l.708-.707L8 7.792V4H7v4l.146.354 3 3z">
                            </path>
                        </svg>
                    </div>
                </a><a
                    class="flex flex-row items-center cursor-pointer h-full py-1.5 pb-0 px-2 justify-center transition-all flex-1"
                    style="width:80px;z-index:2;opacity:0.5" href="/likes">
                    <div class="relative sm:flex justify-center hidden w-full">
                        <div class="absolute w-full" style="border-bottom:2.5px solid transparent;bottom:-17px"></div><span
                            class="text-slate-50">Likes</span>
                    </div>
                    <div class="relative flex items-center justify-center text-xl sm:hidden w-full">
                        <div class="absolute w-full" style="border-bottom:2.5px solid transparent;bottom:-17px"></div><svg
                            stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round"
                            stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z">
                            </path>
                        </svg>
                    </div>
                </a><a
                    class="flex flex-row items-center cursor-pointer h-full py-1.5 pb-0 px-2 justify-center transition-all flex-1"
                    style="width:80px;z-index:2;opacity:0.5" href="/account">
                    <div class="relative sm:flex justify-center hidden w-full">
                        <div class="absolute w-full" style="border-bottom:2.5px solid transparent;bottom:-17px"></div><span
                            class="text-slate-50">Account</span>
                    </div>
                    <div class="relative flex items-center justify-center text-xl sm:hidden w-full">
                        <div class="absolute w-full" style="border-bottom:2.5px solid transparent;bottom:-17px"></div><svg
                            stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round"
                            stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="12" cy="12" r="3"></circle>
                            <path
                                d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z">
                            </path>
                        </svg>
                    </div>
                </a>
            </div>
            <div class="hidden w-32 h-full  sm:flex items-center justify-end mr-4"></div>
        </div>
        <div
            class="min-h-screen absolute top-0 bottom-0 left-0 right-0 overflow-x-hidden flex flex-col bg-zinc-800 text-gray-100 text-sm">
            <div class="mb-[56px] sm:mb-0 sm:mt-[56px]">
                <div class="w-screen overflow-x-hidden">
                    <div class="sm:hidden w-full flex items-center justify-end mr-4 pt-2"></div>
                    <div class="flex justify-center w-full mt-0 sm:pt-4 md:pt-10">
                        <div class="px-2 md:px-10 lg:px-16 flex items-center flex-col max-w-[1300px] w-full">
                            <div class="w-full flex flex-col-reverse md:flex-row">
                                <div class="flex-1">
                                    <div class="flex justify-between text-xs px-2 pb-1 mt-6 md:mt-0">
                                        <p class="opacity-40">Describe your image</p>
                                    </div>
                                    <div class="relative"><textarea id="main-generate" autoComplete="off"
                                            class="shadow overflow-y-hidden w-full bg-zinc-700 bg-opacity-60 border border-zinc-700 rounded-xl leading-relaxed text-sm px-4 py-2.5 focus:outline-none focus:ring-1 focus:ring-indigo-700 placeholder:opacity-50"
                                            placeholder="A steampunk teddy bear vending machine"></textarea></div>
                                    <p class="opacity-40 text-xs pl-2 pb-1 mt-2">Negative prompt</p><textarea
                                        id="main-generate" autoComplete="off"
                                        class="shadow overflow-y-hidden w-full bg-zinc-700 bg-opacity-60 border border-zinc-700 rounded-xl leading-relaxed text-sm px-4 py-2.5 focus:outline-none focus:ring-1 focus:ring-indigo-700 placeholder:opacity-50"
                                        placeholder="text, blurry"></textarea>
                                    <div class="w-full flex items-center justify-center  md:justify-end">
                                        <div class="transition-all" id="generate-button"><button
                                                class="mt-2 text-sm bg-gradient-to-t from-indigo-900 via-indigo-900 to-indigo-800 rounded-full drop-shadow text-md px-8 py-2  transition-all  opacity-70 cursor-default">Loading...</button>
                                        </div>
                                    </div>
                                </div>
                                <div class="w-full mt-[20px] ml-0 md:ml-8 md:max-w-[300px]">
                                    <div class="relative border border-zinc-700 rounded-lg  shadow-md">
                                        <div class="relative">
                                            <div class="absolute right-0 flex"><button
                                                    class="text-zinc-400 text-[11px] rounded-bl-lg active:scale-95 transition-all transform-gpu whitespace-nowrap flex select-none cursor-pointer bg-zinc-700 bg-opacity-30 hover:bg-opacity-60 hover:text-zinc-100 items-center justify-center py-1 w-fit-content px-2.5 pl-2 pr-2.5 rounded-tr-lg">+
                                                    Upload image</button></div>
                                        </div>
                                        <div class="px-5 py-4 pb-6">
                                            <div class="mt-1">
                                                <div
                                                    class="select-none opacity-50 text-xs flex items-center justify-start mb-3">
                                                    <svg stroke="currentColor" fill="none" stroke-width="2"
                                                        viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"
                                                        class="mr-2 text-sm" height="1em" width="1em"
                                                        xmlns="http://www.w3.org/2000/svg">
                                                        <path
                                                            d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3">
                                                        </path>
                                                    </svg>
                                                    <p>Dimensions</p>
                                                </div>
                                                <div class="">
                                                    <v-slider step="10" show-ticks="always" tick-size="4"></v-slider>
                                                    <input style="display:none" value="4" />
                                                    <div class="flex justify-between w-full  select-none mt-2 text-base">
                                                        <svg stroke="currentColor" fill="currentColor" stroke-width="0"
                                                            viewBox="0 0 16 16" class="opacity-40" height="1em" width="1em"
                                                            xmlns="http://www.w3.org/2000/svg">
                                                            <path fill-rule="evenodd"
                                                                d="M14.5 3h-13a.5.5 0 00-.5.5v9a.5.5 0 00.5.5h13a.5.5 0 00.5-.5v-9a.5.5 0 00-.5-.5zm-13-1A1.5 1.5 0 000 3.5v9A1.5 1.5 0 001.5 14h13a1.5 1.5 0 001.5-1.5v-9A1.5 1.5 0 0014.5 2h-13z"
                                                                clip-rule="evenodd"></path>
                                                            <path
                                                                d="M10.648 7.646a.5.5 0 01.577-.093L15.002 9.5V13h-14v-1l2.646-2.354a.5.5 0 01.63-.062l2.66 1.773 3.71-3.71z">
                                                            </path>
                                                            <path fill-rule="evenodd"
                                                                d="M4.502 7a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"
                                                                clip-rule="evenodd"></path>
                                                        </svg>
                                                        <div class="text-xs flex items-center transition-all text-zinc-200"
                                                            style="opacity:1">768<!-- --> × <!-- -->1152</div><svg
                                                            stroke="currentColor" fill="currentColor" stroke-width="0"
                                                            viewBox="0 0 16 16" class="opacity-40" height="1em" width="1em"
                                                            xmlns="http://www.w3.org/2000/svg">
                                                            <path d="M8.002 5.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z">
                                                            </path>
                                                            <path
                                                                d="M12 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2zM3 2a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v8l-2.083-2.083a.5.5 0 0 0-.76.063L8 11 5.835 9.7a.5.5 0 0 0-.611.076L3 12V2z">
                                                            </path>
                                                        </svg>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="mt-4 flex flex-col"><button
                                                    class="select-none pt-2 text-xs cursor-pointer items-center justify-start opacity-50 hover:opacity-100 transition-all flex ">
                                                    <div class="flex items-center justify-center"><svg stroke="currentColor"
                                                            fill="currentColor" stroke-width="0" viewBox="0 0 16 16"
                                                            height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                                                            <path
                                                                d="M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 01.753 1.659l-4.796 5.48a1 1 0 01-1.506 0z">
                                                            </path>
                                                        </svg></div>
                                                    <p class="ml-2">Advanced settings</p>
                                                </button></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="items-center w-full max-w-[800px] mt-8 px-4 pl-5 md:px-5" style="min-height:1px">
                                <div></div>
                            </div>
                            <div class="flex flex-col w-full flex-1 items-center justify-center"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


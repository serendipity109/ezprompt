<template>
    <div class="fixed bottom-0 sm:top-0 z-50 flex flex-row items-center justify-between  backdrop-blur bg-opacity-80 border-t  sm:border-t-0 sm:border-b border-opacity-50  text-sm select-none bg-zinc-900 border-t-zinc-700 sm:border-b-zinc-700"
    style="height:56px;width:100vw">
    <div class="hidden sm:flex items-center cursor-pointer px-4 pl-6 left-0 h-full w-32 ">
        <div class="font-semibold text-3xl text-slate-50 justify-center items-center">EZPrompt</div>
    </div>
    <div class="flex relative items-center h-full -mt-1 w-full sm:w-auto">
        <div style="height:32px;top:15px;display:absolute" class="absolute  rounded bg-zinc-700"></div><a
            class="flex flex-row items-center cursor-pointer h-full py-1.5 pb-0 px-2 justify-center transition-all flex-1"
            id="homepage" :style="{ opacity: getNavOpa('home') }" style="width:80px;z-index:2;" v-on:click="goToPage('/home')">
            <div class="relative sm:flex justify-center hidden w-full">
                <div class="absolute w-full" :style="{ borderBottom: '2.5px ' + getNavStyle('home') }" style="bottom:-17px"></div><span
                    class="text-slate-50">Home</span>
            </div>
            <div class="relative flex items-center justify-center text-xl sm:hidden w-full">
                <div class="absolute w-full" :style="{ borderBottom: '2.5px ' + getNavStyle('home') }" style="bottom:-17px"></div><svg
                    stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round"
                    stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                </svg>
            </div>
        </a><a
            class="flex flex-row items-center cursor-pointer h-full py-1.5 pb-0 px-2 justify-center transition-all flex-1"
            id="genpage" :style="{ opacity: getNavOpa('generate') }" style="width:80px;z-index:2;" v-on:click="goToPage('/generate')">
            <div class="relative sm:flex justify-center hidden w-full">
                <div class="absolute w-full" :style="{ borderBottom: '2.5px ' + getNavStyle('generate') }" style="bottom:-17px"></div><span
                    class="text-slate-50">Generate</span>
            </div>
            <div class="relative flex items-center justify-center text-xl sm:hidden w-full">
                <div class="absolute w-full" :style="{ borderBottom: '2.5px ' + getNavStyle('generate') }" style="bottom:-17px"></div><svg
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
            style="width:80px;z-index:2;opacity:0.5" href="/">
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
            style="width:80px;z-index:2;opacity:0.5" href="/">
            <div class="relative sm:flex justify-center hidden w-full">
                <div class="absolute w-full" style="border-bottom:2.5px solid transparent;bottom:-17px"></div><span
                    class="text-slate-50">Showcase</span>
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
            style="width:80px;z-index:2;opacity:0.5" href="/">
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
    <div class="hidden w-32 h-full  sm:flex items-center justify-end mr-4">
        <button class="login-button h-6 rounded-md ml-2 opacity-90 hover:brightness-110 px-3 text-xs bg-gradient-to-t from-indigo-800 via-indigo-800 to-indigo-600 drop-shadow mr-2 font-medium" type="button" aria-haspopup="dialog" aria-expanded="false" aria-controls="radix-:r0:" data-state="closed">Get started</button>
    </div>
</div>
</template>
<script>
import { defineComponent } from 'vue'
import { useRouter } from 'vue-router'
export default defineComponent({
    name: 'NavBar',
    props: {
        page: String,
    },
    setup(props) {
        const router = useRouter()
        const goToPage = (pagnition) => {
            router.push(pagnition)
        }
        function getNavStyle(pagnition) {
            return props.page === pagnition ? 'solid #6366f1' : 'solid transparent';
        }
        function getNavOpa(pagnition) {
            return props.page === pagnition ? '1' : '0.5';
        }
        return {
            getNavStyle,
            getNavOpa,
            goToPage
        };
    },
});
</script>
<style scoped>
.login-button {
  color: white;
}
</style>
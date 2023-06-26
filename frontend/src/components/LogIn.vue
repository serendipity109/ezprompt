<template>
    <div>
        <div role="dialog" id="radix-:r0:" aria-describedby="radix-:r2:" aria-labelledby="radix-:r1:" data-state="open"
            class="bg-zinc-800 items-center relative shadow-xl rounded-2xl z-50 px-8 py-8 text-sm drop-shadow-lg border border-zinc-700 fadeInAndScale"
            tabindex="-1" style="max-width: 330px; width: 100%; max-height: 85vh; pointer-events: auto;">
            <button @click="closeModal" type="button" class="hover:bg-zinc-700 p-1 rounded absolute right-3 top-3">
                <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round"
                    stroke-linejoin="round" class="text-xl" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </button>
            <div class="flex flex-col text-zinc-200 text-center items-center">
                <div class="flex-1 w-64 text-2xl text-slate-50 justify-center items-center my-8">EZPrompt</div>
                <div>
                    <auth @login-click="closeModal" />
                </div>
                <div class="flex-1 w-64 flex-shrink-0 opacity-50 my-8 ">Or login with email</div>
            </div>
            <form @submit.prevent="handleSubmit">
                <input v-model="email" autocomplete="email" placeholder="Email address"
                    class="w-64 px-3 py-2 bg-zinc-700 focus:outline-none focus:ring-1 focus:ring-indigo-600 rounded-lg border border-zinc-600 hover:brightness-110 text-white"
                    type="email">
                <button type="submit"
                    class="hover:brightness-110 bg-gradient-to-t from-indigo-800 via-indigo-800 to-indigo-700 border border-indigo-800 px-4 py-1.5 rounded-lg shadow h-9 w-64 drop-shadow flex items-center justify-center mt-3 text-white">
                    Continue
                </button>
            </form>
        </div>
    </div>
</template>

<script>
import { SET_AUTHENTICATION, SET_USERNAME, SET_EMAIL } from "@/store/storeconstants";
import { defineComponent, ref } from 'vue';
import 'viewerjs/dist/viewer.css';
import Auth from '@/components/GoogleAuth.vue';
import { useStore } from 'vuex'

export default defineComponent({
    components: {
        Auth
    },
    setup(_, context) {
        const store = useStore()
        const email = ref('');
        const closeModal = () => {
            context.emit('login-click');
        }
        const handleSubmit = () => {
            const parts = email.value.split('@');
            store.commit(`auth/${SET_AUTHENTICATION}`, true);
            store.commit(`auth/${SET_USERNAME}`, parts[0]);
            store.commit(`auth/${SET_EMAIL}`, email.value);
            context.emit('login-click');
        };
        return {
            closeModal,
            handleSubmit,
            email
        }
    }
})
</script>


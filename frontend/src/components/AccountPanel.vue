<template>
    <div>
        <div
            class="w-64 bg-gray-800 fixed z-50 right-0 top-5 rounded-md shadow text-sm flex flex-col items-start overflow-hidden border border-gray-700">
            <div class="px-4 py-2 bg-gray-700 w-full flex items-center">
                <div class="rounded-full h-7 w-7 flex items-center justify-center bg-gray-800 mr-2 text-zinc-100">
                    <p>{{ username_first_letter }}</p>
                </div>
                <span class="font-medium truncate text-zinc-100">{{ email }}</span>
            </div>
            <a class="w-full px-4 py-2 hover:bg-gray-700 flex justify-center text-zinc-100" href="/account">Credits {{ credits }}</a>
            <button @click="handleSignout" class="w-full px-4 py-2 hover:bg-gray-700 text-zinc-100">Sign out</button>
        </div>
    </div>
</template>
  
<script>
import axios from 'axios'
import { defineComponent, computed, ref } from 'vue'
import { GET_EMAIL, GET_USERNAME, SET_AUTHENTICATION, SET_USERNAME, SET_EMAIL, SET_TOKEN, GET_TOKEN } from "@/store/storeconstants";
import { useStore } from 'vuex'
import { onMounted } from 'vue';

export default defineComponent({
    setup(_, context) {
        const credits = ref(0);
        const store = useStore()
        const email = computed(() => {
            let Email = store.getters[`auth/${GET_EMAIL}`]
            return Email;
        });
        const username = computed(() => {
            let userName = store.getters[`auth/${GET_USERNAME}`]
            return userName;
        });
        const username_first_letter = computed(() => {
            let userName = username.value;
            return (typeof userName === 'string' && userName.length > 0) ? userName[0] : '';
        });
        const handleSignout = () => {
            store.commit(`auth/${SET_AUTHENTICATION}`, false);
            store.commit(`auth/${SET_USERNAME}`, "");
            store.commit(`auth/${SET_EMAIL}`, "");
            store.commit(`auth/${SET_TOKEN}`, "");
            context.emit('signout-click');
        };
        const getCredits = async () => {
            const token = store.getters[`auth/${GET_TOKEN}`]
            try {
                const response = await axios.get(`http://${process.env.VUE_APP_BACKEND_IP}/user/credits`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                })
                if (response.data.data && 'credits' in response.data.data) {
                    credits.value = response.data.data.credits;
                } else {
                    console.error('Invalid response structure:', response.data);
                }
            } catch (error) {
                console.error('Failed to get credits:', error);
            }
        }

        onMounted(getCredits);
        return {
            credits,
            email,
            username,
            username_first_letter,
            handleSignout,
            getCredits
        }
    }
})
</script>
  

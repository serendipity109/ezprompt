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
            <a class="w-full px-4 py-2 hover:bg-gray-700 flex justify-center text-zinc-100" v-on:click="goToPage('/account')">Credits: {{ credits }}</a>
            <button @click="handleSignout" class="w-full px-4 py-2 hover:bg-gray-700 text-zinc-100">Sign out</button>
        </div>
    </div>
</template>
  
<script>
import axios from 'axios'
import { defineComponent, computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { onMounted } from 'vue';
import store from '@/utils/store'; 

export default defineComponent({
    setup(_, context) {
        const username = ref("");
        const email = ref("");
        const token = ref("");

        const router = useRouter()
        const credits = ref(0);
        
        const goToPage = (pagnition) => {
            router.push(pagnition)
        }

        const username_first_letter = computed(() => {
            let userName = username.value;
            return (typeof userName === 'string' && userName.length > 0) ? userName[0] : '';
        });

        const handleSignout = () => {
            store.commit('setUser', '')
            store.commit('setAuth', false)
            store.commit('setEmail', '')
            store.commit('setToken', '')
            context.emit('signout-click');
            window.location.reload();
        };

        const getCredits = async () => {
            console.log(token.value)
            try {
                const response = await axios.get(`http://${process.env.VUE_APP_BACKEND_IP}/user/credits`, {
                    headers: {
                        Authorization: `Bearer ${token.value}`
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

        onMounted(() => {
            const sessionUser = sessionStorage.getItem('vuex'); // 'vuex' 是默认的键名
            if (sessionUser) {
                const parsedUser = JSON.parse(sessionUser);
                username.value = parsedUser.user;
                email.value = parsedUser.email;
                token.value = parsedUser.token;
                if (token.value){
                    getCredits();
                }
            }
        });
        
        return {
            credits,
            getCredits,
            email,
            username,
            username_first_letter,
            handleSignout,
            goToPage
        }
    }
})
</script>
  

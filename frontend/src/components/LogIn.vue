<template>
    <div>
        <div role="dialog" id="radix-:r0:" aria-describedby="radix-:r2:" aria-labelledby="radix-:r1:" data-state="open"
            class="bg-zinc-800 text-zinc-100 items-center relative shadow-xl rounded-2xl z-50 px-8 py-8 text-sm drop-shadow-lg border border-zinc-700 fadeInAndScale"
            tabindex="-1" style="max-width: 330px; width: 100%; max-height: 85vh; pointer-events: auto;">
            <button @click="closeModal" type="button" class="hover:bg-zinc-700 p-1 rounded absolute right-3 top-3">
                <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round"
                    stroke-linejoin="round" class="text-xl" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </button>
            <div v-if="page == 1" v-loading="loading" element-loading-background="rgba(10, 10, 10, 0.2)">
                <div class="flex flex-1 w-64 text-2xl text-slate-50 justify-center items-center mb-4">
                    Welcome back
                </div>
                <form @submit.prevent="SubmitEmail">
                    <input v-model="email" autocomplete="email" placeholder="Email address"
                        class="w-64 px-3 py-2 bg-zinc-700 focus:outline-none focus:ring-1 focus:ring-indigo-600 rounded-lg border border-zinc-600 hover:brightness-110 text-zinc-100"
                        type="email">
                    <button type="submit"
                        class="hover:brightness-110 bg-gradient-to-t from-indigo-800 via-indigo-800 to-indigo-700 border border-indigo-800 px-4 py-1.5 rounded-lg shadow h-9 w-64 drop-shadow flex items-center justify-center mt-3 text-zinc-100 mb-4">
                        Continue
                    </button>
                    <div class="flex flex-1 w-64 text-m text-slate-50 justify-center items-center mb-2">
                        Don't have an account?
                        <button @click="gotoCreate" class="text-purple-400 ml-2">Sign up</button>
                    </div>
                    <div class="flex flex-1 w-64 text-s text-slate-50 justify-center items-center mb-4">
                        <div class="bar"></div>
                        <span>Or</span>
                        <div class="bar"></div>
                    </div>
                </form>
                <div class="flex flex-col text-zinc-200 text-center items-center">
                    <div>
                        <auth @login-click="closeModal" />
                    </div>
                </div>
            </div>
            <div v-else-if="page == 2" v-loading="loading" element-loading-background="rgba(10, 10, 10, 0.2)">
                <div class="flex flex-1 w-64 text-2xl text-slate-50 justify-center items-center mb-4">
                    Enter your password
                </div>
                <form @submit.prevent="SubmitLogin">
                    <div class="relative">
                        <input v-model="email" autocomplete="email" :placeholder="email"
                            class="w-64 px-3 py-2 bg-zinc-700 focus:outline-none focus:ring-1 focus:ring-indigo-600 rounded-lg border border-zinc-600 hover:brightness-110 text-zinc-100"
                            type="email" readonly>
                        <label @click.prevent="page = 1"
                            class="absolute inset-y-0 right-3 flex items-center text-purple-600 cursor-pointer">
                            edit
                        </label>
                    </div>
                    <input v-model="password" autocomplete="password" placeholder="Password"
                        class="w-64 px-3 py-2 bg-zinc-700 focus:outline-none focus:ring-1 focus:ring-indigo-600 rounded-lg border border-zinc-600 hover:brightness-110 text-zinc-100 mt-4  mb-4"
                        type="password">
                    <div class="flex flex-1 w-64 text-m text-slate-50 justify-center items-center mb-4">
                        Forgot password?
                    </div>
                    <button type="submit"
                        class="hover:brightness-110 bg-gradient-to-t from-indigo-800 via-indigo-800 to-indigo-700 border border-indigo-800 px-4 py-1.5 rounded-lg shadow h-9 w-64 drop-shadow flex items-center justify-center mt-3 text-zinc-100 mb-4">
                        Continue
                    </button>
                </form>
                <div class="flex flex-1 w-64 text-m text-slate-50 justify-center items-center mb-2">
                    Don't have an account?
                    <button @click="gotoCreate" class="text-purple-400 ml-2">Sign up</button>
                </div>
            </div>
            <div v-else-if="page == 3" v-loading="loading" element-loading-background="rgba(10, 10, 10, 0.2)">
                <div class="flex flex-1 min-w-64 text-2xl text-slate-50 justify-center items-center mb-4">
                    Create your account
                </div>
                <form @submit.prevent="SubmitCreate">
                    <input v-model="email" autocomplete="email" placeholder="Email address"
                        class="w-64 px-3 py-2 bg-zinc-700 focus:outline-none focus:ring-1 focus:ring-indigo-600 rounded-lg border border-zinc-600 hover:brightness-110 text-zinc-100 overflow-auto"
                        type="email">
                    <input v-model="password" autocomplete="password" placeholder="Password"
                        class="w-64 px-3 py-2 bg-zinc-700 focus:outline-none focus:ring-1 focus:ring-indigo-600 rounded-lg border border-zinc-600 hover:brightness-110 text-zinc-100 mt-4  mb-4 overflow-auto"
                        type="password">
                    <button type="submit"
                        class="hover:brightness-110 bg-gradient-to-t from-indigo-800 via-indigo-800 to-indigo-700 border border-indigo-800 px-4 py-1.5 rounded-lg shadow h-9 w-64 drop-shadow flex items-center justify-center text-zinc-100">
                        Register
                    </button>
                </form>
                <div class="flex flex-1 w-64 text-m text-slate-50 justify-center items-center mt-2 mb-2">
                    Already have an account? Log in
                </div>
                <div class="flex flex-1 w-64 text-s text-slate-50 justify-center items-center mb-4">
                    <div class="bar"></div>
                    <span>Or</span>
                    <div class="bar"></div>
                </div>
                <div class="flex flex-col text-zinc-200 text-center items-center">
                    <div>
                        <auth @login-click="closeModal" />
                    </div>
                </div>
            </div>
            <div v-else-if="page == 4">
                <div class="flex flex-1 w-64 text-2xl text-slate-50 justify-center items-center mb-4">
                    Check your email for a login link
                </div>
                <div class="flex flex-1 w-64 text-m text-slate-50 justify-center items-center mb-2">
                    If you don't see the email, check your spam folder.
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import { SET_AUTHENTICATION, SET_USERNAME, SET_EMAIL, SET_TOKEN } from "@/store/storeconstants";
import { defineComponent, ref } from 'vue';
import 'viewerjs/dist/viewer.css';
import Auth from '@/components/GoogleAuth.vue';
import { ElMessage } from 'element-plus'
import { useStore } from 'vuex'

export default defineComponent({
    components: {
        Auth
    },
    setup(_, context) {
        const store = useStore()
        const email = ref('');
        const page = ref(1);
        const username = ref('');
        const password = ref('');
        const loading = ref(false);
        const closeModal = () => {
            context.emit('login-click');
        }

        const gotoCreate = () => {
            page.value = 3;
        };

        const SubmitEmail = () => {
            username.value = email.value;
            page.value = 2;
        };

        const SubmitLogin = async () => {
            let formData = new FormData()
            formData.append('username', username.value)
            formData.append('password', password.value)
            await axios.post(`http://${process.env.VUE_APP_BACKEND_IP}/user/login`, formData)
                .then(function (response) {
                    if (response.data.code === 200) {
                        ElMessage.info({showClose: true, message: "Successfully login!"})
                        store.commit(`auth/${SET_AUTHENTICATION}`, true);
                        store.commit(`auth/${SET_USERNAME}`, username.value);
                        store.commit(`auth/${SET_EMAIL}`, email.value);
                        store.commit(`auth/${SET_TOKEN}`, response.data.access_token);
                        context.emit('login-click');
                    } else {
                        ElMessage.error({showClose: true, message: response.data.message});
                    }
                })
        };

        const SubmitCreate = async () => {
            const mail = email.value
            const pwd = password.value
            loading.value = true
            const response = await axios.post(`http://${process.env.VUE_APP_BACKEND_IP}/user/encode?user_id=${mail}&password=${pwd}`)
            const token = response.data
            await axios.post(`http://${process.env.VUE_APP_BACKEND_IP}/user/send-email?receiver_email=${mail}&token=${token}`)
                .then(function (response) {
                    if (response.data.code === 200) {
                        ElMessage.info({showClose: true, message: "Already sent an email to confirm the registration."})
                        page.value = 4;
                    } else {
                        ElMessage.error({showClose: true, message: 'Failed to send email'});
                    }
                }
                )
            loading.value = false
        }

        return {
            page,
            gotoCreate,
            closeModal,
            username,
            password,
            SubmitEmail,
            SubmitLogin,
            SubmitCreate,
            email,
            loading
        }
    }
})
</script>
<style scoped>
.bar {
    flex-grow: 1;
    height: 0.1px;
    margin-left: 5px;
    margin-right: 5px;
    background-color: #fdfdfd;
}

.relative {
    position: relative;
}

.absolute {
    position: absolute;
}

.right-3 {
    right: 0.75rem;
}

.inset-y-0 {
    top: 0;
    bottom: 0;
}

.pr-20 {
    padding-right: 5rem;
}

.cursor-pointer {
    cursor: pointer;
}
</style>
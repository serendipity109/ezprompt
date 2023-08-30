<template>
  <GoogleLogin :callback="callback" auto-login />
</template>

<script>
import axios from "axios";
import { decodeCredential } from 'vue3-google-login'
import { useRouter } from 'vue-router'
import store from '@/utils/store'; 
import { ElMessage } from 'element-plus'

export default {
  setup(_, context) {
    const router = useRouter()
    const callback = async (response) => {
      const userData = decodeCredential(response.credential)
      const user = userData.name;
      const email = userData.email;
      let login = await Login(user, email)
      if (login === false){
        const create = await Create(user, email)
        if (create) {
          login = await Login(user, email)
        }
      }
      context.emit('login-click'); // 點擊X
      router.push('/home');
    }
    const Login = async (username, email) => {
      let formData = new FormData()
      formData.append('username', email)
      formData.append('password', username)
      return await axios.post(`http://${process.env.VUE_APP_BACKEND_IP}/user/login`, formData)
        .then(function (response) {
          if (response.data.code === 200) {
            ElMessage.info({showClose: true, message: "Successfully login!"})
            store.commit('setUser', email)
            store.commit('setAuth', true)
            store.commit('setEmail', email)
            store.commit('setToken', response.data.access_token)
            window.location.reload();
            return true
          } else {
            return false
          }
        })
    };

    const Create = async (username, email) => {
      return axios.post(`http://${process.env.VUE_APP_BACKEND_IP}/user/create?username=${email}&password=${username}`)
        .then(function (response) {
          if (response.data.code === 200) {
            return true
          } else if (response.data.code === 400) {
            ElMessage.error({
                showClose: true,
                message: response.data.message,
                duration: 5000
              });
            return false
          }
        })
    };

    return {
      callback,
      Login,
      Create
    };
  }
}
</script>

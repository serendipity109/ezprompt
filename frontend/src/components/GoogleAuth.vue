<template>
  <GoogleLogin :callback="callback" auto-login />
</template>

<script>
import axios from "axios";
import { SET_AUTHENTICATION, SET_USERNAME, SET_EMAIL } from "@/store/storeconstants";
import { decodeCredential } from 'vue3-google-login'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default {
  setup(_, context) {
    const router = useRouter()
    const store = useStore()
    const callback = (response) => {
      const userData = decodeCredential(response.credential)
      store.commit(`auth/${SET_AUTHENTICATION}`, true);
      store.commit(`auth/${SET_USERNAME}`, userData.name);
      store.commit(`auth/${SET_EMAIL}`, userData.email);
      context.emit('login-click'); // 點擊X
      router.push('/home');
      axios.post(`http://${process.env.VUE_APP_BACKEND_IP}/create?user_id=${userData.name}&password=6666&credits=100`);
    }

    return {
      callback
    };
  }
}
</script>

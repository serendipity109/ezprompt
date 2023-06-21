<template>
  <GoogleLogin :callback="callback" auto-login />
</template>

<script>
import { SET_AUTHENTICATION, SET_USERNAME } from "@/store/storeconstants";
import { decodeCredential } from 'vue3-google-login'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default {
  setup(_, context) {
    const router = useRouter()
    const store = useStore()
    const callback = (response) => {
      // decodeCredential will retrive the JWT payload from the credential
      console.log("Handle the response", response)
      const userData = decodeCredential(response.credential)
      console.log("Handle the userData", userData)
      store.commit(`auth/${SET_AUTHENTICATION}`, true);
      store.commit(`auth/${SET_USERNAME}`, userData.name);
      context.emit('login-click'); // 點擊X
      router.push('/home');
    }

    return {
      callback
    };
  }
}
</script>

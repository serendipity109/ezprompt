<template>
  <GoogleLogin :callback="callback" auto-login />
</template>

<script>
import { decodeCredential } from 'vue3-google-login'
import { useRouter } from 'vue-router'

export default {
  setup(_, context) {
    const router = useRouter()
    const callback = (response) => {
      // decodeCredential will retrive the JWT payload from the credential
      console.log("Handle the response", response)
      const userData = decodeCredential(response.credential)
      console.log("Handle the userData", userData)
      context.emit('login-click');
      router.push('/home');
    }

    return {
      callback
    };
  }
}
</script>

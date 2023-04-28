<template>
  <div>
    <h1>{{ message }}</h1>
    <div v-for="(imageUrl, index) in imageUrls" :key="index">
      <img :src="imageUrl" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      message: "",
      imageUrls: [],
    };
  },
  async created() {
    const response = await axios.get('http://192.168.3.16:8877/get_images');
    this.imageUrls = response.data;
    fetch("http://192.168.3.16:8877/")
      .then((response) => response.json())
      .then((data) => {
        this.message = data.Hello;
    });
  },
};
</script>

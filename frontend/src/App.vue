<template>
  <div>
    <h1>{{ message }}</h1>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      message: null,
    };
  },
  created() {
    fetch("http://localhost:8877/")
      .then((response) => response.json())
      .then((data) => {
        this.message = data.Hello;
      });
  },
};
</script>

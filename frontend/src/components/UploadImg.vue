<template>
  <div>
    <input type="file" id="file-input" @change="uploadFile" style="display: none" />
    <label for="file-input" style="cursor: pointer;">
        <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
        </svg>
    </label>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import axios from "axios";

const file = ref(null);

const fileName = computed(() => file.value?.name);
const fileMimeType = computed(() => file.value?.type);

const uploadFile = (event) => {
  file.value = event.target.files[0];
  submitFile();
};

const submitFile = async () => {
    const reader = new FileReader();
    reader.onload = async () => {
        const blobData = new Blob([reader.result], { type: fileMimeType.value });
        let formData = new FormData();
        formData.append('file', blobData, fileName.value);
        try {
            const endpoint = 'http://192.168.3.16:9527/dcmj/upload?user_id=adam';
            const response = await axios.post(endpoint, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            console.log(response.data);
        } catch (error) {
            console.error(error);
        }
    };
    reader.readAsArrayBuffer(file.value);
};

</script>
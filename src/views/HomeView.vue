<template>
    <div class="page">
        <div v-if="isLoading" class="loading-overlay">
            <div class="spinner"></div>
        </div>
        <img :src="logo"
             style="width: 7rem; height: 7rem; margin-top: 2rem;">
        <img
            :src="previewUrl || fileUpload" 
            alt="upload"
            :class="{ 'upload-box': previewUrl }"
            @click="triggerFileInput"
            style="
            cursor: pointer;
            object-fit: cover;
            margin-top: 2rem;
            width: 250px;
            height: 250px;
            "
        />
        <input
            type="file"
            accept="image/*"
            style="display: none;"
            @change="handleFileChange"
            id="fileUploadInput"
            ref="fileInput"
        />

        <button
        :class="{ uploaded: isUploaded }"
        class="start-button"
        :disabled="!isUploaded"
        @click="handleClick"
        >
        <span :class="{'text-white': isUploaded, 'text-neutral-500': !isUploaded}">
            시작하기
        </span>
        </button>

        <div class="bottom-navigator">
            <img :src="homeIcon" 
           :style="{ filter: $route.path === '/' ? 'invert(45%) sepia(88%) saturate(1376%) hue-rotate(194deg) brightness(95%) contrast(94%)' : 'none' }" 
           @click="() => router.push({ path: '/' })"
           alt="Home" />
            <img :src="dimigoIcon" 
           :style="{ filter: $route.path !== '/' && $route.path !== '/info' ? 'invert(45%) sepia(88%) saturate(1376%) hue-rotate(194deg) brightness(95%) contrast(94%)' : 'none' }" 
           alt="Dimigo" />
            <img :src="infoIcon" 
           :style="{ filter: $route.path === '/info' ? 'invert(45%) sepia(88%) saturate(1376%) hue-rotate(194deg) brightness(95%) contrast(94%)' : 'none' }" 
           @click="() => router.push({ path: '/info' })"
           alt="Info" />
        </div>
    </div>
</template>

<style scoped>
.page {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: start;
    align-items: center;
}
#fileUploadButton {
  margin-top: 5rem;
}

.start-button {
  position: relative;
  top:0;
  border-radius: 10px;
  margin-top: 4rem;
  width: 250px;
  height: 55px;
  background-color: #D9D9D9;
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.25); /* filter: 제거 */
  transition: all 0.3s ease;
}

.start-button.uploaded:hover {
  top: -5px;
}

.start-button span {
  font-size: 1.5rem;
}

.uploaded {
  background-color: #2196F3;
}


.bottom-navigator {
  position: fixed;
  display: flex;
  justify-content: space-around;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #EAEAEA;
  padding: 1rem;
  box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
}

.upload-box {
  width: 200px;
  height: 200px;
  border: 2px dashed #7E7E7E;
  border-radius: 10px;
}

.loading-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(255,255,255,0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.spinner {
  width: 3rem;
  height: 3rem;
  border: 0.4rem solid #ccc;
  border-top-color: #2196F3;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>

<script setup>
import { ref } from 'vue';
const isLoading = ref(false);
import { useRouter } from 'vue-router';
import fileUpload from '../assets/fileUpload.svg';
import dimigoIcon from '../assets/dimigo.svg';
import infoIcon from '../assets/info.svg';
import homeIcon from '../assets/home.svg';
import logo from '../assets/NoMoreDeepfake.png';
import axios from 'axios';
const router = useRouter();
const isUploaded = ref(false);
const previewUrl = ref(null);
const Sfile = ref(null);
const fileInput = ref(null);

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    Sfile.value = file;
    previewUrl.value = URL.createObjectURL(file);
    isUploaded.value = true;
  };

/**
 * 업로드된 파일을 백엔드(FastAPI)로 전송한다.
 * ENV: VITE_API_BASE_URL (예: http://localhost:8000)
 */
const BACKEND_URL = 'https://sharp-unified-racer.ngrok-free.app';

const handleClick = async () => {
  if (!isUploaded.value || !Sfile.value) return;

  isLoading.value = true;
  const formData = new FormData();
  formData.append('file', Sfile.value);

  try {
    const { data } = await axios.post(`${BACKEND_URL}/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    console.log('서버 응답:', data);
    router.push({ path: '/result', query: { fileURL: previewUrl.value, isDeepfake:data.isDeepfake, reliability: data.reliability } });
    isLoading.value = false;
  } catch (error) {
    console.error('파일 업로드 실패:', error);
    alert('파일 업로드에 실패했습니다.');
    isLoading.value = false;
  }
};
</script>
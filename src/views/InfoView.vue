<template>
    <div class="page">
        <div v-if="isLoading" class="loading-overlay">
            <div class="spinner"></div>
        </div>
        <img :src="logo"
             style="width: 7rem; height: 7rem; margin-top: 2rem;">
        <h2 style="font-size: 30px;">Project.</h2>
        <div class="hcontainer" style="width: 100%; display: flex; justify-content: center; align-items:center;">
          <h1 style="width: 200px;">No More Deepfake</h1>
        </div>

        <div class="info-card">
          <h2 class="nsk-bold">딥페이크란?</h2>
          <p class="nsk-regular">딥페이크는 인공지능, 특히 GAN(Generative Adversarial Network)을 활용해 사람의 얼굴이나 목소리를 합성하는 기술입니다.</p>
          <h3 class="nsk-bold">위험 요소</h3>
          <ul>
            <li class="nsk-regular">사기·금전적 이득을 위한 허위 영상 생성</li>
            <li class="nsk-regular">허위 정보 유포 및 명예 훼손</li>
            <li class="nsk-regular">개인 프라이버시 침해</li>
          </ul>
          <h3 class="nsk-bold">이 프로그램의 기능</h3>
          <ul>
            <li class="nsk-regular">CNN 딥러닝을 이용한 이미지의 딥페이크 여부 감지</li>
            <li class="nsk-regular">신뢰도(확률) 수치 제공</li>
          </ul>
        </div>
        <div class="hcontainer" style="justify-content: center; align-items: center;margin-top: 2rem;">
            <img :src="fregicIcon" style="width: 3rem; height: 3rem; margin-right: 0.6rem;">
            <span class="nsk-bold" style=" font-size: 1.4rem;">2025 프레직 내부 해커톤</span>
        </div>
        <p style="margin-top: 16px;">ⓒ 2025. FREGIC All rights reserved.</p>
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
  margin-top: 8rem;
}

.start-button {
  position: relative;
  top:0;
  border-radius: 10px;
  margin-top: 6rem;
  width: 300px;
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
  width: 300px;
  height: 300px;
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
.info-card {
  width: 70%;
  background-color: #f9f9f9;
  border-radius: 12px;
  padding: 1.5rem;
  margin: 2rem 0;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  font-family: "Noto Sans KR", sans-serif;
}
.info-card h2 {
  margin-bottom: 0.75rem;
  color: #333;
  font-size: 1.75rem;
}
.info-card h3 {
  margin-top: 1rem;
  margin-bottom: 0.5rem;
  color: #555;
  font-size: 1.25rem;
}
.info-card p {
  color: #444;
  line-height: 1.6;
  margin-bottom: 1rem;
}
.info-card ul {
  list-style-type: disc;
  margin-left: 1.5rem;
  color: #444;
  line-height: 1.5;
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
import fregicIcon from '../assets/fregic_logo.webp';
import logo from '../assets/NoMoreDeepfake.png';
import axios from 'axios';
const router = useRouter();

</script>
<template>
    <div class="page">
        <img :src="logo"
             style="width: 7rem; height: 7rem; margin-top: 2rem;">
        <img
            :src="previewUrl" 
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
        
        <div class="result-container">
          <span style="font-size: 24px; color:#7B7B7B;" class="nsk-regular">{{ reliability <= 40 ? (100 - reliability) : reliability }}% 확률로</span>
          <div class="hcontainer">
            <span v-if="reliability <= 40" class="result-text-normal nsk-bold">
              정상
            </span>
            <span v-else-if="reliability <= 60" class="result-text-suspect nsk-bold">
              딥페이크 의심
            </span>
            <span v-else class="result-text nsk-bold">
              딥페이크
            </span>
          </div>
        </div>
        <button
        :class="{ uploaded: isUploaded }"
        class="restart-button"
        @click="router.push({path: '/'})"
        >
        <div class="hcontainer">
          <img src="/src/assets/again.svg" alt="다시 검사하기" style="width: 24px; height: 24px; margin-right: 8px;">
          <span class="text-white">
              다시 검사하기
          </span>
        </div>
        
        </button>
        <!-- <div class="hcontainer detail-btn">
          <span class="nsk-regular">상세 확인</span>
        </div> -->
        
        <!--  -->
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
.result-text-normal {
  font-size: 64px;
  background: linear-gradient(to right top, #34c759, #4cd964);
  color: transparent;
  -webkit-background-clip: text;
  background-clip: text;
}

.result-text-suspect {
  font-size: 64px;
  background: linear-gradient(to right top, #ffcc00, #ff9500);
  color: transparent;
  -webkit-background-clip: text;
  background-clip: text;
}
.save-btn {
  position: fixed;
  bottom: 78px;
  right: 10px;

  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 10px;
  width: 160px;
  height: 40px;
  background-color: #2196F3;
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.25); /* filter: 제거 */
  transition: all 0.3s ease;
}

.save-btn:hover {
  bottom: 83px;
}

.detail-btn {
  margin-top: 8px; 
  cursor: pointer; 
  justify-content: end; 
  width: 300px;
  
}
.detail-btn span {
  color:#7B7B7B;
  font-size: 16px;
  transition: all 0.3s ease;
}
.detail-btn span:hover {
  color: #2196F3; 
  text-decoration: underline;
}

.result-text {
  font-size: 64px;
  background: linear-gradient(to right top, #5966FF, #C934FF);
  color: transparent;
  -webkit-background-clip: text;
  background-clip: text;
}


.result-container {
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: start;
  width: 240px;
  margin-top: 2rem;
}

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

.restart-button {
  position: relative;
  top: 0; /* Add initial position for smooth transition */
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 10px;
  margin-top: 1rem;
  width: 250px;
  height: 55px;
  background-color: #2196F3;
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.25); /* filter: 제거 */
  transition: all 0.3s ease;
}

.restart-button:hover {
  top: -5px;
}

.restart-button .hcontainer {
  width: 200px;
  height: 55px;
  align-items: center;
}

.restart-button span {
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
  border: 2px solid rgb(33, 131, 254);
  border-radius: 10px;
}
</style>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import fileUpload from '../assets/fileUpload.svg';
import dimigoIcon from '../assets/dimigo.svg';
import infoIcon from '../assets/info.svg';
import homeIcon from '../assets/home.svg';
import logo from '../assets/NoMoreDeepfake.png';
import axios from 'axios';
const router = useRouter();
const route = useRoute();
const isUploaded = ref(false);
const previewUrl = ref(null);
const Sfile = ref(null);
const fileInput = ref(null);

const isDeepfake = ref(false);
const reliability = ref(0);

onMounted(() => {
  previewUrl.value = route.query.fileURL;
  isDeepfake.value = route.query.isDeepfake === 'true';
  reliability.value = parseFloat(route.query.reliability) || 0;
  reliability.value *= 100;
  reliability.value = Math.round(reliability.value * 100) / 100; // 소수점 둘째 자리까지 반올림
});
</script>
<script setup>
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <router-view />
</template>

<style scoped>

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
#app {
  width: 100%;
  height: 100%;
  max-height: 100%;
  overflow: hidden;
}

</style>

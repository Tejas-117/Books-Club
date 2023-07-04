<script setup>
  import { onMounted, watchEffect } from 'vue';
  import { RouterView } from 'vue-router';
  import Navbar from './components/Navbar.vue';
  import Footer from './components/Footer.vue';
  import store from "./state/store";

  // update access and refresh token every ten minutes.
  let interval = null;
  watchEffect(async (onCleanUp) => {
    // clean up function that runs before effect.
    onCleanUp(cleanUpInterval);

    if(store.authTokens){
      interval = setInterval(() => {
        store.updateAuthToken();
      }, 13 * 10 * 1000); // refresh token every 13 minutes after initial load.
    }
  })

  function cleanUpInterval(){
    clearInterval(interval);
  }

  // update tokens on mount.
  onMounted(() => {
    store.updateAuthToken();
  })
</script>

<template>
  <Navbar />
  <RouterView />
  <Footer />
</template>

<style>
  @import "./assets/base.css";
</style>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import BottomNav from '@/components/manager/BottomNav.vue'
import AppBar from '@/components/manager/AppBar.vue'
import { useUserStore } from '@/stores/user'
import LoginView from './LoginView.vue'
const userStore = useUserStore()
</script>

<template>
  <v-layout class="rounded rounded-md">
    <AppBar />

    <v-main class="d-flex align-center justify-center main-background">
      <div class="content">
        <component :is="userStore.isLoggedIn ? RouterView : LoginView" />
      </div>
    </v-main>

    <BottomNav />
  </v-layout>
</template>

<style scoped>
.main-background {
  background-image: url('https://alist.dn11.ch405.icu/d/home/share_files/pink_miku.jpg?sign=yfsKsTKn8FnYxVsm8n1fJT36R2zDxaWNh4i6ajF9tWo=:0');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  min-height: 100vh; /* 确保背景覆盖整个视口高度 */
  display: flex;
  align-items: center;
  justify-content: center;
  animation: flow 10s infinite alternate; /* 添加动画 */
}

.content {
  width: 100%;
  height: 100%;
  backdrop-filter: blur(20px); /* 高斯模糊效果 */
  -webkit-backdrop-filter: blur(20px); /* 兼容 Safari */
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

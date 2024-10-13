<template>
  <v-btn prepend-icon="mdi-theme-light-dark" @click="toggleTheme" />
</template>

<script setup lang="ts">
import { useTheme } from 'vuetify'

// 获取主题对象
const theme = useTheme()

// 定义切换主题的函数
function toggleTheme(): void {
  // 切换主题
  theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
}
</script>

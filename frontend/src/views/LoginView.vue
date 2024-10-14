<template>
  <v-container>
    <v-form @submit.prevent="handleSubmit">
      <v-text-field
        v-model="username"
        name="username"
        label="用户名"
        type="text"
        required
        autocomplete="username"
        clearable
      ></v-text-field>
      <v-text-field
        v-model="password"
        name="current-password"
        label="密码"
        type="password"
        autocomplete="current-password"
        required
        clearable
      ></v-text-field>
      <v-row>
        <v-col cols="12">
          <v-btn type="submit" block>登录</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { login } from '@/api/fetchDataConsumer'
const username = ref('')
const password = ref('') // 假设需要密码进行登录
const router = useRouter()
const userStore = useUserStore()

async function handleSubmit() {
  if (username.value && password.value) {
    try {
      const token = await login(username.value, password.value)
      userStore.login(token)
      // 判断是否是管理员
      if (userStore.isAdmin) {
        router.push({ name: 'manager-home' }) // 登录成功后跳转到管理员页面
      } else {
        router.push({ name: 'home' }) // 登录成功后跳转到首页
      }
    } catch (error) {
      alert('登录失败，请检查用户名和密码')
      console.error(error)
    }
  } else {
    alert('请输入用户名和密码')
  }
}
</script>

<style scoped>
/* 添加一些简单的样式 */
.v-container {
  max-width: 400px;
  margin: 0 auto;
  padding-top: 100px;
}
</style>

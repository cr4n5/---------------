<template>
  <v-container>
    <v-form @submit.prevent="handleSubmit">
      <v-text-field v-model="username" label="用户名" required></v-text-field>
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

const username = ref('')
const router = useRouter()
const userStore = useUserStore()

function handleSubmit() {
  if (username.value) {
    userStore.login(username.value)
    console.log('用户名:', username.value)
    router.push({ name: 'home' }) // 登录成功后跳转到首页
  } else {
    alert('请输入用户名')
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

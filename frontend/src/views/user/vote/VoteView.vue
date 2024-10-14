<template>
  <v-container>
    <h2 class="text-h4 text-success ps-4">
      项目:&nbsp;
      <v-fade-transition leave-absolute>
        <span :key="`tasks-${tasks.length}`">
          {{ tasks.length }}
        </span>
      </v-fade-transition>
    </h2>

    <v-divider class="mb-4"></v-divider>

    <v-card v-if="tasks.length > 0" style="max-height: 50vh" class="overflow-y-auto">
      <template v-for="(task, i) in tasks" :key="`${i}-${task.text}`">
        <v-divider v-if="i !== 0" :key="`${i}-divider`"></v-divider>
        <v-fade-transition>
          <v-list-item>
            <v-list-item-title>
              <span>{{ task.text }}</span>
            </v-list-item-title>
            <template v-slot:append>
              <v-btn name="enter" icon variant="plain" @click="navigateToDetail(task.text)">
                <v-icon>mdi-arrow-right-box</v-icon>
              </v-btn>
            </template>
          </v-list-item>
        </v-fade-transition>
      </template>
    </v-card>
    <v-divider class="mb-4"></v-divider>
  </v-container>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { getVoteInfo } from '@/api/fetchDataConsumer'
import router from '@/router'
import type { VoteInfoResponse, VoteInfo } from '@/api/fetchDataConsumer'
const userStore = useUserStore()
const token = userStore.token

const tasks = ref<{ text: string }[]>([])
if (token !== null) {
  getVoteInfo(token)
    .then((res: VoteInfoResponse) => {
      if (res.status === 'success' && res.code === 200) {
        tasks.value = res.result.map((item: VoteInfo) => ({
          text: item.vote_obj,
          done: false
        }))
      } else {
        console.error('获取投票信息失败:', res.message)
      }
    })
    .catch((error) => {
      console.error('获取投票信息失败:', error)
    })
} else {
  console.error('Token 为空，无法获取投票信息')
}

function navigateToDetail(vote_obj: string) {
  router.push(`/vote/${vote_obj}`)
}
</script>
<style scoped>
/* 应用 JetBrains Mono 字体 */
* {
  font-family: 'JetBrains Mono', monospace;
}
</style>

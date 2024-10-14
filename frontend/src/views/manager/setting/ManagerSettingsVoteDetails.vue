<template>
  <v-container>
    <v-text-field
      v-model="newTask"
      :rules="taskRules"
      label="请输入你要创建的选项"
      variant="solo"
      @keydown.enter="create"
    >
      <template v-slot:append-inner>
        <v-fade-transition>
          <v-btn v-show="newTask" icon="mdi-plus-circle" variant="text" @click="create"></v-btn>
        </v-fade-transition>
      </template>
    </v-text-field>
    <v-row align="center" justify="space-between">
      <v-col>
        <h1 class="text-h4 ps-4">{{ vote_obj }}</h1>
      </v-col>
      <v-col class="d-flex justify-end">
        <v-btn @click="goBack" variant="plain" icon="mdi-arrow-left" class="me-4"></v-btn>
      </v-col>
    </v-row>
    <v-divider class="mb-4"></v-divider>
    <h2 class="text-h4 text-success ps-4">
      选项:&nbsp;
      <v-fade-transition leave-absolute>
        <span :key="`list-${list.length}`">
          {{ list.length }}
        </span>
      </v-fade-transition>
    </h2>

    <v-divider class="mb-4"></v-divider>

    <v-card v-if="list.length > 0" style="max-height: 40vh" class="overflow-y-auto">
      <v-card-text>
        <v-list>
          <template v-for="(item, i) in list" :key="`${i}-${item}`">
            <v-divider v-if="i !== 0" :key="`${i}-divider`"></v-divider>

            <v-list-item>
              <v-list-item-title>
                <span>{{ item }}</span>
              </v-list-item-title>
              <template v-slot:append>
                <v-btn name="delete" icon variant="plain" @click="deleteTask(i)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
            </v-list-item>
          </template>
        </v-list>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getVoteInfo, setVoteInfo } from '@/api/fetchDataConsumer'
import type { VoteInfoResponse, VoteInfo } from '@/api/fetchDataConsumer'
import { useUserStore } from '@/stores/user'
import router from '@/router'

const userStore = useUserStore()
const token = userStore.token
const route = useRoute()
const vote_obj = route.params.vote_obj as string
const list = ref<string[]>([])
const tasks = ref<{ text: string }[]>([])
const newTask = ref<string | null>(null)
const loading = ref(true) // 添加 loading 状态

function taskExists(value: string): boolean {
  return tasks.value.some((task) => task.text === value)
}

const taskRules = [(value: string) => !taskExists(value) || '任务已存在']

async function deleteTask(index: number) {
  if (token !== null) {
    const newVoteInfo: VoteInfo = {
      vote_obj: vote_obj,
      list: list.value.filter((_, i) => i !== index)
    }
    try {
      const response = await setVoteInfo(token, newVoteInfo)
      if (response.status === 'success') {
        list.value = list.value.filter((_, i) => i !== index)
      } else {
        console.error('删除投票信息失败:', response.message)
      }
    } catch (error) {
      console.error('删除投票信息失败:', error)
    }
  }
}

async function create() {
  if (newTask.value !== null) {
    if (taskExists(newTask.value)) {
      return
    }
    const newVoteInfo: VoteInfo = {
      vote_obj: vote_obj,
      list: [...list.value, newTask.value]
    }

    try {
      if (token !== null) {
        const response = await setVoteInfo(token, newVoteInfo)
        if (response.status === 'success') {
          list.value.push(newTask.value) // 确保 list 是一个字符串数组
          newTask.value = null
        } else {
          console.error('设置投票信息失败:', response.message)
        }
      }
    } catch (error) {
      console.error('设置投票信息失败:', error)
    }
  }
}

onMounted(async () => {
  if (token) {
    const res: VoteInfoResponse = await getVoteInfo(token)
    const voteInfo = res.result.find((item) => item.vote_obj === vote_obj)
    if (voteInfo) {
      list.value = voteInfo.list
    }
    loading.value = true // 数据加载完成后隐藏骨架屏
  }
})
function goBack() {
  router.push('/manager/settings')
}
</script>

<style scoped>
/* 应用 JetBrains Mono 字体 */
* {
  font-family: 'JetBrains Mono', monospace;
}

.small-unit {
  font-size: 0.4em; /* 调整为你需要的大小 */
}
</style>

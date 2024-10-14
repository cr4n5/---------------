<template>
  <v-container>
    <v-text-field
      v-model="newTask"
      :rules="taskRules"
      label="请输入你要创建的投票或者评分项目"
      variant="solo"
      @keydown.enter="create"
    >
      <template v-slot:append-inner>
        <v-fade-transition>
          <v-btn v-show="newTask" icon="mdi-plus-circle" variant="text" @click="create"></v-btn>
        </v-fade-transition>
      </template>
    </v-text-field>

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
              <v-row>
                <v-col cols="auto">
                  <v-btn name="delete" icon variant="plain" @click="deleteTask(i)">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </v-col>
                <v-col cols="auto">
                  <v-btn name="enter" icon variant="plain" @click="navigateToDetail(task.text)">
                    <v-icon>mdi-arrow-right-box</v-icon>
                  </v-btn>
                </v-col>
              </v-row>
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
import { getVoteInfo, setVoteInfo, restartVote } from '@/api/fetchDataConsumer'
import router from '@/router'
import { restartVoteThird } from '@/api/fetchThirdComputed'
import type { VoteInfoResponse, VoteInfo, restartVoteObj } from '@/api/fetchDataConsumer'
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

const newTask = ref<string | null>(null)
function taskExists(value: string): boolean {
  return tasks.value.some((task) => task.text === value)
}

const taskRules = [(value: string) => !taskExists(value) || '任务已存在']

async function create() {
  if (newTask.value !== null) {
    if (taskExists(newTask.value)) {
      return
    }
    const newVoteInfo: VoteInfo = {
      vote_obj: newTask.value,
      list: [] // 假设新创建的投票项目的列表为空
    }

    try {
      if (token !== null) {
        const response = await setVoteInfo(token, newVoteInfo)
        if (response.status === 'success') {
          tasks.value.push({
            text: newTask.value
          })
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
function deleteTask(index: number) {
  if (token !== null) {
    const restartTask: restartVoteObj = {
      vote_obj: tasks.value[index].text
    }
    restartVote(token, restartTask)
      .then((res) => {
        if (res.status === 'success') {
          tasks.value.splice(index, 1)
        } else {
          console.error('重置投票失败:', res.message)
        }
      })
      .catch((error) => {
        console.error('重置投票失败:', error)
      })
    restartVoteThird(token, restartTask).then((res) => {
      if (res.status === 'success') {
        tasks.value.splice(index, 1)
      } else {
        console.error('重置三方投票失败:', res.message)
      }
    })
  }
}
function navigateToDetail(vote_obj: string) {
  router.push(`/manager/settings/${vote_obj}`)
}
</script>
<style scoped>
/* 应用 JetBrains Mono 字体 */
* {
  font-family: 'JetBrains Mono', monospace;
}
</style>

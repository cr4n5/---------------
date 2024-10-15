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

    <v-card flat v-if="tasks.length > 0" style="max-height: 70vh" class="overflow-y-auto">
      <template v-slot:text>
        <v-text-field
          v-model="search"
          label="Search"
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          hide-details
          single-line
        ></v-text-field>
      </template>
      <v-data-table :headers="headers" :items="tasks" :search="search">
        <template v-slot:[`item.number`]="{ value }">
          <v-chip :color="getColorByNumber(value)">
            {{ value }}
          </v-chip>
        </template>
        <template v-slot:[`item.list`]="{ item }">
          <div>
            <v-chip
              v-for="(option, index) in item.list"
              :key="index"
              :color="getColorByOptionCount(item.list.length)"
              class="ma-1"
            >
              {{ option }}
            </v-chip>
          </div>
        </template>
        <template v-slot:[`item.score`]="{ value }">
          <v-chip :color="getColorByScore(value)">
            {{ value }}
          </v-chip>
        </template>
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon size="small" @click="enter(item)"> mdi-arrow-right-box </v-icon>
        </template>
      </v-data-table>
    </v-card>
    <v-divider class="mb-4"></v-divider>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { getVoteResult } from '@/api/fetchDataConsumer'
const search = ref('')
import router from '@/router'
import type { VoteResultResponse } from '@/api/fetchDataConsumer'
const userStore = useUserStore()
const token = userStore.token

function getColorByNumber(number: number) {
  if (number > 200) return 'darkred'
  else if (number > 150) return 'red'
  else if (number > 100) return 'orange'
  else if (number > 75) return 'yellow'
  else if (number > 50) return 'lightgreen'
  else return 'green'
}

function getColorByScore(score: number) {
  if (score > 2000) return 'darkpurple'
  else if (score > 150) return 'purple'
  else if (score > 100) return 'blue'
  else if (score > 25) return 'lightblue'
  else if (score > 5) return 'grey'
  else return 'lightgrey'
}

function getColorByOptionCount(count: number) {
  if (count > 20) return 'darkpink'
  else if (count > 15) return 'pink'
  else if (count > 10) return 'lightpink'
  else if (count > 7) return 'yellow'
  else if (count > 5) return 'lightyellow'
  else return 'teal'
}

const headers = [
  {
    text: '项目',
    key: 'name',
    sortable: false,
    value: 'name'
  },
  { key: 'vote_obj', title: '项目' },
  { key: 'list', title: '选项' },
  { key: 'score', title: '总共得分' },
  { key: 'number', title: '投票人数' },
  { key: 'actions', title: '操作' }
]

const enter = (item: { vote_obj: string }) => {
  router.push(`/form/${item.vote_obj}`)
}

const tasks = ref<{ vote_obj: string; list: string[]; score: number; number: number }[]>([])
if (token !== null) {
  getVoteResult(token)
    .then((res: VoteResultResponse) => {
      console.log(res)
      if (res.status === 'success' && res.code === 200) {
        tasks.value = Object.keys(res.vote_obj).map((key) => {
          console.log(res.vote_obj[key])
          const item = res.vote_obj[key]
          return {
            vote_obj: key,
            list: Object.keys(item.result),
            score: Object.values(item.result).reduce((acc, curr) => acc + curr, 0),
            number: item.vote_people_number
          }
        })
      } else {
        console.error('获取投票信息失败:', res.message)
      }
    })
    .catch((error) => {
      console.error('获取投票信息失败:', error)
    })
}
</script>

<style scoped>
/* 应用 JetBrains Mono 字体 */
* {
  font-family: 'JetBrains Mono', monospace;
}
</style>

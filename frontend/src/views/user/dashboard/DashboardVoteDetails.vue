<template>
  <v-container>
    <v-row align="center" justify="space-between">
      <v-col>
        <h1 class="text-h4 ps-4">{{ vote_obj }}</h1>
      </v-col>
      <v-col class="d-flex justify-end">
        <v-btn @click="back" variant="plain" icon="mdi-arrow-left" class="me-4"></v-btn>
      </v-col>
    </v-row>
    <v-divider class="mb-4"></v-divider>
    <h2 class="text-h4 text-success ps-4">
      选项:&nbsp;
      <v-fade-transition leave-absolute>
        <span :key="`list-${tasks.length}`">
          {{ tasks.length }}
        </span>
      </v-fade-transition>
    </h2>

    <v-divider class="mb-4"></v-divider>

    <v-card flat v-if="tasks.length > 0" style="max-height: 70vh" class="overflow-y-auto">
      <v-card-title class="d-flex align-center pe-2">
        <v-text-field
          v-model="search"
          label="Search"
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          hide-details
          single-line
        ></v-text-field>
      </v-card-title>
      <v-data-table :headers="headers" :items="tasks" :search="search"> </v-data-table>
    </v-card>
    <v-divider class="mb-4"></v-divider>
  </v-container>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { getVoteResult } from '@/api/fetchDataConsumer'
import { useRoute } from 'vue-router'
const route = useRoute()
const search = ref('')
const vote_obj = route.params.vote_obj as string
import router from '@/router'
import type { VoteResultResponse } from '@/api/fetchDataConsumer'
const userStore = useUserStore()
const token = userStore.token

const headers = [
  {
    text: vote_obj,
    key: 'name',
    sortable: false,
    value: 'name'
  },
  { key: 'option', title: '选项' },
  { key: 'score', title: '得分' }
]
const back = () => {
  router.push(`/form`)
}
const tasks = ref<{ option: string; score: number }[]>([])

if (token !== null) {
  getVoteResult(token)
    .then((res: VoteResultResponse) => {
      if (res.status === 'success' && res.code === 200) {
        tasks.value = Object.keys(res.vote_obj).flatMap((key) => {
          const item = res.vote_obj[key]
          const result = item.result
          return Object.keys(result).map((optionKey) => {
            return {
              option: optionKey,
              score: result[optionKey]
            }
          })
        })
      }
    })
    .catch((error) => {
      console.error(error)
    })
}
</script>
<style scoped>
/* 应用 JetBrains Mono 字体 */
* {
  font-family: 'JetBrains Mono', monospace;
}
</style>

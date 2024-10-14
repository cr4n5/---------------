<template>
  <v-container>
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
                <v-text-field
                  variant="outlined"
                  v-model="score[i]"
                  outlined
                  dense
                  class="small-unit"
                  type="number"
                  min="0"
                  max="100"
                ></v-text-field>
              </template>
            </v-list-item>
          </template>
        </v-list>
      </v-card-text>
    </v-card>
    <v-btn class="mb-4 blurred" block color="transparent" @click="submit"> 提交 </v-btn>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getVoteInfo, getPublicKey } from '@/api/fetchDataConsumer'
import { submitVote } from '@/api/fetchThirdComputed'
import type { VoteInfoResponse, getPublicKeyResponse } from '@/api/fetchDataConsumer'
import type { SubmitVoteRequest } from '@/api/fetchThirdComputed'
import { useUserStore } from '@/stores/user'
import { encrypt } from '@/utils/Paillier'
import router from '@/router'

const userStore = useUserStore()
const score = ref<number[]>([])
const token = userStore.token
const route = useRoute()
const vote_obj = route.params.vote_obj as string
const list = ref<string[]>([])
const publicKey = ref<[bigint, bigint] | null>(null) // 定义 publicKey
onMounted(async () => {
  if (token) {
    const res: VoteInfoResponse = await getVoteInfo(token)
    const voteInfo = res.result.find((item) => item.vote_obj === vote_obj)
    const publicKeyResponse: getPublicKeyResponse = await getPublicKey(token)
    if (voteInfo) {
      list.value = voteInfo.list
      score.value = Array(list.value.length).fill(0)
    } else {
      console.error('未找到该投票')
    }
    if (publicKeyResponse.status === 'success') {
      const key = publicKeyResponse.key[vote_obj]
      if (key) {
        publicKey.value = [BigInt(key[0]), BigInt(key[1])]
      } else {
        publicKey.value = null
      }
    }
  }
})

const data = ref<SubmitVoteRequest>({
  vote_obj,
  vote: {},
  username: userStore.username,
  pubkey: [BigInt(0), BigInt(0)]
})

async function submit() {
  if (token) {
    const key = publicKey.value

    if (key) {
      list.value.forEach((item, index) => {
        const m = BigInt(score.value[index])
        data.value.vote[item] = encrypt(key, m)
      })
      data.value.pubkey = key
      const res = await submitVote(token, data.value)
      if (res.status === 'success') {
        router.push('/vote')
      } else {
        console.error('提交失败')
      }
    } else {
      console.error('公钥未找到')
    }
  }
}

function goBack() {
  router.push('/vote')
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

.blurred {
  backdrop-filter: blur(20px);
}
</style>

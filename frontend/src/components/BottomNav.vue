<template>
  <v-bottom-navigation v-model="value" class="blurred" mode="shift">
    <v-btn v-for="(btn, index) in buttons" :key="index" :to="btn.to">
      <v-icon>{{ btn.icon }}</v-icon>
      <span>{{ btn.label }}</span>
    </v-btn>
  </v-bottom-navigation>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

const value = ref(1)
const buttons = [
  { to: { name: 'home' }, icon: 'mdi-home', label: 'Home' },
  { to: { name: 'vote' }, icon: 'mdi-vote', label: 'Vote' },
  { to: { name: 'dashboard' }, icon: 'mdi-view-dashboard', label: 'Dashboard' }
]

const color = computed(() => {
  switch (value.value) {
    case 0:
      return 'blue-grey'
    case 1:
      return 'teal'
    case 2:
      return 'brown'
    case 3:
      return 'indigo'
    default:
      return 'blue-grey'
  }
})
</script>

<style lang="css" scoped>
.blurred {
  backdrop-filter: blur(20px);
  background-color: rgba(255, 255, 255, 0.1); /* 可调整透明度 */
}
</style>

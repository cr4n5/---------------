<template>
  <v-container>
    <v-text-field
      v-model="newTask"
      label="请选择你要投票的人"
      variant="solo"
      @keydown.enter="create"
      disabled
    >
      <template v-slot:append-inner>
        <v-fade-transition>
          <v-btn v-show="newTask" icon="mdi-plus-circle" variant="text" @click="create"></v-btn>
        </v-fade-transition>
      </template>
    </v-text-field>

    <h2 class="text-h4 text-success ps-4">
      选项:&nbsp;
      <v-fade-transition leave-absolute>
        <span :key="`tasks-${tasks.length}`">
          {{ tasks.length }}
        </span>
      </v-fade-transition>
    </h2>

    <v-divider class="mt-4"></v-divider>

    <v-row align="center" class="my-1">
      <strong class="mx-4 text-info-darken-2"> 未选中: {{ remainingTasks }} </strong>

      <v-divider vertical></v-divider>

      <strong class="mx-4 text-success-darken-2"> 已选中: {{ completedTasks }} </strong>

      <v-spacer></v-spacer>

      <v-progress-circular v-model="progress" class="me-2"></v-progress-circular>
    </v-row>

    <v-divider class="mb-4"></v-divider>

    <v-card v-if="tasks.length > 0" style="max-height: 200px" class="overflow-y-auto">
      <v-slide-y-transition class="py-0" tag="v-list" group>
        <template v-for="(task, i) in tasks" :key="`${i}-${task.text}`">
          <v-divider v-if="i !== 0" :key="`${i}-divider`"></v-divider>

          <v-list-item @click="task.done = !task.done">
            <template v-slot:prepend>
              <v-checkbox-btn v-model="task.done" color="grey"></v-checkbox-btn>
            </template>

            <v-list-item-title>
              <span :class="task.done ? 'text-grey' : 'text-primary'">{{ task.text }}</span>
            </v-list-item-title>

            <template v-slot:append>
              <v-expand-x-transition>
                <v-icon v-if="task.done" color="success"> mdi-check </v-icon>
              </v-expand-x-transition>
            </template>
          </v-list-item>
        </template>
      </v-slide-y-transition>
    </v-card>
    <v-divider class="mb-4"></v-divider>

    <v-btn class="mb-4" block color="success" @click="create"> 提交 </v-btn>
  </v-container>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue'

const tasks = ref([
  {
    done: false,
    text: 'Foobar'
  },
  {
    done: false,
    text: 'Fizzbuzz'
  }
])
const newTask = ref<string | null>(null)

const completedTasks = computed(() => {
  return tasks.value.filter((task) => task.done).length
})
const progress = computed(() => {
  return (completedTasks.value / tasks.value.length) * 100
})
const remainingTasks = computed(() => {
  return tasks.value.length - completedTasks.value
})

function create() {
  if (newTask.value !== null) {
    tasks.value.push({
      done: false,
      text: newTask.value
    })
    newTask.value = null
  }
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

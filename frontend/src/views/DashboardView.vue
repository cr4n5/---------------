<template>
  <v-container grid-list-xs>
    <DashboardBlock
      title="票数"
      subtitle="统计到的参与投票的总票数"
      mdi-icon="mdi-vote"
      mdi-icon-color="green"
      subtitle-icon="mdi-ticket"
      subtitle-icon-color="green"
      text="514"
      text-unit="票"
    />
    <v-spacer class="mb-4" />
    <DashboardBlock
      title="投票人数"
      subtitle="参与投票人数总计"
      mdi-icon="mdi-human"
      subtitle-icon-color="brown"
      subtitle-icon="mdi-account-group"
      mdi-icon-color="brown"
      text="114"
      text-unit="人"
    />
  </v-container>
</template>

<script setup lang="ts">
import DashboardBlock from '@/components/DashboardBlock.vue'
</script>

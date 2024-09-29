<template>
  <v-row>
    <v-col>
      <DashboardBlock
        title="票数"
        subtitle="统计到的参与投票的总票数"
        mdi-icon="mdi-vote"
        mdi-icon-color="green"
        subtitle-icon="mdi-note-edit"
        text="514"
        text-unit="票"
      />
    </v-col>
    <v-col>
      <DashboardBlock
        title="投票人数"
        subtitle="参与投票人数总计"
        mdi-icon="mdi-human"
        subtitle-icon="mdi-account-group"
        mdi-icon-color="brown"
        text="114"
        text-unit="人"
      />
    </v-col>
  </v-row>
</template>

<script setup>
import DashboardBlock from '@/components/DashboardBlock.vue'
</script>

<template>
  <v-row>
    <v-col>
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
    </v-col>
    <v-divider class="border-opacity-0"></v-divider>
    <v-col>
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
    </v-col>
  </v-row>
  <v-divider class="border-opacity-0"></v-divider>
  <v-row>
    <v-col>
      <DashboardBlock
        title="今日新增票数"
        subtitle="今天新增的投票数"
        mdi-icon="mdi-vote-outline"
        mdi-icon-color="blue"
        subtitle-icon="mdi-calendar-today"
        subtitle-icon-color="blue"
        text="50"
        text-unit="票"
      />
    </v-col>

    <v-col>
      <DashboardBlock
        title="今日新增用户"
        subtitle="今天新增的用户数"
        mdi-icon="mdi-account-plus"
        mdi-icon-color="purple"
        subtitle-icon="mdi-calendar-today"
        subtitle-icon-color="purple"
        text="10"
        text-unit="人"
      />
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import DashboardBlock from '@/components/DashboardBlock.vue'
</script>

<template>
  <v-card variant="tonal" class="mx-auto" max-width="368">
    <v-card-item :title="props.title">
      <template v-slot:subtitle>
        <v-icon
          class="me-1 pb-1"
          :color="props.subtitleIconColor"
          :icon="props.subtitleIcon"
          size="18"
        ></v-icon>

        {{ props.subtitle }}
      </template>
    </v-card-item>

    <v-card-text class="py-0">
      <v-row align="center" no-gutters>
        <v-col class="text-h2" cols="6">
          {{ props.text }}
          <span class="small-unit">{{ props.textUnit }}</span>
        </v-col>

        <v-col class="text-right" cols="6">
          <v-icon :color="props.mdiIconColor" :icon="props.mdiIcon" size="88" />
        </v-col>
      </v-row>
    </v-card-text>

    <div class="d-flex py-3 justify-space-between"></div>

    <v-divider></v-divider>
  </v-card>
</template>

<script setup lang="ts">
interface TextProps {
  text: string
  textUnit: string
}

interface TitleProps {
  title: string
}

interface SubtitleProps {
  subtitle: string
  subtitleIcon: string
  subtitleIconColor: string
}

interface IconProps {
  mdiIcon: string
  mdiIconColor: string
}

type Props = TextProps & TitleProps & SubtitleProps & IconProps

const props = defineProps<Props>()
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

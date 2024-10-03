<template>
  <v-container class="pa-4">
    <!-- 页面标题 -->
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="pa-4">
          <v-card-title class="headline">
            <v-icon left>mdi-account-circle</v-icon>
            联系我们
          </v-card-title>
          <v-card-subtitle>通过以下方式与我们联系</v-card-subtitle>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="4" class="text-center">
                <v-avatar size="120">
                  <img
                    src="https://avatars.githubusercontent.com/sd0ric4"
                    alt="GitHub Avatar"
                    class="avatar-img"
                  />
                </v-avatar>
                <p class="mt-2">sd0ric4</p>
              </v-col>
              <v-col cols="12" md="8">
                <v-list dense>
                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon>mdi-github</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>
                        <a href="https://github.com/sd0ric4" target="_blank">GitHub</a>
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon>mdi-email</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>35507187ch405@gmail.com</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon>mdi-phone</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>+195 4919 1273</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts"></script>

<style scoped>
.pa-4 {
  padding: 16px;
}
.text-center {
  text-align: center;
}
.mt-2 {
  margin-top: 8px;
}
.avatar-img {
  width: 100%;
  height: auto;
  max-width: 80px; /* 确保图片不会超过 v-avatar 的大小 */
  border-radius: 50%;
  object-fit: cover;
}
.blurred {
  backdrop-filter: blur(20px);
}
</style>

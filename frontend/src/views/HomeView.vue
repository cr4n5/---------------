<template>
  <v-container class="pa-4">
    <!-- 页面标题 -->
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="pa-4">
          <v-card-title class="headline">
            <v-icon left>mdi-information</v-icon>
            欢迎来到我们的介绍页面
          </v-card-title>
          <v-card-subtitle>了解更多关于我们的信息</v-card-subtitle>
          <v-card-text>
            <p>
              我们致力于提供最好的服务和产品。我们的团队由经验丰富的专业人士组成，致力于为客户提供卓越的体验。
            </p>
            <p>
              请浏览我们的页面，了解更多关于我们的信息。如果您有任何问题或需要进一步的帮助，请随时与我们联系。
            </p>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="navigateToContact">
              <v-icon left>mdi-phone</v-icon>
              联系我们
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- 同态加密投票系统介绍 -->
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="pa-4">
          <v-card-title class="headline">
            <v-icon left>mdi-lock</v-icon>
            同态加密投票系统
          </v-card-title>
          <v-card-subtitle>安全且隐私保护的投票解决方案</v-card-subtitle>
          <v-card-text>
            <p>
              同态加密是一种加密技术，允许在加密数据上执行计算，而无需先解密数据。这种技术在投票系统中具有重要应用，因为它可以确保投票的隐私和安全。
            </p>
            <p>
              在同态加密投票系统中，选民的投票会被加密，然后在加密状态下进行计票。这样可以防止任何人在计票过程中窥探选民的选择。
            </p>
            <p>该系统的主要优点包括：</p>
            <ul>
              <li>
                <v-icon left>mdi-check-circle</v-icon>
                <strong>隐私保护：</strong> 选民的投票在整个过程中保持加密状态，确保隐私。
              </li>
              <li>
                <v-icon left>mdi-check-circle</v-icon>
                <strong>安全性：</strong>
                由于投票数据是加密的，任何人都无法在未经授权的情况下篡改投票结果。
              </li>
            </ul>
            <p>
              我们的同态加密投票系统采用了最新的加密技术，确保每一张选票的安全和隐私。我们致力于为客户提供最安全、最可靠的投票解决方案。
            </p>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="navigateToContact">
              <v-icon left>mdi-phone</v-icon>
              联系我们
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateToContact = () => {
  router.push({ name: 'contactus' })
}
</script>

<style scoped>
.pa-4 {
  padding: 16px;
}
</style>

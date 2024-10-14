<template>
  <v-app-bar prominent color="transparent" class="blurred">
    <template v-slot:prepend>
      <v-app-bar-nav-icon
        :icon="!drawer ? 'mdi-menu' : 'mdi-close'"
        variant="text"
        @click.stop="drawer = !drawer"
      ></v-app-bar-nav-icon>
    </template>
    <template v-slot:append>
      <schema-switch-button />
    </template>

    <v-app-bar-title id="code-blocks">{{ currentTitle }}</v-app-bar-title>
  </v-app-bar>
  <v-navigation-drawer
    color="transparent"
    class="blurred"
    v-model="drawer"
    :location="$vuetify.display.mobile ? 'bottom' : undefined"
    temporary
  >
    <template v-slot:prepend>
      <v-list-item
        lines="two"
        prepend-avatar="https://alist.dn11.ch405.icu/d/home/share_files/glasswear_tressia.jpg?sign=hDNoqmMup0mR2E_B7dklBGkejFE84VFRRUlC1HtY_kQ=:0"
        subtitle="Logged in"
        :title="userName"
      ></v-list-item>
    </template>
    <v-divider></v-divider>
    <v-list>
      <v-list-item
        v-for="item in items"
        :key="item.value"
        :to="item.link"
        :prepend-icon="item.icon"
        @click="selectItem(item)"
      >
        <v-list-item-title>{{ item.title }}</v-list-item-title>
      </v-list-item>
    </v-list>
    <template v-slot:append>
      <div class="pa-2">
        <v-btn block color="transparent" class="blurred" @click="Logout">
          <v-icon>mdi-logout</v-icon>
          退出登录
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
import { ref, watch, type Ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import SchemaSwitchButton from '../SchemaSwitchButton.vue'
// 如果用户名为null，默认terrasia
const userName = useUserStore().username || 'terrasia'
// 退出登录,然后跳转到登录页面
const Logout = () => {
  useUserStore().logout()
  router.push({ name: 'login' })
}
interface Item {
  title: string
  value: string
  link: string
  icon?: string
}

const items: Item[] = [
  {
    title: 'home',
    value: '首页',
    link: '/manager/home',
    icon: 'mdi-home'
  },
  {
    title: 'settings',
    value: '设置',
    link: '/manager/settings',
    icon: 'mdi-cog'
  },
  {
    title: 'dashboard',
    value: '仪表盘',
    link: '/manager/dashboard',
    icon: 'mdi-view-dashboard'
  }
]

const drawer: Ref<boolean> = ref(false)
const currentTitle: Ref<string> = ref('') // 初始化为空字符串

const route = useRoute()
const router = useRouter()

// 根据当前路由设置 currentTitle
const updateTitle = () => {
  const currentItem = items.find((item) => item.link === route.path)
  if (currentItem) {
    currentTitle.value = currentItem.value
  }
}

// 监听路由变化
watch(route, updateTitle, { immediate: true })

const selectItem = (item: Item) => {
  currentTitle.value = item.value
  drawer.value = false
  router.push(item.link)
}

updateTitle() // 初始化时调用一次
</script>

<style lang="css" scoped>
.blurred {
  backdrop-filter: blur(20px);
}
</style>

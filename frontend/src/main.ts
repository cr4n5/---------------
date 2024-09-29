import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Components

// Import the icons you need
import '@mdi/font/css/materialdesignicons.css' // Ensure you are using css-loader

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi' // This is already the default value - only for display purposes
  },
  theme: {
    defaultTheme: window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  }
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vuetify)

app.mount('#app')

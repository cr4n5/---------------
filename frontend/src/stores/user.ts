import { defineStore } from 'pinia'

// 设置了24小时的过期时间
const USERNAME_KEY = 'username'
const TIMESTAMP_KEY = 'timestamp'
const EXPIRATION_TIME = 24 * 60 * 60 * 1000 // 24 hours in milliseconds

export const useUserStore = defineStore('user', {
  state: () => ({
    username: getUsernameFromLocalStorage()
  }),
  actions: {
    login(username: string) {
      this.username = username
      localStorage.setItem(USERNAME_KEY, username)
      localStorage.setItem(TIMESTAMP_KEY, Date.now().toString())
    },
    logout() {
      this.username = null
      localStorage.removeItem(USERNAME_KEY)
      localStorage.removeItem(TIMESTAMP_KEY)
    }
  },
  getters: {
    isLoggedIn: (state) => !!state.username
  }
})

function getUsernameFromLocalStorage(): string | null {
  const username = localStorage.getItem(USERNAME_KEY)
  const timestamp = localStorage.getItem(TIMESTAMP_KEY)

  if (username && timestamp) {
    const currentTime = Date.now()
    const savedTime = parseInt(timestamp, 10)

    if (currentTime - savedTime < EXPIRATION_TIME) {
      return username
    } else {
      localStorage.removeItem(USERNAME_KEY)
      localStorage.removeItem(TIMESTAMP_KEY)
    }
  }

  return null
}

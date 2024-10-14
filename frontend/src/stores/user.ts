import { defineStore } from 'pinia'
import { jwtDecode } from 'jwt-decode'

const TOKEN_KEY = 'jwt_token'

export const useUserStore = defineStore('user', {
  state: () => {
    const token = getTokenFromLocalStorage()
    let isAdmin = false

    if (token) {
      try {
        const decodedToken: any = jwtDecode(token)
        isAdmin = decodedToken.isAdmin
      } catch (error) {
        console.error('Failed to decode token:', error)
      }
    }

    return {
      token,
      isAdmin
    }
  },
  actions: {
    login(token: string) {
      this.token = token
      const decodedToken: any = jwtDecode(token)
      this.isAdmin = decodedToken.isAdmin
      localStorage.setItem(TOKEN_KEY, token)
    },
    logout() {
      this.token = null
      this.isAdmin = false
      localStorage.removeItem(TOKEN_KEY)
    }
  },
  getters: {
    isLoggedIn: (state) => !!state.token,
    username: (state) => {
      if (state.token) {
        try {
          const decodedToken: any = jwtDecode(state.token)
          return decodedToken.username
        } catch (e) {
          return null
        }
      }
      return null
    }
  }
})

function getTokenFromLocalStorage(): string | null {
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) {
    try {
      const decodedToken: any = jwtDecode(token)
      const currentTime = Date.now() / 1000
      if (decodedToken.exp > currentTime) {
        return token
      } else {
        localStorage.removeItem(TOKEN_KEY)
      }
    } catch (e) {
      console.error('Error decoding', e)
      localStorage.removeItem(TOKEN_KEY)
    }
  }
  return null
}

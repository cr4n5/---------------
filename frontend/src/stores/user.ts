import { defineStore } from 'pinia'
import { jwtDecode } from 'jwt-decode'

const TOKEN_KEY = 'jwt_token'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: getTokenFromLocalStorage(),
    isAdmin: false
  }),
  actions: {
    login(token: string) {
      this.token = token
      const decodedToken: any = jwtDecode(token)
      console.log('exp', decodedToken.exp)
      this.isAdmin = decodedToken.isAdmin
      localStorage.setItem(TOKEN_KEY, token)
      console.log('Logged in as', decodedToken.username)
    },
    logout() {
      this.token = null
      this.isAdmin = false
      localStorage.removeItem(TOKEN_KEY)
      console.log('Logged out')
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
      console.log('exp', decodedToken.exp)
      const currentTime = Date.now() / 1000
      if (decodedToken.exp > currentTime) {
        console.log('Token is still valid')
        return token
      } else {
        console.log('Token has expired')
        localStorage.removeItem(TOKEN_KEY)
      }
    } catch (e) {
      console.error('Error decoding', e)
      localStorage.removeItem(TOKEN_KEY)
    }
  }
  return null
}

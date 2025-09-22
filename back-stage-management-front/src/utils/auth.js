import { checkAuthStatus } from '@/api/login';
import store from '@/store'

export async function checkAuth() {
  try {
    const res = await checkAuthStatus()
    store.commit('LoginModule/setUserInfo', res.data.user)
  } catch (err) {
  }
}
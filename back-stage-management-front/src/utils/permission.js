import store from '@/store'

export function hasPermission(code) {
    const codes = store.getters['permission/permissionCodes']
    return codes.includes(code)
}

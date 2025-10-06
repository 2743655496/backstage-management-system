import ajax from "@/api/ajax"
import base from "@/api/base"

export const getUsers = (params) => {
  return ajax.get(base.get_users, { params })
}

export const toDeleteUser = (id) => {
  return ajax.post(`${base.delete_user}${id}/`, { action: 'delete' })
}

export const toEnableUser = (id) => {
  return ajax.post(`${base.delete_user}${id}/`, { action: 'enable' })
}

export const toDisableUser = (id) => {
  return ajax.post(`${base.delete_user}${id}/`, { action: 'disable' })
}

export const toAddUser = (params) => {
  return ajax.post(base.add_user, params)
}

export const toUpdateUser = (id, params) => {
  return ajax.post(`${base.update_user}${id}/`, params)
}

export const toGetUserDetail = (id) => {
  return ajax.get(`${base.get_user_detail}${id}/`)
}
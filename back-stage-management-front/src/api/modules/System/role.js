import ajax from "@/api/ajax"
import base from "@/api/base"
import qs from 'qs'; 

export const getRoles = (params) => {
  return ajax.get(base.get_roles,{params});
}

export const toDeleteRole = (id) => {
  return ajax.post(`${base.delete_role}${id}/`)
}

export const toGetRoleDetail = (id) => {
  return ajax.get(`${base.get_role_detail}${id}/`)
}

export const toAddRole = (params) => {
  return ajax.post(`${base.add_role}`, params)
}

export const toUpdateRole = (id, params) => {
  return ajax.post(`${base.update_role}${id}/`, params)
}
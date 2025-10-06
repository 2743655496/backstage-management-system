import ajax from "@/api/ajax"
import base from "@/api/base"

export const getPermissions = () => {
  return ajax.get(base.get_permissions);
}

export const toDeletePermission = (id) => {
  return ajax.post(`${base.delete_permission}${id}/`)
}

export const toAddPermission = (params) => {
  return ajax.post(`${base.add_permission}`, params)
}

export const toUpdatePermission = (id, params) => {
  return ajax.post(`${base.update_permission}${id}/`, params)
}

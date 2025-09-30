import ajax from "../ajax"
import base from "../base"

export const getPermissions = () => {
  return ajax.get(base.get_permissions);
}

export const toDeletePermission = (id) => {
  return ajax.post(`${base.delete_permission}${id}/`)
}

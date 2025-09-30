import ajax from "../ajax"
import base from "../base"

export const getMenus = () => {
  return ajax.get(base.get_menu);
}

export const toAddMenu = (params) => {
  return ajax.post(base.add_menu, params)
}

export const toUpdateMenu = (id,params) => {
  return ajax.post(`${base.update_menu}${id}/`, params)
}

export const toDeleteMenu = (id) => {
  return ajax.post(`${base.delete_menu}${id}/`)
}

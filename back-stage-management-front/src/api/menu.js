import ajax from "./ajax"
import base from "./base"

export const getMenus = () => {
  return ajax.get(base.get_menu);
}

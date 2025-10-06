import ajax from "@/api/ajax"
import base from "@/api/base"

export const getDepartments = () => {
  return ajax.get(base.get_departments);
}

export const getDepartmentPrincipal = () => {
  return ajax.get(base.get_department_principal);
}

export const toDeleteDepartment = (id) => {
  return ajax.post(`${base.delete_department}${id}/`)
}

export const toAddDepartment = (params) => {
  return ajax.post(`${base.add_department}`, params)
}

export const toUpdateDepartment = (id, params) => {
  return ajax.post(`${base.update_department}${id}/`, params)
}

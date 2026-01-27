/**
 * v-permission 权限指令（增强版）
 *
 * ⭐ 支持三种模式：
 * 
 * 1. OR（默认）—— 只要拥有任意一个权限即可显示
 *    <el-button v-permission="['user:add', 'user:update']">按钮</el-button>
 *
 * 2. AND —— 必须同时拥有所有权限才显示
 *    <el-button v-permission="{ mode: 'and', codes: ['user:add', 'user:update'] }">
 *      按钮
 *    </el-button>
 *
 * 3. NOT —— 当用户完全没有这些权限时显示（反向权限）
 *    <el-button v-permission="{ mode: 'not', codes: ['user:delete'] }">
 *      按钮
 *    </el-button>
 *
 * ⭐ 支持两种写法：
 *    - 直接传数组（默认 OR 模式）
 *    - 传对象（可指定 mode）
 *
 * ⭐ 自动从 Vuex 的 PermissionModule 中读取 permissionCodes
 */

import store from '@/store'

export default {
  inserted(el, binding) {
    const permissionCodes = store.getters['PermissionModule/permissionCodes']

    let mode = 'or'
    let codes = []

    /**
     * 解析指令参数
     * 
     * 支持：
     *   v-permission="['a','b']"
     *   v-permission="{ mode:'and', codes:['a','b'] }"
     */
    if (Array.isArray(binding.value)) {
      // 写法：v-permission="['a','b']"
      codes = binding.value
    } else if (typeof binding.value === 'object' && binding.value !== null) {
      // 写法：v-permission="{ mode:'and', codes:['a','b'] }"
      mode = binding.value.mode || 'or'
      codes = binding.value.codes || []
    } else {
      throw new Error("v-permission expects an array or object")
    }

    if (!Array.isArray(codes) || codes.length === 0) {
      throw new Error("v-permission requires a non-empty code list")
    }

    let hasPermission = false

    /**
     * 权限判断逻辑
     */
    if (mode === 'or') {
      // ⭐ OR 模式：任意一个权限命中即可显示
      hasPermission = codes.some(code => permissionCodes.includes(code))

    } else if (mode === 'and') {
      // ⭐ AND 模式：必须全部权限命中才显示
      hasPermission = codes.every(code => permissionCodes.includes(code))

    } else if (mode === 'not') {
      // ⭐ NOT 模式：全部权限都不命中才显示
      hasPermission = codes.every(code => !permissionCodes.includes(code))

    } else {
      throw new Error("v-permission mode must be 'or', 'and', or 'not'")
    }

    /**
     * 无权限 → 从 DOM 移除元素
     */
    if (!hasPermission) {
      el.parentNode && el.parentNode.removeChild(el)
    }
  }
}

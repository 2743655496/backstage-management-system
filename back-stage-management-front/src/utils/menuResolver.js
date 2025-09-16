/**
 * 根据路径从菜单树中解析出当前菜单层级和标签菜单项
 * @param {Array} menuTree - 完整的菜单结构数组
 * @param {String} targetPath - 当前路由路径
 * @returns {Object|null} 包含 currentMenu 和 tabMenu 的对象，或 null
 */
export function resolveMenuPath(menuTree, targetPath) {
  for (const parent of menuTree) {
    if (parent.children && parent.children.length > 0) {
      const child = parent.children.find(c => c.path === targetPath)
      if (child) {
        return {
          currentMenu: [parent, child],
          tabMenu: child
        }
      }
    } else if (parent.path === targetPath) {
      return {
        currentMenu: [parent],
        tabMenu: parent
      }
    }
  }
  return null
}

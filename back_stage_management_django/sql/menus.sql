INSERT INTO `menus` (
    `id`,
    `parent_id`,
    `name`,
    `icon`,
    `path`,
    `component`,
    `sort`,
    `visible`,
    `status`,
    `creator_id`,
    `create_time`,
    `update_time`,
    `is_deleted`
) VALUES
(1, 0, '概览', 'el-icon-menu', '/dashboard', 'Layout', 0, 1, 1, 1, '2025-09-11 21:01:14', '2025-09-11 21:01:16', 0),
(2, 1, '分析页', 'el-icon-s-data', '/dashboard/analysis', 'dashboard/analysis', 0, 1, 1, 1, '2025-09-11 21:14:50', '2025-09-11 21:14:55', 0),
(3, 1, '工作台', 'el-icon-s-cooperation', '/dashboard/workbench', 'dashboard/workbench', 1, 1, 1, 1, '2025-09-11 21:15:47', '2025-09-11 21:15:50', 0),
(4, 0, '系统管理', 'el-icon-setting', '/system', 'Layout', 1, 1, 1, 1, '2025-09-11 21:16:33', '2025-09-11 21:16:36', 0),
(5, 4, '角色管理', 'el-icon-user-solid', '/system/role', 'system/role', 0, 1, 1, 1, '2025-09-11 21:18:47', '2025-09-11 21:18:49', 0),
(6, 4, '部门管理', 'el-icon-s-platform', '/system/department', 'system/department', 1, 1, 1, 1, '2025-09-11 21:19:37', '2025-09-11 21:19:40', 0),
(7, 4, '用户管理', 'el-icon-user', '/system/user', 'system/user', 2, 1, 1, 1, '2025-09-11 21:20:27', '2025-09-11 21:20:30', 0),
(8, 4, '权限管理', 'el-icon-s-grid', '/system/permission', 'system/permission', 3, 1, 1, 1, '2025-09-11 21:21:14', '2025-09-11 21:21:19', 0),
(9, 4, '菜单管理', 'iconfont icon-caidanguanli', '/system/menu', 'system/menu', 4, 1, 1, 1, '2025-09-17 12:09:53', '2025-09-17 12:09:57', 0);

-- ========================
-- 1. 建表语句
-- ========================

CREATE TABLE `departments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL UNIQUE COMMENT '部门名称',
  `parent_id` bigint NOT NULL DEFAULT 0 COMMENT '父部门ID',
  `code` varchar(50) NOT NULL UNIQUE COMMENT '部门编码',
  `description` text COMMENT '部门描述',
  `manager_id` bigint DEFAULT NULL COMMENT '部门负责人ID',
  `sort` int NOT NULL DEFAULT 0 COMMENT '排序',
  `status` smallint NOT NULL DEFAULT 1 COMMENT '状态',
  `creator_id` bigint DEFAULT NULL COMMENT '创建人ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` smallint NOT NULL DEFAULT 0 COMMENT '删除标志',
  PRIMARY KEY (`id`),
  INDEX (`name`),
  INDEX (`code`),
  INDEX (`parent_id`),
  INDEX (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='部门';

CREATE TABLE `roles` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL UNIQUE COMMENT '角色名称',
  `code` varchar(50) NOT NULL UNIQUE COMMENT '角色编码',
  `description` text COMMENT '角色描述',
  `status` smallint NOT NULL DEFAULT 1 COMMENT '状态',
  `creator_id` bigint DEFAULT NULL COMMENT '创建人ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` smallint NOT NULL DEFAULT 0 COMMENT '删除标志',
  PRIMARY KEY (`id`),
  INDEX (`name`),
  INDEX (`code`),
  INDEX (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色';

CREATE TABLE `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL UNIQUE COMMENT '用户名',
  `password` varchar(255) NOT NULL COMMENT '密码',
  `real_name` varchar(50) DEFAULT NULL COMMENT '真实姓名',
  `email` varchar(100) DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像',
  `department_id` bigint DEFAULT NULL COMMENT '所属部门ID',
  `status` smallint NOT NULL DEFAULT 1 COMMENT '状态',
  `last_login_time` datetime DEFAULT NULL COMMENT '最后登录时间',
  `last_login_ip` varchar(50) DEFAULT NULL COMMENT '最后登录IP',
  `creator_id` bigint DEFAULT NULL COMMENT '创建人ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` smallint NOT NULL DEFAULT 0 COMMENT '删除标志',
  PRIMARY KEY (`id`),
  INDEX (`username`),
  INDEX (`department_id`),
  INDEX (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户';

CREATE TABLE `user_roles` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `role_id` bigint NOT NULL COMMENT '角色ID',
  `creator_id` bigint DEFAULT NULL COMMENT '创建人ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_user_role` (`user_id`,`role_id`),
  INDEX (`user_id`),
  INDEX (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户角色关联';

CREATE TABLE `menus` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `parent_id` bigint NOT NULL DEFAULT 0 COMMENT '父菜单ID',
  `name` varchar(50) NOT NULL COMMENT '菜单名称',
  `icon` varchar(50) DEFAULT NULL COMMENT '菜单图标',
  `path` varchar(100) DEFAULT NULL COMMENT '路由路径',
  `component` varchar(100) DEFAULT NULL COMMENT '组件路径',
  `sort` int NOT NULL DEFAULT 0 COMMENT '排序',
  `visible` smallint NOT NULL DEFAULT 1 COMMENT '是否显示',
  `status` smallint NOT NULL DEFAULT 1 COMMENT '状态',
  `creator_id` bigint DEFAULT NULL COMMENT '创建人ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` smallint NOT NULL DEFAULT 0 COMMENT '删除标志',
  PRIMARY KEY (`id`),
  INDEX (`parent_id`),
  INDEX (`sort`),
  INDEX (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='菜单';

CREATE TABLE `permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL COMMENT '权限名称',
  `code` varchar(100) NOT NULL UNIQUE COMMENT '权限标识',
  `description` text COMMENT '权限描述',
  `type` smallint NOT NULL COMMENT '权限类型',
  `menu_id` bigint DEFAULT NULL COMMENT '关联菜单ID',
  `parent_id` bigint NOT NULL DEFAULT 0 COMMENT '父权限ID',
  `api_method` varchar(10) DEFAULT NULL COMMENT '接口方法',
  `api_path` varchar(255) DEFAULT NULL COMMENT '接口路径',
  `status` smallint NOT NULL DEFAULT 1 COMMENT '状态',
  `creator_id` bigint DEFAULT NULL COMMENT '创建人ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` smallint NOT NULL DEFAULT 0 COMMENT '删除标志',
  PRIMARY KEY (`id`),
  INDEX (`code`),
  INDEX (`type`),
  INDEX (`menu_id`),
  INDEX (`parent_id`),
  INDEX (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='权限';

CREATE TABLE `role_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role_id` bigint NOT NULL COMMENT '角色ID',
  `permission_id` bigint NOT NULL COMMENT '权限ID',
  `creator_id` bigint DEFAULT NULL COMMENT '创建人ID',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_role_permission` (`role_id`,`permission_id`),
  INDEX (`role_id`),
  INDEX (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色权限关联';

-- ========================
-- 2. 初始化数据
-- ========================

-- 角色
INSERT INTO `roles` (`name`, `code`, `description`) VALUES
('超级管理员', 'super_admin', '系统最高权限'),
('管理员', 'admin', '系统管理权限'),
('普通员工', 'staff', '普通用户权限');

-- 用户（密码这里建议用加密后的值，这里示例为明文123456）
INSERT INTO `users` (`username`, `password`, `real_name`, `email`, `status`)
VALUES ('superadmin', '123456', '超级管理员', 'admin@example.com', 1);

-- 用户角色绑定（假设超级管理员用户ID=1，超级管理员角色ID=1）
INSERT INTO `user_roles` (`user_id`, `role_id`) VALUES (1, 1);

-- 菜单
INSERT INTO `menus` (`parent_id`, `name`, `icon`, `path`, `component`, `sort`) VALUES
(0, '概览', 'dashboard', '/dashboard', 'Layout', 1),
(1, '分析页', 'analysis', '/dashboard/analysis', 'dashboard/analysis', 1),
(1, '工作台', 'workbench', '/dashboard/workbench', 'dashboard/workbench', 2),
(0, '系统管理', 'system', '/system', 'Layout', 2),
(4, '角色管理', 'role', '/system/role', 'system/role', 1),
(4, '部门管理', 'department', '/system/department', 'system/department', 2),
(4, '用户管理', 'user', '/system/user', 'system/user', 3),
(4, '权限管理', 'permission', '/system/permission', 'system/permission', 4);

-- 权限（type=1 表示菜单权限）
INSERT INTO `permissions` (`name`, `code`, `type`, `menu_id`) VALUES
('概览-访问', 'menu:dashboard', 1
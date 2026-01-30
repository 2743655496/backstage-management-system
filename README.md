# 后台管理

## 介绍
自己开发着玩的一个后台管理项目

## 技术栈

```
前端（back-stage-management-front）
- Vue.js 2.x
- Vue Router / Vuex
- Axios
- Node.js v18.12.1
- Webpack

后端（back_stage_management_django）
- Python 3.12
- Django 5.0.3
- Django REST Framework
- Redis
- MySQL
```

## 环境要求

| 组件    | 版本     |
| ------- | -------- |
| Node.js | v18.12.1 |
| Python  | 3.12     |
| Django  | 5.0.3    |



## JWT 与 HTTPS 开发环境说明

### 1. JWT 存储方式：HttpOnly Cookie

本项目采用 **HttpOnly Cookie** 存储 JWT，以提升安全性并防止 XSS 攻击。

#### 设计原则

- **access_token** 存储在 HttpOnly Cookie 中
  - 前端无法通过 JavaScript 读取
  - 浏览器会自动随请求发送
- 后端 Django 通过 `request.COOKIES['access_token']` 获取 token
- 前端 Axios 需开启跨域携带 Cookie：

```
axios.defaults.withCredentials = true
```

这种方式比 LocalStorage 更安全，适用于企业级前后端分离项目。

### 2. 为什么必须使用 HTTPS？

由于浏览器安全策略：

- **HttpOnly + Secure Cookie 只有在 HTTPS 下才能写入**
- 在 `http://localhost` 下 Cookie 会被浏览器直接拒绝
- 因此前端和后端的开发环境都必须支持 HTTPS

这也是本项目提供前后端 HTTPS 启动配置的原因。

### 3. 前端 HTTPS 启动（Vue CLI + Webpack）

前端通过 `vue.config.js` 配置自签证书，使开发环境以 HTTPS 方式运行：

```
devServer: {
  https: {
    key: fs.readFileSync('./certificate/localhost+3-key.pem'),
    cert: fs.readFileSync('./certificate/localhost+3.pem'),
  },
  host: '0.0.0.0',
  port: 8080,
  open: true,
}
```

#### 启动方式

```
npm run serve
```

启动后访问：

```
https://192.168.10.143:8080/
```

这样前端才能正常写入 HttpOnly Cookie。

### 4. 后端 HTTPS 启动（Django 5.0.3）

项目提供了一个企业级 HTTPS 启动脚本 `manage_https.py`，用于在本地或局域网以 HTTPS 方式运行 Django 服务。

#### 为什么后端也要 HTTPS？

因为：

- 前端通过 HTTPS 访问
- 后端如果是 HTTP，会触发 **混合内容（Mixed Content）** 错误
- Cookie 的 Secure 属性要求 **前后端都必须是 HTTPS**

#### 启动方式

```
python manage_https.py --host 127.0.0.1 --port 8000
```

局域网访问示例：

```
python manage_https.py --host 192.168.10.143 --port 8000
```

访问地址：

```
https://192.168.10.143:8000
```

脚本功能包括：

- 检查证书是否存在
- 可选自动安装依赖（Werkzeug、pyOpenSSL）
- 使用 `runserver_plus` 启动 HTTPS
- 支持自定义 host / port

### 5.证书

证书生成可参考：

https://blog.csdn.net/dreams_dream/article/details/151352681?spm=1001.2014.3001.5501

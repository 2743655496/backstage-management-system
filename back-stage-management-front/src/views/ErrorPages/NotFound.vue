<template>
  <div class="not-found">
    <div class="content">
      <img src="@/assets/404.png" alt="Brand Logo" class="logo" />
      <h1>Oops! 页面走丢了 🧭</h1>
      <p>你是不是走得太快，把页面甩丢了？<br />别担心，我们带你回家 🏡</p>
      <router-link to="/" class="home-button">返回首页</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound'
}
</script>

<style scoped>
.not-found {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
  font-family: 'Segoe UI', 'PingFang SC', sans-serif;
}

.content {
  text-align: center;
  padding: 2rem;
  max-width: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.logo {
  height: 200px;
  margin-bottom: 1rem;
}

h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 1rem;
}

p {
  font-size: 1rem;
  color: #666;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.home-button {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background-color: #0078d4;
  color: white;
  border-radius: 6px;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.home-button:hover {
  background-color: #005ea2;
}
</style>

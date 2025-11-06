const { defineConfig } = require('@vue/cli-service')
const fs = require('fs');
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    https: {
      key: fs.readFileSync('./certificate/localhost+3-key.pem'),
      cert: fs.readFileSync('./certificate/localhost+3.pem'),
    },
    host: '0.0.0.0',
    port: 8080,
    open: true,
  }
  // devServer: {
  //   proxy: {
  //     '/api': {  // 以/api开头的请求
  //       target: 'http://your-api-server.com',  // 目标服务器地址
  //       changeOrigin: true,  // 是否改变源
  //       pathRewrite: {
  //         '^/api': ''  // 重写路径，去掉/api前缀
  //       }
  //     }
  //   }
  // }
})

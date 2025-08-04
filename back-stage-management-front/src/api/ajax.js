import axios from "axios";
import base from "./base";

const service=axios.create({
    baseURL:base.baseUrl,
    timeout:5000
})

//请求拦截
service.interceptors.request.use(config=>{
    return config
})

//响应拦截
service.interceptors.response.use(res=>{
    return res.data
},err=>{
    return Promise.reject(err)
})

export default service;
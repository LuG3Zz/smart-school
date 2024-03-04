import { getToken,removeToken } from './util/auth'
import axios from "axios"
import {notice} from '~/util/util'
import store from './store'

const service = axios.create({
    baseURL:"/api"
})

// 添加请求拦截器
service.interceptors.request.use(function (config) {
    //向header 头添加token
    const token = getToken()
    if(token){
        config.headers["token"] = token
    }
    return config;
  }, function (error) {
    // 对请求错误做些什么
    return Promise.reject(error);
  });

// 添加响应拦截器
service.interceptors.response.use(function (response) {
    // 2xx 范围内的状态码都会触发该函数。
    // 对响应数据做点什么
    return response.data;
  }, function (error) {
    // 超出 2xx 范围的状态码都会触发该函数。
    // 对响应错误做点什么

    const message = error.response.data.detail ||error.response.data.data ||'请求失败，请查看网络'
    if(message=='验证失败'|| message=='用户未登录或者登陆token已经失效'){
      store.dispatch("logout").finally(()=>location.reload())
    }else{
      console.log("axios",error)
    }
    notice(message,'error','错误')
    return Promise.reject(error);

  });

  export default service
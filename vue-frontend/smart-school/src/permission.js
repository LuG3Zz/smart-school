import {router,addRoutes} from "~/router"
import { getToken } from "./util/auth";
import { notice,showLoading,hideLoading } from "./util/util";
import store from "./store";
//全局前置守卫

router.beforeEach(async(to, from, next) => {
    //显示loading
    showLoading()
    const token = getToken()
    if(!token&&to.path=="/create"){
        return next()

    }
    //未登录，强制跳转为登录页
    if(!token&&(to.path!="/login")){
        notice('请先登录','error','错误')
        
        return next({path:"/login"})
    }
    if(token&&to.path=="/login"){
        notice('请勿重复登录','error','错误')
        return next({path:from.path?from.path:"/"})

    }
    //如果用户登录了，自动获取信息，并存储再vuex中
    let hasNewRoutes  = false
    if(token){
        let res = await store.dispatch("getinfo")
        //动态添加路由
        hasNewRoutes= addRoutes(res.data.menu)

    }
    //
    console.log(to.meta.title)
    const title=(to.meta.title?to.meta.title:"")+"-智能学工平台"
    document.title=title
    hasNewRoutes?next(to.fullPath):next();
});
//全局后置守卫
router.afterEach((to, from) =>hideLoading());
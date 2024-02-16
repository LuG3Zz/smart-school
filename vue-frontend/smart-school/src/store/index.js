import { createStore } from "vuex";
import {login,getinfo} from '~/api/users'
import {setToken} from '~/util/auth'
import { removeToken } from '~/util/auth';
import { notice } from "../util/util";

const store = createStore({
    state(){
        return{
            //用户信息
            user:{},
            menus:[]
        }
    },
    mutations:{
        // 记录用户信息
        SET_USERINFO(state,user){
            state.user=user

        },
        SET_MENUS(state,menus){
            state.menus = menus
        }

    },
    actions:{
        //获取当前登录用户信息
        getinfo( {commit}){
            return new Promise((resolve,reject)=>{
                getinfo().then(res=>{
                    commit("SET_USERINFO",res.data.info)
                    commit("SET_MENUS",res.data.menu)
                    resolve(res)
                   }).catch(err=>reject(err))
            })
        },
        login({commit} ,{username,password}){
            return new Promise((resolve,reject)=>{
                login(username,password).then(res=>{
                    if (res.code !== 200) {
                        notice(res.message,'info','提示信息')
                        throw new Error('error');
                      }
                    setToken(res.data.token)
                    resolve(res.data)
                }).catch(err=>{
                    reject(err)
                })
            })
        },
        logout({commit}){
            removeToken()
            commit("SET_USERINFO",{})


        }
    }
})

export default store
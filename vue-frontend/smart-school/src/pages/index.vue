<template>
    <div>
        <el-row :gutter="20">
            <el-col :span="6" :offset="0">
                <el-card shadow="hover" class="bg-green-200 text-gray-500 my-10"  >
                    
                    <template #header>
                    <div class="flex justify-between font-bold ">
                        <span>基本信息</span>
                        <el-tag effect="plain" type="success">
                            {{$store.state.user.position}}
                        </el-tag>
                        
                    </div>
                    </template>
                    <div class="flex flex-col justify-between ">
                    <span class="flex justify-between">姓名:
                    <span class="font-bold items-center">{{$store.state.user.name}}</span></span>
                    <span class="flex justify-between">性别:<span>{{$store.state.user.gender}}</span></span>
                    <span class="flex justify-between">联系方式:<span>{{$store.state.user.contact_info}}</span></span>
                    <el-divider/>
                    </div>
                </el-card>
                
            
            </el-col>
          </el-row>


        {{ $store.state.user}}

        <el-button @click="Logout">退出登录</el-button>
        
    </div>
</template>


<script setup>
import {ref} from 'vue'
import { msgbox,notice } from '~/util/util';
import {useRouter} from 'vue-router';
import {useStore} from 'vuex';

const router = useRouter()
const store = useStore()

function Logout(){
    msgbox("确定退出?","提示","Info").then(res=>{
        console.log('已退出')
    }).finally(()=>{
        store.dispatch("logout")
        router.push("/login")
        notice("退出成功","success")
    })


    
}


</script>

<style lang="scss" scoped>

</style>

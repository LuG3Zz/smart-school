<template>
    <el-row class="login-container">
        <el-col :lg="20" :md="12" class="left">
            <div>
            <div class="font-bold text-5xl text-light-50 mb-5">中南民族大学</div>
            <div class="text-sm text-gray-50 ml-50">智慧学工平台</div>
            </div>
        </el-col>

        <el-col :lg="0" :md="12" class="right">
            <div class="w-[150px]">
        <img src="../assets/logos.png" class="bg-contain my-5">
            </div>
        <el-card class="box-card">
                <span class="text-4xl text-dark-500 mx-12">学工平台</span>
                <div class="flex items-center justify-center space-x-2 text-gray-300 my-5">
                <span class="my-2 h-[1px] w-16 bg-gray-300"></span>
                <span>用户登录</span>
                <span class="my-3 h-[1px] w-16 bg-gray-300"></span>
                </div >
                    <el-form ref="formRef" :model="form" :rules="rules" class="w-[250px]">
                        <el-form-item prop="username">
                          <el-input v-model="form.username" placeholder="请输入账号">
                            <template #prefix>
                                <el-icon class="el-input__icon"><User /></el-icon>

                              </template>
                          </el-input>
                        </el-form-item>
                        <el-form-item prop="password">
                          <el-input v-model="form.password" placeholder="请输入密码" type="password" show-password @keydown.enter="onsubmit">
                            <template #prefix>
                                <el-icon class="el-input__icon"><Lock /></el-icon>
                              </template>
                          </el-input>
                        </el-form-item>
                    <el-button type="primary"  round class="w-[250px] bg-cyan-400 " :loading="loading" @click="onsubmit" >登录</el-button>
                    </el-form>
        </el-card>
        <el-button class="underline text-light-50" text :loading="loading" @click="router.push('/create')" >没有账号？请注册</el-button>

        </el-col>
      </el-row>
</template>

<script setup>
import {ref,reactive} from 'vue'
import {useRouter} from 'vue-router'//使用路由需要引入useRouter方法
import {useStore} from 'vuex'
import {setToken} from '~/util/auth'
import {notice} from '~/util/util'


const router = useRouter()
const store = useStore()


const form = reactive({
    username: '',
    password: '',
})

const loading = ref(false)
const rules={
    username:[
        {required:true,message:'用户名不能为空',trigger:'blur'},
],
    password:[
        {required:true,message:'密码不能为空',trigger:'blur'},
    ],
}
const formRef=ref(null)
const onsubmit= () =>{
    formRef.value.validate((valid)=>{
        if(!valid){
            return false
        }
        loading.value = true
        store.dispatch("login",form).then(res=>{
            notice('登录成功','success',"提示信息")
            //4. 跳转主页
            router.push("/")
        }).finally(loading.value=false)
    })
}


</script>
<style>
.login-container{
    @apply min-h-screen bg-gradient-to-r from-cyan-500 to-green-500;
}
.login-container .left{
    @apply flex items-center justify-center;

}
.login-container .right{
    @apply bg-gray-400 flex items-center justify-center flex-col;

}

</style>

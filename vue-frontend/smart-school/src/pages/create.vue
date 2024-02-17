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
                    <span>用户注册</span>
                    <span class="my-3 h-[1px] w-16 bg-gray-300"></span>
                </div>
                <el-form ref="formRef" :model="form" :rules="rules" class="w-[250px]">
                    <el-form-item prop="username">
                        <el-input v-model="form.username" placeholder="请输入用户名">
                            <template #prefix>
                                <el-icon class="el-input__icon">
                                    <User />
                                </el-icon>

                            </template>
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="password_hash">
                        <el-input v-model="form.password_hash" placeholder="请输入密码" type="password" show-password
                            @keydown.enter="onsubmit">
                            <template #prefix>
                                <el-icon class="el-input__icon">
                                    <Lock />
                                </el-icon>
                            </template>
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="role">
                        <el-select v-model="value" placeholder="请选择角色">
                            <template #prefix>
                                <el-icon class="el-input__icon">
                                    <User />
                                </el-icon>

                            </template>
                            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                        </el-select>
                    </el-form-item>
                    <el-form-item prop="userid">
                        <el-input v-model="form.associated_id" placeholder="请输入绑定的学号/工号">
                            <template #prefix>
                                <el-icon class="el-input__icon">
                                    <User />
                                </el-icon>
                            </template>
                        </el-input>
                    </el-form-item>
                    <el-button type="primary" round class="w-[250px] bg-cyan-400 " :loading="loading"
                        @click="onsubmit">注册</el-button>
                </el-form>
            </el-card>

        </el-col>
    </el-row>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'//使用路由需要引入useRouter方法
import { useStore } from 'vuex'
import { setToken } from '~/util/auth'
import { create_user } from '../api/users'
import { notice } from '~/util/util'


const router = useRouter()
const store = useStore()
const value = ref('')

const form = reactive({
    username: "",
    password_hash: "",
    role: "",
    associated_id: ""
})

const loading = ref(false)
const rules = {
    username: [
        { required: true, message: '用户名不能为空', trigger: 'blur' },
    ],
    password_hash: [
        { required: true, message: '密码不能为空', trigger: 'blur' },
    ],
}
const formRef = ref(null)
const onsubmit = () => {
    formRef.value.validate((valid) => {
        if (!valid) {
            return false
        }
        create_user(value.value,form).then(res => {
            notice('注册成功', 'success', "提示信息")
            router.push("/login")
        }).finally(loading.value = false)

    })
}
const options = [
    {
        value: '1',
        label: '学生',
    },
    {
        value: '4',
        label: '学生处管理员',
    },
    {
        value: '2',
        label: '院系管理员',
    },
    {
        value: '3',
        label: '辅导员',
    },
]

</script>
<style>
.login-container {
    @apply min-h-screen bg-gradient-to-r from-cyan-500 to-green-500;
}

.login-container .left {
    @apply flex items-center justify-center;

}

.login-container .right {
    @apply bg-gray-400 flex items-center justify-center flex-col;

}</style>

<template>
    <header class="header">
        <div class="logo">
            <img src="../../assets/logo.png" class="h-19" />
            <span class="text-xl text-white font-bold ">智慧学工平台</span>
        </div>
        <div class="container">

            <nav class="navigation">
                <ul class="flex space-x-4">
                    <li><a href="#" class="text-white hover:text-blue-300">主页</a></li>
                </ul>
            </nav>
            <div class="flex items-center space-x-5 mr-15">
                <el-dropdown>
                    <span class="el-dropdown-link cursor-pointer flex items-center text-white hover:text-blue-300">
                        <el-avatar v-if="store.state.user.student_id" :size="30" class="mr-2" :src="store.state.user.photo" />
                        <el-icon v-else class="mr-2" size="20" color="white">
                            <User />
                        </el-icon> {{ $store.state.user.name }} <el-icon name="el-icon-arrow-down"
                            class="ml-2"></el-icon>
                    </span>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item @click="$router.push({ path: '/' })">个人中心</el-dropdown-item>
                            <el-dropdown-item @click="formDrawerRef.open()">修改密码</el-dropdown-item>
                            <el-dropdown-item v-if="store.state.user.student_id" @click="dialogFormVisible = true">上传头像</el-dropdown-item>

                            <el-dropdown-item @click="Logout">退出登录</el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
                <!-- Message Notification -->
                <el-dropdown>
                    <span class="el-dropdown-link cursor-pointer flex items-center text-white">
                        <el-badge :value="count">
                            <el-icon class="text-2xl" color="white">
                                <MessageBox />
                            </el-icon>
                        </el-badge>
                    </span>
                    <template #dropdown>
                        <el-dropdown-menu @click="()=>{$router.push({ path: '/notification' },count='')}">
                            <el-dropdown-item v-if="count!=0">{{`${count}条未读消息`}}</el-dropdown-item>
                            <!-- More messages -->
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </div>
        </div>
    </header>
    <el-dialog v-model="dialogFormVisible" title="上传头像" width="300" destroy-on-close>
        <el-form :model="form1" class="flex justify-center">
            <el-form-item label="" prop="photo">
                <ChooseImage v-model="form1.photo" />
              </el-form-item>
        </el-form>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="dialogFormVisible.value = false">取消</el-button>
            <el-button type="primary" @click="submit">
              确定
            </el-button>
          </div>
        </template>
      </el-dialog>
    <form-drawer ref="formDrawerRef" title="修改密码" size="30%" destroyOnClose @submit="onsubmit">
        <el-form ref="formRef" :model="form" :rules="rules">
            <el-form-item prop="oldpasswd">
                <el-input v-model="form.oldpasswd" placeholder="请输入旧密码" type="password" show-password>
                </el-input>
            </el-form-item>
            <el-form-item prop="newpasswd">
                <el-input v-model="form.newpasswd" placeholder="请输入新密码" type="password" show-password
                    @keydown.enter="onsubmit">
                </el-input>
            </el-form-item>

        </el-form>
        <div></div>

    </form-drawer>
    <!-- <el-drawer v-model="drawer" title="修改密码" size="30%">
            
        </el-drawer> -->
</template>
  
<script setup>
import FormDrawer from '~/layout/components/FormDrawer.vue';
import { ElDropdown, ElDropdownMenu, ElDropdownItem, ElBadge, ElIcon } from 'element-plus';
import { msgbox, notice } from '~/util/util';
import { changepsw } from '~/api/users'
import { update_student_photo } from '~/api/studentadmin'
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { ref, reactive } from 'vue'
import {get_uncheck_notification_count } from '~/api/notification'
import ChooseImage from "~/layout/components/ChooseImage.vue";
const dialogFormVisible = ref(false)
const store = useStore()
const router = useRouter()
const formLabelWidth = '140px'
const count = ref(0)

get_uncheck_notification_count().then(res => {
    count.value=res.data.total
}).catch()
//密码
//const drawer = ref(false)
const {
        formDrawerRef,
        form,
        rules,
        formRef,
        onsubmit
} = useRepassword()

function Logout() {
    msgbox("确定退出?", "提示", "Info").then(res => {
        console.log('已退出')
        store.dispatch("logout")
        router.push("/login")
        notice("退出成功", "success")
    }).catch()
}

function useRepassword() {
    const formDrawerRef = ref(null)
    const form = reactive({
        oldpasswd: '',
        newpasswd: '',
    })
    const rules = {
        oldpasswd: [
            { required: true, message: '旧密码不能为空', trigger: 'blur' },
        ],
        newpasswd: [
            { required: true, message: '新密码不能为空', trigger: 'blur' },
        ],
    }
    const formRef = ref(null)
    const onsubmit = () => {
        formRef.value.validate((valid) => {
            if (!valid) {
                return false
            }
            formDrawerRef.value.showLoading()
            changepsw(form).then(res => {
                if (res.code !== 200) {
                    notice(res.message, 'info', '提示信息')
                }
                else {
                    notice('修改密码成功，请重新登录', 'success', "提示信息")
                    store.dispatch("logout")
                    router.push("/login")
                }
            }).finally(
                formDrawerRef.value.hideLoading()
            )
        })
    }
    return {
        formDrawerRef,
        form,
        rules,
        formRef,
        onsubmit
    }
}
const form1 = reactive({
    photo:''
})
const submit = () => {

            formDrawerRef.value.showLoading()
            update_student_photo(store.state.user.student_id,form1).then(res => {
                if (res.code !== 200) {
                    notice(res.message, 'info', '提示信息')
                }
                else {
                    notice('修改头像成功', 'success', "提示信息")
                }
            }).finally(
                dialogFormVisible.value = false,
                location.reload()
            )
        }
    
</script>
  
<style scoped>
@tailwind base;
@tailwind components;
@tailwind utilities;

.header {
    @apply bg-gradient-to-r from-green-500 to-blue-300 w-full h-20 flex justify-between items-center px-3;
}

.logo {
    @apply flex items-center justify-center mr-12 ml-3 min-w-[200px];
}

.container {
    @apply flex justify-between items-center;
}

.navigation ul {
    @apply flex space-x-4;
}
</style>
  
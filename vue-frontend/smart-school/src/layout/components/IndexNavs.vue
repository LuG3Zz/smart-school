<template>
    <el-row :gutter="20" class="mt-5">
        <el-col :span="3" :offset="0" v-for="(item,index) in iconNavs" :key="index">
            <el-card shadow="hover" @click="$router.push(item.path)">
                <div class="flex flex-col items-center justify-center cursor-pointer">
                    <el-icon :size="16" :class="item.color">
                        <component :is="item.icon"/>
                    </el-icon>
                    <span class="text-sm mt-2">{{ item.title }}</span>
                </div>
            </el-card>
        </el-col>
    </el-row>
</template>
<script setup>

const iconNavs = [
        {
            icon:"user",
            color:"text-light-blue-500",
            title:"用户",
            path:"/info"
        },
        {
            icon:"shopping-cart",
            color:"text-violet-500",
            title:"选课",
            path:"/course-selection"
        },
        {
            icon:"tickets",
            color:"text-fuchsia-500",
            title:"处分",
            path:"/discipline-search"
        },
        {
            icon:"chat-dot-square",
            color:"text-teal-500",
            title:"消息",
            path:"/notification"
        },
        {
            icon:"house",
            color:"text-rose-500",
            title:"宿舍",
            path:"/dormitory-info"
        },
        {
            icon:"bell",
            color:"text-green-500",
            title:"公告",
            path:"/notification"
        },
        {
            icon:"picture",
            color:"text-grey-500",
            title:"资料",
            path:"/image"
        },
        {
            icon:"van",
            color:"text-yellow-500",
            title:"离校",
            path:"/checkout-process"
        }
    ]
</script>
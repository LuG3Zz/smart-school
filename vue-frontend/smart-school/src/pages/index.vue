<template>
    <div>
        <div class="my-10">
            <el-row :gutter="20" v-permission="['getStatistics1,POST']">
                <template v-if="panels.length == 0">
                    <el-col :span="6" v-for="i in 4" :key="i">
                        <el-skeleton style="width: 100%;" animated loading>
                            <template #template>
                                <el-card shadow="hover" class="border-0">
                                    <template #header>
                                        <div class="flex justify-between">
                                            <el-skeleton-item variant="text" style="width: 50%" />
                                            <el-skeleton-item variant="text" style="width: 10%" />
                                        </div>
                                    </template>
                                    <el-skeleton-item variant="h3" style="width: 80%" />
                                    <el-divider />
                                    <div class="flex justify-between text-sm text-gray-500">
                                        <el-skeleton-item variant="text" style="width: 50%" />
                                        <el-skeleton-item variant="text" style="width: 10%" />
                                    </div>
                                </el-card>
                            </template>
                        </el-skeleton>
                    </el-col>
                </template>


                <el-col :span="6" :offset="0" v-for="(item, index) in panels" :key="index">
                    <el-card shadow="hover" class="border-0">
                        <template #header>
                            <div class="flex justify-between">
                                <span class="text-sm">{{ item.title }}</span>
                                <el-tag :type="item.unitColor" effect="plain">
                                    {{ item.unit }}
                                </el-tag>
                            </div>
                        </template>
                        <span class="text-3xl font-bold text-gray-500">
                            {{item.value}}
                        </span>
                        <el-divider />
                        <div class="flex justify-between text-sm text-gray-500">
                            <span>{{ item.subTitle }}</span>
                            <span>{{ item.subValue }}</span>
                        </div>
                    </el-card>

                </el-col>
            </el-row>

            <IndexNavs />

            <el-row :gutter="20" class="mt-5">
                <el-col :span="12" :offset="0">
                    <IndexChart v-permission="['getStatistics3,GET']" v-if="store.state.user.student_id" />
                    <pieChart v-permission="['getStatistics3,GET']" v-else />
                </el-col>
                <el-col :span="12" :offset="0" v-permission="['getStatistics2,GET']">
                    <IndexCard title="学工事务提示" tip="违纪和得奖提示" :btns="record" class="mb-2" />
                    <IndexCard title="消息提示" tip="需要立即处理的消息" :btns="notification" />
                </el-col>
            </el-row>

        </div>
        </div>
</template>


<script setup>
import { ref } from 'vue'
import { msgbox, notice } from '~/util/util';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import IndexCard from '~/layout/components/IndexCard.vue'
import IndexChart from '~/layout/components/IndexChart.vue'
import pieChart from '~/layout/components/pieChart.vue'
import IndexNavs from '~/layout/components/IndexNavs.vue'

const router = useRouter()
const store = useStore()

function Logout() {
    msgbox("确定退出?", "提示", "Info").then(res => {
        console.log('已退出')
    }).finally(() => {
        store.dispatch("logout")
        router.push("/login")
        notice("退出成功", "success")
    })

}
import {
    getStatistics1,
    getStatistics2
} from "~/api/users.js"

const panels = ref([])
getStatistics1()
    .then(res => {
        console.log(res.data)
        panels.value = res.data.panels
    })

const notification = ref([])
const record = ref([])
getStatistics2().then(res=>{
    notification.value = res.data.notification
    record.value = res.data.record
})

</script>

<style lang="scss" scoped></style>

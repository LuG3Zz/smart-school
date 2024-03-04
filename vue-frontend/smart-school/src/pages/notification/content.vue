<template>
    <FormDrawer ref="formDrawerRef" title="通知详情" v-bind:submit="store.state.user.student_id ? submit : null" destroy-on-close v-if="store.state.user.student_id">
        <el-form :model="form">
            <el-form-item>
                <Editor v-model="form.content"/>
            </el-form-item>
        </el-form>
    </FormDrawer>
</template>
<script setup>
import { ref,reactive } from "vue"
import FormDrawer from "~/layout/components/FormDrawer.vue";
import Editor from "~/layout/components/Editor.vue"
import {
//    readGoods,
    read_notification,
    update_notification
//    updateGoods
} from "~/api/notification"
import { useStore } from 'vuex';

import {
  notice
} from "~/util/util"


const store = useStore()

const formDrawerRef = ref(null)

const form = reactive({
    content:"",
})

const goodsId = ref(0)
const open = (row)=>{
    goodsId.value = row.notification_id
    row.contentLoading = true
    read_notification(goodsId.value).then(res=>{
        form.content = res.data.content
        formDrawerRef.value.open()
    })
    .finally(()=>{
        row.contentLoading = false
    })
}
const emit = defineEmits(["reloadData"])

const submit = ()=>{
    formDrawerRef.value.showLoading()
    update_notification(goodsId.value,form)
    .then(res=>{
        notice("设置详情成功")
        formDrawerRef.value.close()
        emit("reloadData")
    })
    .finally(()=>{
        formDrawerRef.value.hideLoading()
    })
}

defineExpose({
    open
})
</script>

<template>
    <FormDrawer ref="formDrawerRef" title="资料详情" @submit="submit" destroy-on-close>
        <el-form :model="form">
            <el-form-item>
                <Editor v-model="form.leave_reason"/>
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
    read_LeaveSchool,
    update_LeaveSchool
//    updateGoods
} from "~/api/leave_school"
import { notice } from "~/util/util";

const formDrawerRef = ref(null)

const form = reactive({
    leave_reason:"",
})

const goodsId = ref(0)
const open = (row)=>{
    goodsId.value = row.application_id
    row.contentLoading = true
    read_LeaveSchool(goodsId.value).then(res=>{
        form.leave_reason = res.data.LeaveSchool.leave_reason
        formDrawerRef.value.open()
    })
    .finally(()=>{
        row.contentLoading = false
    })
}
const emit = defineEmits(["reloadData"])

const submit = ()=>{
    formDrawerRef.value.showLoading()
    update_LeaveSchool(goodsId.value,form)
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

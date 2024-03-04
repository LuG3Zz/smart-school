<template>
    <FormDrawer ref="formDrawerRef" title="资料详情" @submit="submit" destroy-on-close>
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
    read_record,
    update_record
//    updateGoods
} from "~/api/record"
import { notice } from "~/util/util";

const formDrawerRef = ref(null)

const form = reactive({
    content:"",
})

const goodsId = ref(0)
const open = (row)=>{
    goodsId.value = row.record_id
    row.contentLoading = true
    read_record(goodsId.value).then(res=>{
        form.content = res.data.StudentRecord.content
        formDrawerRef.value.open()
    })
    .finally(()=>{
        row.contentLoading = false
    })
}
const emit = defineEmits(["reloadData"])

const submit = ()=>{
    formDrawerRef.value.showLoading()
    update_record(goodsId.value,form)
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

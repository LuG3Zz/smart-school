<template>
        <el-drawer v-model="drawer" 
        :title="title" 
        :size="size" 
        :destroy-on-close="destroyOnClose">
            <div class="formDrawer">
                <div class="body">
                    <slot></slot>
                </div>
                
                <div class="actions">
                    <el-button v-show="showButton" type="primary" @click="submit" :loading="loading">{{confirmText}}</el-button>
                    <el-button type="default" @click="cancel">取消</el-button>

                </div>
            </div>
            
        </el-drawer>
</template>

<script setup>
import { Loading } from "element-plus/es/components/loading/src/service";
import {ref} from "vue"
const drawer = ref(false)
const loading = ref(false)

const showButton = ref(true)
const open = ()=>drawer.value=true
const close = ()=>drawer.value=false
const emit = defineEmits(['submit','cancle'])
const submit =()=>emit("submit")
const cancel =()=>close()
const showLoading =()=>loading.value=true
const hideLoading =()=>loading.value=false

defineExpose({
    open,
    close,
    showLoading,
    hideLoading
})

defineProps({
    title:String,
    size:{
        type:String,
        default:"45%",
    },
    destroyOnClose:{
        type:Boolean,
        default:false
    },
    confirmText:{
        type:String,
        default:"提交"
    }

})

</script>

<style>
.formDrawer{
    width:100%;
    height:100%;
    position: relative;
    @apply  flex flex-col

}
.formDrawer .body{
    overflow-y:auto;

}
.formDrawer .actions{
    height: 50px;
    @apply mt-auto flex items-center

}

</style> 

<template>
    <el-card shadow="never" class="border-0 my-10 mr-10 ">
        <div class="flex items-center justify-between mb-4">
            <el-button type="primary" size="small">新增</el-button>
            <el-tooltip 
            class="box-item"
            effect="dark" 
            content="刷新"
            place="top"
            
            >
            <el-button text @click="getData">
                <el-icon :size="20"><Refresh /></el-icon>
            </el-button>
        
        
        </el-tooltip>

        </div>
        <el-table :data="tableData" stripe style="width: 100%">
            <el-table-column prop="student_id" label="学号" width="180" />
            <el-table-column prop="record_id" label="违纪编号" width="180" />
            <el-table-column prop="violation_date" label="违纪时间" width="180" />
            <el-table-column prop="description" label="违纪描述" width="180" />
            <el-table-column prop="penalty_level" label="程度" width="180" />
            <el-table-column  label="操作" />
          </el-table>

    </el-card>
    
    <div>
    

    </div>
</template>

<script setup>
import {  ref } from 'vue';
import  {read_own_discipline_record} from '~/api/record'
const tableData = ref([])

function getData(){
    read_own_discipline_record().then(res=>{
        console.log(res)
        tableData.value = res.data
    })
}

getData()

</script>

<style lang="scss" scoped>

</style>
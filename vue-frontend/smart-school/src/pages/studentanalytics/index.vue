<template>
    
        <div class="my-10">
            <el-row :gutter="20" class="mt-5">
                <el-col :span="12"><pieChart1/></el-col>
                <el-col :span="12"><pieChart2/></el-col>
                
                
            </el-row>
            <el-row :gutter="20" class="mt-5">
                
                  
                
            </el-row>

        </div>
</template>


<script setup>



import pieChart1 from './StudentpieChart_gender.vue'
import pieChart2 from './StudentpieChart_major.vue'




</script>

<style lang="scss" scoped></style>

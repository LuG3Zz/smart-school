<template>
    <el-drawer :title="drawerTitle" v-model="dialogVisible" size="70%">
        <!-- 搜索 -->
        

        <el-table :data="tableData" stripe style="width: 100%" v-loading="loading">
            <template v-if="type === 'course_detail'">
                <el-table-column label="课程信息" prop="course_info.name" align="center" />
                <el-table-column label="课程性质" prop="course_info.description" />
                <el-table-column label="学年" prop="course_info.semester" align="center" />
                <el-table-column label="学分" prop="course_info.credits" align="center" />
                <el-table-column label="开课单位" prop="department_name" align="center" />
                <el-table-column label="成绩" prop="grade" align="center" />
            </template>
            <template v-else>
                <el-table-column label="教师工号" prop="teacher_info.teacher_id"/>
                <el-table-column label="教师名字" prop="teacher_info.name"/>
                <el-table-column label="教师职位" prop="teacher_info.position"/>
                <el-table-column label="联系方式" prop="teacher_info.contact_info"/>
                <el-table-column label="性别" prop="teacher_info.gender"/>
                <el-table-column label="专业方向" prop="teacher_info.specialization"/>
            </template>
        </el-table>

    </el-drawer>
</template>
<script setup>
import { ref,computed } from 'vue';
import {
    get_student_courses
} from "~/api/studentcourse"
import { useInitTable } from '~/util/useCommon.js'

const props = defineProps({
    type:{
        type:String,
        default:"user"
    }
})
const drawerTitle = computed(()=>props.type === 'course_detail' ? "课程详情" : "任课教师详情")
const dialogVisible = ref(false)

const {
    searchForm,
    tableData,
    loading,
    currentPage,
    total,
    limit,
    getData,
} = useInitTable({
    searchForm: {
        semester: "all",
    },
    getList: (()=>{
        return props.type === 'course_detail' ?  get_student_courses :get_student_courses
    })(),
    onGetListSuccess: (res) => {
        tableData.value = res.data.list
        total.value = res.data.total
    },
})

const resetSearchForm = ()=>{
    searchForm.semester = "all"
    //searchForm.starttime = null
    //searchForm.endtime = null
    searchForm.word = ""
}

const open = (id) => {
    dialogVisible.value = true
    searchForm.word = id
    getData()
}

defineExpose({
    open
})
</script>
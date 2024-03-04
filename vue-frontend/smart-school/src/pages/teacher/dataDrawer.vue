<template>
    <el-drawer :title="drawerTitle" v-model="dialogVisible" size="70%">
        <!-- 搜索 -->
        <el-table :data="tableData" stripe style="width: 100%" v-loading="loading">
            <template v-if="type === 'update_course'">
                <el-table-column label="课程信息" prop="course_info.name" align="center" />
                <el-table-column label="课程性质" prop="course_info.description" />
                <el-table-column label="学年" prop="course_info.semester" align="center" />
                <el-table-column label="学分" prop="course_info.credits" align="center" />
                <el-table-column label="开课单位" prop="department_name" align="center" />

            </template>
            <template v-else>
                <el-table-column prop="student_id" label="学号" />
                <el-table-column prop="name" label="姓名" />
                <el-table-column prop="gender" label="性别" />
                <el-table-column prop="contact_info" label="联系电话" />
                <el-table-column prop="department_name" label="院系" />
                <el-table-column prop="major" label="专业" />
                <el-table-column prop="enrollment_date" label="注册时间" />
                <el-table-column prop="student_grade" label="成绩" />
                <el-table-column v-if="type != 'course_detail'" fixed="right" label="操作" width="180" align="center">
                <template #default="{ row }">
                    <el-button type="primary" size="small" text @click="InputGrade(row.student_id,searchForm.course_id,form)"> 录入成绩</el-button>
                </template>
                </el-table-column>
            </template>
        </el-table>
        <div class="flex items-center justify-center mt-5">
            <el-pagination background layout="prev, pager ,next" :total="total" :current-page="currentPage"
                :page-size="limit" @current-change="getData" />
        </div>

    </el-drawer>
</template>
<script setup>
import { ElMessage, ElMessageBox } from 'element-plus'

import { ref, computed,reactive } from 'vue';
import {
    get_student_courses,
    get_students_by_course,
    update_grade
} from "~/api/studentcourse"
import { useInitTable } from '~/util/useCommon.js'

const props = defineProps({
    type: {
        type: String,
        default: "user"
    }
})
const drawerTitle = computed(() => props.type === 'update_course' ? "修改课程" : "选课学生详情")
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
        course_id: ""
    },
    getList: (() => {
        return props.type === 'update_course' ? get_student_courses : get_students_by_course
    })(),
    onGetListSuccess: (res) => {
        tableData.value = res.data.list
        total.value = res.data.total
    },
})

const resetSearchForm = () => {
    //`searchForm.semester = "all"
    //searchForm.starttime = null
    //searchForm.endtime = null
    searchForm.course_id = ""
    searchForm.word = ""
}

const open = (id) => {
    dialogVisible.value = true
    searchForm.course_id = id
    getData()
}

const InputGrade = (student_id,course_id) => {
    ElMessageBox.prompt('请输入成绩', '成绩录入', {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        inputPattern: /^(?:100|[1-9][0-9]?)$/,
        inputErrorMessage: 'Invalid Number'

    })
        .then(({ value }) => {
            update_grade(student_id,course_id,{"grade":value}).then(
            ElMessage({
                type: 'success',
                message: `学号:${student_id} 录入成绩:${value}`,

            }),
                getData()

            )
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: '取消输入',
            })
        })
}
defineExpose({
    open
})
</script>
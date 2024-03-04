<template>
    <el-card shadow="never" class="border-0 my-10">
        <!-- 新增|刷新 -->
        <ListHeader @create="handleCreate" @refresh="getData" />

        <el-table :data="tableData" stripe style="width: 100%" v-loading="loading" class='min-h-2xl'>
            <el-table-column label="课程名称" width="350">
                <template #default="{ row }">
                    <div class="border border-dashed py-2 px-4 rounded"
                        :class="is_in_semester(row)=='进行中' ? 'active' : 'inactive'">
                        <h5 class="font-bold text-md">{{ row.name }}</h5>
                        <div class="flex justify-between">
                        <small>{{ row.semester }}</small>
                        <small>{{ row.description }}</small>
                        </div>
                    </div>
                </template>
            </el-table-column>
            <el-table-column prop="department_name" label="开课学院" />
            <el-table-column label="状态">
                <template #default="{ row }">
                    {{ is_in_semester(row)}}
                </template>
            </el-table-column>
            <el-table-column prop="credits" label="学分" />
            <el-table-column label="操作" width="180" align="center">
                <template #default="scope">
                    <el-button v-if="is_in_semester(scope.row)=='进行中'" type="primary" size="small" text
                        @click="handleEdit(scope.row.course_id,scope.row.course_info)">修改</el-button>

                    <el-popconfirm v-if="is_in_semester(scope.row)=='进行中'" title="是否要删除该课程？" confirmButtonText="确认"
                        cancelButtonText="取消" @confirm="handleDelete(scope.row.course_id)">
                        <template #reference>
                            <el-button text type="primary" size="small">删除</el-button>
                        </template>
                    </el-popconfirm>
                </template>
            </el-table-column>
        </el-table>

        <div class="flex items-center justify-center mt-5">
            <el-pagination background layout="prev, pager ,next" :total="total" :current-page="currentPage"
                :page-size="limit" @current-change="getData" />
        </div>

        <FormDrawer ref="formDrawerRef" :title="drawerTitle" @submit="handleSubmit">
            <el-form :model="form" ref="formRef" :rules="rules" label-width="80px" :inline="false">
                <el-form-item label="课程名称" prop="name">
                    <el-input v-model="form.name" placeholder="课程名称" style="width: 50%;"></el-input>
                </el-form-item>
                <el-form-item label="类型" prop="description">
                    <el-radio-group v-model="form.description">
                        <el-radio v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="学分" prop="credits">
                    <el-input-number v-model="form.credits" :min="0" :max="10"></el-input-number>
                </el-form-item>
                <el-form-item label="院系" prop="department_id">
                    <el-select v-model="form.department_id" placeholder="请选择院系">
                      <el-option v-for="item in options_department" :key="item.department_id" :label="item.name" :value="item.department_id" />
                    </el-select>
                  </el-form-item>
            </el-form>
        </FormDrawer>

    </el-card>
</template>
<script setup>
import { computed,ref } from "vue"
import ListHeader from "~/layout/components/ListHeader.vue";
import FormDrawer from "~/layout/components/FormDrawer.vue";
import {
    get_course_list,
    create_course,
    delete_course,
    update_course
} from "~/api/course"

import {
get_student_courses
} from "~/api/studentcourse";
import{get_departments}
from "~/api/studentadmin"

import { useInitTable, useInitForm } from '~/util/useCommon.js'
import { getCurrentSemester } from "~/util/util"


function is_in_semester(row) {
     // 判断日期是否在输入学期范围内
     if(row.semester == getCurrentSemester())
    {
      return "进行中";
    }else{
        return "未开放或已过期"
    }
}
const options_department = ref([])

get_departments().then(res => {
    options_department.value = res.data
  })
    .finally(() => {
      loading.value = false
})

const options = [
  {
    value: '选修',
    label: '选修',
  },
  {
    value: '公共课',
    label: '公共课',
  },
  {
    value: '必修',
    label: '必修',
  },
]
const {
    tableData,
    loading,
    currentPage,
    total,
    limit,
    getData,
    handleDelete,
    handleStatusChange
} = useInitTable({
    getList: get_student_courses,

    onGetListSuccess: (res) => {
        tableData.value = res.data.list
        total.value = res.total
    },
    delete: delete_course,
    drawerTitle :  computed(() => editId.value ? "修改" : "新增")
})

const {
    formDrawerRef,
    formRef,
    form,
    rules,
    drawerTitle,
    handleSubmit,
    handleCreate,
    handleEdit
} = useInitForm({
    form: {
        name: "",
        course_id:"",
        semester: getCurrentSemester(),
        credits: 0,
        department_id: "",
        teacher_id:"",
    },
    getData,
    update: update_course,
    create: create_course,

    
})


</script>
<style scoped>
.active {
    @apply border-rose-200 bg-rose-50 text-red-400;
}

.inactive {
    @apply border-gray-200 bg-gray-50 text-gray-400;
}
</style>
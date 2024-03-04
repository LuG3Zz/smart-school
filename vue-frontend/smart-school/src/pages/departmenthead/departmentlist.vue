<template>
    <el-card shadow="never" class="border-0 my-10">
        <!-- 新增|刷新 -->
        <ListHeader v-if="!store.state.user.student_id" @create="handleCreate" @refresh="getData" />
        <ListHeader v-else @create="handleCreate" @refresh="getData" />
        <el-table :data="tableData" stripe style="width: 100%" v-loading="loading" class='min-h-2xl'>
            <el-table-column label="学院名称" width="350">
                <template #default="{ row }">
                    <div class="border border-dashed py-2 px-4 rounded"
                    :class="row.department_student!='0' ? 'active' : 'inactive'">
                        <h5 class="font-bold text-md">{{ row.name }}</h5>
                        <div class="flex justify-between">
                        <small>{{ "学院编号:"+row.department_id }}</small>
                        <small v-if="row.department_student">{{ "学生人数:"+row.department_student }}</small>
                        </div>
                    </div>
                </template>
            </el-table-column>
            
            <el-table-column prop="contact_info" label="联系信息" />
            <el-table-column prop="teacher_info.name" label="负责人" />
            <el-table-column label="操作" width="180" align="center">
                <template #default="scope">
                    <el-button  type="primary" size="small" text
                        @click="handleEdit(scope.row)" v-if="!store.state.user.student_id">修改</el-button>

                    <el-popconfirm  title="是否要删除该院系？" confirmButtonText="确认"
                        cancelButtonText="取消" @confirm="handleDelete(scope.row.department_id)">
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
                <el-form-item label="院系名称" prop="name">
                    <el-input v-model="form.name" placeholder="院系名称" style="width: 50%;"></el-input>
                </el-form-item>
                <el-form-item label="负责人" prop="head_id">
                    <el-input v-model="form.head_id" placeholder="负责人" style="width: 50%;"></el-input>
                </el-form-item>
                <el-form-item label="学院编号" prop="department_id">
                    <el-input v-model="form.department_id" placeholder="学院编号" style="width: 50%;"></el-input>
                </el-form-item>
                <el-form-item label="联系方式" prop="contact_info">
                    <el-input v-model="form.contact_info" placeholder="联系方式" style="width: 50%;"></el-input>
                </el-form-item>
            </el-form>
        </FormDrawer>

    </el-card>
</template>
<script setup>
import { computed } from "vue"
import ListHeader from "~/layout/components/ListHeader.vue";
import FormDrawer from "~/layout/components/FormDrawer.vue";
import {
    get_departments_info,
    create_department_info,
    update_department_info,
    delete_department_info
} from "~/api/department"
import { useInitTable, useInitForm } from '~/util/useCommon.js'
import { useStore } from 'vuex';
const store = useStore()

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
    getList: get_departments_info,

    onGetListSuccess: (res) => {
        tableData.value = res.data.list
        total.value = res.total
    },
    delete: delete_department_info,
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
        head_id: "",
        department_id: "",
        contact_info: null,
        teacher_info: null
    },
    getData,
    update: update_department_info,
    create: create_department_info,
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
<template>
  <el-card shadow="never" class="border-0 my-10">
    <!-- 搜索 -->
    <div v-if="!store.state.user.student_id">
    <Search :model="searchForm" @search="getData" @reset="resetSearchForm">
      <SearchItem label="关键词">
        <el-input v-model="searchForm.word" placeholder="门牌号" clearable></el-input>
      </SearchItem>
    </Search>
    <!-- 新增|刷新 -->
    <ListHeader v-if="!store.state.user.student_id" layout="create,refresh" @create="handleCreate" @refresh="getData">
    </ListHeader>
    <ListHeader v-else layout="refresh" @create="handleCreate" @refresh="getData">
    </ListHeader>
    </div>
    <el-table :data="tableData" stripe style="width: 100%" v-loading="loading" class='min-h-2xl'>
      <el-table-column type="expand">
        <template #default="{ row }">
          <div class="flex pl-18 mb-6" v-for="(item, index) in row.students" :key="index">
            <el-avatar :size="30" class="mr-2" :src="item.Student.photo" />
            <div class="flex-1">
              <h6 class="flex items-center">
                {{ item.Student.name || '五' }}
                <small class=" text-gray-400 ml-2 mr-10">{{ item.Student.gender }}</small>
                <el-popconfirm title="是否要删除？" confirmButtonText="确认" cancelButtonText="取消"
                  @confirm="deleteStudent(item)">
                  <template #reference>
                    <el-button v-if="!store.state.user.student_id" type="primary" size="small" text
                      class="ml-auto underline">删除</el-button>
                  </template>
                </el-popconfirm>
              </h6>
              <div class="flex justify-between">
                {{ item.department }}
                <small>入住时间:{{ item.StudentDormitory.assignment_date || '无' }}</small>
              </div>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="ID" width="50" align="center" prop="dormitory_id" />
      <el-table-column label="门牌号" width="120">

        <template #default="{ row }">
          <div class="flex items-center">
            <div class="ml-3">
              <h6>{{ row.dorm_number ? row.dorm_number : '宿舍已被删除' }}</h6>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="宿舍卫生等级" width="200">

        <template #default="{ row }">
          <div>
            <p>
              <el-rate v-if="store.state.user.student_id" v-model="row.grade" disabled show-score
                text-color="#ff9900" />
              <el-rate v-else v-model="row.grade" show-score text-color="#ff9900"
                @click="handleStatusChange({ 'grade': row.grade }, row.dormitory_id)" />
            </p>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="宿舍基本情况" >

        <template #default="{ row }">
          <div class="flex">
            <div class="flex-1">
              <p>所在楼层: {{ row.floor }}</p>
              <div>
                <span class="text-gray-500">{{ '容量: ' + row.students.length }}</span>
                <el-divider direction="vertical" />
                <span class="text-rose-500 text-xs">{{ row.capacity }}</span>
              </div>
              <p class="text-gray-400 text-xs mb-1">联系方式:{{ row.contact_phone ? row.floor
      : "未留" }}</p>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="操作" v-if="!store.state.user.student_id">

        <template #default="{ row }">
          <el-form-item>
            <el-button class="underline flex-col" size="small" text @click="addStudent(row)">添加学生</el-button>
          </el-form-item>
          <el-form-item>
            <el-button class="underline" size="small" text @click="handleEdit(row.dormitory_id)">修改宿舍信息</el-button>
          </el-form-item>
          <el-popconfirm title="是否要删除？" confirmButtonText="确认" cancelButtonText="取消"
            @confirm="handleDelete(row.dormitory_id)">
            <template #reference>
              <el-button v-if="!store.state.user.student_id" type="primary" size="small" text
                class="ml-auto underline">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    <FormDrawer ref="formDrawerRef" :title="drawerTitle" @submit="handleSubmit">
      <el-form :model="form" ref="formRef" :rules="rules" label-width="80px" :inline="false">
        <el-form-item label="容量" prop="capacity">
          <el-input-number v-model="form.capacity" class="mx-4" :min="1" :max="6" controls-position="right" />
        </el-form-item>
        <el-form-item label="楼层" prop="floor">
          <el-input-number v-model="form.floor" class="mx-4" :min="1" :max="6" controls-position="right" />
        </el-form-item>
        <el-form-item label="门牌号" prop="dorm_number">
          <el-input v-model="form.dorm_number"></el-input>
        </el-form-item>
        <el-form-item label='联系方式' prop=contact_phone>
          <el-input v-model="form.contact_phone" />
        </el-form-item>
      </el-form>
    </FormDrawer>

    <div class="flex items-center justify-center mt-5">
      <el-pagination background layout="prev, pager ,next" :total="total" :current-page="currentPage" :page-size="limit"
        @current-change="getData" />
    </div>

  </el-card>
</template>

<script setup>
import { ref } from "vue"
import FormDrawer from "~/layout/components/FormDrawer.vue";
import Search from "~/layout/components/Search.vue";
import SearchItem from "~/layout/components/SearchItem.vue";
import { notice } from "~/util/util"
import ListHeader from "~/layout/components/ListHeader.vue";
import {
  get_role_dormitorys,
  create_dormitory,
  create_student_dormitory,
  delete_student_dormitory
  //  getGoodsCommentList,
  //  updateGoodsCommentStatus,
  //  reviewGoodsComment
} from "~/api/dorm"

import { useInitTable, useInitForm } from '~/util/useCommon.js'
import { useStore } from 'vuex';
import { delete_dormitory, update_dormitory } from "../../api/dorm";
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useStore()

const roles = ref([])
const option = ref([])

const {
  searchForm,
  resetSearchForm,
  tableData,
  loading,
  currentPage,
  total,
  limit,
  getData,
  handleDelete,
  handleStatusChange
} = useInitTable({
  searchForm: {
    title: ""
  },
  getList: get_role_dormitorys,
  onGetListSuccess: (res) => {
    tableData.value = res.data.list.map(o => {
      o.statusLoading = false
      o.textareaEdit = false
      return o
    })
    total.value = res.data.total
    roles.value = res.roles
  },
  updateStatus: update_dormitory,
  delete: delete_dormitory
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
    floor: 1
  },
  getData,
  update: update_dormitory,
  create: create_dormitory
})

const textarea = ref("")
const openTextarea = (row, data = "") => {
  textarea.value = data
  row.textareaEdit = true
}

const deleteStudent = (row) => {
delete_student_dormitory(row.StudentDormitory.assignment_id)
  .then(res=>{
    notice("删除成功")
    getData()
  })
}

const addStudent = (id) => {
  ElMessageBox.prompt('请输入要添加学生的学号', '添加学生', {
    confirmButtonText: 'OK',
    cancelButtonText: 'Cancel',
  })
    .then(({ value }) => {
      const data = {
        student_id: value,
        dormitory_id: id.dormitory_id
      }
      create_student_dormitory(data).then((res) => {
        if (res.code!=200){
        ElMessage({
          type: 'warning',
          message:res.detail
        })

        }else{
        ElMessage({
          type: 'success',
          message:'成功'
        })
        }
      }
      )
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '取消输入',
      })
    })
}
</script>
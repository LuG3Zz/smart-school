<template>
  <div>
    <el-tabs v-model="searchForm.tab" @tab-change="getData" class="top-10">
      <el-tab-pane :label="item.name" :name="item.key" v-for="(item, index) in tabbars" :key="index"></el-tab-pane>
    </el-tabs>

    <el-card shadow="never" class="border-0 ">
      <!-- 搜索 -->
      <Search :model="searchForm" @search="getData" @reset="resetSearchForm">
        <SearchItem label="关键词">
          <el-input v-model="searchForm.word" placeholder="审核人" clearable></el-input>
        </SearchItem>
        <template #show>
          <SearchItem label="离校类型">
            <el-select v-model="searchForm.leave_type" placeholder="请选择类型" clearable>
              <el-option :label="毕业离校" :value="'毕业离校'">毕业离校
              </el-option>
              <el-option :label="退学离校" :value="'退学离校'">退学离校
              </el-option>
              <el-option :label="休学离校" :value="'休学离校'">休学离校
              </el-option>
              <el-option :label="放假离校" :value="'放假离校'">放假离校
              </el-option>/el-option>
            </el-select>
          </SearchItem>
        </template>
      </Search>

      <!-- 新增|刷新 -->
      <ListHeader v-if="store.state.user.student_id" layout="create,refresh" @create="handleCreate" @refresh="getData">
      </ListHeader>
      <ListHeader v-else layout="refresh" @create="handleCreate" @refresh="getData">
      </ListHeader>

      <el-table ref="multipleTableRef" @selection-change="handleSelectionChange" :data="tableData" stripe
        style="width: 100%" v-loading="loading" class='min-h-2xl'>
        <el-table-column type="selection" width="55" />
        <el-table-column label="申请事务" width="300">
          <template #default="{ row }">
            <div class="flex">
              <div class="flex-1">
                <p>{{ row.title }}</p>
                <div>
                  <span class="text-cyan-500">{{ row.LeaveSchool.leave_type }}</span>
                  <el-divider direction="vertical" />
                  <span class="text-gray-500 text-xs">{{ row.s_name }}</span>
                </div>
                <p class="text-gray-400 text-xs mb-1">类型:{{ row.LeaveSchool.record_type ? row.LeaveSchool.record_type
                  : "未分类" }}</p>
                <p class="text-gray-400 text-xs">离校时间：{{ row.LeaveSchool.leave_date }}</p>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="['已通过'].includes(row.LeaveSchool.application_status) ? 'success' : 'danger'" size="small">{{
              row.LeaveSchool.application_status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="审核状态" width="120" align="center" v-if="searchForm.tab != 'delete'">
          <template #default="{ row }">
            <div class="flex flex-col" v-if="row.LeaveSchool.application_status == '待审核' && !store.state.user.student_id">
              <el-button type="success" size="small" plain @click="auditPass(row, '已通过')">审核通过</el-button>
              <el-button class="mt-2 !ml-0" type="danger" size="small" plain @click="auditPass(row, '已驳回')">审核拒绝</el-button>
            </div>
            <span v-else>{{ row.LeaveSchool.application_status }}</span>
          </template>
        </el-table-column>
        <el-table-column label="审核人" width="90" prop="t_name" align="center" />
        <el-table-column label="操作" align="center" class="flex flex-col">
          <template #default="scope">
            <div v-if="searchForm.tab != 'delete'">
              <el-button class="px-1" type="primary" size="small" v-if="scope.row.LeaveSchool.application_status!=='通过'" text @click="handleEdit(scope.row.LeaveSchool.application_id)">修改</el-button>
              <el-button v-if="store.state.user.student_id && scope.row.LeaveSchool.application_status=='待审核'" class="px-1" :type="!scope.row.LeaveSchool.leave_reason ? 'danger' : 'primary'" size="small" text
                @click="handleSetGoodsContent(scope.row.LeaveSchool)"
                :loading="scope.row.contentLoading">提交申请资料</el-button>
                <el-button v-else class="px-1" :type="!scope.row.leave_reason ? 'danger' : 'primary'" size="small" text @click="open(scope.row.LeaveSchool)"> 查看申请资料 </el-button>


              <el-popconfirm title="是否要删除该申请？" confirmButtonText="确认" cancelButtonText="取消"
                @confirm="handleDelete(scope.row.LeaveSchool.application_id)">
                <template #reference>
                  <el-button class="px-1" text type="primary" size="small" v-if="scope.row.LeaveSchool.application_status=='待审核'" >删除</el-button>
                </template>
              </el-popconfirm>
            </div>
            <span v-else>暂无操作</span>
          </template>
        </el-table-column>
      </el-table>

      <div class="flex items-center justify-center mt-5">
        <el-pagination background layout="prev, pager ,next" :total="total" :current-page="currentPage" :page-size="limit"
          @current-change="getData" />
      </div>

      <FormDrawer ref="formDrawerRef" :title="drawerTitle" @submit="handleSubmit">
        <el-form :model="form" ref="formRef" :rules="rules" label-width="80px" :inline="false">
          
          <el-form-item label="离校类型" prop="LeaveSchool.leave_type">
            <el-select v-model="form.leave_type" placeholder="选择分类">
              <el-option :label="毕业离校" :value="'毕业离校'">毕业离校
              </el-option>
              <el-option :label="退学离校" :value="'退学离校'">退学离校
              </el-option>
              <el-option :label="休学离校" :value="'休学离校'">休学离校
              </el-option>
              <el-option :label="放假离校" :value="'放假离校'">放假离校
              </el-option>
            </el-select>
          </el-form-item>
          
        <el-form-item label="离校时间" prop="LeaveSchool.leave_date" >
          <el-date-picker v-model="form.leave_date" type="date" placeholder="请选择日期" format="YYYY/MM/DD"
            value-format="YYYY-MM-DD" />
      </el-form-item>
  </el-form>
      </FormDrawer>

    </el-card>

    <content ref="contentRef" @reload-data="getData" />

  </div>
</template>
<script setup>
import { ref } from "vue"
import ListHeader from "~/layout/components/ListHeader.vue";
import FormDrawer from "~/layout/components/FormDrawer.vue";
import ChooseImage from "~/layout/components/ChooseImage.vue";
import Search from "~/layout/components/Search.vue";
import SearchItem from "~/layout/components/SearchItem.vue";
import content from "./content.vue";
import {
  get_role_LeaveSchools,
  create_LeaveSchool,
  delete_LeaveSchool,
  update_LeaveSchool,
  
} from "~/api/leave_school"


import { useInitTable, useInitForm } from '~/util/useCommon.js'
import { ElNotification } from 'element-plus'

import {
  notice
} from "~/util/util"

import { useStore } from 'vuex';
const store = useStore()

const {
  handleSelectionChange,
  multipleTableRef,
  handleMultiDelete,

  searchForm,
  resetSearchForm,
  tableData,
  loading,
  currentPage,
  total,
  limit,
  getData,
  handleDelete,
  handleMultiapplication_statusChange,

  multiSelectionIds
} = useInitTable({
  searchForm: {
    word: "",
    tab: "all",
    category_id: null,
  },
  getList: get_role_LeaveSchools,
  onGetListSuccess: (res) => {
    tableData.value = res.data.list.map(o => {
      o.contentLoading = false
      return o
    })
    total.value = res.total
  },
  delete: delete_LeaveSchool,
  //`updateapplication_status: updateGoodsapplication_status
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
  },
  getData,
  update: update_LeaveSchool,
  create: create_LeaveSchool
})
const auditPass = (row, application_status) => {
  update_LeaveSchool(row.LeaveSchool.application_id, { application_status: application_status,student_id:row.LeaveSchool.student_id} ).then(res => {
    // 处理响应数据，例如刷新列表或显示提示信息
    getData()
  })
    .catch(err => {
      // 处理错误，例如显示错误信息
      console.error(err)
    })
}

const tabbars = [{
  key: "all",
  name: "全部"
}, {
  key: "待审核",
  name: "审核中"
}, {
  key: "已通过",
  name: "已完成"
}, {
  key: "已驳回",
  name: "未通过"
} 
]


// 设置商品详情
const contentRef = ref(null)
const handleSetGoodsContent = (row) => contentRef.value.open(row)

const open = (row) => {
  ElNotification({
    title: "申请资料",
    dangerouslyUseHTMLString: true,
    message: row.leave_reason,
  })
}
function useMultiAction(func, msg) {
  loading.value = true
  func(multiSelectionIds.value)
    .then(res => {
      notice(msg + "成功")
      // 清空选中
      if (multipleTableRef.value) {
        multipleTableRef.value.clearSelection()
      }
      getData()
    })
    .finally(() => {
      loading.value = false
    })
}
</script>
<template>
  <div>
    <el-tabs v-model="searchForm.tab" @tab-change="getData" class="top-10">
      <el-tab-pane :label="item.name" :name="item.key" v-for="(item, index) in tabbars" :key="index"></el-tab-pane>
    </el-tabs>

    <el-card shadow="never" class="border-0 ">
      <!-- 搜索 -->
      <Search :model="searchForm" @search="getData" @reset="resetSearchForm">
        <SearchItem label="关键词">
          <el-input v-model="searchForm.word" placeholder="题目" clearable></el-input>
        </SearchItem>
        <template #show>
          <SearchItem label="消息类型">
            <el-select v-model="searchForm.is_check" placeholder="请选择类型" clearable>
              <el-option :label="'已读'" :value="false">
              </el-option>
              <el-option :label="'未读'" :value="true">
              </el-option>
            </el-select>
          </SearchItem>
        </template>
      </Search>

      <!-- 新增|刷新 -->
      <ListHeader v-if="!store.state.user.student_id" layout="create,refresh" @create="handleCreate" @refresh="getData">
      </ListHeader>
      <ListHeader v-else layout="refresh" @create="handleCreate" @refresh="getData">
      </ListHeader>

      <el-table ref="multipleTableRef" @selection-change="handleSelectionChange" :data="tableData" stripe
        style="width: 100%" v-loading="loading" class='min-h-2xl'>
        <el-table-column type="selection" width="55" />
        <el-table-column label="消息标题" width="300">
          <template #default="{ row }">
            <div class="flex">
              <div class="flex-1">
                <p>{{ row.title }}</p>
                <div>
                </div>
                <p class="text-gray-400 text-xs">创建时间：{{ row.created_at }}</p>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_check ? 'success' : 'danger'" size="small">{{
              row.is_check?"已读":"未读" }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="store.state.user.student_id" label="发送人" width="90" prop="publisher" align="center" />
        <el-table-column v-if="!store.state.user.student_id" label="接受者" width="90" prop="target_user" align="center" />
        <el-table-column label="操作" align="center">
          <template #default="scope">
            <div v-if="searchForm.tab != 'delete'">



              <el-button v-if="store.state.user.student_id" class="px-1" :type="!scope.row.content ? 'danger' : 'primary'" size="small" text
                @click="handleSetGoodsContent(scope.row)"
                :loading="scope.row.contentLoading">查看详情</el-button>
                <el-button v-else class="px-1" :type="!scope.row.content ? 'danger' : 'primary'" size="small" text
                @click="handleSetGoodsContent(scope.row)"
                :loading="scope.row.contentLoading">标为未读</el-button>

              <el-popconfirm title="是否要删除该信息？" confirmButtonText="确认" cancelButtonText="取消"
                @confirm="handleDelete([scope.row.notification_id])">
                <template #reference>
                  <el-button class="px-1" text type="primary" size="small" >删除</el-button>
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
          <el-form-item label="发送对象">
          <el-input v-model="form.target_user_id" placeholder="学号/工号" /> 
          </el-form-item>
        <el-form-item label="消息标题" prop="title">
          <el-input v-model="form.title" placeholder="标题" /> 
      </el-form-item>
        <el-form-item label="消息内容" prop="content">
          <Editor v-model="form.content"/>
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
import Editor from "~/layout/components/Editor.vue"
import {
  get_departments,
} from "~/api/studentadmin"
import {
  get_role_notification,
  delete_notification,
  update_notification,
  create_notification,
  //delete_record,
  //update_record,
  //getGoodsList,
  //updateGoodsStatus,
  //createGoods,
  //updateGoods,
  //deleteGoods,
  //restoreGoods,
  //destroyGoods
} from "~/api/notification"
//import {
//  getCategoryList
//} from "~/api/category"

import { useInitTable, useInitForm } from '~/util/useCommon.js'
import { useStore } from 'vuex';

import {
  notice
} from "~/util/util"


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
  handleMultiStatusChange,

  multiSelectionIds
} = useInitTable({
  searchForm: {
    word: "",
    if_check:"",
    tab: "all",
    category_id: null,
  },
  getList: get_role_notification,
  onGetListSuccess: (res) => {
    tableData.value = res.data.list.map(o => {
      o.contentLoading = false
      return o
    })
    total.value = res.total
  },
  delete: delete_notification,
  //`updateStatus: updateGoodsStatus
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
  //update: updateGoods,
  create: create_notification
})
const auditPass = (row, status) => {
  update_notification(row.notification_id, { is_check: status }).then(res => {
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
  key: "uncheck",
  name: "未读"
}, {
  key: "check",
  name: "已读"
}, 
]

// 商品分类
//const category_list = ref([])
const category_list1 = ref([])
const target = ref('')
const category_list2 = ['院系管理员', '学生管理员','辅导员']



// 设置商品详情
const contentRef = ref(null)
const handleSetGoodsContent = (row) => {
  auditPass(row,true)
  contentRef.value.open(row)}


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
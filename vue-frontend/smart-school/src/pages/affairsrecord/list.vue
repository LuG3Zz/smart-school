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
          <SearchItem label="学工类型">
            <el-select v-model="searchForm.record_type" placeholder="请选择类型" clearable>
              <el-option :label="学工事务" :value="'学工事务'">学工事务
              </el-option>
              <el-option :label="学生奖惩" :value="'学生奖惩'">学生奖惩
              </el-option>
              <el-option :label="资助发放" :value="'资助发放'">资助发放
              </el-option>
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
                  <span class="text-rose-500">{{ row.StudentRecord.details }}</span>
                  <el-divider direction="vertical" />
                  <span class="text-gray-500 text-xs">{{ row.s_name }}</span>
                </div>
                <p class="text-gray-400 text-xs mb-1">类型:{{ row.StudentRecord.record_type ? row.StudentRecord.record_type
                  : "未分类" }}</p>
                <p class="text-gray-400 text-xs">创建时间：{{ row.StudentRecord.created_at }}</p>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="['通过'].includes(row.StudentRecord.status) ? 'success' : 'danger'" size="small">{{
              row.StudentRecord.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="审核状态" width="120" align="center" v-if="searchForm.tab != 'delete'">
          <template #default="{ row }">
            <div class="flex flex-col" v-if="row.StudentRecord.status == '待审核' && !store.state.user.student_id">
              <el-button type="success" size="small" plain @click="auditPass(row, '通过')">审核通过</el-button>
              <el-button class="mt-2 !ml-0" type="danger" size="small" plain @click="auditPass(row, '拒绝')">审核拒绝</el-button>
            </div>
            <span v-else>{{ row.StudentRecord.status }}</span>
          </template>
        </el-table-column>
        <el-table-column label="审核人" width="90" prop="t_name" align="center" />
        <el-table-column label="操作" align="center">
          <template #default="scope">
            <div v-if="searchForm.tab != 'delete'">
              <el-button class="px-1" type="primary" size="small" v-if="scope.row.StudentRecord.status!=='通过'" text @click="handleEdit(scope.row.StudentRecord.record_id)">修改</el-button>



              <el-button class="px-1" :type="!scope.row.content ? 'danger' : 'primary'" size="small" text
                @click="handleSetGoodsContent(scope.row.StudentRecord)"
                :loading="scope.row.contentLoading">资料详情</el-button>

              <el-popconfirm title="是否要删除该商品？" confirmButtonText="确认" cancelButtonText="取消"
                @confirm="handleDelete([scope.row.StudentRecord.record_id])">
                <template #reference>
                  <el-button class="px-1" text type="primary" size="small" v-if="scope.row.StudentRecord.status=='待审核'" >删除</el-button>
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
          <el-form-item label="类型" prop="record_type">
            <el-radio-group v-model="form.record_type">
              <el-radio :label="'学工事务'">学工事务</el-radio>
              <el-radio :label="'学生奖惩'">学生奖惩</el-radio>
              <el-radio :label="'资助发放'">资助发放</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="详细分类" prop="details">
            <el-select v-model="form.details" placeholder="选择分类">
              <el-option v-if="form.record_type == '学工事务'" v-for="item in category_list1" :key="item" :label="item"
                :value="item"></el-option>
              <el-option v-if="form.record_type == '学生奖惩'" v-for="item in category_list2" :key="item" :label="item"
                :value="item"></el-option>
              <el-option v-if="form.record_type == '资助发放'" v-for="item in category_list3" :key="item" :label="item"
                :value="item"></el-option>
            </el-select>
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
  get_role_records,
  create_record,
  delete_record,
  update_record,
  //getGoodsList,
  //updateGoodsStatus,
  //createGoods,
  //updateGoods,
  //deleteGoods,
  //restoreGoods,
  //destroyGoods
} from "~/api/record"
//import {
//  getCategoryList
//} from "~/api/category"

import { useInitTable, useInitForm } from '~/util/useCommon.js'


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
  handleMultiStatusChange,

  multiSelectionIds
} = useInitTable({
  searchForm: {
    word: "",
    tab: "all",
    category_id: null,
  },
  getList: get_role_records,
  onGetListSuccess: (res) => {
    tableData.value = res.data.list.map(o => {
      o.contentLoading = false
      return o
    })
    total.value = res.total
  },
  delete: delete_record,
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
  update: update_record,
  create: create_record
})
const auditPass = (row, status) => {
  update_record(row.StudentRecord.record_id, { status: status,student_id:row.StudentRecord.student_id} ).then(res => {
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
  key: "通过",
  name: "已完成"
}, {
  key: "拒绝",
  name: "未通过"
} 
//{
//  key: "min_stock",
//  name: "库存预警"
//}, {
//  key: "delete",
//  name: "回收站"
//}
]

// 商品分类
//const category_list = ref([])
const category_list1 = ['学生证办理','学籍异动申请']
const category_list2 = ['奖学金', '荣誉称号']
const category_list3 = ['困难生', '助学金申请', '勤工助学管理', '国家助学贷款']
//getCategoryList().then(res => category_list.value = res)


// 设置商品详情
const contentRef = ref(null)
const handleSetGoodsContent = (row) => contentRef.value.open(row)



</script>
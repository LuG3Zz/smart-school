<template>
    <div>

        <el-card shadow="never" class="border-0 my-10">
            <!-- 搜索 -->
            <Search :model="searchForm" @search="getData" @reset="resetSearchForm">
                    
                    <SearchItem label="违纪日期">
                        <el-date-picker
                            v-model="searchForm.discipline_date"
                            type="date"
                            placeholder="违纪日期"
                            style="width: 90%;"
                            value-format="YYYY-MM-DD"
                        />
                    </SearchItem>
                    <SearchItem v-if="store.state.user.student_id" label="处理人">
                        <el-input v-model="searchForm.word" placeholder="支持模糊查询" clearable></el-input>
                    </SearchItem>
                    <SearchItem  label="学生姓名">
                        <el-input v-model="searchForm.word" placeholder="支持模糊查询" clearable @change="searchForm.word='s:'+searchForm.word"></el-input>
                    </SearchItem>
            </Search>
            <ListHeader v-if="!store.state.user.student_id"  @create="handleCreate" @refresh="getData" />

            <el-table :data="tableData" stripe style="width: 100%" v-loading="loading" class='min-h-2xl'>
                <el-table-column label="违纪的学生" prop="student_name" align="center"/>
                <el-table-column label="违纪的类型" prop="discipline_type" align="center"/>
                <el-table-column label="违纪的详情" prop="discipline_detail" align="center"/>
                <el-table-column label="违纪的时间" prop="discipline_date" align="center"/>
                <el-table-column label="违纪的处分" prop="discipline_result" align="center"/>
                <el-table-column label="处理人" prop="handler_name" align="center"/>
                <el-table-column v-if="!store.state.user.student_id" fixed="right" label="操作" width="180" align="center" >
                    <template #default="{ row }">
                        
                        <el-popconfirm  title="是否要删除该记录？" confirmButtonText="确认"
                        cancelButtonText="取消" @confirm="handleDelete(row.discipline_id)">
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
        </el-card>

        <FormDrawer ref="formDrawerRef" :title="drawerTitle" @submit="handleSubmit">
            <el-form :model="form" ref="formRef" :rules="rules" label-width="80px" :inline="false">
                <el-form-item label="学生学号" prop="student_id">
                    <el-input v-model="form.student_id" placeholder="学号" style="width: 50%;"></el-input>
                </el-form-item>
                <el-form-item label="违纪类型" prop="discipline_type">
                    <el-radio-group v-model="form.discipline_type">
                        <el-radio v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="日期" prop="discipline_date">
                    <el-date-picker v-model="form.discipline_date" type="date" placeholder="请选择日期" format="YYYY/MM/DD"
                      value-format="YYYY-MM-DD" />
                  </el-form-item>
                <el-form-item label="处分" prop="discipline_result">
                    <el-select v-model="form.discipline_result" placeholder="请选择">
                      <el-option v-for="item in options_result" :key="item.department_id" :label="item.label" :value="item.value" />
                    </el-select>
                  </el-form-item>
                  <el-form-item label="详情" prop="discipline_detail">
                    <el-input v-model="form.discipline_detail" placeholder="描述" type="textarea" :rows="5"></el-input>
                  </el-form-item>
            </el-form>
        </FormDrawer>
    </div>
</template>
<script setup>
import { ref } from "vue";
import Search from "~/layout/components/Search.vue";
import SearchItem from "~/layout/components/SearchItem.vue";
import ListHeader from "~/layout/components/ListHeader.vue";
import FormDrawer from "~/layout/components/FormDrawer.vue";

import {
    get_role_disciplines,
    delete_discipline,
    create_discipline
 //student_select_course
} from "~/api/discipline";
import { useStore } from 'vuex'
import { useInitTable, useInitForm } from '~/util/useCommon.js';
import { notice } from "~/util/util";

const store = useStore()

console.log("store",store.state.user.student_id)
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
} = useInitTable({
    searchForm: {
        word: "",
        discipline_date:""
        //starttime:null,
        //endtime:null
    },
    getList: get_role_disciplines,
    onGetListSuccess: (res) => {
        tableData.value = res.data.list
        total.value = res.data.total
    },
    delete:delete_discipline
})

const starttime = ref(null)
const endtime = ref(null)
const coursedataDrawerRef = ref(null)
const teacherDataDrawerRef = ref(null)
const openDataDrawer = (id,type)=>{
    (type == "course_detail" ? coursedataDrawerRef : teacherDataDrawerRef).value.open(id)
}

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
        discipline_date: "",
        discipline_result: "",
        discipline_detail: "",
        student_id:"",
        discipline_type: "",
    },
    getData,
    create:create_discipline
})


const options = [
  {
    value: '违反校规',
    label: '违反校规',
  },
  {
    value: '违反课堂纪律',
    label: '违反课堂纪律',
  },
  {
    value: '违反考试纪律',
    label: '违反考试纪律',
  },
]

const options_result = [
  {
    value: '警告',
    label: '警告',
  },
  {
    value: '记过',
    label: '记过',
  },
  {
    value: '留校察看',
    label: '留校察看',
  },
  {
    value: '开除学籍',
    label: '开除学籍',
  },
]


</script>
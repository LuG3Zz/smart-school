<template>
  <el-card shadow="never" class="border-0 my-10 mr-10">
    <!-- 新增|刷新 -->
    <div class="flex items-center justify-between mb-4">
      <el-button v-if="!store.state.user.student_id" type="primary" size="small" @click="handleCreate">新增</el-button>
      <el-tooltip effect="dark" content="刷新数据" placement="top">
        <el-button text @click="getData">
          <el-icon :size="20">
            <Refresh />
          </el-icon>
        </el-button>
      </el-tooltip>
    </div>
    <el-table :data="tableData" stripe style="width: 100%" v-loading="loading" class='min-h-2xl'>
      <el-table-column prop="student_id" label="学号" />
      <el-table-column prop="date_of_birth" label="生日" />
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="gender" label="性别" />
      <el-table-column prop="contact_info" label="联系电话" />
      <el-table-column prop="status" label="状态" />
      <el-table-column prop="department_name" label="院系" />
      <el-table-column prop="major" label="专业" />
      <el-table-column prop="enrollment_date" label="注册时间" />
      <el-table-column label="操作" width="180" align="center" v-if="!store.state.user.student_id">
        <template #default="scope">
          <el-button type="primary" size="small" text @click="handleEdit(scope.row)">修改</el-button>

          <el-popconfirm title="是否要删除该学生？" confirmButtonText="确认" cancelButtonText="取消"
            @confirm="handleDelete(scope.row.student_id)">
            <template #reference>
              <el-button text type="primary" size="small">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <div class="flex items-center justify-center mt-5">
      <el-pagination  background layout="prev, pager ,next" :total="total" :current-page="currentPage" :page-size="limit" v-if="!store.state.user.student_id"
        @current-change="getData" />
    </div>

    <FormDrawer ref="formDrawerRef" :title="drawerTitle" @submit="handleSubmit">
      <el-form :model="form" ref="formRef" :rules="rules" label-width="80px" :inline="false">
        <el-form-item label="学号" prop="student_id">
          <el-input v-model="form.student_id" placeholder="学号"></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="姓名"></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="name">
          <el-select v-model="form.gender" placeholder="请选择性别">
            <el-option v-for="item in options_gender" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="生日" prop="name">
          <el-date-picker v-model="form.date_of_birth" type="date" placeholder="请选择日期" format="YYYY/MM/DD"
            value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="院系" prop="name">
          <el-select v-model="form.department_id" placeholder="请选择院系">
            <el-option v-for="item in options_department" :key="item.department_id" :label="item.name" :value="item.department_id" />
          </el-select>
        </el-form-item>
        <el-form-item label="专业" prop="name">
          <el-input v-model="form.major" placeholder="专业"></el-input>
        </el-form-item>
        <el-form-item label="班级" prop="name">
          <el-input v-model="form.class_" placeholder="班级"></el-input>
        </el-form-item>
        <el-form-item label="注册时间" prop="name">
          <el-date-picker v-model="form.enrollment_date" type="date" placeholder="请选择日期" format="YYYY/MM/DD"
            value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="联系方式" prop="name">
          <el-input v-model="form.contact_info" placeholder="联系方式"></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="name">
          <el-select v-model="form.status" placeholder="请选择">
            <el-option v-for="item in options_status" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
      </el-form>
    </FormDrawer>

  </el-card>
</template>
<script setup>
import { ref, reactive, computed } from "vue"
import FormDrawer from "~/layout/components/FormDrawer.vue";
import {
  get_student_list,
  create_student,
  update_student,
  delete_student,
  get_departments,
} from "~/api/studentadmin"
import {
  notice
} from "~/util/util"

import { useStore } from 'vuex';
const store = useStore()

const tableData = ref([])
const loading = ref(false)

// 分页
const currentPage = ref(1)
const total = ref(0)
const limit = ref(10)
const value = ref('')
const options_department = ref([])

const options_gender = [
  {
    value: '男',
    label: '男',
  },
  {
    value: '女',
    label: '女',
  },
]

const options_status = [
  {
    value: '在读',
    label: '在读',
  },
  {
    value: '休学',
    label: '休学',
  },
  {
    value: '退学',
    label: '退学',
  },
]
// 获取数据
function getData(p = null) {
  if (typeof p == "number") {
    currentPage.value = p
  }

  loading.value = true
  get_student_list(currentPage.value)
    .then(res => {
      tableData.value = res.data.list
      total.value = res.data.total
      console.log(res.data)
    })
  get_departments().then(res => {
    options_department.value = res.data
  })
    .finally(() => {
      loading.value = false
    })
}

getData()

// 删除
const handleDelete = (id) => {
  loading.value = true
  console.log(id)
  delete_student(id).then(res => {
    notice("删除成功")
    getData()
  }).catch(res => {
    notice("删除失败", type = "warn")

  })
    .finally(() => {
      loading.value = false
    })
}

// 表单部分
const formDrawerRef = ref(null)
const formRef = ref(null)
const form = reactive({
  student_id: "",
  name: "",
  gender: "",
  date_of_birth: "",
  department_id: "",
  major: "",
  class_: "",
  enrollment_date: "",
  contact_info: "",
  status: ""
})
const rules = {
  student_id: [{
    required: true,
    message: '学号不能为空',
    trigger: 'blur'
  }],
  name: [{
    required: true,
    message: '不能为空',
    trigger: 'blur'
  }]
}
const editId = ref(0)
const drawerTitle = computed(() => editId.value ? "修改" : "新增")

const handleSubmit = () => {
  formRef.value.validate((valid) => {
    if (!valid) return

    formDrawerRef.value.showLoading()

    const fun = editId.value ? update_student(editId.value, form) : create_student(form)

    fun.then(res => {
      notice(drawerTitle.value + "成功")
      // 修改刷新当前页，新增刷新第一页
      getData(editId.value ? false : 1)
      formDrawerRef.value.close()
    })
      .finally(() => {
        formDrawerRef.value.hideLoading()
      })

  })
}

// 重置表单
function resetForm(row = false) {
  if (formRef.value) formRef.value.clearValidate()
  if (row) {
    for (const key in form) {
      form[key] = row[key]
    }
  }
}

// 新增
const handleCreate = () => {
  editId.value = 0
  resetForm({
    title: "",
    content: ""
  })
  formDrawerRef.value.open()
}

// 编辑
const handleEdit = (row) => {
  editId.value = row
  resetForm(row)
  formDrawerRef.value.open()
}




</script>
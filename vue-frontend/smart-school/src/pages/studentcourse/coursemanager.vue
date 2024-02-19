<template>
    <el-card shadow="never" class="border-0">
        <!-- 新增|刷新 -->
        <ListHeader @create="handleCreate" @refresh="getData" />

        <el-table :data="tableData" stripe style="width: 100%" v-loading="loading">
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
            <el-table-column prop="teacher_name" label="任课老师" />
            <el-table-column label="操作" width="180" align="center">
                <template #default="scope">
                    <el-button v-if="is_in_semester(scope.row)=='进行中'" type="primary" size="small" text
                        @click="handleEdit(scope.row)">修改</el-button>

                    <el-popconfirm v-if="is_in_semester(scope.row)=='进行中'" title="是否要删除该课程？" confirmButtonText="确认"
                        cancelButtonText="取消" @confirm="handleDelete(scope.row.id)">
                        <template #reference>
                            <el-button text type="primary" size="small">删除</el-button>
                        </template>
                    </el-popconfirm>

                    <el-popconfirm v-if="is_in_semester(scope.row)=='进行中'" title="是否要让该课程失效？" confirmButtonText="失效"
                        cancelButtonText="取消" @confirm="handleStatusChange(0, scope.row)">
                        <template #reference>
                            <el-button type="danger" size="small">失效</el-button>
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
                <el-form-item label="类型" prop="type">
                    <el-radio-group v-model="form.description">
                        <el-radio :label="0">选修</el-radio>
                        <el-radio :label="1">必修</el-radio>
                        <el-radio :label="2">公选课</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="学分" prop="credits">
                    <el-input-number v-model="form.total" :min="0" :max="10"></el-input-number>
                </el-form-item>
                <el-form-item label="最低使用价格" prop="min_price">
                    <el-input v-model="form.min_price" placeholder="最低使用价格" type="number"></el-input>
                </el-form-item>
                <el-form-item label="排序" prop="order">
                    <el-input-number v-model="form.order" :min="0" :max="1000"></el-input-number>
                </el-form-item>
                <el-form-item label="活动时间">
                    <el-date-picker :editable="false" v-model="timerange" value-format="YYYY-MM-DD HH:mm:ss"
                        type="datetimerange" range-separator="To" start-placeholder="开始时间" end-placeholder="结束时间" />
                </el-form-item>
                <el-form-item label="描述" prop="desc">
                    <el-input v-model="form.desc" placeholder="描述" type="textarea" :rows="5"></el-input>
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
    get_course_list,
} from "~/api/course"
import { useInitTable, useInitForm } from '~/util/useCommon.js'


function is_in_semester(row) {
    // 解析学年和学期
    let [year, term] = row.semester.split(" 学年 ");
    let [start_year, end_year] = year.split("-");
    // 根据学期判断日期范围
    let start_date, end_date;
    if (term === "第一学期") {
        start_date = new Date(start_year, 8, 1); // 9 月 1 日
        end_date = new Date(end_year, 5, 30); // 6 月 30 日
    } else if (term === "第二学期") {
        start_date = new Date(end_year, 6, 1); // 7 月 1 日
        end_date = new Date(end_year, 11, 31); // 12 月 31 日
    } else {
        return "无效的学期";
    }
    // 获取当前日期
    let today = new Date();
    // 将日期转换为时间戳
    let today_time = today.getTime();
    let start_time = start_date.getTime();
    let end_time = end_date.getTime();
     // 判断日期是否在输入学期范围内
     if (start_time <= today_time && today_time <= end_time){
      return "进行中";
    } else if (today_time < start_time){
      return "未开放";
    } else {
      return "已过期";
    }
    
}



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
    getList: get_course_list,

    onGetListSuccess: (res) => {
        tableData.value = res.data.list
        total.value = res.total
    },
    //delete: deleteCoupon,
    //updateStatus:updateCouponStatus
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
        semester: "",
        credits: 0,
        teacher_name:"",
        department_name: "",
    },
    getData,
    //update: updateCoupon,
    //create: createCoupon,

    beforeSubmit: (f) => {
        if (typeof f.start_time != "number") {
            f.start_time = (new Date(f.start_time)).getTime()
        }
        if (typeof f.end_time != "number") {
            f.end_time = (new Date(f.end_time)).getTime()
        }
        return f
    }
})

const timerange = computed({
    get() {
        return form.start_time && form.end_time ? [form.start_time, form.end_time] : []
    },
    set(val) {
        form.start_time = val[0]
        form.end_time = val[1]
    }
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
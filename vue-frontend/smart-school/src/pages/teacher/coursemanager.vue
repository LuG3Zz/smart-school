<template>
    <div>
        <panel />
        <el-card shadow="never" class="border-0">

            <!-- 搜索 -->
            <Search :model="searchForm" @search="getData" @reset="resetSearchForm">
                <SearchItem label="时间选择">
                    <el-radio-group v-model="searchForm.semester">
                        <el-radio-button label="all">全部</el-radio-button>
                        <el-radio-button :label="getCurrentSemester()">本学期</el-radio-button>
                    </el-radio-group>
                </SearchItem>
                <template #show>
                    <SearchItem label="开始时间">
                        <el-date-picker
                            v-model="starttime"
                            type="date"
                            placeholder="开始日期"
                            style="width: 90%;"
                            value-format="YYYY-MM-DD"
                        />
                    </SearchItem>
                    <SearchItem label="结束时间">
                        <el-date-picker
                            v-model="endtime"
                            type="date"
                            placeholder="结束日期"
                            style="width: 90%;"
                            value-format="YYYY-MM-DD"
                            @change="searchForm.semester=dateToSemester(starttime,endtime)"
                        />
                    </SearchItem>
                    <SearchItem label="课程名称">
                        <el-input v-model="searchForm.word" placeholder="支持模糊查询" clearable></el-input>
                    </SearchItem>
                </template>
            </Search>

            <el-table :data="tableData" stripe style="width: 100%" v-loading="loading" class='min-h-2xl'>
                <el-table-column label="课程名" prop="course_info.name" align="center"/>
                <el-table-column label="学期" prop="course_info.semester" align="center"/>
                <el-table-column fixed="right" label="操作" width="180" align="center">
                    <template #default="{ row }">
                        <el-button type="primary" size="small" text @click="openDataDrawer(row.course_info.name,'update_course')"> 查看课程详情</el-button>
                        <el-button type="primary" size="small" text
                        @click="openDataDrawer(row.course_id,'students_detail')">查看选课学生的详情</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <div class="flex items-center justify-center mt-5">
                <el-pagination background layout="prev, pager ,next" :total="total" :current-page="currentPage"
                    :page-size="limit" @current-change="getData" />
            </div>
        </el-card>

        <dataDrawer ref="coursedataDrawerRef" type="update_course"/>
        <dataDrawer ref="StudentDataDrawerRef" type="students_detail"/>
    </div>
</template>
<script setup>
import { ref } from "vue";
import Search from "~/layout/components/Search.vue";
import SearchItem from "~/layout/components/SearchItem.vue";
import dataDrawer from "./dataDrawer.vue";
import panel from "./panel.vue";

import {
get_student_courses
} from "~/api/studentcourse";

import { useInitTable } from '~/util/useCommon.js';
import { dateToSemester, getCurrentSemester } from '~/util/util.js';
import ListHeader from "~/layout/components/ListHeader.vue";
const {
    searchForm,
    resetSearchForm,
    tableData,
    loading,
    currentPage,
    total,
    limit,
    getData,
} = useInitTable({
    searchForm: {
        word: "",
        semester: "all",
        course_id:""
        //starttime:null,
        //endtime:null
    },
    getList: get_student_courses,
    onGetListSuccess: (res) => {
        tableData.value = res.data.list
        total.value = res.data.total
    },
})

const starttime = ref(null)
const endtime = ref(null)
const coursedataDrawerRef = ref(null)
const StudentDataDrawerRef = ref(null)
const openDataDrawer = (id,type)=>{
    (type == "update_course" ? coursedataDrawerRef : StudentDataDrawerRef).value.open(id)
}




</script>
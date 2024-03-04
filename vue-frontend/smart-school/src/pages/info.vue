<template>
    <div>
    字体：
    <el-radio-group v-model="size">
      <el-radio label="large">大号</el-radio>
      <el-radio>默认</el-radio>
      <el-radio label="small">小号</el-radio>
    </el-radio-group>
    </div>
    <ElCard class="min-h-2xl mt-5">
    <el-descriptions
      class="margin-top"
      title="基本信息"
      :column="3"
      :size="size"
      border
    >
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            <el-icon :style="iconStyle">
              <user />
            </el-icon>
            姓名
          </div>
        </template>
        {{store.state.user.name }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            <el-icon :style="iconStyle">
              <iphone />
            </el-icon>
            联系方式
          </div>
        </template>
        {{store.state.user.contact_info }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            <el-icon :style="iconStyle" v-if="store.state.user.gender=='男'">
              <Male />
            </el-icon>
            <el-icon :style="iconStyle" v-else>
              <Female />
            </el-icon>
            性别
          </div>
        </template>
        {{store.state.user.gender }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            <el-icon :style="iconStyle">
              <House />
            </el-icon>
            学院
          </div>
        </template>
        {{store.state.user.department_name }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item" v-if="store.state.user.student_id" >
            <el-icon :style="iconStyle">
              <InfoFilled />
            </el-icon>
            学号
          </div>
          <div class="cell-item" v-else >
            <el-icon :style="iconStyle">
              <InfoFilled />
            </el-icon>
            工号
          </div>
        </template>
        <span v-if="store.state.user.student_id">{{store.state.user.student_id  }}</span>
        <span v-else>{{store.state.user.teacher_id  }}</span>
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            <el-icon :style="iconStyle">
              <tickets />
            </el-icon>
            身份
          </div>
        </template>
        <el-tag v-if="store.state.user.student_id" size="small">学生</el-tag>
        <el-tag v-else size="small">{{store.state.user.position}}</el-tag>
      </el-descriptions-item>
    <div v-if="store.state.user.student_id">
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            <el-icon :style="iconStyle">
              <Calendar/>
            </el-icon>
            生日
          </div>
        </template>
        {{store.state.user.date_of_birth }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            <el-icon :style="iconStyle">
              <Odometer />
            </el-icon>
            状态
          </div>
        </template>
        {{store.state.user.status }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            <el-icon :style="iconStyle">
              <Tools />
            </el-icon>
            专业
          </div>
        </template>
        {{store.state.user.major }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            <el-icon :style="iconStyle">
              <CloseBold />
            </el-icon>
            班级
          </div>
        </template>
        {{store.state.user.class_ }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            <el-icon :style="iconStyle">
              <ChatLineRound />
            </el-icon>
            注册时间
          </div>
        </template>
        {{store.state.user.enrollment_date }}
      </el-descriptions-item>
    </div>
    </el-descriptions>
  
    <el-descriptions
      class="margin-top"
      title="用户信息"
      :column="3"
      :size="size"
      :style="blockMargin"
    >
      <el-descriptions-item label="用户id">{{store.state.user.user_info.user_id}}</el-descriptions-item>
      <el-descriptions-item label="用户名">{{store.state.user.user_info.username}}</el-descriptions-item>
    </el-descriptions>
</ElCard>
  </template>
  v-if="!store.state.user.student_id"
  <script setup lang="ts">
  import { computed, ref } from 'vue'
  import {
      Calendar,
      ChatLineRound,
      CloseBold,
      InfoFilled,
    Iphone,
    Location,
    Male,
    Odometer,
    OfficeBuilding,
    Tickets,
    Tools,
    User,
  } from '@element-plus/icons-vue'
  import { useStore } from 'vuex';
import { ElCard } from 'element-plus';

const store = useStore()
  
  const size = ref('')
  const iconStyle = computed(() => {
    const marginMap = {
      large: '8px',
      default: '6px',
      small: '4px',
    }
    return {
      marginRight: marginMap[size.value] || marginMap.default,
    }
  })
  const blockMargin = computed(() => {
    const marginMap = {
      large: '32px',
      default: '28px',
      small: '24px',
    }
    return {
      marginTop: marginMap[size.value] || marginMap.default,
    }
  })
  </script>
  
  <style scoped>
  .el-descriptions {
    margin-top: 20px;
  }
  .cell-item {
    display: flex;
    align-items: center;
  }
  .margin-top {
    margin-top: 20px;
  }
  </style>
  
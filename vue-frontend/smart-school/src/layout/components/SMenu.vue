<template>
  <el-aside class="sidebar">
    <el-menu
      class="nav-links"
      :default-active="defaultActive"
      router
      background-color="transparent"
      text-color="#fff"
      active-text-color="#ffd04b"
    >
      <!-- Submenu example -->
      <div class="flex flex-col mx-auto my-3">
      <el-sub-menu v-for="submenu in submenus" :key="submenu.name" :index="submenu.index">
        <template #title>
          <el-icon :size="20"><component :is="submenu.icon" /></el-icon>
          <span>{{ submenu.name }}</span>
        </template>
        <el-menu-item v-for="item in submenu.children" :key="item.name" :index="item.href">
          <el-icon :size="20"><component :is="item.icon" /></el-icon>
          <span>{{ item.name }}</span>
        </el-menu-item>
      </el-sub-menu>
   </div>
    </el-menu>
  </el-aside>
</template>

<script setup>
import {ref,computed} from 'vue'
import { ElAside, ElMenu, ElMenuItem, ElSubMenu, ElIcon } from 'element-plus';
import { User, Notebook, House, Menu } from '@element-plus/icons-vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex'

const router = useRouter()
const store = useStore()
const defaultActive = ref(router.currentRoute.value.path)



const mainLinks = [
  { href: '/home', icon: House, text: '主页' },
];

const submenus = computed(()=>store.state.menus)
  



</script>

<style >
.sidebar {
  width: 240px;
  min-height: 87.5vh; 
  @apply  bg-gradient-to-b from-green-500 to-blue-200 my-5 ml-5  

}

.nav-links {
  @apply text-center
}
</style>

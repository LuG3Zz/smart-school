<template>
    <div>
        <el-container>
            <el-header>
                <s-header></s-header>
            </el-header>
            <el-container>
                <el-aside>
                    <s-menu></s-menu>
                </el-aside>
                <el-main>
                    <s-tag-list></s-tag-list>
                    <Transition name="fade">
                    <RouterView>
                    </RouterView>

                    </Transition>
                </el-main>
            </el-container>
        </el-container>

    </div>
</template>

<script setup>
import SHeader from './components/SHeader.vue'
import SMenu from './components/SMenu.vue'
import STagList from './components/STagList.vue'

</script>

<style >
.fade-enter-from {
    opacity: 0;
    -webkit-transform: translate3d(0, -2000px, 0);
    transform: translate3d(0, -2000px, 0);

}
.fade-enter-to {
    opacity: 1;
    -webkit-transform: translate3d(0, 0, 0);
    transform: translate3d(0, 0, 0);

}
.fade-leave-from {
    opacity: 1;

}
.fade-leave-to {
    opacity: 0;
    -webkit-transform: translate3d(0, 2000px, 0);
    transform: translate3d(0, 2000px, 0);

}

.fade-enter-active,
.fade-leave-active{
    transition: all 0.3s;
}
.fade-enter-active{
    transition-delay: 0.3s;
}






</style>
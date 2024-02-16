<script setup>

</script>

<template>
  <router-view></router-view>
</template>

<style >
body{
   @apply bg-green-100

}

.btn{
  @apply bg-purple-500 text-indigo-50 px-4 py-2 rounded-full transition-all duration-500 hover:(bg-purple-900) focus:(ring-8 ring-light-100)

}
#nprogress .bar{
  background-color: #f4f4f4!important;
  height: 3px!important;

}
</style>

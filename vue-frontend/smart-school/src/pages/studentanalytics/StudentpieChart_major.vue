
<template>
    <el-card shadow="never">
        <template #header>
            <div class="flex justify-between">
                <span class="text-sm">{{ myTitle2 }}</span>
                
            </div>
        </template>
        <div ref="el" id="chart1" style="width: 100%;height: 300px;"></div>
    </el-card>
</template>
<script setup>
import { ref, onMounted,onBeforeUnmount } from 'vue';
import * as echarts from 'echarts';
import { useResizeObserver } from '@vueuse/core'


import {
  get_analytics1
} from "~/api/users.js"

const current = ref("all")

const handleChoose = (type) => {
    current.value = type
    getData()
}
const myTitle2=ref('')
var myChart1 = null
onMounted(() => {
    var chartDom1 = document.getElementById('chart1');
    if(chartDom1){
        myChart1 = echarts.init(chartDom1);
        getData()
    }
})

onBeforeUnmount(()=>{
    if(myChart1) echarts.dispose(myChart1)
})

function getData() {
  let option = {
  title: {
    text: '',
    subtext: '',
    left: ''
  },
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b} : {c} ({d}%)'
  },
  legend: {
    orient: 'horizontal',
    left: 'left'

  },
  
  series: [
    {
      name: '',
      type: 'pie',
      radius: [20, 100],
      center: ['50%', '50%'],
      roseType: 'area',
      itemStyle: {
        borderRadius: 5
      },
      data: [
        
      ]
    }
  ]
};

    myChart1.showLoading()
    get_analytics1().then(res=>{
        
        option.series[0].name = res.data.title.text
        option.series[0].data = res.data.data
        option.legend.data = res.data.data

        myChart1.setOption(option)
        myTitle2.value=res.data.title.text
    }).finally(()=>{
        myChart1.hideLoading()
    })



}

const el = ref(null)


</script>

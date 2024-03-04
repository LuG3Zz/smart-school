
<template>
    <el-card shadow="never">
        <template #header>
            <div class="flex justify-between">
                <span class="text-sm">{{ myTitle }}</span>
                
            </div>
        </template>
        <div ref="el" id="chart" style="width: 100%;height: 300px;"></div>
    </el-card>
</template>
<script setup>
import { ref, onMounted,onBeforeUnmount } from 'vue';
import * as echarts from 'echarts';
import { useResizeObserver } from '@vueuse/core'


import {
    getStatistics3
} from "~/api/users.js"

const current = ref("all")

const handleChoose = (type) => {
    current.value = type
    getData()
}
const myTitle=ref('')
var myChart = null
onMounted(() => {
    var chartDom = document.getElementById('chart');
    if(chartDom){
        myChart = echarts.init(chartDom);
        getData()
    }
})

onBeforeUnmount(()=>{
    if(myChart) echarts.dispose(myChart)
})

function getData() {
    let option = {
  title: {
    text: '',
    subtext: '',
    left: 'center'
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      name: '',
      type: 'pie',
      radius: '50%',
      data: [
      ],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
};
    myChart.showLoading()
    getStatistics3(current.value).then(res=>{
        
        option.series[0].name = res.data.title.name
        option.series[0].data = res.data.data

        myChart.setOption(option)
        myTitle.value=res.data.title.text
    }).finally(()=>{
        myChart.hideLoading()
    })



}

const el = ref(null)
useResizeObserver(el, (entries) => myChart.resize())

</script>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'

const chartRef = ref(null)
const dateValue = ref(new Date().toISOString().split('T')[0])
let chart = null

const formatDate = (date) => {
  return date.replace(/-/g, '')
}

const fetchData = async () => {
  try {
    const formattedDate = formatDate(dateValue.value)
    const response = await axios.get(`http://ebike.littleking.site/api/get_vehicle_data?date=${formattedDate}`)
    const data = response.data

    const timestamps = data.map(item => new Date(parseInt(item.timestamp) * 1000).toLocaleTimeString())
    const voltages = data.map(item => parseFloat(item.voltage))
    const speeds = data.map(item => parseFloat(item.speed))

    updateChart(timestamps, voltages, speeds)
  } catch (error) {
    console.error('获取数据失败:', error)
  }
}

const updateChart = (timestamps, voltages, speeds) => {
  const option = {
    title: {
      text: '电动车数据监控',
      subtext: `日期: ${dateValue.value}`
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['电压', '速度']
    },
    xAxis: {
      type: 'category',
      data: timestamps
    },
    yAxis: [
      {
        name: '电压(V)',
        type: 'value'
      },
      {
        name: '速度(km/h)',
        type: 'value'
      }
    ],
    series: [
      {
        name: '电压',
        type: 'line',
        data: voltages,
        yAxisIndex: 0,
        smooth: true
      },
      {
        name: '速度',
        type: 'line',
        data: speeds,
        yAxisIndex: 1,
        smooth: true
      }
    ]
  }
  
  chart.setOption(option)
}

onMounted(() => {
  chart = echarts.init(chartRef.value)
  fetchData()
})
</script>

<template>
  <div class="chart-container">
    <div class="date-picker">
      <input 
        type="date" 
        v-model="dateValue"
        @change="fetchData"
      >
    </div>
    <div ref="chartRef" class="chart"></div>
  </div>
</template>

<style scoped>
.chart-container {
  width: 100%;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.date-picker {
  margin-bottom: 20px;
}

.date-picker input {
  padding: 8px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
}

.chart {
  width: 100%;
  height: 500px;
}
</style> 
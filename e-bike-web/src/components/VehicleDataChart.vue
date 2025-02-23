<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'

const chartRef = ref(null)
const activeTab = ref('today')
const dateRange = ref({
  start: new Date().toISOString().split('T')[0],
  end: new Date().toISOString().split('T')[0]
})
let chart = null

const formatDate = (date) => {
  return date.replace(/-/g, '')
}

const getFormattedDate = (daysAgo) => {
  const date = new Date()
  date.setDate(date.getDate() - daysAgo)
  return date.toISOString().split('T')[0]
}

const getDatesBetween = (startDate, endDate) => {
  const dates = []
  let currentDate = new Date(startDate)
  const end = new Date(endDate)
  
  while (currentDate <= end) {
    dates.push(new Date(currentDate).toISOString().split('T')[0])
    currentDate.setDate(currentDate.getDate() + 1)
  }
  return dates
}

const mergeData = (allData) => {
  const timestamps = []
  const voltages = []
  const speeds = []
  
  allData.forEach(dayData => {
    dayData.forEach(item => {
      const time = new Date(parseInt(item.timestamp) * 1000)
      timestamps.push(time.toLocaleString())
      voltages.push(parseFloat(item.voltage))
      speeds.push(parseFloat(item.speed))
    })
  })
  
  return { timestamps, voltages, speeds }
}

const fetchData = async (dates) => {
  try {
    const allData = []
    for (const date of dates) {
      const formattedDate = formatDate(date)
      const response = await axios.get(`http://ebike.littleking.site/api/get_vehicle_data?date=${formattedDate}`)
      allData.push(response.data)
    }
    
    const { timestamps, voltages, speeds } = mergeData(allData)
    updateChart(timestamps, voltages, speeds)
  } catch (error) {
    console.error('获取数据失败:', error)
  }
}

const handleTabChange = (tab) => {
  activeTab.value = tab
  const today = new Date().toISOString().split('T')[0]
  
  switch (tab) {
    case 'today':
      dateRange.value = { start: today, end: today }
      fetchData([today])
      break
    case 'threeDays':
      const threeDaysAgo = getFormattedDate(2)
      dateRange.value = { start: threeDaysAgo, end: today }
      fetchData(getDatesBetween(threeDaysAgo, today))
      break
    case 'sevenDays':
      const sevenDaysAgo = getFormattedDate(6)
      dateRange.value = { start: sevenDaysAgo, end: today }
      fetchData(getDatesBetween(sevenDaysAgo, today))
      break
    case 'custom':
      fetchData(getDatesBetween(dateRange.value.start, dateRange.value.end))
      break
  }
}

const validateDateRange = () => {
  const start = new Date(dateRange.value.start)
  const end = new Date(dateRange.value.end)
  
  if (start > end) {
    dateRange.value.end = dateRange.value.start
  }
}

const handleDateRangeChange = (type) => {
  validateDateRange()
  activeTab.value = 'custom'
  handleTabChange('custom')
}

const updateChart = (timestamps, voltages, speeds) => {
  const option = {
    title: {
      // text: '电动车数据监控',
      subtext: '时间范围: ' + timestamps[0] + ' 至 ' + timestamps[timestamps.length - 1],
      left: 'center',
      padding: [10, 0]
    },
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        const time = params[0].axisValue
        let result = `${time}<br/>`
        params.forEach(param => {
          result += `${param.seriesName}: ${param.value}<br/>`
        })
        return result
      }
    },
    legend: {
      data: ['电压', '速度'],
      top: 40
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',  // 增加底部空间
      top: '15%',     // 增加顶部空间
      containLabel: true  // 确保刻度标签在图表区域内
    },
    xAxis: {
      type: 'category',
      data: timestamps,
      axisLabel: {
        rotate: 45,
        interval: 'auto',  // 自动计算间隔
        formatter: function (value) {
          // 只显示时间部分
          return value
        }
      }
    },
    yAxis: [
      {
        name: '电压(V)',
        type: 'value',
        nameTextStyle: {
          padding: [0, 0, 0, 40]  // 调整y轴名称位置
        }
      },
      {
        name: '速度(km/h)',
        type: 'value',
        nameTextStyle: {
          padding: [0, 40, 0, 0]  // 调整y轴名称位置
        }
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
  handleTabChange('today')
})
</script>

<template>
  <div class="chart-container">
    <div class="header">
      <h1>电动车数据监控</h1>
      <div class="controls">
        <div class="tabs">
          <button 
            :class="{ active: activeTab === 'today' }"
            @click="handleTabChange('today')"
          >
            今天
          </button>
          <button 
            :class="{ active: activeTab === 'threeDays' }"
            @click="handleTabChange('threeDays')"
          >
            最近三天
          </button>
          <button 
            :class="{ active: activeTab === 'sevenDays' }"
            @click="handleTabChange('sevenDays')"
          >
            最近七天
          </button>
        </div>
        <div class="date-range-picker">
          <input 
            type="date" 
            v-model="dateRange.start"
            :max="dateRange.end"
            @change="handleDateRangeChange('start')"
          >
          <span>至</span>
          <input 
            type="date" 
            v-model="dateRange.end"
            :min="dateRange.start"
            @change="handleDateRangeChange('end')"
          >
        </div>
      </div>
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
  box-sizing: border-box;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 20px;
}

.controls {
  display: flex;
  align-items: center;
  gap: 20px;
}

.tabs {
  display: flex;
  gap: 10px;
}

.tabs button {
  padding: 8px 16px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  transition: all 0.3s;
}

.tabs button.active {
  background: #409eff;
  color: #fff;
  border-color: #409eff;
}

.tabs button:hover {
  border-color: #409eff;
}

h1 {
  margin: 0;
  font-size: 24px;
  color: #2c3e50;
}

.date-range-picker {
  display: flex;
  align-items: center;
  gap: 8px;
}

.date-range-picker input {
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  width: 150px;
}

.date-range-picker span {
  color: #606266;
}

.chart {
  width: 100%;
  height: calc(100vh - 120px);
  min-height: 600px;
  padding: 10px;  /* 添加内边距 */
}
</style> 
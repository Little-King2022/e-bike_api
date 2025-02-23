<script setup>
import VehicleDataChart from './components/VehicleDataChart.vue'
</script>

<template>
  <div class="container">
    <h1>电动车数据监控</h1>
    <VehicleDataChart />
  </div>
</template>

<style>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
}
</style>

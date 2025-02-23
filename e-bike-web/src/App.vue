<script setup>
import VehicleDataChart from './components/VehicleDataChart.vue'
</script>

<template>
  <div class="container">
    <!-- <h1>电动车数据监控</h1> -->
    <VehicleDataChart />
  </div>
</template>

<style>
.container {
  width: 100%;
  min-height: 100vh;
  margin: 0;
  padding: 0;
  background-color: #f5f7fa;
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
}
</style>

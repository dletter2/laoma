<template>
  <div class="dashboard">
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-value">{{ stats?.resource_count || 0 }}</div>
            <div class="stat-label">资源总数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-value warning">{{ stats?.pending_count || 0 }}</div>
            <div class="stat-label">待审核资源</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-value success">{{ stats?.published_count || 0 }}</div>
            <div class="stat-label">已上架资源</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-value">{{ stats?.user_count || 0 }}</div>
            <div class="stat-label">用户总数</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-card class="chart-card">
      <template #header><span>资源分类分布</span></template>
      <div ref="chartRef" style="height: 400px;"></div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { statisticsApi } from '../api/statistics'
import type { Statistics } from '../types'

const stats = ref<Statistics | null>(null)
const chartRef = ref<HTMLElement>()
let chartInstance: echarts.ECharts | null = null
let resizeHandler: (() => void) | null = null

onMounted(async () => {
  try {
    const res = await statisticsApi.get()
    stats.value = res.data.data || null
    if (chartRef.value && stats.value) {
      chartInstance = echarts.init(chartRef.value)
      chartInstance.setOption({
        tooltip: { trigger: 'item' },
        xAxis: {
          type: 'category',
          data: stats.value.category_distribution.map((c) => c.name),
        },
        yAxis: { type: 'value' },
        series: [{
          data: stats.value.category_distribution.map((c) => c.count),
          type: 'bar',
          itemStyle: { color: '#409eff', borderRadius: [4, 4, 0, 0] },
        }],
      })
      resizeHandler = () => chartInstance?.resize()
      window.addEventListener('resize', resizeHandler)
    }
  } catch {
    // ignore
  }
})

onUnmounted(() => {
  if (resizeHandler) {
    window.removeEventListener('resize', resizeHandler)
  }
  chartInstance?.dispose()
  chartInstance = null
})
</script>

<style scoped>
.stat-cards { margin-bottom: 24px; }
.stat-item { text-align: center; padding: 16px 0; }
.stat-value { font-size: 32px; font-weight: 700; color: #303133; }
.stat-value.warning { color: #e6a23c; }
.stat-value.success { color: #67c23a; }
.stat-label { font-size: 14px; color: #909399; margin-top: 8px; }
.chart-card { margin-top: 24px; }
</style>

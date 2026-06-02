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
            <div class="stat-value">{{ stats?.user_count || 0 }}</div>
            <div class="stat-label">用户总数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-value success">{{ stats?.today_resources || 0 }}</div>
            <div class="stat-label">今日新增资源</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-value success">{{ stats?.today_users || 0 }}</div>
            <div class="stat-label">今日新增用户</div>
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
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { statisticsApi } from '../api/statistics'
import type { Statistics } from '../types'

const stats = ref<Statistics | null>(null)
const chartRef = ref<HTMLElement>()

onMounted(async () => {
  try {
    const res = await statisticsApi.get()
    stats.value = res.data.data || null
    if (chartRef.value && stats.value) {
      const chart = echarts.init(chartRef.value)
      chart.setOption({
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
      window.addEventListener('resize', () => chart.resize())
    }
  } catch {
    // ignore
  }
})
</script>

<style scoped>
.stat-cards { margin-bottom: 24px; }
.stat-item { text-align: center; padding: 16px 0; }
.stat-value { font-size: 32px; font-weight: 700; color: #303133; }
.stat-value.success { color: #67c23a; }
.stat-label { font-size: 14px; color: #909399; margin-top: 8px; }
.chart-card { margin-top: 24px; }
</style>

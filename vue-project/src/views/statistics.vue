<script lang="js" setup>
import {onMounted, ref} from "vue"
import echarts from "@/router/echars.js";
import {get_statistics} from "@/views/statistics/statistics.js";

const r_user_count = ref()

function f_user_count(s) {
  if (!s.user_count) {
    return
  }
  let data = []
  for (let i in s.user_count) {
    data.push({
      name: i,
      value: s.user_count[i]
    })
  }
  const option = {
    title: {
      text: '用户类型统计',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      top: '5%',
      left: 'center'
    },
    series: [
      {
        name: '用户类型',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        padAngle: 5,
        itemStyle: {
          borderRadius: 10
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 40,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: data,
      }
    ]
  }
  const myChart = echarts.init(r_user_count.value)
  myChart.setOption(option)
}

const r_user_verify = ref()

function f_user_verify(s) {
  if (!s.user_verify) {
    return
  }
  let data = []
  for (let i in s.user_verify) {
    data.push({
      name: i,
      value: s.user_verify[i]
    })
  }
  const option = {
    title: {
      text: '用户审核统计',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      top: '5%',
      left: 'left'
    },
    series: [
      {
        name: '用户审核',
        type: 'pie',
        data: data,
      }
    ]
  };
  const myChart = echarts.init(r_user_verify.value)
  myChart.setOption(option)
}

const r_user_log_by = ref()

function f_user_log_by(s) {
  if (!s.user_log_by) {
    return
  }
  let data = []
  for (let i in s.user_log_by) {
    data.push({
      name: i,
      value: s.user_log_by[i]
    })
  }
  const option = {
    title: {
      text: '用户登录方式统计',
      left: 'center'
    },
    series: [
      {
        name: '用户登录方式',
        type: 'pie',
        roseType: 'area',
        itemStyle: {
          borderRadius: 8
        },
        data: data,
      }
    ]
  }
  const myChart = echarts.init(r_user_log_by.value)
  myChart.setOption(option)
}

const r_user_department = ref()

function f_user_department(s) {
  if (!s.user_department) {
    return
  }
  let data = []
  let xAxis = []
  for (let i in s.user_department) {
    data.push(s.user_department[i])
    xAxis.push(i)
  }
  const option = {
    title: {
      text: '用户科室统计',
      left: 'center'
    },
    xAxis: {
      type: 'category',
      data: xAxis
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: data,
        colorBy: 'data',
        type: 'bar'
      }
    ]
  }
  const myChart = echarts.init(r_user_department.value)
  myChart.setOption(option)
}

const r_consent_count = ref()

function f_consent_count(s) {
  if (!s.consent_count) {
    return
  }
  let data = []
  for (let i in s.consent_count) {
    data.push({
      name: i,
      value: s.consent_count[i]
    })
  }
  let option = {
    title: {
      text: '同意书统计',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      top: '5%',
      left: 'center'
    },
    series: [
      {
        name: '总计',
        type: 'pie',
        radius: ['45%', '60%'],
        labelLine: {
          length: 30
        },
        data: data
      },
    ]
  };
  if (s.consent_me) {
    let data1 = []
    for (let i in s.consent_me) {
      data1.push({
        name: i,
        value: s.consent_me[i]
      })
    }
    let data2 = {
      name: '我的',
      type: 'pie',
      selectedMode: 'single',
      radius: [0, '30%'],
      label: {
        position: 'inner',
        fontSize: 14
      },
      labelLine: {
        show: false
      },
      data: data1
    }
    option.series.push(data2)
  }
  const myChart = echarts.init(r_consent_count.value)
  myChart.setOption(option)
}

const r_consent_sign_date = ref()

function f_consent_sign_date(s) {
  if (!s.consent_sign_date) {
    return
  }
  let data = []
  let xAxis = []
  for (let i in s.consent_sign_date) {
    data.push(s.consent_sign_date[i])
    xAxis.push(i)
  }
  const option = {
    title: {
      text: '每日签署',
      left: 'center'
    },
    xAxis: {
      type: 'category',
      data: xAxis
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: data,
        colorBy: 'data',
        type: 'line'
      }
    ]
  };
  const myChart = echarts.init(r_consent_sign_date.value)
  myChart.setOption(option)
}

onMounted(async () => {
  const s0 = await get_statistics()
  const s = s0.data
  // 1. 用户类型统计
  await f_user_count(s)
  // 2. 用户审核统计
  await f_user_verify(s)
  // 3. 用户登录方式统计
  await f_user_log_by(s)
  // 4. 用户科室统计
  await f_user_department(s)
  // 5. 同意书统计
  await f_consent_count(s)
  // 6. 同意书签署日期统计
  await f_consent_sign_date(s)
})
</script>

<template>
  <div class="box0">
    <el-scrollbar>
      <div ref="r_user_log_by" class="box"></div>
      <div ref="r_consent_count" class="box"></div>
      <div ref="r_consent_sign_date" class="box"></div>
      <div ref="r_user_department" class="box"></div>
      <div ref="r_user_count" class="box"></div>
      <div ref="r_user_verify" class="box"></div>
    </el-scrollbar>
  </div>
</template>

<style scoped>
.box0 {
  width: 100%;
  height: 100%;
  padding: 10px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.box {
  min-width: 300px;
  width: 100%;
  height: 400px;
  padding: 20px;
}
</style>
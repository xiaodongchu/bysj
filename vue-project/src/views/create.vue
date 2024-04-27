<script lang="js" setup>
import {ref} from 'vue'

import sign from '@/views/create/sign.vue'
import templ from '@/views/create/templ.vue'

const activeName = ref('template')
</script>

<template>
  <div style="width: 100%;boxShadow: --el-box-shadow;">
    <el-tabs v-model="activeName" class="demo-tabs" type="border-card">
      <el-tab-pane label="创建模板" name="template">
        <div style="width: 100%;text-align: center;">
          <el-text class="mx-1">您正在创建模板</el-text>
        </div>
        <templ></templ>
      </el-tab-pane>
      <el-tab-pane label="创建同意书" name="sign">
        <div style="width: 100%;text-align: center;">
          <el-text class="mx-1">您正在创建同意书</el-text>
        </div>
        <sign></sign>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>

</style>

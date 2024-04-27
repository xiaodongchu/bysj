<script lang="js" setup>
import {ref} from 'vue'

import userinfo from '@/views/admin/userinfo.vue'
import inform from '@/views/admin/inform.vue'

const activeName = ref('userinfo')
</script>

<template>
  <div style="width: 100%;">
    <el-tabs v-model="activeName" class="demo-tabs" type="border-card">
      <el-tab-pane label="管理用户" name="userinfo">
        <userinfo></userinfo>
      </el-tab-pane>
      <el-tab-pane label="通知管理" name="inform">
        <inform></inform>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>

</style>

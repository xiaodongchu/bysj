<script lang="js" setup>
import {useStore} from "vuex";
import {useRouter} from "vue-router";

const store = useStore()
const router = useRouter();

</script>

<template>
  <div style="width: 100%">
    <el-menu
        :ellipsis="false"
        :router="true"
        active-text-color="#ffffff"
        background-color="#409eff"
        class="el-menu-top"
        mode="horizontal"
        text-color="#ecf5ff"
    >
      <el-menu-item class="el-menu-item" index="0" @click="router.back">
        <el-text style="color: white">欢迎，{{ store.state.user_name }}{{ store.state.user_class }}</el-text>
      </el-menu-item>
      <div class="flex-grow" style="flex-grow: 1;width: 100%;"/>
      <el-menu-item v-if="store.state.user_class === '管理员'" class="el-menu-item" index="/admin">管理员</el-menu-item>
      <el-menu-item class="el-menu-item" index="/statistics">数据统计</el-menu-item>
      <el-menu-item class="el-menu-item" index="/create">创建</el-menu-item>
      <el-menu-item class="el-menu-item" index="/settings">设置</el-menu-item>
      <el-menu-item class="el-menu-item" index="/">回到首页</el-menu-item>
    </el-menu>
  </div>
</template>

<style scoped>

.el-menu-top {
  width: 100%;
  padding: 0;
  margin: 0;
}

.el-menu-item {
  padding: 0 5px;
  margin: 0;
}
</style>

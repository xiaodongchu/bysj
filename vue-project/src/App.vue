<script lang="js" setup>
import appMenu from "./views/app/appMenu.vue";
import {useStore} from "vuex";
import {onMounted} from "vue";
import {getSelfBaseProfile} from "@/views/app/app.js";
import {ElNotification} from "element-plus";
import {useRouter} from "vue-router";

const store = useStore()
const router = useRouter()

onMounted(async () => {
  if(!localStorage._authing_token){
    await router.push('/login')
  }
  else{
    const res = await getSelfBaseProfile()
    store.commit('set_user_verify', res.data['user_verify'])
    store.commit('set_user_name', res.data['user_name'])
    store.commit('set_user_class', res.data['user_class'])
    localStorage.setItem('authing_id', res.data['authing_id'])
    if (res.data['user_verify']) {
      ElNotification({
        title: '登陆成功',
        message: '欢迎',
        type: 'success',
      })
    } else {
      ElNotification({
        title: '请联系管理员认证账号身份',
        message: '',
        type: 'warning',
        duration: 0,
      })
      await router.replace({path: '/settings'})
    }
  }
})
</script>

<template>
  <div style="width: 100%;height: 100%">
    <appMenu style="width: 100%"></appMenu>
    <router-view style="width: 100%;"></router-view>
  </div>
</template>

<style scoped>

</style>

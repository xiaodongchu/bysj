<script lang="js">
import {Guard} from "@authing/vue-ui-components";
import "@authing/vue-ui-components/lib/index.min.css";
import {getSelfBaseProfile} from "@/views/app/app.js";
import store from "@/router/store.js";
import router from '@/router'
import {ElMessage} from "element-plus";


export default {
  name: 'login',
  data() {
    return {
      appId: "62fc94595854df71f7bbe61e",
      guard_config: {
        target: "#guard",
        autoRegister: true,
        disableRegister: false,
        contentCss: ".g2-view-container {margin: 0 auto;background-color: #f7f8fa;} .g2-view-header > img { width:70px !important; height:70px !important; } .title {font-size:30px !important;}",
      },
    }
  },
  components: {
    Guard
  },
  computed: {},
  methods: { //登录或注册后,localStorage中就有了user的信息,可直接跳转至主页,让主页组件读取信息
    onLogin: async () => {
      store.commit('set_search_content', '')
      store.commit('set_search_type', 'unsigned')
      store.commit('clear_home_cards')
      const res = await getSelfBaseProfile()
      store.commit('set_user_verify', res.data['user_verify'])
      store.commit('set_user_name', res.data['user_name'])
      store.commit('set_user_class', res.data['user_class'])
      localStorage.setItem('authing_id', res.data['authing_id'])
      ElMessage.success('登录成功')
      await router.replace('/')
      // location.reload()
    },
    onRegister: async () => {
      store.commit('set_search_content', '')
      store.commit('set_search_type', 'unsigned')
      store.commit('clear_home_cards')
      const res = await getSelfBaseProfile()
      store.commit('set_user_verify', res.data['user_verify'])
      store.commit('set_user_name', res.data['user_name'])
      store.commit('set_user_class', res.data['user_class'])
      localStorage.setItem('authing_id', res.data['authing_id'])
      ElMessage.success('注册成功, 请完善个人信息')
      await router.replace('/settings')
    },
  },
}
</script>

<template>
  <div style="width: 100%">
    <div id="guard">
      <!-- Authing提供的Guard组件 -->
      <Guard :appId="appId" :config="guard_config" class="guard-component" @login="onLogin"
             @register="onRegister"></Guard>
    </div>
  </div>
</template>

<style scoped>

</style>
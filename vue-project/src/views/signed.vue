<script lang="js" setup>
import {get_html, get_pdf} from "@/views/sign/sign.js";
import {onMounted, ref} from "vue";
import {useRoute} from "vue-router";
import {get_full_link, openLink} from "@/router/newwindow.js";
import clipboard from 'clipboard';
import {ElNotification} from "element-plus";

const active = ref(6)
const route = useRoute()
const signed_id = ref('')
const pre_html = ref('')

onMounted(async () => {
  signed_id.value = route.params.id
  const res = await get_html(signed_id.value)
  pre_html.value = res.data['html']
})

async function open_pdf() {
  const res = await get_pdf(signed_id.value)
  openLink("/download/" + res.data['code'])
}

async function copy_pdf_link() {
  const res = await get_pdf(signed_id.value)
  const link = get_full_link("/download/" + res.data['code'])
  clipboard.copy(link)
  ElNotification({
    title: '成功',
    message: '一次性下载链接已写入剪切板！有效期：24h',
    type: 'success',
    duration: 10000
  });
}

</script>

<template>
  <div style="width: 100%">
    <el-steps :active="active" finish-status="success" simple style="max-width: 100%">
      <el-step title="信息"/>
      <el-step title="介绍"/>
      <el-step title="风险"/>
      <el-step title="特殊"/>
      <el-step title="选择"/>
      <el-step title="签署"/>
      <el-step title="完成"/>
    </el-steps>
  </div>
  <el-button style="margin: 20px" type="success" @click="open_pdf">打开pdf</el-button>
  <el-button style="margin: 20px" type="success" @click="copy_pdf_link">复制下载链接</el-button>
  <div style="width: 100%;margin: 20px">
    <el-scrollbar>
      <div v-html="pre_html"></div>
    </el-scrollbar>
  </div>
</template>

<style scoped>

</style>
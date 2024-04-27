<script lang="js" setup>
import {onMounted, reactive, ref} from "vue";
import signpad from "@/views/sign/signpad.vue";
import {ElMessage} from "element-plus";
import {useRoute, useRouter} from "vue-router";
import {post_html, post_sign} from "@/views/sign/sign.js";


const active_choice = ref('0')
const router = useRouter()
const route = useRoute()
const edit_id = ref('')
const pre_html = ref('')
const dialogVisible = ref(false)
const form = reactive({
  id: 0,
  doctor_sign: '',
  patient_sign: '',
  other_sign: false,
  other_sign_info: '',
})
onMounted(() => {
  edit_id.value = route.params.id
  form.id = parseInt(route.params.id)
})

const change_choice = (val) => {
  form.other_sign = val !== '0';
}

function to_next_page() {
  router.replace('/signed/' + edit_id.value)
}

async function submit() {
  if (form.patient_sign === '' || form.doctor_sign === '') {
    ElMessage.error('请签名')
    return
  }
  if (form.other_sign) {
    if (form.other_sign_info === '') {
      ElMessage.error('请填写代签署人信息')
      return
    }
  }
  await post_sign(edit_id.value, form)
  ElMessage.success('签署成功')
  to_next_page()
}

async function open_dialog() {
  console.log(form)
  const res = await post_html(edit_id.value, form)
  console.log(res)
  pre_html.value = res.data['html']
  dialogVisible.value = true
}

</script>

<template>
  <div style="width: 100%">
    <el-form :model="form" label-width="auto" style="width: 100%;">
      <el-form-item>
        <el-text class="demo-text">签名人</el-text>
        <el-radio-group v-model="active_choice" @change="change_choice">
          <el-radio size="large" value="0">本人</el-radio>
          <el-radio size="large" value="1">代签署</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item v-if="form.other_sign">
        <el-text class="demo-text">签署人信息</el-text>
        <el-input
            v-model="form.other_sign_info"
            autosize
            type="textarea"
        ></el-input>
      </el-form-item>

      <el-form-item>
        <el-text>患者签名</el-text>
        <signpad v-model="form.patient_sign"></signpad>
      </el-form-item>

      <el-form-item>
        <el-text>医生签名</el-text>
        <signpad v-model="form.doctor_sign"></signpad>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submit">提交签署</el-button>
        <el-button type="primary" @click="open_dialog">预览</el-button>
      </el-form-item>
    </el-form>
  </div>

  <div>
    <el-dialog
        v-model="dialogVisible"
        title="预览"
        width="100%"
    >
      <el-scrollbar max-height="700px">
        <div v-html="pre_html"></div>
      </el-scrollbar>
    </el-dialog>
  </div>
</template>

<style scoped>
.end-button {
  width: 100%;
  /* top | right | bottom | left */
  margin: 20px 0 10px 30px;
  justify-items: center;
}

.demo-text {
  margin: 5px;
}
</style>
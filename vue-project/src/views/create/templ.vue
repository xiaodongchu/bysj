<script lang="js" setup>
import {onMounted, reactive} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {create_template} from "@/views/create/create.js";
import {ElMessage, ElMessageBox} from "element-plus";

const router = useRouter()
const route = useRoute()

onMounted(() => {
  if (route.query.base_type && route.query.base_id && route.query.base_id !== '0') {
    form.base_type = route.query.base_type
    form.base_id = route.query.base_id
    form.link = '/' + route.query.base_type + '/' + route.query.base_id
    form.surgery_name = route.query.name
  }
})

// do not use same name with ref
const form = reactive({
  base_type: "",
  base_id: "0",
  link: '',
  surgery_name: "",
  template_intro: '',
  is_public: true,
})

const onSubmit = async () => {
  if (!form.base_id) {
    form.base_id = "0"
  }
  const res = await create_template(form)
  const new_id = res.data['new_id']
  ElMessage.success('创建成功')
  await router.replace('/edit/template/' + new_id)
}
const onCancel = () => {
  ElMessageBox.confirm(
      '更改可能未保存，确定要离开吗？',
      'Warning',
      {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        type: 'warning',
      }
  )
      .then(() => {
        router.back()
      })
      .catch()
}
</script>

<template>
  <div>
    <el-form :model="form" label-width="auto" style="max-width: 100%">

      <el-form-item label="引用链接">
        <el-input v-model="form.link" disabled/>
      </el-form-item>

      <el-form-item
          :rules="{
          required: true,
          message: 'Please input Activity name',
          trigger: ['blur', 'change'],
        }"
          label="手术名称"
          prop="surgery_name"
      >
        <el-input v-model="form.surgery_name"/>
      </el-form-item>

      <el-form-item label="模板说明">
        <el-input
            v-model="form.template_intro"
            autosize
            type="textarea"
        />
      </el-form-item>

      <el-form-item label="是否公开">
        <el-switch v-model="form.is_public"/>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit">创建模板</el-button>
        <el-button @click="onCancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>


<style scoped>

</style>

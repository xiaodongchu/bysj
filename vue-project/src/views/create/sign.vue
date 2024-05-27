<script lang="js" setup>
import {onMounted, reactive, ref} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {create_sign, search_user_by_name} from "@/views/create/create.js";
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
  base_id: "",
  link: "",
  surgery_name: "",
  patient_name: '',
  patient_sex: '女',
  patient_birth: '',
  hospital_id: '',
  permission_list: [],
})

const loading = ref(false)
const options = ref([])

async function remoteMethod(query) {
  if (query) {
    loading.value = true
    const res = await search_user_by_name(query)
    options.value = res.data['search_result']
    loading.value = false
  }
}

const onSubmit = async () => {
  console.log(form)
  if (!form.base_id) {
    form.base_id = "0"
  }
  if (!form.patient_birth) {
    form.patient_birth = new Date().toISOString().slice(0, 10)
  }
  const res = await create_sign(form)
  const new_id = res.data['new_id']
  ElMessage.success('创建成功')
  await router.replace('/edit/unsigned/' + new_id)
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
        prop="surgery_name">
      <el-input v-model="form.surgery_name"/>
    </el-form-item>

    <el-form-item
        :rules="{
          required: true,
          message: 'Please input Activity name',
          trigger: ['blur', 'change'],
        }"
        label="病人姓名"
        prop="patient_name"
    >
      <el-input v-model="form.patient_name"/>
    </el-form-item>

    <el-form-item label="病人性别">
      <el-radio-group v-model="form.patient_sex">
        <el-radio value="女">女</el-radio>
        <el-radio value="男">男</el-radio>
      </el-radio-group>
    </el-form-item>

    <el-form-item label="病人生日">
      <el-date-picker
          v-model="form.patient_birth"
          format="YYYY-MM-DD"
          placeholder="选择病人生日"
          type="date"
          value-format="YYYY-MM-DD"
      />
    </el-form-item>

    <el-form-item label="病历号">
      <el-input v-model="form.hospital_id"/>
    </el-form-item>

    <el-form-item label="授权他人查看">
      <el-select
          v-model="form.permission_list"
          :loading="loading"
          :remote-method="remoteMethod"
          filterable
          multiple
          placeholder="输入姓名以查找"
          remote
          reserve-keyword
      >
        <el-option
            v-for="item in options"
            :key="item.authing_id"
            :label="item.user_name + '  ' + item.hospital_id"
            :value="item.authing_id"
        />
        <template #loading>
          <svg class="circular" viewBox="0 0 50 50">
            <circle class="path" cx="25" cy="25" fill="none" r="20"/>
          </svg>
        </template>
      </el-select>
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="onSubmit">创建同意书</el-button>
      <el-button @click="onCancel">取消</el-button>
    </el-form-item>
  </el-form>
</template>


<style scoped>
.circular {
  display: inline;
  height: 30px;
  width: 30px;
  animation: loading-rotate 2s linear infinite;
}

.path {
  animation: loading-dash 1.5s ease-in-out infinite;
  stroke-dasharray: 90, 150;
  stroke-dashoffset: 0;
  stroke-width: 2;
  stroke: var(--el-color-primary);
  stroke-linecap: round;
}
</style>

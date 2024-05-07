<script lang="js" setup>
import {onMounted, reactive, ref} from 'vue'
import {getUserSetting, updateUserSetting} from "@/views/settings/settings.js";
import {useStore} from "vuex";
import {useRouter} from "vue-router";
import {logOut, unVerify} from "@/router/log_out.js";
import {ElMessage, ElMessageBox} from "element-plus";


const store = useStore()
const router = useRouter()

const user_class = ref('')

const form = reactive({
  user_id: "",
  user_name: "",
  user_class: "",
  user_verify: true,
  verify_info: '',
  department: '',
  hospital_id: '',
  email: '',
  phone: '',
  create_time: '',
})

onMounted(async () => {
  form.user_id = localStorage.getItem('authing_id')
  form.user_verify = store.state.user_verify
  form.user_name = store.state.user_name
  form.user_class = store.state.user_class
  await reset()
})

async function reset() {
  const res = await getUserSetting()
  user_class.value = res.data['user_class']
  form.user_name = res.data['user_name']
  form.user_class = res.data['user_class']
  form.user_verify = res.data['user_verify']
  form.verify_info = res.data['verify_info']
  form.department = res.data['department']
  form.hospital_id = res.data['hospital_id']
  form.email = res.data['email']
  form.phone = res.data['phone']
  form.create_time = res.data['create_time']
}

function pop_box() {
  ElMessageBox.confirm(
      '更改身份组需要管理员重新验证，确定继续吗？',
      'Warning',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
  ).then(
      () => {
        form.user_verify = false
        form.verify_info = ''
      }
  ).catch(() => {
    reset()
  })
}

async function onSubmit() {
  await updateUserSetting(form)
  if (!form.user_verify) {
    unVerify()
  }
  await reset()
  ElMessage.success('更新成功')
  await onCancel()
}

async function onCancel() {
  if (form.user_verify) {
    router.back()
  }
}

function refresh() {
  location.reload()
}

function onLogOut() {
  logOut()
}

</script>

<template>
  <div class="out-button-div">
    <el-button type="danger" @click="onLogOut">退出登录</el-button>
    <el-button type="success" @click="refresh">刷新</el-button>
  </div>

  <div style="width: 100%">
    <el-form :model="form" class="el-form1" label-width="auto">

      <el-form-item label="用户id">
        <el-input v-model="form.user_id" disabled/>
      </el-form-item>

      <el-form-item label="姓名">
        <el-input v-model="form.user_name"/>
      </el-form-item>

      <el-form-item label="用户身份">
        <el-select
            v-model="form.user_class"
            placeholder="用户身份"
            size="large"
            style="width: 200px"
            @change="pop_box"
        >
          <el-option label="医生" value="医生"/>
          <el-option label="护士" value="护士"/>
          <el-option label="管理员" value="管理员"/>
        </el-select>
      </el-form-item>

      <el-form-item label="所属部门">
        <el-input v-model="form.department"/>
      </el-form-item>

      <el-form-item label="医院工号">
        <el-input v-model="form.hospital_id"/>
      </el-form-item>

      <el-form-item label="认证权限">
        <el-switch v-model="form.user_verify" disabled/>
      </el-form-item>

      <el-form-item label="认证备注">
        <el-input
            v-model="form.verify_info"
            autosize
            disabled
            type="textarea"
        />
      </el-form-item>

      <el-form-item label="邮箱">
        <el-input v-model="form.email" disabled/>
      </el-form-item>

      <el-form-item label="手机">
        <el-input v-model="form.phone" disabled/>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit">更新信息</el-button>
        <el-button @click="reset">重置</el-button>
        <el-button type="info" @click="onCancel">取消</el-button>
      </el-form-item>

    </el-form>

  </div>
</template>

<style scoped>
.el-form1 {
  max-width: 100%;
  margin: 10px;
  background-color: #FAFCFF;
}

.out-button-div {
  width: 100%;
  margin: 10px;
}
</style>
<script lang="js" setup>
import {onMounted, reactive, ref} from "vue";
import {Search} from '@element-plus/icons-vue'
import {get_search, get_user_data, hide_user, post_user_data} from "@/views/admin/admin.js";
import {ElMessage} from "element-plus";

const input = ref('')
const verify = ref(false)
const show_hide = ref(false)
const result = ref([])
const edit_authing_id = ref('')
const dialogFormVisible = ref(false)

const form = reactive({
  user_id: '',
  user_name: '',
  user_class: '',
  user_verify: false,
  verify_info: '',
  phone: '',
  email: '',
  department: '',
  hospital_id: '',
})

const tableRowClassName = (row) => {
  if (!row.user_verify) {
    return 'warning-row'
  } else if (row.user_class === '管理员') {
    return 'success-row'
  }
  return ''
}

async function do_search() {
  let search_content = input.value
  let res = await get_search(search_content, verify.value, show_hide.value)
  res = res.data['search_result']
  result.value = res
  ElMessage.success('搜索成功')
}

async function click_edit(row) {
  dialogFormVisible.value = true
  edit_authing_id.value = row.authing_id
  let res = await get_user_data(edit_authing_id.value)
  form.user_id = res.data["authing_id"]
  form.user_name = res.data["user_name"]
  form.user_class = res.data["user_class"]
  form.user_verify = res.data["user_verify"]
  form.verify_info = res.data["verify_info"]
  form.phone = res.data["phone"]
  form.email = res.data["email"]
  form.department = res.data["department"]
  form.hospital_id = res.data["hospital_id"]
}

function click_cancel() {
  dialogFormVisible.value = false
}

async function click_confirm() {
  let res = await post_user_data(edit_authing_id.value, form)
  ElMessage.success('更新成功')
  dialogFormVisible.value = false
  await do_search()
}


async function click_hide(row, hide) {
  let res = await hide_user(row.authing_id, hide)
  ElMessage.success('操作成功')
  await do_search()
}

onMounted(async () => {
  await do_search()
})
</script>


<template>
  <div style="width: 100%">
    <div style="width: 100%; padding: 10px">
      <el-row justify="space-between" style="width: 100%;">
        <el-input
            v-model="input"
            class="input-with-select"
            placeholder="用户姓名"
            style="width: 100%"
        >
          <template #append>
            <el-button :icon="Search" @click="do_search"/>
          </template>
        </el-input>
        <el-switch v-model="verify" active-text="未验证用户"/>
        <el-switch v-model="show_hide" active-text="显示隐藏的未验证用户"/>
      </el-row>
    </div>


    <div style="width: 100%">
      <el-table
          :data="result"
          :row-class-name="tableRowClassName"
          border
          max-height="700"
          stripe
          style="width: 100%"
      >
        <el-table-column fixed="left" label="姓名" prop="user_name"/>
        <el-table-column label="身份" prop="user_class"/>
        <el-table-column label="认证" prop="user_verify">
          <template #default="{row}">
            <el-tag v-if="row.user_verify" type="success">已验证</el-tag>
            <el-tag v-else type="danger">未验证</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="id" prop="authing_id"/>
        <el-table-column align="left" fixed="right" label="操作" style="flex-direction: column;">
          <template #default="{row}">
            <el-button type="warning" @click="click_edit(row)">操作</el-button>
          </template>
        </el-table-column>
        <el-table-column label="隐藏">
          <template #default="{row}">
            <el-button v-if="row.hide_in_admin" type="primary" @click="click_hide(row,false)">取消</el-button>
            <el-button v-else type="danger" @click="click_hide(row,true)">隐藏</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>


    <div style="width: 100%">
      <el-dialog v-model="dialogFormVisible" class="el-dialog1" style="width: 100%" title="用户操作">
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
                clearable
                placeholder="用户身份"
                size="large"
            >
              <el-option label="医生" value="医生"/>
              <el-option label="护士" value="护士"/>
              <el-option label="管理员" value="管理员"/>
            </el-select>
          </el-form-item>

          <el-form-item label="认证权限">
            <el-switch v-model="form.user_verify"/>
          </el-form-item>

          <el-form-item label="认证备注">
            <el-input
                v-model="form.verify_info"
                autosize
                type="textarea"
            />
          </el-form-item>

          <el-form-item label="所属部门">
            <el-input v-model="form.department"/>
          </el-form-item>

          <el-form-item label="医院工号">
            <el-input v-model="form.hospital_id"/>
          </el-form-item>

          <el-form-item label="邮箱">
            <el-input v-model="form.email" disabled/>
          </el-form-item>

          <el-form-item label="手机">
            <el-input v-model="form.phone" disabled/>
          </el-form-item>

        </el-form>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="click_cancel">取消</el-button>
            <el-button type="primary" @click="click_confirm">更新</el-button>
          </div>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<style scoped>
.el-form1 {
  width: 100%;
  margin: 5px;
  background-color: #FAFCFF;
}

.el-dialog1 {
  width: 100%;
  margin: 5px;
  border: 1px solid #e0e0e0;
}
</style>
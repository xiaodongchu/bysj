<script lang="js" setup>
import {onMounted, reactive, ref} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {search_user_by_name} from "@/views/create/create.js";
import {get_unsigned, post_unsigned} from "@/views/edit/edit.js";
import {ElMessage, ElMessageBox} from "element-plus";
import htmlview from "@/views/edit/htmlview.vue";

const dialogFormVisible = ref(false)
const router = useRouter()
const route = useRoute()

onMounted(async () => {
  await form_init()
})

// 表单数据
const form = reactive({
  id: 0,
  surgery_name: '',
  hospital_name: "",
  patient_name: '',//c
  patient_sex: '女',//c
  patient_birth: '',//c
  hospital_id: '',//c
  disease_name: '',
  anesthesia_type: '',
  surgery_intro: "",
  risk_intro: "",
  risk_list: [],
  patient_choice: [],
  doctor_state: "",
  template_intro: "",//t
  is_public: false,//t
  update_data: [],//t
  special_risk_list: [],//c
  permission_list: [],//c
})

// 表单数据初始化
async function form_init() {
  const res = await get_unsigned(Number(route.params.id))
  if (res.data["is_signed"]) {
    await router.replace({path: '/signed/' + route.params.id})
  }
  form.id = res.data['id']
  form.surgery_name = res.data['surgery_name']
  form.hospital_name = res.data['hospital_name']
  form.patient_name = res.data['patient_name']
  form.patient_sex = res.data['patient_sex']
  form.patient_birth = res.data['patient_birth']
  form.hospital_id = res.data['hospital_id']
  form.disease_name = res.data['disease_name']
  form.anesthesia_type = res.data['anesthesia_type']
  form.surgery_intro = res.data['surgery_intro']
  form.risk_intro = res.data['risk_intro']
  form.risk_list = res.data['risk_list']
  form.special_risk_list = res.data['special_risk_list']
  form.patient_choice = res.data['patient_choice']
  form.doctor_state = res.data['doctor_state']
  form.permission_list = res.data['permission_list']
  form.update_data = res.data['update_data']
}

// 提交表单
async function onSubmit() {
  await post_unsigned(route.params.id, form)
  ElMessage.success('更新成功')
  router.back()
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

// 搜索用户
const loading = ref(false)
const options = ref([])

async function search_user(query) {
  if (query) {
    loading.value = true
    const res = await search_user_by_name(query)
    options.value = res.data['search_result']
    loading.value = false
  }
}

// 编辑列表
const edit_type = ref('')
const list_edit = ref([])
const allow_sub = ref(false)

function edit_menu(type) {
  if (type === 'risk') {
    edit_type.value = 'risk'
    list_edit.value = form.risk_list
    allow_sub.value = true
    dialogFormVisible.value = true
  } else if (type === 'special_risk') {
    edit_type.value = 'special_risk'
    list_edit.value = form.special_risk_list
    allow_sub.value = true
    dialogFormVisible.value = true
  } else if (type === 'patient_choice') {
    edit_type.value = 'patient_choice'
    list_edit.value = form.patient_choice
    allow_sub.value = false
    dialogFormVisible.value = true
  } else if (type === "update_data") {
    edit_type.value = 'update_data'
    list_edit.value = form.update_data
    allow_sub.value = false
    dialogFormVisible.value = true
  }
}

function dialog_close() {
  if (edit_type.value === 'risk') {
    form.risk_list = list_edit.value
  } else if (edit_type.value === 'special_risk') {
    form.special_risk_list = list_edit.value
  } else if (edit_type.value === 'patient_choice') {
    form.patient_choice = list_edit.value
  } else if (edit_type.value === 'update_data') {
    form.update_data = list_edit.value
  }
  edit_type.value = ''
  dialogFormVisible.value = false
}

function dialog_close_warning() {
  if (edit_type.value) {
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
          edit_type.value = ''
          dialogFormVisible.value = false
        })
        .catch(() => {
          dialogFormVisible.value = true
        })
  }
}

function add_parent() {
  list_edit.value.push({text: ''})
}

function remove_parent(index) {
  list_edit.value.splice(index, 1)
}

function add_child(index) {
  if (!list_edit.value[index].children) {
    list_edit.value[index].children = []
  }
  list_edit.value[index].children.push({text: ''})
}

function remove_child(index, index_child) {
  list_edit.value[index].children.splice(index_child, 1)
}

const show_html = ref(false)
</script>

<template>
  <div style="width: 100%;margin: 20px">
    <el-button type="success" @click="show_html = !show_html">查看html</el-button>
    <htmlview v-if="show_html" v-model="form"></htmlview>
  </div>
  <div style="width: 100%;margin: 10px">

    <el-form :model="form" label-width="auto" style="max-width: 95%">

      <el-form-item label="id">
        <el-input v-model="form.id" disabled/>
      </el-form-item>

      <el-form-item
          label="医院名称"
          prop="hospital_name">
        <el-input v-model="form.hospital_name"/>
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

      <el-form-item label="疾病名称">
        <el-input v-model="form.disease_name"/>
      </el-form-item>

      <el-form-item label="麻醉方式">
        <el-input v-model="form.anesthesia_type"/>
      </el-form-item>

      <el-form-item label="手术简介">
        <el-input
            v-model="form.surgery_intro"
            autosize
            type="textarea"
        />
      </el-form-item>

      <el-form-item label="风险简介">
        <el-input
            v-model="form.risk_intro"
            autosize
            type="textarea"
        />
      </el-form-item>

      <el-form-item label="风险列表">
        <el-button type="success" @click="edit_menu('risk')">编辑风险列表</el-button>
      </el-form-item>

      <el-form-item label="特殊风险列表">
        <el-button type="success" @click="edit_menu('special_risk')">编辑特殊风险列表</el-button>
      </el-form-item>

      <el-form-item label="病人选择">
        <el-button type="success" @click="edit_menu('patient_choice')">编辑病人选择</el-button>
      </el-form-item>

      <el-form-item label="医生声明">
        <el-input
            v-model="form.doctor_state"
            autosize
            type="textarea"
        />
      </el-form-item>

      <el-form-item label="授权他人查看">
        <el-select
            v-model="form.permission_list"
            :loading="loading"
            :remote-method="search_user"
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

      <el-form-item label="更新记录">
        <el-button type="success" @click="edit_menu('update_data')">更新记录</el-button>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit">更新同意书</el-button>
        <el-button type="danger" @click="onCancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>

  <div>
    <el-dialog v-model="dialogFormVisible" title="编辑" width="500" @close="dialog_close_warning">
      <el-form :model="list_edit" style="max-width: 100%;flex-direction: column;justify-items: center;">
        <el-form-item>
          <div v-for="(item, index) in list_edit" :key="'p-{{index}}'" class="parent">
            <el-input
                v-model="item.text"
                autosize
                placeholder="描述"
                type="textarea"
            />
            <el-button @click="remove_parent(index)">删除</el-button>
            <div v-for="(item_child, index_child) in item.children" v-if="allow_sub" :key="'c-{{index_child}}'"
                 class="child">
              <el-input
                  v-model="item_child.text"
                  autosize
                  placeholder="子项描述"
                  type="textarea"
              />
              <el-button @click="remove_child(index, index_child)">删除</el-button>
            </div>
            <el-button v-if="allow_sub" @click="add_child(index)">增加子项</el-button>
          </div>
        </el-form-item>
        <el-form-item>
          <el-button @click="add_parent">增加</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="dialog_close">确定</el-button>
          <el-button type="danger" @click="dialog_close_warning">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>

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

.parent {
  width: 90%;
  flex-direction: column;
  justify-items: center;
  /* top | right | bottom | left */
  padding: 3px;
  margin: 5px;
  border: 1px solid #e0e0e0;
  background-color: #F2F3F5;
}

.child {
  max-width: 90%;
  padding: 5px;
  /* top | right | bottom | left */
  margin: 5px 5px 5px 10px;
  border: 1px solid #e0e0e0;
  background-color: #FAFCFF;
}
</style>

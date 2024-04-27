<script lang="js" setup>
import {onMounted, reactive, ref} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {get_template, post_template} from "@/views/edit/edit.js";
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
  const res = await get_template(Number(route.params.id))
  form.id = res.data['id']
  form.surgery_name = res.data['surgery_name']
  form.hospital_name = res.data['hospital_name']
  form.disease_name = res.data['disease_name']
  form.anesthesia_type = res.data['anesthesia_type']
  form.surgery_intro = res.data['surgery_intro']
  form.risk_intro = res.data['risk_intro']
  form.risk_list = res.data['risk_list']
  form.patient_choice = res.data['patient_choice']
  form.doctor_state = res.data['doctor_state']
  form.template_intro = res.data['template_intro']
  form.is_public = res.data['is_public']
  form.update_data = res.data['update_data']
}

// 提交表单
async function onSubmit() {
  await post_template(route.params.id, form)
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
    <el-form :model="form" label-width="auto" style="max-width:95%">

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

      <el-form-item label="模板说明">
        <el-input
            v-model="form.template_intro"
            autosize
            type="textarea"
        />
      </el-form-item>

      <el-form-item label="是否公开">
        <el-switch v-model="form.is_public" active-text="公开" inactive-text="不公开"/>
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

<script lang="js" setup>
import {onMounted, reactive, ref} from 'vue'
import {useRoute, useRouter} from "vue-router";
import {get_unsigned} from "@/views/sign/sign.js";
import signpads from "@/views/sign/signpads.vue";

const active = ref(0)
const router = useRouter()
const route = useRoute()

function next() {
  active.value++
  if (active.value >= 6) {
    router.replace('/signed/' + route.params.id)
  }
}

function prev() {
  active.value--
  if (active.value < 0) {
    active.value = 0
  }
}


onMounted(async () => {
  await form_init()
})

// 表单数据
const form = reactive({
  id: 0,
  surgery_name: '',
  hospital_name: "",
  patient_name: '',
  patient_sex: '女',
  patient_birth: '',
  hospital_id: '',
  disease_name: '',
  anesthesia_type: '',
  surgery_intro: "",
  risk_intro: "",
  risk_list: [],
  special_risk_list: [],
  patient_choice: [],
  doctor_state: "",
  permission_list: [],
  update_data: [],
})

// 表单数据初始化
async function form_init() {
  const res = await get_unsigned(Number(route.params.id))
  if (res.data['is_signed']) {
    await router.replace('/signed/' + route.params.id)
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

  <div style="width: 100%">
    <!-- 表单1:用户基础信息 -->
    <el-card v-if="0===active" class="card0">
      <el-form :model="form" class="form0" label-width="auto">
        <el-form-item label="姓名">
          <el-text>{{ form.patient_name }}</el-text>
        </el-form-item>
        <el-form-item label="性别">
          <el-text>{{ form.patient_sex }}</el-text>
        </el-form-item>
        <el-form-item label="生日">
          <el-text>{{ form.patient_birth }}</el-text>
        </el-form-item>
        <el-form-item label="病历号">
          <el-text>{{ form.hospital_id }}</el-text>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 表单2:手术介绍 -->
    <el-card v-if="active===1" class="card0">
      <el-form :model="form" class="form0" label-width="auto">
        <el-form-item label="手术名称">
          <el-text>{{ form.surgery_name }}</el-text>
        </el-form-item>
        <el-form-item label="疾病名称">
          <el-text>{{ form.disease_name }}</el-text>
        </el-form-item>
        <el-form-item label="麻醉方式">
          <el-text>{{ form.anesthesia_type }}</el-text>
        </el-form-item>
        <el-form-item label="手术介绍">
          <el-text>{{ form.surgery_intro }}</el-text>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 表单3:风险介绍 -->
    <el-card v-if="active===2" class="card0">
      <el-form :model="form" class="form0" label-width="auto">
        <el-form-item label="风险介绍">
          <el-text>{{ form.risk_intro }}</el-text>
        </el-form-item>
        <el-form-item label="风险列表">
          <div class="subform">
            <div v-for="(item, index) in form.risk_list" :key="'p-{{index}}'" class="parent">
              <el-text>{{ item.text }}</el-text>
              <div v-for="(item_child, index_child) in item.children" :key="'c-{{index_child}}'" class="child">
                <el-text>{{ item_child.text }}</el-text>
              </div>
            </div>
          </div>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 表单4:特殊风险 -->
    <el-card v-if="active===3" class="card0">
      <el-form :model="form" class="form0" label-width="auto">
        <el-form-item label="特殊风险列表">
          <div class="subform">
            <div v-for="(item, index) in form.special_risk_list" :key="'p-{{index}}'" class="parent">
              <el-text>{{ item.text }}</el-text>
            </div>
          </div>
        </el-form-item>
        <el-form-item label="医生声明">
          <el-text type="info">{{ form.doctor_state }}</el-text>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 表单5:知情选择 -->
    <el-card v-if="active===4" class="card0">
      <el-form :model="form" class="form0" label-width="auto">
        <el-form-item label="知情选择">
          <div class="subform">
            <div v-for="item in form.patient_choice" class="choose-for">
              <el-checkbox class="long-check-box">
                <el-text>{{ item.text }}</el-text>
              </el-checkbox>
            </div>
          </div>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 表单6:签署 -->
    <el-card v-if="active===5" class="card0">
      <signpads></signpads>
    </el-card>

  </div>


  <div style="width: 100%">
    <el-row v-if="active<6" class="end-button">
      <el-col :span="4"></el-col>
      <el-col :span="4">
        <el-button type="primary" @click="prev">上一步</el-button>
      </el-col>
      <el-col :span="4"></el-col>
      <el-col :span="4"></el-col>
      <el-col :span="4">
        <el-button v-if="active<5" type="primary" @click="next">下一步</el-button>
      </el-col>
      <el-col :span="4"></el-col>
    </el-row>
  </div>

</template>

<style scoped>
.card0 {
  margin: 10px;
  padding: 10px;
  width: 100%;
}

.end-button {
  width: 100%;
  margin-top: 20px;
}

.subform {
  max-width: 100%;
  flex-direction: column;
  justify-items: center;
}

.parent {
  width: 90%;
  flex-direction: column;
  justify-items: center;
  /* top | right | bottom | left */
  padding: 3px;
  margin: 5px;
  border: 1px solid #e0e0e0;
  background-color: #FAFCFF;
}

.child {
  max-width: 90%;
  padding: 5px;
  /* top | right | bottom | left */
  margin: 5px 5px 5px 10px;
  border: 1px solid #e0e0e0;
  background-color: #F2F3F5;
}

.choose-for {
  max-width: 90%;
  padding: 5px;
  margin: 5px;
  border: 1px solid #e0e0e0;
  background-color: #FAFCFF;
}

.long-check-box {
  width: 100%;
  margin: 5px;
  white-space: normal;
  word-wrap: break-word;
  word-break: break-word;
}
</style>
<script lang="js" setup>
import {ref} from 'vue'
import {delete_by_id, get_search} from "@/views/home/home.js";
import {useStore} from "vuex";
import {useRouter} from 'vue-router'

import {CircleCheckFilled, CirclePlusFilled, Loading} from "@element-plus/icons-vue";

const store = useStore()
const router = useRouter()

const search_c = ref('')
const in_load = ref(true)
const search_t = ref('')
const need_load = ref(true)

const load = async () => {
  in_load.value = true
  let end_id = store.state.home_cards.length
  const search_content = store.state.search_content
  const search_type = store.state.search_type
  if (search_content !== search_c.value || search_type !== search_t.value) {
    search_c.value = search_content
    search_t.value = search_type
    need_load.value = true
  }
  if (need_load.value) {
    const res = await get_search(search_type, search_content, end_id, 10)
    store.commit('merge_home_cards', res.data['search_result'])
    if (res.data['search_result'].length < 10) {
      need_load.value = false
    }
  }
  in_load.value = false
}

function click_edit(self_class, self_id) {
  const s = {path: '/edit/' + self_class + '/' + self_id}
  router.push(s)
}

function click_sign(self_id) {
  const s = {path: '/sign/' + self_id}
  router.push(s)
}

function click_signed(self_id) {
  const s = {path: '/signed/' + self_id}
  router.push(s)
}

function click_create(self_class, self_id, surgery_name) {
  const s = {path: '/create', query: {'base_type': self_class, 'base_id': self_id, 'name': surgery_name}}
  router.push(s)
}

async function click_delete(self_class, self_id) {
  await delete_by_id(self_class, self_id)
}

// item = {
// # 是否有权（未签署返回一定有权，已签署返回无权会脱敏）
// 'have_permission': True,
// # 未签署、有权、医生
// 'can_sign': True,
// # 创建(模板或脱敏的已签署）
// 'create_time': '2021-10-01 12:00:00',
// 'create_user_name': '张三',
// # 未签署同意书或模板显示
// 'last_update_time': '2021-10-01 12:00:00',
// 'last_update_user_name': '张三',
// # 已签署同意书显示
// 'sign_time': '2021-10-01 12:00:00',
// # 链接信息
// 'self_class': 'template',
// 'self_id': '1',
// # 已签署同意书非授权不显示姓名，仅支持创建模板
// 'patient_name': '张三',
// 'surgery_name': '腹腔镜手术',
// # 模板信息
// 'template_info': '胆囊结石',
// }
</script>

<template>
  <div style="width: 100%; height:700px">
    <ul v-infinite-scroll="load" class="infinite-list">
      <li v-for="item in store.state.home_cards" class="infinite-list-item">
        <el-card class="infinite-card" shadow="always">
          <template #header>
            <div class="common-layout" style="width: 100%;align-content: center;align-items: center;text-align: left">
              <!-- 已签署 -->
              <el-text v-if="item.have_permission && item.self_class === 'signed'" class="mx-1" type="success">
                <el-icon color="green" size="20px">
                  <CircleCheckFilled/>
                </el-icon>
                签署于 {{ item.sign_time }}
              </el-text>
              <!-- 未签署 -->
              <el-text v-else class="mx-1">
                <el-icon v-if="item.self_class === 'unsigned'" color="#409eff" size="20px">
                  <CirclePlusFilled/>
                </el-icon>
                <el-icon v-else color="green" size="20px">
                  <CircleCheckFilled/>
                </el-icon>
                &emsp;{{ item.last_update_user_name }} 编辑于{{ item.last_update_time }}
              </el-text>
            </div>
          </template>
          <div>
            <!-- 有权的已签署、未签署 -->
            <el-text v-if="item.self_class === 'template'" class="mx-1">{{ item.template_info }}</el-text>
            <el-text v-else-if="item.have_permission" class="mx-1">{{ item.patient_name }}</el-text>
            <br>
            <el-text class="mx-1">{{ item.surgery_name }}</el-text>
            <br>
            <el-text class="mx-1">{{ item.create_user_name }} 创建于 {{ item.create_time }}</el-text>
          </div>
          <template #footer>
            <!-- 未签署的返回内容一定有权 -->
            <!-- 可下载：有权的已签署 -->
            <el-button v-if="item.have_permission && item.self_class === 'signed'" type="success"
                       @click="click_signed(item.self_id)">查看与下载
            </el-button>
            <!-- 可编辑：未签署、模板 -->
            <el-button v-if="item.self_class === 'unsigned' || item.self_class === 'template'" type="primary"
                       @click="click_edit(item.self_class,item.self_id)">编辑
            </el-button>
            <!-- 可签署：未签署 -->
            <el-button v-if="item.can_sign && item.self_class === 'unsigned'" type="success"
                       @click="click_sign(item.self_id)">签署
            </el-button>
            <!-- 可生成模板：已签署、模板 -->
            <el-button v-if="item.self_class === 'signed' || item.self_class === 'template'" type="primary"
                       @click="click_create(item.self_class,item.self_id,item.surgery_name)">引用创建
            </el-button>
            <!-- 可删除：未签署、有权的模板 -->
            <el-button v-if="item.have_permission && (item.self_class === 'unsigned' || item.self_class === 'template')"
                       type="danger" @click="click_delete(item.self_class,item.self_id)">删除
            </el-button>
          </template>
        </el-card>
      </li>

    </ul>
    <div style="text-align: center;width: 100%">
      <el-icon v-if="need_load" class="is-loading" color="#409eff" size="30px" style="text-align: center;width: 100%">
        <Loading/>
      </el-icon>
      <el-text v-else>没有更多了</el-text>
    </div>
  </div>
</template>


<style scoped>
.infinite-list {
  max-height: 1000px;
  flex-direction: column;
  overflow: scroll;
  width: 100%;
  align-items: center;
  justify-content: center;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}

.infinite-list-item {
  width: 90%;
  align-items: center;
  justify-content: center;
  padding: 5px;
  margin: 10px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}

.infinite-card {
  width: 100%;
}
</style>
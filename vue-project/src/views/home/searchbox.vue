<script lang="js" setup>
import {onMounted, ref} from "vue";
import {Search} from '@element-plus/icons-vue'
import {useStore} from "vuex";
import {get_search} from "@/views/home/home.js";

const store = useStore()
const select = ref('unsigned')
const input = ref('')

onMounted(() => {
  do_search().then()
})

async function do_search() {
  store.commit('set_search_content', input.value)
  store.commit('set_search_type', select.value)
  store.commit('clear_home_cards')
  const res = await get_search(select.value, input.value, 0, 10)
  store.commit('merge_home_cards', res.data['search_result'])
}
</script>

<template>
  <div>
    <el-input
        v-model="input"
        class="input-with-select"
        placeholder="患者姓名或手术名称"
        @change="do_search"
    >
      <template #prepend>
        <el-select v-model="select" placeholder="Select" style="width: 120px" @change="do_search">
          <el-option label="待签署" value="unsigned"/>
          <el-option label="已签署" value="signed"/>
          <el-option label="模板" value="template"/>
          <el-option label="全部" value="any"/>
        </el-select>
      </template>
      <template #append>
        <el-button :icon="Search" @click="do_search"/>
      </template>
    </el-input>
  </div>
</template>

<style scoped>

</style>
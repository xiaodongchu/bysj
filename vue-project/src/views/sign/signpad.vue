<script lang="js" setup>
import {onMounted, ref} from "vue";
import {ElMessage} from "element-plus";

const model = defineModel()
const signaturePad = ref(null);
const is_locked = ref(false)

onMounted(() => {
  model.value = ''
  signaturePad.value.openSignaturePad()
})

function undo() {
  signaturePad.value.undoSignature();
}

function save_sign() {
  signaturePad.value.lockSignaturePad()
  is_locked.value = true
  const {isEmpty, data} = signaturePad.value.saveSignature();
  if (isEmpty) {
    ElMessage.error('请签名')
    unlock_pad()
    return
  }
  model.value = data
  ElMessage.success('签名已暂存')
}

function unlock_pad() {
  signaturePad.value.openSignaturePad()
  is_locked.value = false
  model.value = ''
}
</script>

<template>
  <div style="width: 100%">
    <div class="box">
      <VueSignaturePad ref="signaturePad" height="180px" width="300px"></VueSignaturePad>
    </div>
    <el-row class="end-button">
      <el-col :span="8">
        <el-button v-if="!is_locked" type="info" @click="undo">撤销</el-button>
        <el-button v-else type="info" @click="unlock_pad">解锁</el-button>
      </el-col>
      <el-col :span="8">
        <el-button v-if="!is_locked" type="info" @click="save_sign">保存</el-button>
      </el-col>
      <el-col :span="8"></el-col>
    </el-row>
  </div>
</template>

<style scoped>
.box {
  width: 300px;
  height: 180px;
  border: 1px solid black;
  background-color: #FAFCFF;
}

.end-button {
  width: 320px;
  margin-top: 5px;
}
</style>
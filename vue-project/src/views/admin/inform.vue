<script lang="js" setup>
import {onMounted, reactive, ref} from "vue";
import {delete_inform, get_inform, post_inform} from "@/views/admin/admin.js";
import {ElMessage} from "element-plus";

const result = ref([])
const edit_inform_id = ref(-1)
const dialogFormVisible = ref(false)

const form = reactive({
  inform_id: -1,
  title: '',
  img_b64: '',
  url: "",
  create_info: '',
})

async function do_search() {
  let res = await get_inform()
  res = res.data['inform_list']
  result.value = res
  ElMessage.success('搜索成功')
}

async function click_edit(row) {
  edit_inform_id.value = row.inform_id
  form.inform_id = row.inform_id
  form.title = row.title
  form.img_b64 = row.img_b64
  form.url = row.url
  form.create_info = row.create_info
  dialogFormVisible.value = true
}

function click_new() {
  edit_inform_id.value = 0
  form.title = ''
  form.img_b64 = ''
  form.url = ""
  form.create_info = ''
  dialogFormVisible.value = true
}

function click_cancel() {
  dialogFormVisible.value = false
}

async function click_delete(row) {
  let res = await delete_inform(row.inform_id)
  await do_search()
}

async function click_confirm() {
  let res = await post_inform(edit_inform_id.value, form)
  dialogFormVisible.value = false
  ElMessage.success('更新成功')
  await do_search()
}

const fileList = ref([])

function changeFile(file, fileList) {
  const file_new = fileList[0].raw
  const reader = new FileReader();
  reader.onload = e => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const maxWidth = 960; // 设置最大宽度
      const maxHeight = 480; // 设置最大高度
      let width = img.width;
      let height = img.height;
      if (width > maxWidth) {
        height = height * (maxWidth / width);
        width = maxWidth;
      }
      if (height > maxHeight) {
        width = width * (maxHeight / height);
        height = maxHeight;
      }
      canvas.width = width;
      canvas.height = height;
      ctx.drawImage(img, 0, 0, width, height);
      const base64 = canvas.toDataURL('image/jpeg', 0.6);
      form.img_b64 = base64
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file_new);
  ElMessage.success('图片上传')
  return false; // 阻止自动上传
}

onMounted(async () => {
  await do_search()
})
</script>


<template>
  <div style="width: 100%">
    <div style="width: 100%;padding: 20px">
      <el-button type="primary" @click="click_new">新建通知</el-button>
    </div>
    <div style="width: 100%">
      <el-table
          :data="result"
          border
          max-height="700"
          stripe
          style="width: 100%"
      >
        <el-table-column fixed="left" label="标题" prop="title"/>
        <el-table-column label="链接" prop="url"/>
        <el-table-column label="图片" prop="img_b64">
          <template #default="{row}">
            <el-tag v-if="row.img_b64" type="success">已上传</el-tag>
            <el-tag v-else type="primary">未上传</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建说明" prop="create_info"/>
        <el-table-column fixed="right" label="操作" width="160">
          <template #default="{row}">
            <el-button type="warning" @click="click_edit(row)">操作</el-button>
            <el-button type="danger" @click="click_delete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div style="width: 100%">
      <el-dialog v-model="dialogFormVisible" class="el-dialog1" style="width: 100%" title="发布通知">
        <el-form :model="form" class="el-form1" label-width="auto">

          <el-form-item label="通知id">
            <el-input v-model="form.inform_id" disabled/>
          </el-form-item>

          <el-form-item label="标题">
            <el-input
                v-model="form.title"
                autosize
                type="textarea"
            />
          </el-form-item>

          <el-form-item label="图片预览">
            <el-image
                :src="`${form.img_b64}`"
                fit="cover"
                style="max-width: 50%; max-height: 180px"></el-image>
            <el-input v-model="form.img_b64" disabled/>
          </el-form-item>

          <el-form-item label="图片">
            <el-upload
                :auto-upload="false"
                :file-list="fileList"
                :limit="1"
                :on-change="changeFile"
                accept=".jpg, .png"
                action=""
                list-type="picture"
            >
              <el-button type="primary">上传图片</el-button>
            </el-upload>
          </el-form-item>

          <el-form-item label="链接">
            <el-input v-model="form.url"/>
          </el-form-item>

          <el-form-item label="备注">
            <el-input
                v-model="form.create_info"
                autosize
                type="textarea"
            />
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
  border: 1px solid #e0e0e0;
}
</style>
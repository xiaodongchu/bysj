<script lang="js" setup>
import {onMounted} from "vue";
import {get_inform} from "@/views/home/home.js";
import {useStore} from "vuex";

const store = useStore()

onMounted(async () => {
  const res = await get_inform();
  store.commit("set_inform", res.data['inform_list'])
});
</script>

<template>
  <div style="width: 100%">
    <el-carousel height="200px" indicator-position="outside" motion-blur>
      <el-carousel-item v-for="item in store.state.inform" :key="item.title">
        <!-- 整个链接作为点击区域 -->
        <a :href="item.url" class="item-link" target="_blank">
          <!-- 图片，使用object-fit: cover确保等比缩放 -->
          <img :alt="item.title" :src="`${item.img_b64}`" class="item-image">
          <!-- 标题 -->
          <el-text class="mx-1">{{ item.title }}</el-text>
        </a>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<style scoped>
.item-link {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  height: 100%;
  width: 100%;
}

.item-image {
  width: 100%;
  height: 185px; /* 宽度自适应 */
  object-fit: contain;
}

.mx-1 {
  margin-top: 3px; /* 标题与图片间隔 */
  font-size: 12px;
  color: gray;
}
</style>


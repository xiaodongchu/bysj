<script lang="js" setup>
import {onMounted, ref} from "vue";
import {useRoute, useRouter} from "vue-router";
import templ from "@/views/edit/templ.vue";
import unsigned from "@/views/edit/unsigned.vue";

const router = useRouter()
const route = useRoute()
const edit_id = ref('')
//template,unsigned
const edit_type = ref('')

onMounted(async () => {
  edit_id.value = route.params.id
  edit_type.value = route.params.type
})

// const form = reactive({
//   id: 0,
//   surgery_name: '',
//   hospital_name: "",
//   patient_name: '',//c
//   patient_sex: '女',//c
//   patient_birth: '',//c
//   hospital_id: '',//c
//   disease_name: '',
//   anesthesia_type: '',
//   surgery_intro: "",
//   risk_intro: "",
//   risk_list: [],
//   patient_choice: [],
//   doctor_state: "",
//   template_intro: "",//t
//   is_public: false,//t
//   update_data: [],//t
//   special_risk_list: [],//c
//   permission_list: [],//c
// })

</script>

<template>
  <div style="width: 100%">
    <templ v-if="edit_type === 'template'"></templ>
    <unsigned v-if="edit_type === 'unsigned'"></unsigned>
  </div>
</template>

<style scoped>

</style>
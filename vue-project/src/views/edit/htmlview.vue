<script lang="js" setup>
// 表单数据
const form = defineModel()

</script>

<template>
  <div class="a4-container">
    <table>
      <tbody>
      <tr id="table line1">
        <td colspan="4">
          <p id="hospital name" class="hospital_name">{{ form.hospital_name }}</p>
          <p id="surgery name title" class="surgery_name">{{ form.surgery_name }}知情同意书</p>
        </td>
      </tr>
      <tr id="table line2">
        <td>
          <p class="patient_info_title">姓名:</p>
          <p id="patient name" class="patient_info">{{ form.patient_name }}</p>
        </td>
        <td>
          <p class="patient_info_title">性别:</p>
          <p id="patient sex" class="patient_info">{{ form.patient_sex }}</p>
        </td>
        <td>
          <p class="patient_info_title">出生日期:</p>
          <p id="patient birth" class="patient_info">{{ form.patient_birth }}</p>
        </td>
        <td>
          <p class="patient_info_title">病历号:</p>
          <p id="patient id" class="patient_info">{{ form.hospital_id }}</p>
        </td>
      </tr>
      <tr id="table line3">
        <td class="normal_paragraph" colspan="4">
          <p class="title1">疾病介绍和治疗建议</p>
          <p>
            <span>医生已告知我患有</span>
            <span id="disease name" class="highlight_text">{{ form.disease_name }}</span>
            <span>。</span>
          </p>
          <p>
                            <span id="anesthesia">
                                <span>需要在</span>
                                <span id="anesthesia type" class="highlight_text">{{ form.anesthesia_type }}</span>
                                <span>下进行</span>
                            </span>
            <span id="surgery name1" class="highlight_text">{{ form.surgery_name }}</span>
            <span>治疗。</span>
          </p>
          <p id="surgery intro">{{ form.surgery_intro }}</p>
          <br>
        </td>
      </tr>
      <tr id="table line4">
        <td class="normal_paragraph" colspan="4">
          <p class="title1">手术潜在风险和对策</p>
          <p id="risk intro">{{ form.risk_intro }}</p>
          <ol id="risk list">
            <li v-for="item in form.risk_list">
              {{ item.text }}
              <ol v-if="item.children">
                <li v-for="item_child in item.children">{{ item_child.text }}</li>
              </ol>
            </li>
          </ol>
          <div v-if="form.special_risk_list">
            <p class="title1">特殊风险或主要高危因素</p>
            <p>我理解根据我个人的病情，我可能出现以下特殊并发症或风险：</p>
            <ol id="special risk list" class="highlight_text">
              <li v-for="item in form.special_risk_list">
                {{ item.text }}
                <ol v-if="item.children">
                  <li v-for="item_child in item.children">{{ item_child.text }}</li>
                </ol>
              </li>
            </ol>
            <p>一旦发生上述风险和意外，医生会采取积极应对措施。</p>
          </div>
        </td>
      </tr>
      <tr id="table line 5">
        <td colspan="4">
          <p class="title1">患者知情选择</p>
          <ol id="patient choice">
            <li v-for="item in form.patient_choice">{{ item.text }}</li>
          </ol>
        </td>
      </tr>
      <tr id="table line 6">
        <td colspan="2">
          <div v-if="form.other_sign">
            <p class="patient_info_title">患者家属签名</p>
            <p class="patient_info_title">{{ form.other_sign_info }}</p>
          </div>
          <div v-else>
            <p class="patient_info_title">患者签名</p>
          </div>
        </td>
        <td colspan="2">
          <p class="patient_info_title">签名时间</p>
        </td>
      </tr>
      <tr id="table line 7">
        <td colspan="2">
          <img id="patient sign" alt="患者或家属签名" src="">
        </td>
        <td colspan="2" style="vertical-align: middle">
          <p id="sign date" class="highlight_text" style="text-align: center"></p>
        </td>
      </tr>
      <tr id="table line 8">
        <td colspan="4">
          <p class="title1">医生陈述</p>
          <p id="doctor state">{{ form.doctor_state }}</p>
        </td>
      </tr>
      <tr id="table line 9">
        <td colspan="2">
          <p class="patient_info_title">医生签名</p>
        </td>
        <td colspan="2">
          <p class="patient_info_title">签名时间</p>
        </td>
      </tr>
      <tr id="table line 10">
        <td colspan="2">
          <img id="doctor sign" alt="医生签名" src="">
        </td>
        <td colspan="2" style="vertical-align: middle">
          <p id="doctor sign date" class="highlight_text" style="text-align: center"></p>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
@media print {
  @page {
    size: A4;/* A4纸宽度210，A4纸高度297 */
    margin: 20mm;  /*打印时的边距设置 top | right | bottom | left */
  }
}

body {
  font: 16px/1.5 "宋体", "SimSun", "Times New Roman", "Microsoft Yahei", "Hiragino Sans GB", "Heiti SC", "Droid Sans", sans-serif;
  line-height: 1;
  color: black; /* 默认字体颜色 */
  padding: 0; /*重置默认内边距 */
  margin: 0; /* 重置默认边距 */
  display: flex; /* 弹性布局 */
  justify-content: center; /* 水平居中 */
}

.a4-container {
  width: 170mm; /* A4纸宽度210，常规左右边距各20mm */
  min-height: 257mm; /* A4纸高度297，常规上下边距20mm */
  padding: 0; /* 内边距 */
  margin: 0; /* 外边距 */
  background: white; /* 背景色设置为白色 */
  page-break-after: always; /* 打印时自动分页 */
}

table {
  width: 100%;
  border-collapse: collapse; /* 合并边框 */
  table-layout: fixed; /* 固定表格布局 */
}

th, td {
  border: 1px solid black; /* 单元格边框 */
  padding: 8px; /* 单元格内边距 */
  text-align: left; /* 文本左对齐 */
  vertical-align: top; /* 文本顶部对齐 */
}

img {
  max-width: 60mm;
  height: auto;
  max-height: 30mm;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

li {
  text-indent: 0;
}

.hospital_name {
  font-family: "黑体", "SimHei", "Microsoft Yahei", "Hiragino Sans GB", "Heiti SC", "Droid Sans", sans-serif;
  font-size: 24px;
  line-height: 1;
  font-weight: bold;
  text-align: center;
}

.surgery_name {
  font-family: "黑体", "SimHei", "Microsoft Yahei", "Hiragino Sans GB", "Heiti SC", "Droid Sans", sans-serif;
  font-size: 22px;
  line-height: 1;
  font-weight: bold;
  text-align: center;
}

.title1 {
  font-family: "黑体", "SimHei", "Microsoft Yahei", "Hiragino Sans GB", "Heiti SC", "Droid Sans", sans-serif;
  font-size: 18px;
  font-weight: bold;
  text-align: left;
  text-indent: 0;
}

.patient_info {
  font-family: "楷体", "KaiTi", "Microsoft Yahei", "Hiragino Sans GB", "Heiti SC", "Droid Sans", sans-serif;
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  line-height: 0.5;
}

.patient_info_title {
  font-family: "黑体", "SimHei", "Microsoft Yahei", "Hiragino Sans GB", "Heiti SC", "Droid Sans", sans-serif;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  text-indent: 0;
  line-height: 0.5;
}

.highlight_text {
  font-size: 16px;
  font-weight: bold;
  text-align: left;
  text-decoration-line: underline;
}

.normal_paragraph {
  text-indent: 2em;
}
</style>
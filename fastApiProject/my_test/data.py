import base64
import os

path_now = str(os.path.dirname(os.path.abspath(__file__)))
if path_now[-1] != '/':
    path_now += '/'
with open(path_now + r"sign.png", "rb") as f:
    img_b64 = "data:image/png;base64," + str(base64.b64encode(f.read()), encoding="utf-8")

data = {
    "hospital_name": "医院A",
    "surgery_name": "腹腔镜手术",
    "patient_name": "张三",
    "patient_sex": "男",
    "patient_birth": "2000年10月10日",
    "hospital_id": "1234567890",
    "disease_name": "胆囊结石",
    "anesthesia_type": "全麻",
    "surgery_intro": "随着内镜技术的发展和在外科领域的广泛应用，“微创外科”的理念逐步深入人心。“微创外科”是指在尽可能准确去除病变的同时，使手术引起机体局部创伤和全身反应尽量降低到最小程度的外科理念和技术体系。内镜技术是微创外科手术的基石，而腹腔镜手术则是最常用的内镜手术之一。目前，可以应用腹腔镜进行的手术包括胆囊切除、脾切除、阑尾切除、肠切除等。与传统的开腹手术相比，腹腔镜手术具有手术创伤小、术后恢复快等优势。但腹腔镜手术也有其局限性和相应的风险，另外腹腔镜手术术中也可能由于情况复杂、解剖变异或发生并发症等情况而中转开腹。",
    "risk_intro": "医生告知我手术可能发生的一些风险，有些不常见的风险可能没有在此列出，具体的手术式根据不同病人的情况有所不同，医生告诉我可与我的医生讨论有关我手术的具体内容，如果我有特殊的问题可与我的医生讨论。",
    "risk_list": [
        {"text": "我理解任何手术麻醉都存在风险。"},
        {"text": "我理解任何所用药物都可能产生副作用，包括轻度的恶心、皮疹等症状到严重的过敏性休克，甚至危及生命。"},
        {"text": "我理解此手术可能发生的风险：",
         "children": [
             {"text": "因病情复杂、有其它病变或并发症的发生时，手术需改为剖腹方式进行；"},
             {"text": "二氧化碳气腹造成的并发症：气体栓塞、皮下气肿、术后右侧肩背部疼痛等；"},
             {"text": "其它目前无法预计的风险和并发症。"}
         ]
         },
        {
            "text": "我理解如果我患有高血压、心脏病、糖尿病、肝肾功能不全、静脉血栓等疾病或者有吸烟史，以上这些风险可能会加大，或者在术中或术后出现相关的病情加重或心脑血管意外，甚至死亡。"},
        {"text": "我理解术后如果不遵医嘱，可能影响手术效果。"}
    ],
    "special_risk_list": [
        {"text": "我知晓我患有高血压，术前和术后需遵医嘱按时服用降压药，否则在术中或术后可能发生无法预估的意外。"},
        {"text": "测试文本"}
    ],
    "patient_choice": [
        {
            "text": "我的医生已经告知我将要进行的手术方式、此次手术及术后可能发生的并发症和风险、可能存在的其它治疗方法并且解答了我关于此次手术的相关问题。"},
        {"text": "我同意在手术中医生可以根据我的病情对预定的手术方式做出调整。"},
        {"text": "我理解我的手术需要多位医生共同进行。"},
        {"text": "我并未得到手术百分之百成功的许诺。"},
        {"text": "我授权医师对手术切除的病变器官、组织或标本进行处置，包括病理学检查、细胞学检查和医疗废物处理等。"},
    ],
    "is_signed": True,
    "other_sign": False,
    "other_sign_info": "",
    "patient_sign": img_b64,
    "patient_sign_date": "2000年10月10日",
    "doctor_state": "我已经告知患者将要进行的手术方式、此次手术及术后可能发生的并发症和风险、可能存在的其它治疗方法并且解答了患者关于此次手术的相关问题。",
    "doctor_sign": img_b64,
    "doctor_sign_date": "2000年10月10日",
}

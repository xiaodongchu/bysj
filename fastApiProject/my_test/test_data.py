from database.models import session, UserInfo, Inform, ConsentForm, ConsentTemplate, str_to_datatime, Base, engine
from my_test.data import data
from file_manager import path_now
from user import authing_server
import base64
import json


def init_user():
    user_list = authing_server.get_all_user_id()
    class_list = ['管理员', '医生', '护士']
    department_list = ['骨科', '内科', '外科']
    j = 0
    user_verify = True
    for i in range(len(user_list)):
        user_i = user_list[i]
        user_name = "张" + str(i)
        uid = user_i['userId']
        if j == 3:
            j = 0
        user_class = class_list[j]
        department = department_list[j]
        user = UserInfo(id=uid, name=user_name, user_class=user_class, user_verify=user_verify, department=department)
        if 'phone' in user_i and user_i['phone']:
            user.phone = user_i['phone']
        if 'email' in user_i and user_i['email']:
            user.email = user_i['email']
        j += 1
        if not session.query(UserInfo).filter(UserInfo.id == uid).first():
            session.add(user)
    session.commit()


def init_template(l=10):
    users = session.query(UserInfo).all()
    for i in range(l):
        session.add(ConsentTemplate(
            hospital_name=data["hospital_name"],
            surgery_name=data["surgery_name"],
            disease_name=data["disease_name"],
            anesthesia_type=data["anesthesia_type"],
            surgery_intro=data["surgery_intro"],
            risk_intro=data["risk_intro"],
            risk_list=json.dumps(data["risk_list"]),
            patient_choice=json.dumps(data["patient_choice"]),
            doctor_state=data["doctor_state"],
            create_user_id=users[0].id,
            is_public=True,
            create_user_name="创建者张三",
            last_update_user_name="最后更新者张三",
        ))
    session.commit()


def init_consent_form(l=10):
    users = session.query(UserInfo).all()
    for i in range(l):
        session.add(ConsentForm(
            hospital_name=data["hospital_name"],
            surgery_name=data["surgery_name"],
            patient_name=data["patient_name"],
            patient_sex=data["patient_sex"],
            patient_birth=str_to_datatime(data["patient_birth"], time=False, chinese=True),
            hospital_id=data["hospital_id"],
            disease_name=data["disease_name"],
            anesthesia_type=data["anesthesia_type"],
            surgery_intro=data["surgery_intro"],
            risk_intro=data["risk_intro"],
            risk_list=json.dumps(data["risk_list"], ensure_ascii=False),
            special_risk_list=json.dumps(data["special_risk_list"], ensure_ascii=False),
            patient_choice=json.dumps(data["patient_choice"], ensure_ascii=False),
            is_signed=data["is_signed"],
            other_sign=data["other_sign"],
            other_sign_info=data["other_sign_info"],
            patient_sign=data["patient_sign"],
            patient_sign_date=str_to_datatime(data["patient_sign_date"], time=False, chinese=True),
            doctor_state=data["doctor_state"],
            doctor_sign=data["doctor_sign"],
            doctor_sign_date=str_to_datatime(data["doctor_sign_date"], time=False, chinese=True),
            doctor_sign_id=users[0].id,
            raw_html="",
            pdf_link="",
            permission_list=users,
            create_user_name="创建者张四",
            last_update_user_name="最后更新者张四",
        ))
    for i in range(l):
        session.add(ConsentForm(
            hospital_name=data["hospital_name"],
            surgery_name=data["surgery_name"],
            patient_name=data["patient_name"],
            patient_sex=data["patient_sex"],
            patient_birth=str_to_datatime(data["patient_birth"], time=False, chinese=True),
            hospital_id=data["hospital_id"],
            disease_name=data["disease_name"],
            anesthesia_type=data["anesthesia_type"],
            surgery_intro=data["surgery_intro"],
            risk_intro=data["risk_intro"],
            risk_list=json.dumps(data["risk_list"], ensure_ascii=False),
            special_risk_list=json.dumps(data["special_risk_list"], ensure_ascii=False),
            patient_choice=json.dumps(data["patient_choice"], ensure_ascii=False),
            doctor_state=data["doctor_state"],
            permission_list=users,
            create_user_name="创建者张四",
            last_update_user_name="最后更新者张四",
        ))
    session.commit()


def init_inform(l=10):
    with open(path_now + "my_test/inform.jpeg", "rb") as f:
        img_b64 = "data:image/jpeg;base64," + str(base64.b64encode(f.read()), encoding="utf-8")
    temp = {
        "title": "晚安重大",
        "url": "https://www.bilibili.com/opus/911371577545719862?spm_id_from=333.1365.0.0",
        "img_b64": img_b64,
        "create_info": "2021-05-01"
    }
    for i in range(l):
        session.add(Inform(title=temp["title"], img_b64=temp["img_b64"], url=temp["url"], create_info=str(i)))
    session.commit()


# relation 需要用类，单纯外键用id
if __name__ == "__main__":
    # 删除表
    Base.metadata.drop_all(engine)
    # 创建表
    Base.metadata.create_all(engine)
    init_user()
    init_inform()
    init_consent_form()
    init_template()
    form = session.query(ConsentForm).first()
    d = form.to_search_dict()
    print(d)

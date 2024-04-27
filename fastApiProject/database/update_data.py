from typing import Literal

from fastapi import HTTPException
from pydantic import BaseModel

from database.get_data import verify_and_get_user
from database.models import *


class UpdateUser(BaseModel):
    user_name: str = ""
    user_class: Literal["管理员", "医生", "护士", ""] = ""
    department: str = ""
    hospital_id: str = ""


async def update_user_info(Authorization: str, update_data: UpdateUser):
    user = verify_and_get_user(Authorization)
    if user:
        if update_data.user_class and update_data.user_class != user.user_class:
            user.user_class = update_data.user_class
            user.verify_info = ""
            user.user_verify = False
        if update_data.user_name:
            user.name = update_data.user_name
        if update_data.department:
            user.department = update_data.department
        if update_data.hospital_id:
            user.hospital_id = update_data.hospital_id
        session.commit()
        return user.id
    raise HTTPException(status_code=404, detail="User not found")


async def admin_hide_user(authing_id: str, hide: bool = True):
    user = session.query(UserInfo).filter(UserInfo.id == authing_id).first()
    if user:
        user.hide_in_admin = hide
        if hide:
            user.user_verify = False
            user.verify_info = ""
        session.commit()
        return authing_id
    raise HTTPException(status_code=404, detail="User not found")


class UpdateConsentForm(BaseModel):
    hospital_name: str = "",
    surgery_name: str = "",
    patient_name: str = "",
    patient_sex: str = "",
    patient_birth: datetime.date = None,
    hospital_id: str = "",
    disease_name: str = "",
    anesthesia_type: str = "",
    surgery_intro: str = "",
    risk_intro: str = "",
    risk_list: List[TextNode] = None,
    special_risk_list: List[TextNode] = None,
    patient_choice: List[TextNode] = None,
    doctor_state: str = "",
    permission_list: List[str] = None
    update_data: List[TextNode] = None


async def update_consent_form(consent_form_id: int, user: UserInfo, update_data: UpdateConsentForm):
    consent_form = session.query(ConsentForm).filter(ConsentForm.id == consent_form_id,
                                                     ConsentForm.status == True).first()
    if not consent_form:
        raise HTTPException(status_code=404, detail="Consent Form not found")
    if not consent_form.check_permission(user.id):
        raise HTTPException(status_code=403, detail="Permission denied")
    if update_data.hospital_name and update_data.hospital_name != consent_form.hospital_name:
        consent_form.hospital_name = update_data.hospital_name
    if update_data.surgery_name and update_data.surgery_name != consent_form.surgery_name:
        consent_form.surgery_name = update_data.surgery_name
    if update_data.patient_name and update_data.patient_name != consent_form.patient_name:
        consent_form.patient_name = update_data.patient_name
    if update_data.patient_sex and update_data.patient_sex != consent_form.patient_sex:
        consent_form.patient_sex = update_data.patient_sex
    if update_data.patient_birth and update_data.patient_birth != consent_form.patient_birth:
        consent_form.patient_birth = update_data.patient_birth
    if update_data.hospital_id and update_data.hospital_id != consent_form.hospital_id:
        consent_form.hospital_id = update_data.hospital_id
    if update_data.disease_name and update_data.disease_name != consent_form.disease_name:
        consent_form.disease_name = update_data.disease_name
    if update_data.anesthesia_type and update_data.anesthesia_type != consent_form.anesthesia_type:
        consent_form.anesthesia_type = update_data.anesthesia_type
    if update_data.surgery_intro and update_data.surgery_intro != consent_form.surgery_intro:
        consent_form.surgery_intro = update_data.surgery_intro
    if update_data.risk_intro and update_data.risk_intro != consent_form.risk_intro:
        consent_form.risk_intro = update_data.risk_intro
    if update_data.risk_list:
        consent_form.risk_list = dump_json(update_data.risk_list)
    if update_data.special_risk_list:
        consent_form.special_risk_list = dump_json(update_data.special_risk_list)
    if update_data.patient_choice:
        consent_form.patient_choice = dump_json(update_data.patient_choice)
    if update_data.doctor_state and update_data.doctor_state != consent_form.doctor_state:
        consent_form.doctor_state = update_data.doctor_state
    for user_id in update_data.permission_list:
        if consent_form.check_permission(user_id):
            continue
        user = session.query(UserInfo).filter(UserInfo.id == user_id).first()
        if user:
            consent_form.permission_list.append(user)
    consent_form.last_update_user_name = user.name
    update_data.update_data.append(TextNode(text="更新"))
    consent_form.update_data = add_update_data(consent_form.update_data, update_data.update_data, user)
    session.commit()
    return consent_form_id


class UpdateConsentTemplate(BaseModel):
    hospital_name: str = ""
    surgery_name: str = ""
    disease_name: str = ""
    anesthesia_type: str = ""
    surgery_intro: str = ""
    risk_intro: str = ""
    risk_list: list[TextNode] = None
    patient_choice: list[TextNode] = None
    doctor_state: str = ""
    template_intro: str = ""
    is_public: bool = True
    update_data: list[TextNode] = None


async def update_consent_template(consent_template_id: int, user: UserInfo, update_data: UpdateConsentTemplate):
    consent_template = session.query(ConsentTemplate).filter(ConsentTemplate.id == consent_template_id,
                                                             ConsentTemplate.status == True).first()
    if not consent_template:
        raise HTTPException(status_code=404, detail="Consent Template not found")
    if user.id != consent_template.create_user_id and consent_template.is_public == False:
        raise HTTPException(status_code=403, detail="Permission denied")
    if update_data.hospital_name and update_data.hospital_name != consent_template.hospital_name:
        consent_template.hospital_name = update_data.hospital_name
    if update_data.surgery_name and update_data.surgery_name != consent_template.surgery_name:
        consent_template.surgery_name = update_data.surgery_name
    if update_data.disease_name and update_data.disease_name != consent_template.disease_name:
        consent_template.disease_name = update_data.disease_name
    if update_data.anesthesia_type and update_data.anesthesia_type != consent_template.anesthesia_type:
        consent_template.anesthesia_type = update_data.anesthesia_type
    if update_data.surgery_intro and update_data.surgery_intro != consent_template.surgery_intro:
        consent_template.surgery_intro = update_data.surgery_intro
    if update_data.risk_intro and update_data.risk_intro != consent_template.risk_intro:
        consent_template.risk_intro = update_data.risk_intro
    if update_data.risk_list:
        consent_template.risk_list = dump_json(update_data.risk_list)
    if update_data.patient_choice:
        consent_template.patient_choice = dump_json(update_data.patient_choice)
    if update_data.doctor_state and update_data.doctor_state != consent_template.doctor_state:
        consent_template.doctor_state = update_data.doctor_state
    if update_data.template_intro and update_data.template_intro != consent_template.template_intro:
        consent_template.template_intro = update_data.template_intro
    if update_data.is_public and update_data.is_public != consent_template.is_public:
        consent_template.is_public = update_data.is_public
    consent_template.last_update_user_name = user.name
    update_data.update_data.append(TextNode(text="更新"))
    consent_template.update_data = add_update_data(consent_template.update_data, update_data.update_data, user)
    session.commit()
    return consent_template_id


class SignConsentForm(BaseModel):
    other_sign: bool = False
    other_sign_info: str = ""
    patient_sign: str = ""
    doctor_sign: str = ""

    def to_bool(self):
        if not self.other_sign:
            self.other_sign_info = ""
        elif not self.other_sign_info:
            return False
        return (self.patient_sign and self.doctor_sign
                and self.patient_sign.startswith("data:image/png;base64,")
                and self.doctor_sign.startswith("data:image/png;base64,"))


async def sign_consent_form(consent_form_id: int, user: UserInfo, sign_data: SignConsentForm):
    if sign_data.other_sign and not sign_data.other_sign_info:
        raise HTTPException(status_code=400, detail="Other sign need info")
    if not sign_data.to_bool():
        raise HTTPException(status_code=400, detail="Patient sign and doctor sign are needed")
    consent_form = session.query(ConsentForm).filter(
        ConsentForm.id == consent_form_id,
        ConsentForm.status == True,
        ConsentForm.is_signed == False
    ).first()
    if not consent_form:
        raise HTTPException(status_code=404, detail="Consent Form not found")
    if not consent_form.check_permission(user.id):
        raise HTTPException(status_code=403, detail="Permission denied")
    consent_form.is_signed = True
    consent_form.other_sign = sign_data.other_sign
    if sign_data.other_sign:
        consent_form.other_sign_info = sign_data.other_sign_info
    consent_form.patient_sign = sign_data.patient_sign
    consent_form.doctor_sign = sign_data.doctor_sign
    consent_form.patient_sign_date = datetime.datetime.now()
    consent_form.doctor_sign_date = datetime.datetime.now()
    consent_form.doctor_sign_id = user.id
    consent_form.last_update_user_name = user.name
    consent_form.update_data = add_update_data(consent_form.update_data, [TextNode(text="签名")], user)
    consent_form.pdf_link = ""
    consent_form.raw_html = ""
    session.commit()
    return consent_form_id


async def unsign_consent_form(
        consent_form_id: int,
        user: UserInfo,
):
    consent_form = session.query(ConsentForm).filter(
        ConsentForm.id == consent_form_id,
        ConsentForm.status == True,
        ConsentForm.is_signed == True,
        ConsentForm.doctor_sign_id == user.id
    ).first()
    if not consent_form:
        raise HTTPException(status_code=404, detail="Consent Form not found")
    consent_form.is_signed = False
    consent_form.last_update_user_name = user.name
    update_data = json_load(consent_form.update_data)
    update_data.append({"text": get_time_now_str(True, True) + "----" + str(user.id) + "取消签名"})
    consent_form.update_data = dump_json(update_data)
    session.commit()
    return consent_form_id


class AdminUpdateUser(BaseModel):
    user_verify: bool = False
    user_name: str = ""
    user_class: Literal["管理员", "医生", "护士", ""] = ""
    verify_info: str = ""
    department: str = ""
    hospital_id: str = ""


async def admin_update_user(authing_id: str, update_data: AdminUpdateUser):
    user = session.query(UserInfo).filter(UserInfo.id == authing_id).first()
    if user:
        user.user_verify = update_data.user_verify
        if update_data.user_verify:
            user.verify_info = update_data.verify_info
        if update_data.user_name:
            user.name = update_data.user_name
        if update_data.user_class:
            user.user_class = update_data.user_class
        if update_data.department:
            user.department = update_data.department
        session.commit()
        return authing_id
    raise HTTPException(status_code=404, detail="User not found")


class UpdateInform(BaseModel):
    title: str = ""
    img_b64: str = ""
    url: str = ""
    create_info: str = ""


async def admin_update_inform(inform_id: int, inform_data: UpdateInform):
    if not inform_data.img_b64.startswith("data:image/jpeg;base64,"):
        inform_data.img_b64 = ""
    if inform_id > 0:
        inform = session.query(Inform).filter(Inform.id == inform_id).first()
        if not inform:
            raise HTTPException(status_code=404, detail="Inform not found")
        if inform_data.title and inform_data.title != inform.title:
            inform.title = inform_data.title
        if inform_data.img_b64 and inform_data.img_b64 != inform.img_b64:
            inform.img_b64 = inform_data.img_b64
        if inform_data.url and inform_data.url != inform.url:
            inform.url = inform_data.url
        if inform_data.create_info and inform_data.create_info != inform.create_info:
            inform.create_info = inform_data.create_info
    else:
        inform = Inform(title=inform_data.title, img_b64=inform_data.img_b64, url=inform_data.url,
                        create_info=inform_data.create_info)
        session.add(inform)
        session.flush()
        session.refresh(inform)
        inform_id = inform.id
    session.commit()
    return inform_id

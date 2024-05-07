from typing import Literal

from fastapi import HTTPException
from pydantic import BaseModel

from database.models import *


async def add_user(authing_id: str):
    user = UserInfo(id=authing_id, user_verify=False)
    session.add(user)
    session.commit()


class AddConsentForm(BaseModel):
    surgery_name: str
    patient_name: str
    patient_sex: Literal["男", "女"] = "女"
    patient_birth: datetime.date = datetime.date.today()
    hospital_id: str = ""
    base_type: str = ""
    base_id: str = ""
    permission_list: list[str] = []


async def add_consent_form(user: UserInfo, add_data: AddConsentForm):
    if user.id not in add_data.permission_list:
        add_data.permission_list.append(user.id)
    constent = ConsentForm(
        surgery_name=add_data.surgery_name,
        patient_name=add_data.patient_name,
        patient_sex=add_data.patient_sex,
        patient_birth=add_data.patient_birth,
        hospital_id=add_data.hospital_id,
        create_user_name=user.name,
    )
    if add_data.base_type and add_data.base_id:
        template = to_template(add_data.base_type, add_data.base_id)
        constent.hospital_name = template.hospital_name
        constent.disease_name = template.disease_name
        constent.anesthesia_type = template.anesthesia_type
        constent.surgery_intro = template.surgery_intro
        constent.risk_intro = template.risk_intro
        constent.risk_list = template.risk_list
        constent.patient_choice = template.patient_choice
        constent.doctor_state = template.doctor_state
    update_data = dump_json(
        [{"text": str(user.name + user.id + "创建 /" + add_data.base_type + str(add_data.base_id))}])
    constent.update_data = update_data
    for i in add_data.permission_list:
        constent.permission_list.append(session.query(UserInfo).filter(UserInfo.id == i).first())
    session.add(constent)
    session.flush()
    session.refresh(constent)
    new_id = constent.id
    session.commit()
    return new_id


def to_template(base_type: str, base_id: int | str):
    base = None
    if base_type == "signed" or base_type == "unsigned":
        base = session.query(ConsentForm).filter(ConsentForm.id == base_id).first()
    elif base_type == "template":
        base = session.query(ConsentTemplate).filter(ConsentTemplate.id == base_id).first()
    if not base:
        raise HTTPException(status_code=400, detail="base_type error")
    tempalte = ConsentTemplate(
        hospital_name=base.hospital_name,
        surgery_name=base.surgery_name,
        disease_name=base.disease_name,
        anesthesia_type=base.anesthesia_type,
        surgery_intro=base.surgery_intro,
        risk_intro=base.risk_intro,
        risk_list=base.risk_list,
        patient_choice=base.patient_choice,
        doctor_state=base.doctor_state
    )
    return tempalte


class AddConsentTemplate(BaseModel):
    surgery_name: str
    template_intro: str = ""
    is_public: bool = True
    base_type: str = ""
    base_id: str = ""


async def add_consent_template(user: UserInfo, add_data: AddConsentTemplate):
    template = ConsentTemplate(surgery_name=add_data.surgery_name,
                               template_intro=add_data.template_intro,
                               is_public=add_data.is_public,
                               create_user_id=user.id,
                               create_user_name=user.name)
    if add_data.base_type and add_data.base_id:
        template0 = to_template(add_data.base_type, add_data.base_id)
        template.hospital_name = template0.hospital_name
        template.disease_name = template0.disease_name
        template.anesthesia_type = template0.anesthesia_type
        template.surgery_intro = template0.surgery_intro
        template.risk_intro = template0.risk_intro
        template.risk_list = template0.risk_list
        template.patient_choice = template0.patient_choice
        template.doctor_state = template0.doctor_state
    template.update_data = dump_json(
        [{"text": str(user.name + user.id + "创建 /" + add_data.base_type + str(add_data.base_id))}])
    session.add(template)
    session.flush()
    session.refresh(template)
    new_id = template.id
    session.commit()
    return new_id

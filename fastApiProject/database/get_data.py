import os
from copy import deepcopy

from fastapi import HTTPException
from sqlalchemy import desc, and_, or_
from pydantic import BaseModel
from typing import Literal

from weasyprint import HTML

from database.models import *
from file_manager import template, save_temp_pdf
from user import authing_server


def verify_id_token(Authorization: str, user_class=None, need_verify: bool = False):
    if user_class is None:
        user_class = []
    authing_id = authing_server.verify_id_token_hs256_redis(Authorization)
    if authing_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    if len(user_class) > 0 or need_verify:
        user = session.query(UserInfo).filter(UserInfo.id == authing_id).first()
        if len(user_class) > 0 and user.user_class not in user_class:
            raise HTTPException(status_code=403, detail="unauthorized user class")
        if need_verify and not user.user_verify:
            raise HTTPException(status_code=412, detail="unauthorized user class")
    return authing_id


def verify_and_get_user(Authorization: str, user_class=None, need_verify: bool = False):
    if user_class is None:
        user_class = []
    authing_id = authing_server.verify_id_token_hs256_redis(Authorization)
    if authing_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = session.query(UserInfo).filter(UserInfo.id == authing_id).first()
    if len(user_class) > 0 and user.user_class not in user_class:
        raise HTTPException(status_code=403, detail="unauthorized user class")
    if need_verify and not user.user_verify:
        raise HTTPException(status_code=412, detail="unauthorized user class")
    return user


async def get_basic_user_info(Authorization: str):
    user_info = authing_server.verify_id_token_hs256(Authorization)
    authing_id = user_info['authing_id']
    user = session.query(UserInfo).filter(UserInfo.id == authing_id).first()
    if user:
        return {
            "user_verify": user.user_verify,
            "user_class": user.user_class,
            "user_name": user.name,
            "authing_id": authing_id,
        }
    else:
        phone = ""
        email = ""
        if user_info['phone']:
            phone = user_info['phone']
        if user_info['email']:
            email = user_info['email']
        user = UserInfo(id=authing_id, user_verify=False, phone=phone, email=email)
        session.add(user)
        session.commit()
        return {
            "user_verify": False,
            "user_class": "",
            "user_name": "",
            "authing_id": authing_id,
        }


async def get_user_info(Authorization: str):
    user = verify_and_get_user(Authorization)
    if user:
        return user.to_detail_dict()
    raise HTTPException(status_code=404, detail="User not found")


async def get_inform_list(info_len: int = 3, limit=True):
    if limit and info_len > 0:
        inform_list = (session.query(Inform).order_by(desc(Inform.create_time))
                       .limit(info_len).all())
    else:
        inform_list = session.query(Inform).order_by(desc(Inform.create_time)).all()
    return [
        {
            "title": inform.title,
            "img_b64": inform.img_b64,
            "url": inform.url,
            "create_info": inform.create_info
        }
        for inform in inform_list]


async def admin_search_user(search_content: str = '', not_verify: bool = False, show_hide=False):
    user_list = session.query(UserInfo)
    if not_verify:
        user_list = user_list.filter(UserInfo.user_verify == False)
    if not show_hide:
        user_list = user_list.filter(or_(UserInfo.hide_in_admin == False, UserInfo.user_verify == True))
    if search_content:
        user_list = user_list.filter(UserInfo.name.like(f"%{search_content}%"))
    user_list = user_list.all()
    return [
        {
            "authing_id": user.id,
            "user_name": user.name,
            "user_verify": user.user_verify,
            "user_class": user.user_class,
            "hospital_id": user.hospital_id,
            "hide_in_admin": user.hide_in_admin,
        }
        for user in user_list]


async def admin_get_user_detail(authing_id: str):
    user = session.query(UserInfo).filter(UserInfo.id == authing_id).first()
    if user:
        return user.to_detail_dict()
    return HTTPException(status_code=404, detail="User not found")


async def user_search_user(search_content: str = ''):
    if not search_content:
        raise HTTPException(status_code=400, detail="Invalid search content")
    user_list = session.query(UserInfo).filter(UserInfo.name.like(f"%{search_content}%")).filter(
        UserInfo.user_verify == True).all()
    return [
        {
            "authing_id": user.id,
            "user_class": user.user_class,
            "user_name": user.name,
            "hospital_id": user.hospital_id,
        }
        for user in user_list]


class SearchConsent(BaseModel):
    search_type: Literal["signed", "unsigned", "template", "any"] = "unsigned"
    search_content: str = ''
    end_id: int = 0
    page_len: int = 10


async def search_consent(user: UserInfo, search: SearchConsent):
    search.page_len = 10 if search.page_len > 10 else search.page_len
    result = None
    search_content_form = or_(
        and_(True, *[ConsentForm.surgery_name.like("%" + i + '%') for i in search.search_content]),
        and_(True, *[ConsentForm.patient_name.like("%" + i + '%') for i in search.search_content])
    )
    search_content_template = and_(True,
                                   *[ConsentTemplate.surgery_name.like("%" + i + '%') for i in search.search_content])
    if search.search_type == "unsigned":
        result = await search_unsigned(search_content_form, user, search.end_id, search.page_len)
    elif search.search_type == "signed":
        result = await search_signed(search_content_form, user, search.end_id, search.page_len)
    elif search.search_type == "template":
        result = await search_template(search_content_template, user, search.end_id, search.page_len)
    elif search.search_type == "any":
        re1 = await search_unsigned(search_content_form, user, search.end_id, search.page_len)
        re2 = await search_signed(search_content_form, user, search.end_id, search.page_len)
        re3 = await search_template(search_content_template, user, search.end_id, search.page_len)
        re = re1 + re2 + re3
        result = re
    end_id = search.end_id + search.page_len
    return {"search_result": result, "end_id": int(end_id)}


async def search_template(search_content_template, user, end_id, page_len):
    res = (session.query(ConsentTemplate)
           .filter(
        ConsentTemplate.status == True,
        search_content_template,
        or_(ConsentTemplate.create_user_id == user.id, ConsentTemplate.is_public == True)
    )
           .order_by(desc(ConsentTemplate.last_update_time))
           .offset(end_id).limit(page_len).all())
    re = [i.to_search_dict() for i in res]
    for i in re:
        i['have_permission'] = False
        if i['create_user_id'] == user.id:
            i['have_permission'] = True
        i['can_sign'] = False
    return re


async def search_signed(search_content_form, user, end_id, page_len):
    res = (session.query(ConsentForm)
           .filter(
        ConsentForm.status == True,
        search_content_form,
        ConsentForm.is_signed == True
    )
           .order_by(desc(ConsentForm.last_update_time))
           .offset(end_id).limit(page_len).all())
    re = [i.to_search_dict() for i in res]
    for i in re:
        i['have_permission'] = False
        if user.id in i['permission_list']:
            i['have_permission'] = True
        i['can_sign'] = False
    return re


async def search_unsigned(search_content_form, user, end_id, page_len):
    res = (session.query(ConsentForm)
           .filter(
        ConsentForm.status == True,
        search_content_form,
        ConsentForm.permission_list.contains(user),
        ConsentForm.is_signed == False
    )
           .order_by(desc(ConsentForm.last_update_time))
           .offset(end_id).limit(page_len).all())
    re = [i.to_search_dict() for i in res]
    for i in re:
        i['have_permission'] = True
        i['can_sign'] = False
    if user.user_class == '医生':
        for i in re:
            i['can_sign'] = True
    return re


async def get_consent_form(consent_id: int, user: UserInfo):
    consent = session.query(ConsentForm).filter(ConsentForm.id == consent_id, ConsentForm.status == True).first()
    if not consent:
        raise HTTPException(status_code=404, detail="Consent not found")
    data = consent.to_ditail_dict()
    if user.id not in data['permission_list']:
        raise HTTPException(status_code=403, detail="Permission denied")
    return data


async def get_consent_template(consent_id: int, user: UserInfo):
    consent = session.query(ConsentTemplate).filter(ConsentTemplate.id == consent_id,
                                                    ConsentTemplate.status == True).first()
    if not consent:
        raise HTTPException(status_code=404, detail="Consent not found")
    if user.id != consent.create_user_id and not consent.is_public:
        raise HTTPException(status_code=403, detail="Permission denied")
    data = consent.to_ditail_dict()
    return data


statistics = {}


async def get_statistics(user: UserInfo):
    await update_statistics()
    count_user = deepcopy(statistics)
    if user.user_class == "管理员":
        return count_user
    count_user["consent_me"] = {
        "已签署": 0,
        "未签署": 0,
        "模板": 0,
    }
    consent_count = session.query(ConsentForm).filter(
        ConsentForm.status == True,
    ).all()
    for i in consent_count:
        if i.check_permission(user.id):
            if i.is_signed:
                count_user["consent_me"]["已签署"] += 1
            else:
                count_user["consent_me"]["未签署"] += 1
    template_count = session.query(ConsentTemplate).filter(
        ConsentTemplate.status == True,
        ConsentTemplate.create_user_id == user.id,
    ).count()
    count_user["consent_me"]["模板"] = template_count
    count_user["user_count"] = False
    count_user["user_verify"] = False
    count_user["user_department"] = False
    return count_user


async def update_statistics():
    global statistics
    statistics = {
        "user_count": {
            "护士": 0,
            "医生": 0,
            "管理员": 0,
        },
        "user_verify": {
            "未审核": 0,
            "已审核": 0,
        },
        "user_log_by": {
            "手机": 0,
            "未绑定手机": 0,
            "邮箱": 0,
            "未绑定邮箱": 0,
        },
        "user_department": {},
        "consent_count": {
            "已签署": 0,
            "未签署": 0,
            "模板": 0,
        },
        "consent_me": False,
        "consent_sign_date": {},
    }
    user_count = session.query(UserInfo).filter(
        UserInfo.hide_in_admin == False,
    ).all()
    for i in user_count:
        if i.user_verify:
            statistics["user_count"][i.user_class] += 1
            statistics["user_verify"]["已审核"] += 1
            if i.phone:
                statistics["user_log_by"]["手机"] += 1
            if i.email:
                statistics["user_log_by"]["邮箱"] += 1
            if i.department:
                if i.department in statistics["user_department"]:
                    statistics["user_department"][i.department] += 1
                else:
                    statistics["user_department"][i.department] = 1
        else:
            statistics["user_verify"]["未审核"] += 1
    statistics["user_log_by"]["未绑定手机"] = len(user_count) - statistics["user_log_by"]["手机"]
    statistics["user_log_by"]["未绑定邮箱"] = len(user_count) - statistics["user_log_by"]["邮箱"]
    today = datetime.date.today()
    for i in range(30):
        date_key = today - datetime.timedelta(days=i)
        date_key = datatime_to_str(date_key, time=False, chinese=True)
        statistics["consent_sign_date"][date_key] = 0
    consent_count = session.query(ConsentForm).filter(
        ConsentForm.status == True,
    ).all()
    for i in consent_count:
        if i.is_signed:
            statistics["consent_count"]["已签署"] += 1
            date = datatime_to_str(i.last_update_time, time=False, chinese=True)
            if date in statistics["consent_sign_date"]:
                statistics["consent_sign_date"][date] += 1
        else:
            statistics["consent_count"]["未签署"] += 1
    template_count = session.query(ConsentTemplate).filter(
        ConsentTemplate.status == True,
    ).all()
    statistics["consent_count"]["模板"] = len(template_count)


class SignConsentFormTest(BaseModel):
    other_sign: bool = False
    other_sign_info: str = ""
    patient_sign: str = ""
    doctor_sign: str = ""


async def get_consent_form_html(consent_form_id: int, user: UserInfo, sign_data: SignConsentFormTest = None):
    consent = session.query(ConsentForm).filter(ConsentForm.id == consent_form_id).first()
    if not consent:
        raise HTTPException(status_code=404, detail="Consent not found")
    if not consent.check_permission(user.id):
        raise HTTPException(status_code=403, detail="Permission denied")
    if consent.is_signed and consent.raw_html:
        return consent.raw_html
    data = consent.to_ditail_dict()
    if sign_data:
        data['other_sign'] = sign_data.other_sign
        data['other_sign_info'] = sign_data.other_sign_info
        data['patient_sign'] = sign_data.patient_sign
        data['doctor_sign'] = sign_data.doctor_sign
        data['patient_sign_date'] = datetime.datetime.now()
        data['doctor_sign_date'] = datetime.datetime.now()
    html = template.render(data=data)
    return html


async def get_consent_form_pdf(consent_form_id: int, user: UserInfo):
    consent = session.query(ConsentForm).filter(ConsentForm.id == consent_form_id).first()
    if not consent:
        raise HTTPException(status_code=404, detail="Consent not found")
    if not consent.check_permission(user.id):
        raise HTTPException(status_code=403, detail="Permission denied")
    if not consent.is_signed:
        raise HTTPException(status_code=400, detail="Consent not signed")
    if not consent.pdf_link or not os.path.exists(consent.pdf_link):
        save_name = consent.patient_name + consent.surgery_name + datatime_to_str(consent.patient_sign_date)
        html = template.render(data=consent.to_ditail_dict())
        pdf = HTML(string=html)
        pdf_bytes = pdf.write_pdf()
        temp_pdf_path = save_temp_pdf(pdf_bytes, save_name)
        consent.pdf_link = temp_pdf_path
        consent.raw_html = html
        session.commit()
    key = make_redis_key()
    # 24h过期
    my_redis.set(key, consent.pdf_link, ex=86400)
    return key


async def get_file_path(key: str, delete: bool = True):
    file_path = my_redis.get(key)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")
    if delete:
        my_redis.delete(key)
    return file_path

import datetime
import json
import random
from typing import List, Optional

import redis
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import create_engine, Column, Integer, String, Enum, DateTime, Boolean, Text, ForeignKey, Table
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, Relationship

my_redis = redis.Redis(host='localhost', port=6379, decode_responses=True)


def make_redis_key() -> str:
    key_len = 64
    letter_list = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    while True:
        key = [random.choice(letter_list) for _ in range(key_len)]
        key = "".join(key)
        if not my_redis.exists(key):
            return key


class TextNode(PydanticBaseModel):
    text: str
    children: Optional[List['TextNode']] = None

    def to_dict(self):
        if not self.children:
            return {"text": self.text}
        return {
            "text": self.text,
            "children": [child.to_dict() for child in self.children]
        }


TextNode.model_rebuild()


def datatime_to_str(data: datetime, time=False, chinese=False):
    if not data:
        return ""
    if chinese:
        if time:
            return data.strftime("%Y年%m月%d日 %H:%M:%S")
        return data.strftime("%Y年%m月%d日")
    if time:
        return data.strftime("%Y-%m-%d %H:%M:%S")
    return data.strftime("%Y-%m-%d")


def str_to_datatime(data: str, time=False, chinese=False):
    if not data:
        return datetime.datetime.now()
    if chinese:
        if time:
            return datetime.datetime.strptime(data, "%Y年%m月%d日 %H:%M:%S")
        return datetime.datetime.strptime(data, "%Y年%m月%d日")
    if time:
        return datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
    return datetime.datetime.strptime(data, "%Y-%m-%d")


def get_time_now_str(time=False, chinese=False):
    now = datetime.datetime.now()
    return datatime_to_str(now, time, chinese)


def dump_json(data: list):
    if not data:
        return "[]"
    for i in range(len(data)):
        if isinstance(data[i], TextNode):
            data[i] = data[i].to_dict()
    json_data = json.dumps(data, ensure_ascii=False)
    return json_data


def json_load(data: str):
    if not data:
        return []
    str_data = json.loads(data)
    return str_data


engine = create_engine(
    "mysql+pymysql://root:123456@localhost:3306/mydb?charset=utf8mb4",
    # 超过链接池大小外最多创建的链接
    max_overflow=0,
    # 链接池大小
    pool_size=5,
    # 链接池中没有可用链接则最多等待的秒数，超过该秒数后报错
    pool_timeout=10,
    # 多久之后对链接池中的链接进行一次回收
    pool_recycle=1,
    # 查看原生语句（未格式化）
    echo=True
)

# 基础类
Base = declarative_base()
Session = sessionmaker(bind=engine)
# 内部会采用threading.local进行隔离
session = scoped_session(Session)

ConsentUser = Table(
    "ConsentUser",
    Base.metadata,
    Column("ConsentForm_id", Integer, ForeignKey("ConsentForm.id", ondelete='CASCADE', onupdate='CASCADE'),
           primary_key=True, comment="同意书id"),
    Column("UserInfo_id", String(64), ForeignKey("UserInfo.id", ondelete='CASCADE', onupdate='CASCADE'),
           primary_key=True, comment="用户authing_id")
)


class UserInfo(Base):
    """
    用户信息表（护士、医生、管理员）
    """
    # 数据库中存储的表名
    __tablename__ = "UserInfo"
    id = Column(String(64), primary_key=True, comment="Authing ID主键")
    name = Column(String(64), index=True, default="", comment="姓名")
    phone = Column(Text, default="", comment="手机号")
    email = Column(Text, default="", comment="邮箱")
    department = Column(Text, default="", comment="科室")
    hospital_id = Column(String(64), default="", comment="工号")
    user_class = Column(Enum("护士", "医生", "管理员"), default="护士", comment="用户类型")
    user_verify = Column(Boolean, default=False, nullable=False, comment="用户审核状态")
    verify_info = Column(Text, default="未审核", comment="审核信息")
    create_time = Column(
        DateTime, default=datetime.datetime.now, comment="创建时间")
    last_update_time = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment="最后更新时间")
    hide_in_admin = Column(Boolean(), default=False, nullable=False, comment="是否删除")

    def to_detail_dict(self):
        return {
            "authing_id": self.id,
            "user_name": self.name,
            "phone": self.phone,
            "email": self.email,
            "department": self.department,
            "hospital_id": self.hospital_id,
            "user_class": self.user_class,
            "user_verify": self.user_verify,
            "verify_info": self.verify_info,
            "create_time": datatime_to_str(self.create_time),
            "last_update_time": datatime_to_str(self.last_update_time),
            "hide_in_admin": self.hide_in_admin,
        }


class ConsentForm(Base):
    """
    同意书表
    """
    __tablename__ = "ConsentForm"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    hospital_name = Column(Text, default="", comment="医院名称")
    surgery_name = Column(String(128), index=True, default="", comment="手术名称")
    patient_name = Column(String(64), index=True, default="", comment="病人姓名")
    patient_sex = Column(Enum("男", "女"), default="女", comment="病人性别")
    patient_birth = Column(DateTime, default=datetime.datetime.now, comment="病人出生日期")
    hospital_id = Column(String(64), default="", comment="病人病历号")
    disease_name = Column(Text, default="", comment="疾病名称")
    anesthesia_type = Column(Text, default="", comment="麻醉方式")
    surgery_intro = Column(LONGTEXT, default="", comment="手术介绍")
    risk_intro = Column(LONGTEXT, default="", comment="风险介绍")
    risk_list = Column(LONGTEXT, default="", comment="风险列表")
    special_risk_list = Column(LONGTEXT, default="", comment="特殊风险列表")
    patient_choice = Column(LONGTEXT, default="", comment="病人选择")
    is_signed = Column(Boolean, default=False, nullable=False, comment="是否完成签名")
    other_sign = Column(Boolean, default=False, nullable=False, comment="是否代签名")
    other_sign_info = Column(Text, default="", comment="代签名信息")
    patient_sign = Column(LONGTEXT, default="", comment="病人签名,base64")
    patient_sign_date = Column(DateTime, default=None, comment="病人签名日期")
    doctor_state = Column(Text, default="", comment="医生声明")
    doctor_sign = Column(LONGTEXT, default="", comment="医生签名,base64")
    doctor_sign_date = Column(DateTime, default=None, comment="医生签名日期")
    doctor_sign_id = Column(String(64), ForeignKey("UserInfo.id", ondelete='SET NULL', onupdate='SET NULL'),
                            nullable=True, comment="医生签名id")
    raw_html = Column(LONGTEXT, default='', comment="pdf预览")
    pdf_link = Column(Text, default='', comment="pdf链接")
    permission_list = Relationship("UserInfo", secondary=ConsentUser, backref="permission_list")
    create_time = Column(
        DateTime, default=datetime.datetime.now, comment="创建时间")
    create_user_name = Column(Text, comment="创建用户名")
    last_update_time = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment="最后更新时间")
    last_update_user_name = Column(Text, comment="最后更新用户名")
    update_data = Column(LONGTEXT, default="", comment="更新记录")
    status = Column(Boolean, default=True, nullable=False, comment="未删除")

    def to_search_dict(self):
        if self.is_signed:
            self_class = "signed"
        else:
            self_class = "unsigned"
        return {
            "create_time": datatime_to_str(self.create_time, chinese=True, time=True),
            "create_user_name": self.create_user_name,
            "last_update_time": datatime_to_str(self.last_update_time, chinese=True, time=True),
            "last_update_user_name": self.last_update_user_name,
            "sign_time": datatime_to_str(self.patient_sign_date, chinese=True, time=True),
            "self_class": self_class,
            "self_id": self.id,
            "patient_name": self.patient_name,
            "surgery_name": self.surgery_name,
            "disease_name": self.disease_name,
            "permission_list": [user.id for user in self.permission_list],
        }

    def to_ditail_dict(self):
        return {
            "id": self.id,
            "hospital_name": self.hospital_name,
            "surgery_name": self.surgery_name,
            "patient_name": self.patient_name,
            "patient_sex": self.patient_sex,
            "patient_birth": datatime_to_str(self.patient_birth),
            "hospital_id": self.hospital_id,
            "disease_name": self.disease_name,
            "anesthesia_type": self.anesthesia_type,
            "surgery_intro": self.surgery_intro,
            "risk_intro": self.risk_intro,
            "risk_list": json_load(self.risk_list),
            "special_risk_list": json_load(self.special_risk_list),
            "patient_choice": json_load(self.patient_choice),
            "is_signed": self.is_signed,
            "other_sign": self.other_sign,
            "other_sign_info": self.other_sign_info,
            "patient_sign": self.patient_sign,
            "patient_sign_date": datatime_to_str(self.patient_sign_date, chinese=True, time=True),
            "doctor_state": self.doctor_state,
            "doctor_sign": self.doctor_sign,
            "doctor_sign_date": datatime_to_str(self.doctor_sign_date, chinese=True, time=True),
            "doctor_sign_id": self.doctor_sign_id,
            "pdf_link": self.pdf_link,
            "permission_list": [user.id for user in self.permission_list],
            "create_time": datatime_to_str(self.create_time, chinese=True, time=True),
            "create_user_name": self.create_user_name,
            "last_update_time": datatime_to_str(self.last_update_time, chinese=True, time=True),
            "last_update_user_name": self.last_update_user_name,
            "update_data": json_load(self.update_data)
        }

    def to_template_dict(self):
        return {
            "hospital_name": self.hospital_name,
            "surgery_name": self.surgery_name,
            "disease_name": self.disease_name,
            "anesthesia_type": self.anesthesia_type,
            "surgery_intro": self.surgery_intro,
            "risk_intro": self.risk_intro,
            "risk_list": json_load(self.risk_list),
            "patient_choice": json_load(self.patient_choice),
            "doctor_state": self.doctor_state
        }

    def check_permission(self, user_id):
        for user in self.permission_list:
            if user.id == user_id:
                return True
        return False


class ConsentTemplate(Base):
    """
    同意书模板表
    """
    __tablename__ = "ConsentTemplate"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    hospital_name = Column(Text, default="", comment="医院名称")
    surgery_name = Column(String(128), index=True, default="", comment="手术名称")
    disease_name = Column(Text, default="", comment="疾病名称")
    anesthesia_type = Column(Text, default="", comment="麻醉方式")
    surgery_intro = Column(LONGTEXT, default="", comment="手术介绍")
    risk_intro = Column(LONGTEXT, default="", comment="风险介绍")
    risk_list = Column(LONGTEXT, default="", comment="风险列表")
    patient_choice = Column(LONGTEXT, default="", comment="病人选择")
    doctor_state = Column(Text, default="", comment="医生声明")
    # 删除权限
    create_user_id = Column(String(64), ForeignKey("UserInfo.id", ondelete='CASCADE', onupdate='CASCADE'),
                            nullable=True, comment="创建用户id")
    template_intro = Column(Text, default="", comment="模板介绍")
    is_public = Column(Boolean, default=False, nullable=False, comment="是否公开")
    create_time = Column(
        DateTime, default=datetime.datetime.now, comment="创建时间")
    create_user_name = Column(Text, comment="创建用户名")
    last_update_time = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment="最后更新时间")
    last_update_user_name = Column(Text, comment="最后更新用户名")
    update_data = Column(LONGTEXT, default="", comment="更新记录")
    status = Column(Boolean(), default=True, nullable=False, comment="未删除")

    def to_search_dict(self):
        return {
            "create_time": datatime_to_str(self.create_time, chinese=True, time=True),
            "create_user_name": self.create_user_name,
            "last_update_time": datatime_to_str(self.last_update_time, chinese=True, time=True),
            "last_update_user_name": self.last_update_user_name,
            "self_id": self.id,
            "self_class": "template",
            "surgery_name": self.surgery_name,
            "disease_name": self.disease_name,
            "create_user_id": self.create_user_id,
            "is_public": self.is_public,
            "template_intro": self.template_intro,
        }

    def to_ditail_dict(self):
        return {
            "id": self.id,
            "hospital_name": self.hospital_name,
            "surgery_name": self.surgery_name,
            "disease_name": self.disease_name,
            "anesthesia_type": self.anesthesia_type,
            "surgery_intro": self.surgery_intro,
            "risk_intro": self.risk_intro,
            "risk_list": json_load(self.risk_list),
            "patient_choice": json_load(self.patient_choice),
            "doctor_state": self.doctor_state,
            "create_user_id": self.create_user_id,
            "template_intro": self.template_intro,
            "is_public": self.is_public,
            "create_time": datatime_to_str(self.create_time, chinese=True, time=True),
            "create_user_name": self.create_user_name,
            "last_update_time": datatime_to_str(self.last_update_time, chinese=True, time=True),
            "last_update_user_name": self.last_update_user_name,
            "update_data": json_load(self.update_data),
        }


class Inform(Base):
    """
    首页通知表
    """
    __tablename__ = "Inform"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    title = Column(String(64), index=True, default="", comment="标题")
    img_b64 = Column(LONGTEXT, default="", comment="图片base64")
    url = Column(Text, default="", comment="链接")
    create_info = Column(Text, default="", comment="创建信息")
    create_time = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment="创建、更新时间")


def add_update_data(before: str, add_data: list[TextNode], user: UserInfo):
    if before:
        before_data = json_load(before)
    else:
        before_data = []
    now = get_time_now_str(time=True, chinese=True)
    for i in add_data:
        if i and i.text:
            j = {"text": now + "---" + user.name + "-" + user.id + i.text}
            before_data.append(j)
    return dump_json(before_data)

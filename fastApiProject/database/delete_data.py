from fastapi import HTTPException

from database.models import *


async def admin_delete_inform(inform_id: int):
    inform = session.query(Inform).filter(Inform.id == inform_id).first()
    if inform:
        session.delete(inform)
        session.commit()
        return True
    raise HTTPException(status_code=404, detail="Inform not found")


async def delete_consent_form(consent_id: int, user: UserInfo):
    consent = session.query(ConsentForm).filter(ConsentForm.id == consent_id).first()
    if not consent:
        raise HTTPException(status_code=404, detail="ConsentForm not found")
    if not consent.check_permission(user.id):
        raise HTTPException(status_code=403, detail="Permission denied")
    consent.status = False
    session.commit()
    return True


async def delete_consent_template(template_id: int, user: UserInfo):
    template = session.query(ConsentTemplate).filter(ConsentTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="ConsentTemplate not found")
    if user.id != template.create_user_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    template.status = False
    session.commit()
    return True


async def delete_user(user_id: str):
    user = session.query(UserInfo).filter(UserInfo.id == user_id).first()
    if user:
        session.delete(user)
        session.commit()
    user = session.query(UserInfo).filter(UserInfo.id == "").all()
    if user:
        session.delete(user)
        session.commit()
    return True

import multiprocessing
import uvicorn
from fastapi import Request, FastAPI, Query, Header, Depends, BackgroundTasks, Body
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import *

from database.delete_data import *
from database.get_data import *
from database.insert_data import *
from database.update_data import *

multiprocessing.freeze_support()
app = FastAPI()

# 添加CORS中间件，配置允许的源、方法等
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的域名或'*'代表所有域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许的请求方法
    allow_headers=["*"],  # 允许的请求头
)


# home
@app.get("/")
async def get_index_app():
    return {"status": "success"}
    # index = "localhost:5173"
    # return RedirectResponse(index)


# home
@app.get("/me/profile/base/")
async def get_base_profile_app(request: Request, Authorization=Header()):
    # 获取用户基本信息
    res = await get_basic_user_info(Authorization)
    return res


# settings
@app.get("/me/profile/")
async def get_settings_app(request: Request, Authorization=Header()):
    return await get_user_info(Authorization)


# settings
@app.post("/me/profile/")
async def post_settings_app(request: Request, r_data: UpdateUser, Authorization=Header()):
    await update_user_info(Authorization=Authorization, update_data=r_data)
    return {"status": "success"}


# home
@app.get("/inform/")
async def get_inform_app(request: Request, Authorization=Header(), info_len: int = 3):
    verify_id_token(Authorization, need_verify=True)
    info_len = 4 if info_len > 4 else info_len
    res = await get_inform_list(info_len)
    return {"inform_list": res}


# create
@app.get("/search/user_name/")
async def search_user_name_app(request: Request, Authorization=Header(), search_content: str = Query(None)):
    verify_id_token(Authorization, need_verify=True)
    user = await user_search_user(search_content)
    return {"search_result": user}


# home
@app.get("/search/")
async def search_app(request: Request, Authorization=Header(), search_params: SearchConsent = Depends()):
    user = verify_and_get_user(Authorization, need_verify=True)
    search_result = await search_consent(user, search_params)
    return search_result


# create
@app.post("/create/consent_form/")
async def create_consent_form_app(request: Request, r_data: AddConsentForm, Authorization=Header()):
    user = verify_and_get_user(Authorization, need_verify=True)
    new_id = await add_consent_form(user, r_data)
    return {"new_id": new_id}


# create
@app.post("/create/consent_template/")
async def create_consent_template_app(request: Request, r_data: AddConsentTemplate, Authorization=Header()):
    user = verify_and_get_user(Authorization, need_verify=True)
    new_id = await add_consent_template(user, r_data)
    return {"new_id": new_id}


# sign
@app.get("/consent_form/{consent_form_id}/html/")
async def get_consent_form_html_app(request: Request, consent_form_id: int, Authorization=Header()):
    user = verify_and_get_user(Authorization, need_verify=True)
    content = await get_consent_form_html(consent_form_id, user)
    return {"html": content}


# sign
@app.post("/consent_form/{consent_form_id}/html/")
async def post_consent_form_html_app(request: Request, consent_form_id: int, sign_data: SignConsentFormTest,
                                     Authorization=Header()):
    user = verify_and_get_user(Authorization, need_verify=True)
    content = await get_consent_form_html(consent_form_id, user, sign_data)
    return {"html": content}


# sign
@app.get("/consent_form/{consent_form_id}/pdf/")
async def get_consent_form_pdf_app(request: Request, consent_form_id: int, Authorization=Header()):
    user = verify_and_get_user(Authorization, need_verify=True)
    pdf_code = await get_consent_form_pdf(consent_form_id, user)
    return {"code": pdf_code}


# sign
@app.get("/consent_form/{consent_form_id}/unsign/")
async def unsign_consent_form_app(request: Request, consent_form_id: int,
                                  Authorization=Header()):
    user = verify_and_get_user(Authorization, user_class=["医生"], need_verify=True)
    await unsign_consent_form(consent_form_id, user)
    return {"status": "success"}


# sign
@app.post("/consent_form/{consent_form_id}/sign/")
async def sign_consent_form_app(request: Request, r_data: SignConsentForm, consent_form_id: int,
                                background_tasks: BackgroundTasks,
                                Authorization=Header()):
    user = verify_and_get_user(Authorization, user_class=["医生"], need_verify=True)
    await sign_consent_form(consent_form_id=consent_form_id, user=user, sign_data=r_data)
    background_tasks.add_task(get_consent_form_pdf, consent_form_id, user)
    return {"status": "success", "consent_form_id": consent_form_id}


# edit
@app.get("/consent_form/{consent_form_id}/")
async def get_consent_form_app(request: Request, consent_form_id: int, Authorization=Header()):
    user = verify_and_get_user(Authorization, need_verify=True)
    data = await get_consent_form(consent_form_id, user)
    return data


# edit
@app.post("/consent_form/{consent_form_id}/")
async def post_consent_form_app(request: Request, consent_form_id: int, r_data: UpdateConsentForm = Body(...),
                                Authorization=Header()):
    user = verify_and_get_user(Authorization, need_verify=True)
    await update_consent_form(consent_form_id=consent_form_id, user=user, update_data=r_data)
    return {"status": "success", "consent_form_id": consent_form_id}


# edit
@app.delete("/consent_form/{consent_form_id}/")
async def delete_consent_form_app(request: Request, consent_form_id: int, Authorization=Header()):
    user = verify_and_get_user(Authorization, need_verify=True)
    await delete_consent_form(consent_form_id, user)
    # 删除
    return {"status": "success"}


# edit
@app.get("/consent_template/{consent_template_id}/")
async def get_consent_template_app(request: Request, consent_template_id: int, Authorization=Header()):
    user = verify_and_get_user(Authorization, need_verify=True)
    data = await get_consent_template(consent_template_id, user)
    return data


# edit
@app.post("/consent_template/{consent_template_id}/")
async def post_consent_template_app(request: Request, r_data: UpdateConsentTemplate, consent_template_id: int,
                                    Authorization=Header()):
    user = verify_and_get_user(Authorization, need_verify=True)
    await update_consent_template(consent_template_id, user, r_data)
    return {"status": "success"}


# edit
@app.delete("/consent_template/{consent_template_id}/")
async def delete_consent_template_app(request: Request, consent_template_id: int, Authorization=Header()):
    user = verify_and_get_user(Authorization, need_verify=True)
    await delete_consent_template(consent_template_id, user)
    return {"status": "success"}


# admin
@app.get("/admin/user/{authing_id}/")
async def admin_user_detail_app(request: Request, authing_id: str, Authorization=Header()):
    verify_id_token(Authorization, user_class=['管理员'], need_verify=True)
    user = await admin_get_user_detail(authing_id)
    return user


# admin
@app.get("/admin/user/")
async def admin_user_search_app(request: Request, Authorization=Header(), search_content: str = Query(''),
                                not_verify: bool = Query(False), show_hide: bool = Query(False)):
    verify_id_token(Authorization, user_class=['管理员'], need_verify=True)
    users = await admin_search_user(search_content, not_verify, show_hide)
    return {"search_result": users}


# admin
@app.post("/admin/user/{authing_id}/")
async def admin_user_post_app(request: Request, r_data: AdminUpdateUser, authing_id: str, Authorization=Header()):
    verify_id_token(Authorization, user_class=['管理员'], need_verify=True)
    await admin_update_user(authing_id, r_data)
    # 更新用户信息
    return {"status": "success"}


# admin
@app.post("/admin/user/{authing_id}/hide/")
async def admin_user_hide_app(request: Request, authing_id: str, Authorization=Header(), hide: bool = True):
    verify_id_token(Authorization, user_class=['管理员'], need_verify=True)
    await admin_hide_user(authing_id, hide)
    # 隐藏用户
    return {"status": "success"}


# admin
@app.get("/admin/inform/")
async def admin_inform_app(request: Request, Authorization=Header()):
    verify_id_token(Authorization, user_class=['管理员'], need_verify=True)
    informs = await get_inform_list(limit=False)
    return {
        "inform_list": informs
    }


# admin
@app.post("/admin/inform/{inform_id}/")
async def admin_inform_post_app(request: Request, r_data: UpdateInform, inform_id: int, Authorization=Header()):
    verify_id_token(Authorization, user_class=['管理员'], need_verify=True)
    inform_id = await admin_update_inform(inform_id, r_data)
    return {"status": "success", "inform_id": inform_id}


# admin
@app.delete("/admin/inform/{inform_id}/")
async def admin_inform_delete_app(request: Request, inform_id: int, Authorization=Header()):
    verify_id_token(Authorization, user_class=['管理员'], need_verify=True)
    await admin_delete_inform(inform_id)
    return {"status": "success"}


# statistics
@app.get("/statistics/")
async def get_statistics_app(request: Request, Authorization=Header()):
    user = verify_and_get_user(Authorization, need_verify=True)
    data = await get_statistics(user)
    return data


# download
@app.get("/download/{code}/")
async def download_app(request: Request, code: str, file_name: str = ""):
    file_path = await get_file_path(code)
    if not file_path:
        return {"status": "error", "message": "file not found"}
    if not file_name:
        file_name = file_path.split("/")[-1]
    return FileResponse(file_path, filename=file_name)


if __name__ == '__main__':
    uvicorn.run(app="app:app", host="0.0.0.0", port=8082, reload=True)

import axios from 'axios';
import {ElNotification} from "element-plus";
import {logOut, unVerify} from "@/router/log_out.js";

export const base_url = 'http://localhost:8082/'
// export const base_url = 'https://chuxiaodong.top/'

const success_response = function (response) {
    // 2xx 范围内的状态码都会触发该函数。
    // ElNotification({
    //     title: '成功',
    //     message: '操作成功完成！',
    //     type: 'success',
    //     duration: 1000
    // });
    return response;
}

const failure_response = function (error) {
    // 超出 2xx 范围的状态码都会触发该函数。
    let errorMessage = '发生错误，请稍后再试。';
    if (error.response) {
        const status = error.response.status;
        if (status === 401) {
            errorMessage = '未授权，请重新登录。';
            logOut();
        } else if (status === 403) {
            errorMessage = '禁止访问，请联系管理员。';
        } else if (status === 404) {
            errorMessage = '请求的资源未找到。';
        } else if (status === 412) {
            errorMessage = '请更新个人设置或联系管理员验证身份组。';
            unVerify();
        } else if (status === 422) {
            errorMessage = '请求参数错误，请检查输入。';
        } else if (status === 500) {
            errorMessage = '服务器内部错误，请稍后再试。';
        } else {
            errorMessage = `发生错误：${status}`;
        }
    }
    ElNotification({
        title: '错误',
        message: errorMessage,
        type: 'error',
        duration: 5000
    });
}


//统一Axios请求配置
function apiAxios(axiosConfig) {
    const service = axios.create({
        baseURL: base_url, // 设置统一的请求前缀
        timeout: 30000, // 设置统一的超时时长
        headers: {
            'Authorization': `${localStorage._authing_token}`, //router中判断一定有值
            'Content-Type': 'application/json'
        }
    });
    service.interceptors.response.use(success_response, failure_response)
    return service(axiosConfig)
}

export default apiAxios;

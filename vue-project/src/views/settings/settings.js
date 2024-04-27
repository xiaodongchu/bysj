import apiAxios from "@/router/axios.js";

export function getUserSetting() {
    return apiAxios({
        url: '/me/profile/',
        method: 'get',
    })
}

export function updateUserSetting(data) {
    return apiAxios({
        url: '/me/profile/',
        method: 'post',
        data: data
    })
}
import apiAxios from "@/router/axios.js";

export function getSelfBaseProfile() {
    return apiAxios({
        url: '/me/profile/base/',
        method: 'get',
    })
}
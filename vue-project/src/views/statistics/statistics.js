import apiAxios from "@/router/axios.js";

export function get_statistics() {
    return apiAxios({
        url: '/statistics/',
        method: 'get',
    })
}
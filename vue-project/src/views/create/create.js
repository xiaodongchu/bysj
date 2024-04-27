import apiAxios from "@/router/axios.js";


export function search_user_by_name(search_content) {
    return apiAxios({
        url: '/search/user_name/',
        method: 'get',
        params: {
            search_content: search_content,
        }
    })
}

export function create_template(data) {
    return apiAxios({
        url: '/create/consent_template/',
        method: 'post',
        data: data
    })
}

export function create_sign(data) {
    return apiAxios({
        url: '/create/consent_form/',
        method: 'post',
        data: data
    })
}
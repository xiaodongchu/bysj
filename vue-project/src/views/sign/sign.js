import apiAxios from "@/router/axios.js";

export function get_html(unsigned_id) {
    return apiAxios({
        url: '/consent_form/' + unsigned_id + '/html/',
        method: 'get',
    })
}

export function get_unsigned(unsigned_id) {
    return apiAxios({
        url: '/consent_form/' + unsigned_id,
        method: 'get',
    })
}

export function post_html(unsigned_id, data) {
    return apiAxios({
        url: '/consent_form/' + unsigned_id + '/html/',
        method: 'post',
        data: data
    })
}

export function post_sign(unsigned_id, data) {
    return apiAxios({
        url: '/consent_form/' + unsigned_id + '/sign/',
        method: 'post',
        data: data
    })
}

export function get_pdf(signed_id) {
    return apiAxios({
        url: '/consent_form/' + signed_id + '/pdf/',
        method: 'get',
    })
}
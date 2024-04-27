import apiAxios from "@/router/axios.js";

export function get_unsigned(unsigned_id) {
    return apiAxios({
        url: '/consent_form/' + unsigned_id,
        method: 'get',
    })
}

export function post_unsigned(unsigned_id, data) {
    return apiAxios({
        url: '/consent_form/' + unsigned_id,
        method: 'post',
        data: data
    })
}

export function get_template(template_id) {
    return apiAxios({
        url: '/consent_template/' + template_id,
        method: 'get',
    })
}

export function post_template(template_id, data) {
    return apiAxios({
        url: '/consent_template/' + template_id,
        method: 'post',
        data: data
    })
}

import apiAxios from "@/router/axios.js";

export function get_search(search_content = "", not_verify = false, show_hide = false) {
    return apiAxios({
        url: '/admin/user/',
        method: 'get',
        params: {
            search_content: search_content,
            not_verify: not_verify,
            show_hide: show_hide
        }
    })
}


export function get_user_data(authing_id = "") {
    if (authing_id) {
        return apiAxios({
            url: '/admin/user/' + authing_id,
            method: 'get',
        })
    }
}

export function post_user_data(authing_id = "", data = {}) {
    if (authing_id && data) {
        return apiAxios({
            url: '/admin/user/' + authing_id,
            method: 'post',
            data: data
        })
    }
}

export function get_inform() {
    return apiAxios({
        url: '/admin/inform/',
        method: 'get',
    })
}

export function post_inform(inform_id = 0, data = {}) {
    if (data) {
        return apiAxios({
            url: '/admin/inform/' + inform_id,
            method: 'post',
            data: data
        })
    }
}

export function delete_inform(inform_id = 0) {
    return apiAxios({
        url: '/admin/inform/' + inform_id,
        method: 'delete',
    })
}

export function hide_user(authing_id = "", hide = true) {
    if (authing_id) {
        return apiAxios({
            url: '/admin/user/' + authing_id + '/hide/',
            method: 'post',
            params: {
                hide: hide
            }
        })
    }
}
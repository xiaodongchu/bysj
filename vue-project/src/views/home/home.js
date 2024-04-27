import apiAxios from "@/router/axios.js";

export function get_inform(info_len = 3) {
    return apiAxios({
        url: '/inform/',
        method: 'get',
        data: {
            info_len: info_len
        }
    })
}

export function get_search(search_type, search_content, end_id, page_len) {
    return apiAxios({
        url: '/search/',
        method: 'get',
        params: {
            search_type: search_type,
            search_content: search_content,
            end_id: end_id,
            page_len: page_len
        }
    })
}

export function delete_by_id(delete_type, delete_id) {
    if (delete_type === 'unsigned') {
        return apiAxios({
            url: '/consent_form/' + delete_id,
            method: 'delete',
        })
    } else if (delete_type === 'template') {
        return apiAxios({
            url: '/consent_template/' + delete_id,
            method: 'delete',
        })
    }
}
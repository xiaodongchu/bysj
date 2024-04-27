import {base_url} from "@/router/axios.js";

export function openLink(url) {
    // 如果url以/开头，说明是相对路径，需要加上服务器地址
    if (url.startsWith('/')) {
        if (base_url.endsWith('/')) {
            url = url.substring(1);
        }
        url = base_url + url;
    }
    try {
        if (window.cordova && cordova.InAppBrowser) {
            cordova.InAppBrowser.open(url, '_blank', 'location=no,toolbar=no');
        } else {
            window.open(url, '_blank');
        }
    } catch (e) {
        window.open(url, '_blank');
    }
}


export function get_full_link(url) {
    // 如果url以/开头，说明是相对路径，需要加上服务器地址
    if (url.startsWith('/')) {
        if (base_url.endsWith('/')) {
            url = url.substring(1);
        }
        url = base_url + url;
    }
    return url;
}
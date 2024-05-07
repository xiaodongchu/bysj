import store from '@/router/store'
import router from '@/router/index'

export function logOut() {
    localStorage.removeItem('authing_id')
    localStorage.removeItem('_authing_token')
    store.commit('set_user_verify', false)
    store.commit('set_user_name', '')
    store.commit('set_user_class', '管理员')
    store.commit('set_search_content', '')
    store.commit('set_search_type', 'unsigned')
    store.commit('clear_home_cards')
    router.replace('/login').then()
}

export function unVerify() {
    store.commit('set_user_verify', false)
    store.commit('set_search_content', '')
    store.commit('set_search_type', 'unsigned')
    store.commit('clear_home_cards')
    router.replace('/settings').then()
}
import {createStore} from 'vuex';

const store = createStore({
    state() {
        return {
            user_verify: false,
            user_name: 'admin',
            user_class: '管理员',
            search_content: '',
            search_type: 'unsigned',
            home_cards: [],
            hospital_name: "医院",
            inform: [],
        };
    },
    mutations: {
        set_user_verify(state, verify) {
            state.user_verify = verify;
        },
        set_user_name(state, name) {
            state.user_name = name;
        },
        set_user_class(state, user_class) {
            state.user_class = user_class;
        },
        set_search_content(state, search_content) {
            state.search_content = search_content;
        },
        set_search_type(state, search_type) {
            state.search_type = search_type;
        },
        merge_home_cards(state, home_cards) {
            //连接
            home_cards = state.home_cards.concat(home_cards);
            state.home_cards = home_cards
        },
        clear_home_cards(state) {
            state.home_cards = [];
        },
        set_hospital_name(state, hospital_name) {
            state.hospital_name = hospital_name;
        },
        set_inform(state, inform_list) {
            state.inform = inform_list
        }
    },
    actions: {},
});

export default store;

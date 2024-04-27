import {createRouter, createWebHashHistory} from "vue-router";

// 引入
import home from "@/views/home.vue";

import login from "@/views/login.vue";
import settings from "@/views/settings.vue";
import statistics from '@/views/statistics.vue'

import admin from "@/views/admin.vue";

import create from "@/views/create.vue";
import edit from "@/views/edit.vue";
import sign from "@/views/sign.vue";
import signed from "@/views/signed.vue";


// 路由信息
let routes = [
    {
        path: "/",
        name: 'home',
        component: home,
    },
    {
        path: '/login',
        name: 'login',
        component: login,
    },
    {
        path: "/settings",
        name: 'settings',
        component: settings,
    },
    {
        path: "/statistics",
        name: "statistics",
        component: statistics,
    },
    {
        path: "/admin",
        name: 'admin',
        component: admin,
    },
    {
        path: "/create",
        name: 'create',
        component: create,
    },
    {
        path: "/edit/:type/:id",
        name: 'edit',
        component: edit,
    },
    {
        path: "/sign/:id",
        name: 'sign',
        component: sign,
    },
    {
        path: "/signed/:id",
        name: 'signed',
        component: signed,
    },
];

// 路由器
const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    if (to.path !== '/login' && !localStorage._authing_token) {
        next({path: '/login'})
    } else {
        next() // go to wherever I'm going
    }
})

export default router;
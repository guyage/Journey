/*jshint esversion: 6 */
import Vue from 'vue';
import NProgress from 'nprogress';
import 'nprogress/nprogress.css';
//配置路由
import VueRouter from 'vue-router';
Vue.use(VueRouter);

import store from '@/store/store.js';
import { getCookies, setCookies, removeCookies } from '@/utils/auth.js';

// 引入路由
import ConfRouter from './modules/conf.js';
import DbRouter from './modules/db.js';
import QueryRouter from './modules/query.js';
import SqlOrderRouter from './modules/sqlorder.js';
import UserRouter from './modules/user.js';
import WorkOrderRouter from './modules/workorder.js';
import ApprovalGroupRouter from './modules/approvalgroup.js';
import AutoOrderRouter from './modules/autoorder.js';


// 引入错误页面组件
import Error_404 from '@/components/views/error_page/Error_404.vue';

// 配置路由   注意：名字
const login = {
    path: '/login',
    component: resolve => require(['@/components/views/Login.vue'],resolve),
    name: 'login',
}

const DefaultRouter = {
    path: '/index',
    component: resolve => require(['@/components/views/Index.vue'],resolve),
    redirect: 'dashboard',
    meta: {tag: '首页', title: ['首页']},
}

const DynamicRouter = [
    {
        path: '/',
        component: resolve => require(['@/components/views/Index.vue'],resolve),
        name: 'index',
        redirect: 'dashboard',
        meta: { tag: '首页', title: ['首页']},
        children: [
            {
                path: '/dashboard',
                component: resolve => require(['@/components/views/Dashboard.vue'],resolve),
                name: 'dashboard',
                meta: { tag: '仪表盘', title: ['仪表盘']},
            },
            // 组件路由
            ...ConfRouter,
            ...DbRouter,
            ...QueryRouter,
            ...SqlOrderRouter,
            ...UserRouter,
            ...WorkOrderRouter,
            ...ApprovalGroupRouter,
            ...AutoOrderRouter,
        ]
    },

]

// DynamicRouter[0].children.concat(SqlOrderRouter)

console.log(DynamicRouter);


const ErrorRouter = [
    {
        path: '*',
        redirect: '/404',
        hidden: true,
        meta: { tag: '404', title: ['404','404']},
    },
]

// 实例化VueRouter  注意：名字
const router = new VueRouter({
    routes: [login,DefaultRouter] // （缩写）相当于 routes: routes
});

router.beforeEach((to, from, next) => {
    if (store.getters.token) {
        if (to.path === '/login') {
            NProgress.start();
            next()
        } else {
            if (store.getters.username.length === 0) {
                let username_cookies = getCookies('username')
                if (username_cookies != 0) {
                    let userinfo = {}
                    userinfo.username = username_cookies
                    store.dispatch('SetUserInfo',userinfo)
                    store.dispatch('GenerateRoutes',DynamicRouter).then((realrouter) => {
                        router.addRoutes(realrouter)

                    })
                    NProgress.start();
                    next()
                } else {
                    NProgress.start();
                    next( {path:'/login'} );
                }
            }
            else {
                if (store.getters.router.length ==0) {
                    store.dispatch('GenerateRoutes',DynamicRouter).then((realrouter) => {
                        router.addRoutes(realrouter)
                    })
                    NProgress.start();
                    next()
                } else {
                    NProgress.start();
                    next()
                }
            }
        }

    }
    else {
        if (to.path === '/login') {
            NProgress.start();
            next();
        } else {
            NProgress.start();
            next( {path:'/login'} );
        }
    }

})

router.afterEach(()=> {
    NProgress.done();
});

export default router;

/*jshint esversion: 6 */
import Vue from 'vue';

//配置路由
import VueRouter from 'vue-router';
Vue.use(VueRouter);

import store from '@/store/store.js';
import { getCookies, setCookies, removeCookies } from '@/utils/auth.js';

//引入功能组件
import Index from '@/components/views/Index.vue';
import Login from '@/components/views/Login.vue';
import Dashboard from '@/components/views/Dashboard.vue';
import User from '@/components/user/User.vue';
import UserGroup from '@/components/user/UserGroup.vue';
import MailConfig from '@/components/conf/MailConfig.vue';
import MysqlInst from '@/components/db/MysqlInst.vue';
import UserAccessMysql from '@/components/db/UserAccessMysql.vue';
import MysqlMeta from '@/components/db/MysqlMeta.vue';
import MysqlUser from '@/components/db/MysqlUser.vue';
import MysqlStatus from '@/components/db/MysqlStatus.vue';

import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

//配置路由   注意：名字
const login = {
    path: '/login',
    component: Login ,
    name: 'login',
}

const DefaultRouter = {
    path: '/index', 
    component: Index,
    redirect: 'dashboard',
    meta: { issuper: false , tag: '首页', title: ['首页']},
}

const DynamicRouter = [
    {
        path: '/', 
        component: Index,
        name: 'index',
        redirect: 'dashboard',
        meta: { issuper: false, tag: '首页', title: ['首页']},
        children: [
            { 
                path: '/dashboard', 
                component: Dashboard, 
                name: 'dashboard',
                meta: { issuper: false, tag: '仪表盘',title: ['仪表盘']},
            },
            {
                path: '/user', 
                component: User, 
                name: 'user',
                meta: { issuper: true, tag: '用户',title: ['用户管理','用户']},
            },
            {
                path: '/usergroup', 
                component: UserGroup, 
                name: 'usergroup',
                meta: { issuper: true, tag: '用户组',title: ['用户管理','用户组']},
            },
            {
                path: '/mailconfig', 
                component: MailConfig, 
                name: 'mailconfig',
                meta: { issuper: true, tag: '邮件配置',title: ['全局配置','邮件配置']},
            },
            {
                path: '/mysqlinst', 
                component: MysqlInst, 
                name: 'mysqlinst',
                meta: { issuper: true, tag: 'MySQL管理',title: ['MySQL管理','MySQL实例']},
            },
            {
                path: '/mysqlmeta', 
                component: MysqlMeta, 
                name: 'mysqlmeta',
                meta: { issuper: false, tag: 'MySQL元数据',title: ['MySQL管理','MySQL元数据']},
            },
            {
                path: '/mysqlstatus', 
                component: MysqlStatus, 
                name: 'mysqlstatus',
                meta: { issuper: true, tag: 'MySQL实例状态',title: ['MySQL管理','MySQL实例状态']},
            },
            {
                path: '/mysqluser', 
                component: MysqlUser, 
                name: 'mysqluser',
                meta: { issuper: true, tag: 'MySQL用户',title: ['MySQL管理','MySQL用户']},
            },
            {
                path: '/useraccessmysql', 
                component: UserAccessMysql, 
                name: 'useraccessmysql',
                meta: { issuper: false, tag: 'MySQL权限',title: ['数据库权限','MySQL权限']},
            },
            
        ]
    }
]



// 实例化VueRouter  注意：名字
const router = new VueRouter({
    routes: [login,DefaultRouter] // （缩写）相当于 routes: routes
})

router.beforeEach(( to, from, next) => {
    // ${//to and from are Route Object,next() must be called to resolve the hook}
    if(store.getters.token) {
        if (to.path === '/login') {
            NProgress.start();
            next()
        } else {
            if(store.getters.username.length == 0) {
                var username_cookies = getCookies('username')
                var userissuper_cookies = getCookies('userissuper')
                if(username_cookies.length !=0) {
                    var userinfo = {}
                    userinfo.username = username_cookies
                    store.dispatch('SetUserInfo',userinfo)
                    var RouterMap = {}
                    var issuper = userissuper_cookies
                    RouterMap.issuper = issuper
                    RouterMap.dynamicrouter = DynamicRouter
                    store.dispatch('GenerateRoutes',RouterMap).then(() => {
                        store.dispatch('GenerateMenus',issuper).then(() => {
                            router.addRoutes(store.getters.routers) 
                        })
                        NProgress.start();
                        next()
                    })
                } else {
                    next( {path:'/login'} );
                }
            } else {
                if (store.getters.routers.length ==0) {
                    var RouterMap = {}
                    var issuper = store.getters.userissuper
                    RouterMap.issuper = issuper
                    RouterMap.dynamicrouter = DynamicRouter
                    store.dispatch('GenerateRoutes',RouterMap).then(() => {
                        store.dispatch('GenerateMenus',issuper).then(() => {                          
                            router.addRoutes(store.getters.routers)
                            // next()   
                        })
                        NProgress.start(); 
                        next()                       
                    })
                } else {
                    NProgress.start();
                    next()                 
                }
            }
        }        
    } else {
        if (to.path === '/login') {
            NProgress.start();
            next();
        } else {
            next( {path:'/login'} );
        }
    }
})


router.afterEach(()=> {
    NProgress.done();
});

export default router;
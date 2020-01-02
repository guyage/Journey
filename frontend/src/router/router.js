/*jshint esversion: 6 */
import Vue from 'vue';
import NProgress from 'nprogress';
import 'nprogress/nprogress.css';
//配置路由
import VueRouter from 'vue-router';
Vue.use(VueRouter);

import store from '@/store/store.js';
import { getCookies, setCookies, removeCookies } from '@/utils/auth.js';

// //引入功能组件
// import Login from '@/components/views/Login.vue';
// import Index from '@/components/views/Index.vue';
// import Dashboard from '@/components/views/Dashboard.vue';
// import Menus from '@/components/user/menus/Menus.vue';
// import Role from '@/components/user/role/Role.vue';
// import User from '@/components/user/user/User.vue';
// import UserGroup from '@/components/user/usergroup/UserGroup.vue';
// // conf
// import MailConfig from '@/components/conf/MailConfig.vue';
// import QueryLimit from '@/components/conf/QueryLimit.vue';
// import DumpWhiteList from '@/components/conf/DumpWhiteList.vue';
// ////db
// //mysql
// import MysqlInst from '@/components/db/mysql/MysqlInst.vue';
// import UserAccessMysql from '@/components/db/mysql/UserAccessMysql.vue';
// import MysqlMeta from '@/components/db/mysql/MysqlMeta.vue';
// import MysqlUser from '@/components/db/mysql/MysqlUser.vue';
// import MysqlStatus from '@/components/db/mysql/MysqlStatus.vue';
// //mongodb
// import MongodbInst from '@/components/db/mongodb/MongodbInst.vue';
// import UserAccessMongodb from '@/components/db/mongodb/UserAccessMongodb.vue';
// //redis
// import RedisInst from '@/components/db/redis/RedisInst.vue';
// import UserAccessRedis from '@/components/db/redis/UserAccessRedis.vue';
// //// query
// import QuerySql from '@/components/query/QuerySql.vue';
// import QueryMongodb from '@/components/query/QueryMongodb.vue';
// import QueryRedis from '@/components/query/QueryRedis.vue';
// //// workflow
// import WorkOrderConfig from '@/components/workflow/workorderconfig/WorkOrderConfig.vue';
// import ApprovalGroup from '@/components/workflow/ApprovalGroup.vue';
// import NewWorkOrder from '@/components/workflow/NewWorkOrder.vue';
// import MyWorkOrder from '@/components/workflow/MyWorkOrder.vue';
// import WorkOrderDetail from '@/components/workflow/WorkOrderDetail.vue';
// import ToDoWorkOrder from '@/components/workflow/ToDoWorkOrder.vue';

//引入错误页面组件
import Error_404 from '@/components/views/error_page/Error_404.vue';

//配置路由   注意：名字
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
            { 
                path: '/menu', 
                component: resolve => require(['@/components/user/menus/Menus.vue'],resolve), 
                name: 'menu',
                meta: { tag: '菜单', title: ['用户权限','菜单']},
            },
            { 
                path: '/role', 
                component: resolve => require(['@/components/user/role/Role.vue'],resolve), 
                name: 'role',
                meta: { tag: '角色', title: ['用户权限','角色']},
            },
            { 
                path: '/user', 
                component: resolve => require(['@/components/user/user/User.vue'],resolve), 
                name: 'user',
                meta: { tag: '用户', title: ['用户权限','用户']},
            },
            { 
                path: '/usergroup', 
                component: resolve => require(['@/components/user/usergroup/UserGroup.vue'],resolve), 
                name: 'usergroup',
                meta: { tag: '用户组', title: ['用户权限','用户组']},
            },
            {
                path: '/mailconfig', 
                component: resolve => require(['@/components/conf/MailConfig.vue'],resolve), 
                name: 'mailconfig',
                meta: { tag: '邮箱',title: ['全局配置','邮箱']},
            },
            {
                path: '/dumpwhitelist', 
                component: resolve => require(['@/components/conf/DumpWhiteList.vue'],resolve), 
                name: 'dumpwhitelist',
                meta: { tag: '导出白名单',title: ['全局配置','导出白名单']},
            },
            {
                path: '/querylimit', 
                component: resolve => require(['@/components/conf/QueryLimit.vue'],resolve), 
                name: 'querylimit',
                meta: { tag: 'QueryLimit',title: ['全局配置','QueryLimit']},
            },
            {
                path: '/mysqlinst', 
                component: resolve => require(['@/components/db/mysql/MysqlInst.vue'],resolve), 
                name: 'mysqlinst',
                meta: { tag: 'MySQL实例',title: ['MySQL管理','MySQL实例']},
            },
            {
                path: '/mysqlmeta', 
                component: resolve => require(['@/components/db/mysql/MysqlMeta.vue'],resolve), 
                name: 'mysqlmeta',
                meta: { tag: 'MySQL元数据',title: ['Query','MySQL元数据']},
            },
            {
                path: '/mysqlstatus', 
                component: resolve => require(['@/components/db/mysql/MysqlStatus.vue'],resolve), 
                name: 'mysqlstatus',
                meta: { tag: 'MySQL实例状态',title: ['MySQL管理','MySQL实例状态']},
            },
            {
                path: '/mysqluser', 
                component: resolve => require(['@/components/db/mysql/MysqlUser.vue'],resolve), 
                name: 'mysqluser',
                meta: { tag: 'MySQL用户',title: ['MySQL管理','MySQL用户']},
            },
            {
                path: '/useraccessmysql', 
                component: resolve => require(['@/components/db/mysql/UserAccessMysql.vue'],resolve), 
                name: 'useraccessmysql',
                meta: { tag: 'MySQL权限',title: ['数据库权限','MySQL权限']},
            },
            {
                path: '/useraccessmongodb', 
                component: resolve => require(['@/components/db/mongodb/UserAccessMongodb.vue'],resolve), 
                name: 'useraccessmongodb',
                meta: { tag: 'MongoDB权限',title: ['数据库权限','MongoDB权限']},
            },
            {
                path: '/useraccessredis', 
                component: resolve => require(['@/components/db/redis/UserAccessRedis.vue'],resolve), 
                name: 'useraccessredis',
                meta: { tag: 'Redis权限',title: ['数据库权限','Redis权限']},
            },
            {
                path: '/querysql', 
                component: resolve => require(['@/components/query/QuerySql.vue'],resolve), 
                name: 'querysql',
                meta: { tag: 'QuerySql',title: ['Query','QuerySql']},
            },
            {
                path: '/querymongodb', 
                component: resolve => require(['@/components/query/QueryMongodb.vue'],resolve), 
                name: 'querymongodb',
                meta: { tag: 'QueryMongodb',title: ['Query','QueryMongodb']},
            },
            {
                path: '/queryredis', 
                component: resolve => require(['@/components/query/QueryRedis.vue'],resolve), 
                name: 'queryredis',
                meta: { tag: 'QueryRedis',title: ['Query','QueryRedis']},
            },
            {
                path: '/mongodbinst', 
                component: resolve => require(['@/components/db/mongodb/MongodbInst.vue'],resolve),  
                name: 'mongodbinst',
                meta: { tag: 'MongoDB实例',title: ['MongoDB管理','MongoDB实例']},
            },
            {
                path: '/redisinst', 
                component: resolve => require(['@/components/db/redis/RedisInst.vue'],resolve),  
                name: 'redisinst',
                meta: { tag: 'Redis实例',title: ['Redis管理','Redis实例']},
            },
            {
                path: '/workorderconfig', 
                component: resolve => require(['@/components/workflow/workorderconfig/WorkOrderConfig.vue'],resolve),  
                name: 'workorderconfig',
                meta: { tag: '工单配置',title: ['工单系统','工单配置']},
            },
            {
                path: '/approvalgroup', 
                component: resolve => require(['@/components/workflow/ApprovalGroup.vue'],resolve), 
                name: 'approvalgroup',
                meta: { tag: '审批组',title: ['工单系统','审批组']},
            },
            {
                path: '/newworkorder', 
                component: resolve => require(['@/components/workflow/NewWorkOrder.vue'],resolve), 
                name: 'newworkorder',
                meta: { tag: '新建工单',title: ['工单系统','新建工单']},
            },
            {
                path: '/myworkorder', 
                component: resolve => require(['@/components/workflow/MyWorkOrder.vue'],resolve), 
                name: 'myworkorder',
                meta: { tag: '我创建的',title: ['工单系统','我创建的']},
            },
            {
                path: '/todoworkorder', 
                component: resolve => require(['@/components/workflow/ToDoWorkOrder.vue'],resolve),  
                name: 'todoworkorder',
                meta: { tag: '我待办的',title: ['工单系统','我待办的']},
            },
            {
                path: '/workorderdetail/:workorderno', 
                component: resolve => require(['@/components/workflow/WorkOrderDetail.vue'],resolve), 
                name: 'workorderdetail',
                meta: { tag: '工单明细',title: ['工单系统','工单明细']},
            },
            // sqlorder
            {
                path: '/sqlordertype', 
                component: resolve => require(['@/components/sqlorder/SqlOrderType.vue'],resolve), 
                name: 'sqlordertype',
                meta: { tag: '工单类型',title: ['SQL工单','工单类型']},
            },
            {
                path: '/mysqlorder', 
                component: resolve => require(['@/components/sqlorder/MySqlOrder.vue'],resolve), 
                name: 'mysqlorder',
                meta: { tag: '我的SQL工单',title: ['SQL工单','我的SQL工单']},
            },
            {
                path: '/todosqlorder', 
                component: resolve => require(['@/components/sqlorder/ToDoSqlOrder.vue'],resolve), 
                name: 'todosqlorder',
                meta: { tag: '待办SQL工单',title: ['SQL工单','待办SQL工单']},
            },
            {
                path: '/newsqlorder', 
                component: resolve => require(['@/components/sqlorder/NewSqlOrder.vue'],resolve), 
                name: 'newsqlorder',
                meta: { tag: '新建SQL工单',title: ['SQL工单','新建SQL工单']},
            },
            {
                path: '/sqlorderdetail/:sqlorderno', 
                component: resolve => require(['@/components/sqlorder/SqlOrderDetail.vue'],resolve), 
                name: 'sqlorderdetail',
                meta: { tag: 'SQL工单明细',title: ['SQL工单','SQL工单明细']},
            },
        ]
    },

]

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
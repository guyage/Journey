/*jshint esversion: 6 */
import Vue from 'vue';
import NProgress from 'nprogress';
import 'nprogress/nprogress.css';
//配置路由
import VueRouter from 'vue-router';
Vue.use(VueRouter);

import store from '@/store/store.js';
import { getCookies, setCookies, removeCookies } from '@/utils/auth.js';

//引入功能组件
import Login from '@/components/views/Login.vue';
import Index from '@/components/views/Index.vue';
import Dashboard from '@/components/views/Dashboard.vue';
import Menus from '@/components/user/menus/Menus.vue';
import Role from '@/components/user/role/Role.vue';
import User from '@/components/user/user/User.vue';
import UserGroup from '@/components/user/usergroup/UserGroup.vue';
// conf
import MailConfig from '@/components/conf/MailConfig.vue';
import QueryLimit from '@/components/conf/QueryLimit.vue';
import DumpWhiteList from '@/components/conf/DumpWhiteList.vue';
////db
//mysql
import MysqlInst from '@/components/db/mysql/MysqlInst.vue';
import UserAccessMysql from '@/components/db/mysql/UserAccessMysql.vue';
import MysqlMeta from '@/components/db/mysql/MysqlMeta.vue';
import MysqlUser from '@/components/db/mysql/MysqlUser.vue';
import MysqlStatus from '@/components/db/mysql/MysqlStatus.vue';
//mongodb
import MongodbInst from '@/components/db/mongodb/MongodbInst.vue';
import UserAccessMongodb from '@/components/db/mongodb/UserAccessMongodb.vue';
//redis
import RedisInst from '@/components/db/redis/RedisInst.vue';
import UserAccessRedis from '@/components/db/redis/UserAccessRedis.vue';
//// query
import QuerySql from '@/components/query/QuerySql.vue';
import QueryMongodb from '@/components/query/QueryMongodb.vue';
import QueryRedis from '@/components/query/QueryRedis.vue';
//// workflow
import WorkOrderConfig from '@/components/workflow/workorderconfig/WorkOrderConfig.vue';
import ApprovalGroup from '@/components/workflow/ApprovalGroup.vue';
import NewWorkOrder from '@/components/workflow/NewWorkOrder.vue';
import MyWorkOrder from '@/components/workflow/MyWorkOrder.vue';
import WorkOrderDetail from '@/components/workflow/WorkOrderDetail.vue';
import ToDoWorkOrder from '@/components/workflow/ToDoWorkOrder.vue';

//引入错误页面组件
import Error_404 from '@/components/views/error_page/Error_404.vue';

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
    meta: {tag: '首页', title: ['首页']},
}

const DynamicRouter = [
    {
        path: '/', 
        component: Index,
        name: 'index',
        redirect: 'dashboard',
        meta: { tag: '首页', title: ['首页']},
        children: [
            { 
                path: '/dashboard', 
                component: Dashboard, 
                name: 'dashboard',
                meta: { tag: '仪表盘', title: ['仪表盘']},
            },
            { 
                path: '/menu', 
                component: Menus, 
                name: 'menu',
                meta: { tag: '菜单', title: ['用户权限','菜单']},
            },
            { 
                path: '/role', 
                component: Role, 
                name: 'role',
                meta: { tag: '角色', title: ['用户权限','角色']},
            },
            { 
                path: '/user', 
                component: User, 
                name: 'user',
                meta: { tag: '用户', title: ['用户权限','用户']},
            },
            { 
                path: '/usergroup', 
                component: UserGroup, 
                name: 'usergroup',
                meta: { tag: '用户组', title: ['用户权限','用户组']},
            },
            {
                path: '/mailconfig', 
                component: MailConfig, 
                name: 'mailconfig',
                meta: { tag: '邮箱',title: ['全局配置','邮箱']},
            },
            {
                path: '/dumpwhitelist', 
                component: DumpWhiteList, 
                name: 'dumpwhitelist',
                meta: { tag: '导出白名单',title: ['全局配置','导出白名单']},
            },
            {
                path: '/querylimit', 
                component: QueryLimit, 
                name: 'querylimit',
                meta: { tag: 'QueryLimit',title: ['全局配置','QueryLimit']},
            },
            {
                path: '/mysqlinst', 
                component: MysqlInst, 
                name: 'mysqlinst',
                meta: { tag: 'MySQL实例',title: ['MySQL管理','MySQL实例']},
            },
            {
                path: '/mysqlmeta', 
                component: MysqlMeta, 
                name: 'mysqlmeta',
                meta: { tag: 'MySQL元数据',title: ['Query','MySQL元数据']},
            },
            {
                path: '/mysqlstatus', 
                component: MysqlStatus, 
                name: 'mysqlstatus',
                meta: { tag: 'MySQL实例状态',title: ['MySQL管理','MySQL实例状态']},
            },
            {
                path: '/mysqluser', 
                component: MysqlUser, 
                name: 'mysqluser',
                meta: { tag: 'MySQL用户',title: ['MySQL管理','MySQL用户']},
            },
            {
                path: '/useraccessmysql', 
                component: UserAccessMysql, 
                name: 'useraccessmysql',
                meta: { tag: 'MySQL权限',title: ['数据库权限','MySQL权限']},
            },
            {
                path: '/useraccessmongodb', 
                component: UserAccessMongodb, 
                name: 'useraccessmongodb',
                meta: { tag: 'MongoDB权限',title: ['数据库权限','MongoDB权限']},
            },
            {
                path: '/useraccessredis', 
                component: UserAccessRedis, 
                name: 'useraccessredis',
                meta: { tag: 'Redis权限',title: ['数据库权限','Redis权限']},
            },
            {
                path: '/querysql', 
                component: QuerySql, 
                name: 'querysql',
                meta: { tag: 'QuerySql',title: ['Query','QuerySql']},
            },
            {
                path: '/querymongodb', 
                component: QueryMongodb, 
                name: 'querymongodb',
                meta: { tag: 'QueryMongodb',title: ['Query','QueryMongodb']},
            },
            {
                path: '/queryredis', 
                component: QueryRedis, 
                name: 'queryredis',
                meta: { tag: 'QueryRedis',title: ['Query','QueryRedis']},
            },
            {
                path: '/mongodbinst', 
                component: MongodbInst, 
                name: 'mongodbinst',
                meta: { tag: 'MongoDB实例',title: ['MongoDB管理','MongoDB实例']},
            },
            {
                path: '/redisinst', 
                component: RedisInst, 
                name: 'redisinst',
                meta: { tag: 'Redis实例',title: ['Redis管理','Redis实例']},
            },
            {
                path: '/workorderconfig', 
                component: WorkOrderConfig, 
                name: 'workorderconfig',
                meta: { tag: '工单配置',title: ['工单系统','工单配置']},
            },
            {
                path: '/approvalgroup', 
                component: ApprovalGroup, 
                name: 'approvalgroup',
                meta: { tag: '审批组',title: ['工单系统','审批组']},
            },
            {
                path: '/newworkorder', 
                component: NewWorkOrder, 
                name: 'newworkorder',
                meta: { tag: '新建工单',title: ['工单系统','新建工单']},
            },
            {
                path: '/myworkorder', 
                component: MyWorkOrder, 
                name: 'myworkorder',
                meta: { tag: '我创建的',title: ['工单系统','我创建的']},
            },
            {
                path: '/todoworkorder', 
                component: ToDoWorkOrder, 
                name: 'todoworkorder',
                meta: { tag: '我待办的',title: ['工单系统','我待办的']},
            },
            {
                path: '/workorderdetail/:workorderno', 
                component: WorkOrderDetail, 
                name: 'workorderdetail',
                meta: { tag: '工单明细',title: ['工单系统','工单明细']},
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
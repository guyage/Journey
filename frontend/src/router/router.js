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
import PermissionsGroup from '@/components/user/PermissionsGroup.vue';
import MailConfig from '@/components/conf/MailConfig.vue';
import QueryLimit from '@/components/conf/QueryLimit.vue';
import DumpWhiteList from '@/components/conf/DumpWhiteList.vue';
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
//QUery
import QuerySql from '@/components/query/QuerySql.vue';
import QueryMongodb from '@/components/query/QueryMongodb.vue';
import QueryRedis from '@/components/query/QueryRedis.vue';
//workflow
import MyWorkOrder from '@/components/workflow/MyWorkOrder.vue';
import NewWorkOrder from '@/components/workflow/NewWorkOrder.vue';
import ToDoWorkOrder from '@/components/workflow/ToDoWorkOrder.vue';
import WorkOrderDetail from '@/components/workflow/WorkOrderDetail.vue';

import NProgress from 'nprogress';
import 'nprogress/nprogress.css';

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
                path: '/permissionsgroup', 
                component: PermissionsGroup, 
                name: 'permissionsgroup',
                meta: { issuper: true, tag: '权限组',title: ['用户管理','权限组']},
            },
            {
                path: '/mailconfig', 
                component: MailConfig, 
                name: 'mailconfig',
                meta: { issuper: true, tag: '邮件配置',title: ['全局配置','邮件配置']},
            },
            {
                path: '/dumpwhitelist', 
                component: DumpWhiteList, 
                name: 'dumpwhitelist',
                meta: { issuper: true, tag: '导出白名单',title: ['全局配置','导出白名单']},
            },
            {
                path: '/querylimit', 
                component: QueryLimit, 
                name: 'querylimit',
                meta: { issuper: true, tag: 'QueryLimit',title: ['全局配置','QueryLimit']},
            },
            {
                path: '/mysqlinst', 
                component: MysqlInst, 
                name: 'mysqlinst',
                meta: { issuper: true, tag: 'MySQL实例',title: ['MySQL管理','MySQL实例']},
            },
            {
                path: '/mysqlmeta', 
                component: MysqlMeta, 
                name: 'mysqlmeta',
                meta: { issuper: false, tag: 'MySQL元数据',title: ['Query','MySQL元数据']},
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
            {
                path: '/useraccessmongodb', 
                component: UserAccessMongodb, 
                name: 'useraccessmongodb',
                meta: { issuper: false, tag: 'MongoDB权限',title: ['数据库权限','MongoDB权限']},
            },
            {
                path: '/useraccessredis', 
                component: UserAccessRedis, 
                name: 'useraccessredis',
                meta: { issuper: false, tag: 'Redis权限',title: ['数据库权限','Redis权限']},
            },
            {
                path: '/querysql', 
                component: QuerySql, 
                name: 'querysql',
                meta: { issuper: false, tag: 'QuerySql',title: ['Query','QuerySql']},
            },
            {
                path: '/querymongodb', 
                component: QueryMongodb, 
                name: 'querymongodb',
                meta: { issuper: false, tag: 'QueryMongodb',title: ['Query','QueryMongodb']},
            },
            {
                path: '/queryredis', 
                component: QueryRedis, 
                name: 'queryredis',
                meta: { issuper: false, tag: 'QueryRedis',title: ['Query','QueryRedis']},
            },
            {
                path: '/mongodbinst', 
                component: MongodbInst, 
                name: 'mongodbinst',
                meta: { issuper: true, tag: 'MongoDB实例',title: ['MongoDB管理','MongoDB实例']},
            },
            {
                path: '/redisinst', 
                component: RedisInst, 
                name: 'redisinst',
                meta: { issuper: true, tag: 'Redis实例',title: ['Redis管理','Redis实例']},
            },
            //workflow
            {
                path: '/myworkorder', 
                component: MyWorkOrder, 
                name: 'myworkorder',
                meta: { issuper: false, tag: '我创建的',title: ['工单系统','我创建的']},
            },
            {
                path: '/newworkorder', 
                component: NewWorkOrder, 
                name: 'newworkorder',
                meta: { issuper: false, tag: '新建工单',title: ['工单系统','新建工单']},
            },
            {
                path: '/todoworkorder', 
                component: ToDoWorkOrder, 
                name: 'todoworkorder',
                meta: { issuper: false, tag: '我的待办',title: ['工单系统','我的待办']},
            },
            {
                path: '/workorderdetail/:workordernum', 
                component: WorkOrderDetail, 
                name: 'workorderdetail',
                meta: { issuper: false, tag: '工单明细',title: ['工单系统','工单明细']},
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
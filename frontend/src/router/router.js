/*jshint esversion: 6 */
import Vue from 'vue';

//配置路由
import VueRouter from 'vue-router';
Vue.use(VueRouter);

import { getCookies, setCookies, removeCookies } from '@/utils/auth.js'
import store from '@/store/store.js'
//引入功能组件
import Index from '@/components/views/Index.vue';
import Dashboard from '@/components/views/Dashboard.vue';
import Db from '@/components/db/Db.vue';
import DbUser from '@/components/db/DbUser.vue';
import DbMeta from '@/components/db/DbMeta.vue';
import Login from '@/components/views/Login.vue';
import User from '@/components/user/User.vue';
import QuerySql from '@/components/query/QuerySql.vue';
import QuerySql2 from '@/components/query/QuerySql2.vue';
import SQLSoar from '@/components/query/SQLSoar.vue';
import MongodbInst from '@/components/mongodb/MongodbInst.vue';
import MongodbDB from '@/components/mongodb/MongodbDB.vue';
import QueryMongodb from '@/components/query/QueryMongodb.vue';
// 调试组件
import Test from '@/components/test/Test.vue';
// 引入错误页面组件
import Error_500 from '@/components/views/error_page/Error_500.vue';
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
}
const DynamicRouter = [
    {
        path: '/', 
        component: Index,
        name: 'index',
        redirect: 'dashboard',
        meta: { roles: 'dev', title: ['首页']},
        children:[
            { 
                path: '/dashboard', 
                component: Dashboard, 
                name: 'dashboard',
                meta: { roles: 'dev', tag: '仪表盘',title: ['仪表盘']},
            },
            { 
                path: '/db', 
                component: Db, 
                name: 'db',
                meta: { roles: 'admin', tag: 'MySQL数据库管理', title: ['数据库','MySQL数据库管理']},
            },
            { 
                path: '/mongodbinst', 
                component: MongodbInst, 
                name: 'mongodbinst',
                meta: { roles: 'admin', tag: 'MongodbInst管理', title: ['数据库','MongodbInst管理']},
            },
            { 
                path: '/mongodbdb', 
                component: MongodbDB, 
                name: 'mongodbdb',
                meta: { roles: 'admin', tag: 'MongodbDB管理', title: ['数据库','MongodbDB管理']},
            },
            { 
                path: '/dbuser', 
                component: DbUser, 
                name: 'dbuser',
                meta: { roles: 'admin', tag: '数据库用户管理', title: ['数据库','数据库用户管理']},
            },
            { 
                path: '/dbmeta', 
                component: DbMeta, 
                name: 'dbmeta',
                meta: { roles: 'dev', tag: '数据库元数据', title: ['数据库','数据库元数据']},
            },
            { 
                path: '/user', 
                component: User, 
                name: 'user',
                meta: { roles: 'admin', tag: '用户管理', title: ['用户','用户管理']},
            },
            { 
                path: '/query', 
                component: QuerySql, 
                name: 'query',
                meta: { roles: 'dev', tag: 'Query', title: ['SQL','Query']},
            },
            { 
                path: '/query2', 
                component: QuerySql2, 
                name: 'query2',
                meta: { roles: 'dev', tag: 'Query2', title: ['SQL','Query2']},
            },
            { 
                path: '/querymongodb', 
                component: QueryMongodb, 
                name: 'querymongodb',
                meta: { roles: 'dev', tag: 'QueryMongodb', title: ['SQL','QueryMongodb']},
            },
            { 
                path: '/sqlsoar', 
                component: SQLSoar, 
                name: 'sqlsoar',
                meta: { roles: 'dev', tag: 'SQLSoar', title: ['SQL','SQLSoar']},
            },
            {
                path: '*',
                redirect: '/404',
                hidden: true,
                meta: { roles: 'dev', tag: '404', title: ['404']},
            }
        ]
    }
]

const error_page_500 = {
    path: '/500',
    meta: {
        title: '500-服务端错误',
        tag: '500',
    },
    name: 'error-500',
    component: Error_500
}

const error_page_404 = {
    path: '/404',
    meta: {
        title: '404-页面不存在',
        tag: '500',
    },
    name: 'error-404',
    component: Error_404
}

// 实例化VueRouter  注意：名字
const router = new VueRouter({
    routes: [login,DefaultRouter,error_page_500] // （缩写）相当于 routes: routes
})

router.beforeEach(( to, from, next) => {
    // ${//to and from are Route Object,next() must be called to resolve the hook}
    if(store.getters.token) {
        if (to.path === '/login') {
            next()
        } else {
            if(store.getters.username.length ==0 && store.getters.usergroup.length ==0) {
                var username_cookies = getCookies('username')
                var usergroup_cookies = getCookies('usergroup')
                if(username_cookies.length !=0 && usergroup_cookies.length !=0) {
                    var userinfo = {}
                    userinfo.username = username_cookies
                    userinfo.usergroup = usergroup_cookies
                    store.dispatch('SetUserInfo',userinfo)
                    var RouterMap = {}
                    var roles = usergroup_cookies
                    RouterMap.roles = roles
                    RouterMap.dynamicrouter = DynamicRouter
                    store.dispatch('GenerateRoutes',RouterMap).then(() => {
                        store.dispatch('GenerateMenus',roles).then(() => {
                            router.addRoutes(store.getters.routers) 
                        })
                        next()
                    })
                } else {
                    next( {path:'/login'} );
                }
            } else {
                if (store.getters.routers.length ==0) {
                    var RouterMap = {}
                    var roles = store.getters.usergroup
                    RouterMap.roles = roles
                    RouterMap.dynamicrouter = DynamicRouter
                    store.dispatch('GenerateRoutes',RouterMap).then(() => {
                        store.dispatch('GenerateMenus',roles).then(() => {                          
                            router.addRoutes(store.getters.routers)
                            // next()   
                        })
                        next()                       
                    })
                } else {
                    next()                 
                }
            }
        }        
    } else {
        if (to.path === '/login') {
            next();
        } else {
            next( {path:'/login'} );
        }
    }
})








//<router-view></router-view> 放在 App.vue
export default router;
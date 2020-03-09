/*jshint esversion: 6 */

const DbRouter = [
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
]

export default DbRouter;
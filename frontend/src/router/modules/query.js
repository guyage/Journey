/*jshint esversion: 6 */

const QueryRouter = [
    {
        path: '/queryconfig', 
        component: resolve => require(['@/components/query/QueryConfig.vue'],resolve), 
        name: 'queryconfig',
        meta: { tag: 'QueryConfig',title: ['Query','QueryConfig']},
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
]

export default QueryRouter;
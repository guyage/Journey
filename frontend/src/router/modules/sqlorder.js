/*jshint esversion: 6 */

const SqlOrderRouter = [
    // sqlorder
    {
        path: '/sqlordertype', 
        component: resolve => require(['@/components/workorder/sqlorder/SqlOrderType.vue'],resolve), 
        name: 'sqlordertype',
        meta: { tag: 'SQL工单类型',title: ['工单配置','SQL工单类型']},
    },
    // {
    //     path: '/mysqlorder', 
    //     component: resolve => require(['@/components/sqlorder/MySqlOrder.vue'],resolve), 
    //     name: 'mysqlorder',
    //     meta: { tag: '我的SQL工单',title: ['SQL工单','我的SQL工单']},
    // },
    // {
    //     path: '/todosqlorder', 
    //     component: resolve => require(['@/components/sqlorder/ToDoSqlOrder.vue'],resolve), 
    //     name: 'todosqlorder',
    //     meta: { tag: '待办SQL工单',title: ['SQL工单','待办SQL工单']},
    // },
    // {
    //     path: '/allsqlorder', 
    //     component: resolve => require(['@/components/sqlorder/AllSqlOrder.vue'],resolve), 
    //     name: 'allsqlorder',
    //     meta: { tag: '全部SQL工单',title: ['SQL工单','全部SQL工单']},
    // },
    // {
    //     path: '/newsqlorder', 
    //     component: resolve => require(['@/components/sqlorder/NewSqlOrder.vue'],resolve), 
    //     name: 'newsqlorder',
    //     meta: { tag: '新建SQL工单',title: ['SQL工单','新建SQL工单']},
    // },
    {
        path: '/sqlorderdetail/:sqlorderno', 
        component: resolve => require(['@/components/workorder/sqlorder/SqlOrderDetail.vue'],resolve), 
        name: 'sqlorderdetail',
        meta: { tag: 'SQL工单明细',title: ['SQL工单','SQL工单明细']},
    },
];


export default SqlOrderRouter;
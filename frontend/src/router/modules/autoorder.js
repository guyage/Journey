/*jshint esversion: 6 */

const AutoOrderRouter = [
    {
        path: '/autoorderconfig', 
        component: resolve => require(['@/components/workorder/autoorder/autoorderconfig/AutoOrderConfig.vue'],resolve),  
        name: 'autoorderconfig',
        meta: { tag: '自助工单',title: ['工单配置','自助工单']},
    },
    {
        path: '/autoorderdetail/:autoorderno', 
        component: resolve => require(['@/components/workorder/autoorder/AutoOrderDetail.vue'],resolve), 
        name: 'autoorderdetail',
        meta: { tag: '自助工单明细',title: ['工单系统','自助工单明细']},
    },
]

export default AutoOrderRouter;
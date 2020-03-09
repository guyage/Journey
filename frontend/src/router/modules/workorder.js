/*jshint esversion: 6 */

const WorkOrderRouter = [
    {
        path: '/newworkorder', 
        component: resolve => require(['@/components/workorder/NewWorkOrder.vue'],resolve), 
        name: 'newworkorder',
        meta: { tag: '新建工单',title: ['工单系统','新建工单']},
    },
    {
        path: '/allworkorder', 
        component: resolve => require(['@/components/workorder/AllWorkOrder.vue'],resolve), 
        name: 'allworkorder',
        meta: { tag: '全部工单',title: ['工单系统','全部工单']},
    },
]

export default WorkOrderRouter;
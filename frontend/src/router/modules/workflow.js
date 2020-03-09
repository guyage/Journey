/*jshint esversion: 6 */

const WorkFlowRouter = [
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
]

export default WorkFlowRouter;
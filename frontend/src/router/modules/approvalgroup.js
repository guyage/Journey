/*jshint esversion: 6 */

const ApprovalGroupRouter = [
    {
        path: '/approvalgroup', 
        component: resolve => require(['@/components/workorder/ApprovalGroup.vue'],resolve), 
        name: 'approvalgroup',
        meta: { tag: '审批组',title: ['工单系统','审批组']},
    },
]

export default ApprovalGroupRouter;
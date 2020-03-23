/*jshint esversion: 6 */

const ServiceRouter = [
    {
        path: '/paramstemplate',
        component: resolve => require(['@/components/service/ParamsTemplate.vue'],resolve),
        name: 'paramstemplate',
        meta: { tag: '参数模版',title: ['应用管理','参数模版']},
    },
    {
        path: '/service',
        component: resolve => require(['@/components/service/Service.vue'],resolve),
        name: 'service',
        meta: { tag: '服务',title: ['应用管理','服务']},
    },
    // {
    //     path: '/servicetree',
    //     component: resolve => require(['@/components/service/ServiceTree.vue'],resolve),
    //     name: 'servicetree',
    //     meta: { tag: '树',title: ['应用管理','树']},
    // },
]

export default ServiceRouter;

/*jshint esversion: 6 */

const ConfRouter = [
    // {
    //     path: '/mailconfig', 
    //     component: resolve => require(['@/components/conf/MailConfig.vue'],resolve), 
    //     name: 'mailconfig',
    //     meta: { tag: '邮箱配置',title: ['全局配置','邮箱配置']},
    // },
    {
        path: '/sysconfig', 
        component: resolve => require(['@/components/conf/SysConfig.vue'],resolve), 
        name: 'sysconfig',
        meta: { tag: '系统配置',title: ['系统管理','系统配置']},
    },
    {
        path: '/syslog', 
        component: resolve => require(['@/components/conf/SysLog.vue'],resolve), 
        name: 'syslog',
        meta: { tag: '系统日志',title: ['系统管理','系统日志']},
    },
    // {
    //     path: '/dumpwhitelist', 
    //     component: resolve => require(['@/components/conf/DumpWhiteList.vue'],resolve), 
    //     name: 'dumpwhitelist',
    //     meta: { tag: '导出白名单',title: ['全局配置','导出白名单']},
    // },
    // {
    //     path: '/querylimit', 
    //     component: resolve => require(['@/components/conf/QueryLimit.vue'],resolve), 
    //     name: 'querylimit',
    //     meta: { tag: 'QueryLimit',title: ['全局配置','QueryLimit']},
    // },
]

export default ConfRouter;
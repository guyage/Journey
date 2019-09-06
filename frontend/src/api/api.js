/*jshint esversion: 6 */
import request from '../utils/request.js';

//Login
export const Login = params => { return request.post('/login',params) };
//ldap认证登陆
export const LdapAuth = params => { return request.post('/ldapauth',params) };
//Logout
export const Logout = () => { return request.get('/logout') };

////---------------------user文件夹组件api
export const getMenus = params => {
    if (params) {
        return request.get('/menu/'+params.id+'/');
    }
    else {
        return request.get('/menu/');
    }
};
export const searchMenus = params => { return request.get('/menu/'+'?search='+params.searchcontent) };
export const addMenus = params => { return request.post('/menu/',params)};
export const editMenus = params => { return request.patch('/menu/'+params.id+'/',params)};
// role
export const getRole = params => {
    if (params) {
        return request.get('/role/'+params.id+'/');
    }
    else {
        return request.get('/role/');
    }
};
export const addRole = params => { return request.post('/role/',params)};
export const editRole = params => { return request.patch('/role/'+params.id+'/',params)};
// user
//用户
export const getUser = params => {
    if (params) {
        return request.get('/user/'+params.id+'/');
    }
    else {
        return request.get('/user/');
    }
};
export const searchUser = params => { return request.get('/user/'+'?search='+params.searchcontent) };
export const addUser = params => { return request.post('/user/',params) };
export const delUser = params => { return request.delete('/user/'+params.id+'/') };
export const editUser = params => { return request.patch('/user/'+params.id+'/',params) };

// 用户组
export const getUserGroup = params => {
    if (params) {
        return request.get('/usergroup/'+params.id+'/');
    }
    else {
        return request.get('/usergroup/');
    }
};
export const searchUserGroup = params => { return request.get('/usergroup/'+'?search='+params.searchcontent) };
export const addUserGroup = params => { return request.post('/usergroup/',params) };
export const delUserGroup = params => { return request.delete('/usergroup/'+params.id+'/') };
export const editUserGroup = params => { return request.patch('/usergroup/'+params.id+'/',params) };

////---------------------db文件下api
//mysqlinst
export const getMysqlInst = params => {
    if (params) {
        return request.get('/mysqlinst/'+params.id+'/');
    }
    else {
        return request.get('/mysqlinst/');
    }
};
export const searchMysqlInst = params => { return request.get('/mysqlinst/'+'?search='+params.searchcontent) };
export const addMysqlInst = params => { return request.post('/mysqlinst/',params) };
export const delMysqlInst = params => { return request.delete('/mysqlinst/'+params.id+'/') };
export const editMysqlInst = params => { return request.patch('/mysqlinst/'+params.id+'/',params) };

//mongodbinst
export const getMongoDBInst = params => {
    if (params) {
        return request.get('/mongodbinst/'+params.id+'/');
    }
    else {
        return request.get('/mongodbinst/');
    }
};
export const searchMongoDBInst = params => { return request.get('/mongodbinst/'+'?search='+params.searchcontent) };
export const addMongoDBInst = params => { return request.post('/mongodbinst/',params) };
export const delMongoDBInst = params => { return request.delete('/mongodbinst/'+params.id+'/') };
export const editMongoDBInst = params => { return request.patch('/mongodbinst/'+params.id+'/',params) };

//redisinst
export const getRedisInst = params => {
    if (params) {
        return request.get('/redisinst/'+params.id+'/');
    }
    else {
        return request.get('/redisinst/');
    }
};
export const searchRedisInst = params => { return request.get('/redisinst/'+'?search='+params.searchcontent) };
export const addRedisInst = params => { return request.post('/redisinst/',params) };
export const delRedisInst = params => { return request.delete('/redisinst/'+params.id+'/') };
export const editRedisInst = params => { return request.patch('/redisinst/'+params.id+'/',params) };

//// useraccess
// useraccessmysql
export const getUserAccessMysql = params =>  { return request.get('/useraccessmysql/',params) };
export const addUserAccessMysql = params => { return request.post('/useraccessmysql/',params) };
export const editUserAccessMysql = params => { return request.patch('/useraccessmysql/'+params.id+'/',params) };
export const delUserAccessMysql = params => { return request.delete('/useraccessmysql/'+params.id+'/') };
export const searchUserAccessMysql = params => { return request.get('/useraccessmysql/'+'?search='+params.searchcontent) };
// useraccessmongodb
export const getUserAccessMongoDB = params =>  { return request.get('/useraccessmongodb/',params) };
export const addUserAccessMongoDB = params => { return request.post('/useraccessmongodb/',params) };
export const editUserAccessMongoDB = params => { return request.patch('/useraccessmongodb/'+params.id+'/',params) };
export const delUserAccessMongoDB = params => { return request.delete('/useraccessmongodb/'+params.id+'/') };
export const searchUserAccessMongoDB = params => { return request.get('/useraccessmongodb/'+'?search='+params.searchcontent) };
// useraccessredis
export const getUserAccessRedis = params =>  { return request.get('/useraccessredis/',params) };
export const addUserAccessRedis = params => { return request.post('/useraccessredis/',params) };
export const editUserAccessRedis = params => { return request.patch('/useraccessredis/'+params.id+'/',params) };
export const delUserAccessRedis = params => { return request.delete('/useraccessredis/'+params.id+'/') };
export const searchUserAccessRedis = params => { return request.get('/useraccessredis/'+'?search='+params.searchcontent) };

//get user access db
export const getUserAccessDb = params =>  { return request.post('/useraccessdb/',params); }
////mysqlmanager
export const getMysqlMeta = params => { return request.post('/mysqlmeta/',params); };



////mysqluser
export const execMysqlUser = params =>  { return request.post('/mysqluser/',params); };
////mysqlstatus
export const getMysqlStatus = params =>  { return request.post('/mysqlstatus/',params); };
////---------------------query文件下api
//querysql
export const execQuerySql = params =>  { return request.post('/querysql/',params); };
//querymongodb
export const execQueryMongodb = params =>  { return request.post('/querymongodb/',params); };
//queryredis
export const execQueryRedis = params =>  { return request.post('/queryredis/',params); };

////---------------------conf文件下api
// 邮件配置
export const getMailConfig = () => { return request.get('/mailconfig/')};
export const setMailConfig = params => {
    if ('id' in params) {
        return request.patch('/mailconfig/'+params.id+'/',params); 
    }
    else {
        return request.post('/mailconfig/',params);
    }
};
//测试邮件功能
export const execMailTest = params => { return request.post('/mailtest/',params) };
// QueryLimit配置
export const getQueryLimit = () => { return request.get('/querylimit/')};
export const setQueryLimit = params => {
    if (params.id >0) {
        return request.patch('/querylimit/'+params.id+'/',params); 
    }
    else {
        return request.post('/querylimit/',params);
    }
};
// 导出白名单
export const getDumpWhiteList = () => { return request.get('/dumpwhitelist/')};
export const delDumpWhiteList = params => { return request.delete('/dumpwhitelist/'+params.id+'/');};
export const addDumpWhiteList = params => { return request.post('/dumpwhitelist/',params);};
export const editDumpWhiteList = params => { return request.patch('/dumpwhitelist/'+params.id+'/',params);};
export const searchDumpWhiteList = params => { return request.get('/dumpwhitelist/'+'?search='+params.searchcontent);};

//// workflow
// workordertype
export const getWorkOrderType = params => {
    if (params) {
        return request.get('/workordertype/'+params.id+'/');
    }
    else {
        return request.get('/workordertype/');
    }
};
export const addWorkOrderType = params => { return request.post('/workordertype/',params);};
export const editWorkOrderType = params => { return request.patch('/workordertype/'+params.id+'/',params);};
export const delWorkOrderType = params => { return request.delete('/workordertype/'+params.id+'/');};
//approvalgroup
export const getApprovalGroup = params => {
    if (params) {
        return request.get('/approvalgroup/'+params.id+'/');
    }
    else {
        return request.get('/approvalgroup/');
    }
};
export const addApprovalGroup = params => { return request.post('/approvalgroup/',params);};
export const editApprovalGroup = params => { return request.patch('/approvalgroup/'+params.id+'/',params);};
// workorderstep
export const getWorkOrderStep = params => {
    if (params) {
        return request.get('/workorderstep/'+params.id+'/');
    }
    else {
        return request.get('/workorderstep/');
    }
};
export const addWorkOrderStep = params => { return request.post('/workorderstep/',params);};
//workorder
export const getWorkOrder = params => {
    if (params) {
        return request.get('/workorder/'+params.id+'/');
    }
    else {
        return request.get('/workorder/');
    }
};
export const addWorkOrder = params => { return request.post('/workorder/',params); };
export const editWorkOrder = params => { return request.patch('/workorder/'+params.id+'/',params);};
//workorderdetail
export const getWorkOrderDetail = params => { return request.post('/workorderdetail/',params); };
//gitlabinfo
export const getGitLabInfo = params =>  { return request.post('/gitlabinfo/',params); };
//myworkorder
export const getMyWorkOrder = () =>  { return request.get('/myworkorder/'); };
//todoworkorder
export const getToDoWorkOrder = () =>  { return request.get('/todoworkorder/'); };

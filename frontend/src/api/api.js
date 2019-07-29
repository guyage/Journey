/*jshint esversion: 6 */
import request from '../utils/request.js';

//Login
export const Login = params => { return request.post('/login',params) };
//ldap认证登陆
export const LdapAuth = params => { return request.post('/ldapauth',params) };
//Logout
export const Logout = () => { return request.get('/logout') };

////全局配置
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
export const delDumpWhiteList = params => { return request.delete('/dumpwhitelist/'+params.id+'/')};
export const addDumpWhiteList = params => { return request.post('/dumpwhitelist/',params)};
export const editDumpWhiteList = params => { return request.patch('/dumpwhitelist/'+params.id+'/',params)};
export const searchDumpWhiteList = params => { return request.get('/dumpwhitelist/'+'?search='+params.searchcontent) };

////用户管理
//用户组
export const getUserGroupList = params => {
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
//权限组
export const getPermissionsGroupList = params => {
    if (params) {
        return request.get('/permissionsgroup/'+params.id+'/');
    }
    else {
        return request.get('/permissionsgroup/');
    }
};
export const searchPermissionsGroup = params => { return request.get('/permissionsgroup/'+'?search='+params.searchcontent); };
export const addPermissionsGroup = params => { return request.post('/permissionsgroup/',params); };
export const delPermissionsGroup = params => { return request.delete('/permissionsgroup/'+params.id+'/'); };
export const editPermissionsGroup = params => { return request.patch('/permissionsgroup/'+params.id+'/',params); };
//用户
export const getUserList = params => {
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

////db
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

////query
//querysql
export const execQuerySql = params =>  { return request.post('/querysql/',params); };
//querymongodb
export const execQueryMongodb = params =>  { return request.post('/querymongodb/',params); };
//queryredis
export const execQueryRedis = params =>  { return request.post('/queryredis/',params); };

////workflow
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
export const editWorkOrder = params => { return request.patch('/workorder/'+params.id+'/',params); };
export const searchWorkOrder = params => { return request.get('/workorder/'+'?search='+params.searchcontent); };
//workorderstep
export const getWorkOrderStep = params => { return request.post('/workorderstep/',params); };
export const ChangeWorkOrderState = params => { return request.post('/changeworkorderstate/',params); };
//ToDoWorkOrder
export const ToDoWorkOrder = params => { return request.post('/todoworkorder/',params); };
export const WorkOrderDetail = params => { return request.post('/workorderdetail/',params); };

//gitlabinfo
export const getGitLabInfo = params =>  { return request.post('/gitlabinfo/',params); };



/*jshint esversion: 6 */
import request from '../utils/request.js';

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
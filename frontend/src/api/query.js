/*jshint esversion: 6 */
import request from '../utils/request.js';

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


////---------------------query文件下api
//querysql
export const execQuerySql = params =>  { return request.post('/querysql/',params); };
//querymongodb
export const execQueryMongodb = params =>  { return request.post('/querymongodb/',params); };
//queryredis
export const execQueryRedis = params =>  { return request.post('/queryredis/',params); };
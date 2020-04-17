/*jshint esversion: 6 */
import request from '../utils/request.js';



//// sqlorder
export const getMySqlOrder = () =>  { return request.get('/mysqlorder/'); };
export const getToDoSqlOrder = () =>  { return request.get('/todosqlorder/'); };
export const getAllSqlOrder = () =>  { return request.get('/allsqlorder/'); };
export const SearchAllSqlOrder = params => { return request.post('/allsqlorder/'+params.id+'/',params);};
export const getSqlOrderType = params => {
    if (params) {
        return request.get('/sqlordertype/'+params.id+'/');
    }
    else {
        return request.get('/sqlordertype/');
    }
};
export const searchSqlOrderType = params => { return request.get('/sqlordertype/'+'?search='+params.searchcontent) };
export const addSqlOrderType = params => { return request.post('/sqlordertype/',params) };
export const delSqlOrderType = params => { return request.delete('/sqlordertype/'+params.id+'/') };
export const editSqlOrderType = params => { return request.patch('/sqlordertype/'+params.id+'/',params) };

export const getSqlOrderDetail = params => { return request.post('/sqlorderdetail/',params); };
export const getSqlOrder = params => {
    if (params) {
        return request.get('/sqlorder/'+params.id+'/');
    }
    else {
        return request.get('/sqlorder/');
    }
};

export const getSqlText = params => {
    if (params) {
        return request.get('/sqltext/'+params.id+'/');
    }
    else {
        return request.get('/sqltext/');
    }
};
export const editSqlFile = params => { return request.patch('/sqlfile/'+params.id+'/',params);};

export const addSqlOrder = params => { return request.post('/sqlorder/',params); };
export const editSqlOrder = params => { return request.patch('/sqlorder/'+params.id+'/',params);};


export const Inception = params =>  { return request.post('/inception/',params); };



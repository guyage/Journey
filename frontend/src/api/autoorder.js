/*jshint esversion: 6 */
import request from '../utils/request.js';

// autoordertype
export const getAutoOrderType = params => {
    if (params) {
        return request.get('/autoordertype/'+params.id+'/');
    }
    else {
        return request.get('/autoordertype/');
    }
};
export const addAutoOrderType = params => { return request.post('/autoordertype/',params);};
export const editAutoOrderType = params => { return request.patch('/autoordertype/'+params.id+'/',params);};
export const delAutoOrderType = params => { return request.delete('/autoordertype/'+params.id+'/');};

// autoorderstep
export const getAutoOrderStep = params => {
    if (params) {
        return request.get('/autoorderstep/'+params.id+'/');
    }
    else {
        return request.get('/autoorderstep/');
    }
};
export const addAutoOrderStep = params => { return request.post('/autoorderstep/',params);};
//autoorder
export const getAutoOrder = params => {
    if (params) {
        return request.get('/autoorder/'+params.id+'/');
    }
    else {
        return request.get('/autoorder/');
    }
};
export const addAutoOrder = params => { return request.post('/autoorder/',params); };
export const editAutoOrder = params => { return request.patch('/autoorder/'+params.id+'/',params);};
//autoorderdetail
export const getAutoOrderDetail = params => { return request.post('/autoorderdetail/',params); };
//gitlabinfo
export const getGitLabInfo = params =>  { return request.post('/gitlabinfo/',params); };




/*jshint esversion: 6 */
import request from '../utils/request.js';


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
export const searchApprovalGroup = params => { return request.get('/approvalgroup/'+'?search='+params.searchcontent) };
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




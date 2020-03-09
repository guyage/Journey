/*jshint esversion: 6 */
import request from '../utils/request.js';

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



export const getAllWorkOrder = () =>  { return request.get('/allworkorder/'); };
export const SearchAllWorkOrder = params => { return request.post('/allworkorder/',params);};
<template>
    <div class="workorderdetail">
        <el-row>
            <el-divider content-position="left">{{workorderno}}</el-divider>
        </el-row>
        <el-row>
            <el-col style="text-align:left;">
                <el-form size="mini" label-width="100">
                    <el-form-item label="主题:">
                        <span>{{workorderdata['title']}}</span>
                    </el-form-item>
                    <el-form-item label="状态:">
                        <el-tag size="small" type="danger" v-if="workorderdata['status'] == -1">已失败</el-tag>
                            <el-tag size="small" type="danger" v-else-if="workorderdata['status'] == 0">已终止</el-tag>
                            <el-tag size="small" v-else-if="workorderdata['status'] == 1">申批中</el-tag>
                            <el-tag size="small" type="success" v-else-if="workorderdata['status'] == 2">已同意</el-tag>
                            <el-tag size="small" type="success" v-else-if="workorderdata['status'] == 3">已完成</el-tag>
                            <el-tag size="small" type="danger" v-else="workorderdata['status'] == 4">已驳回</el-tag>
                    </el-form-item>
                    <el-form-item label="申请人:">
                        <span>{{workorderdata['creator']}}</span>
                    </el-form-item>
                    <el-form-item v-for="(val, key, index) in content" :key="index" :label="key+':'">
                        <span>{{val}}</span>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
        <el-row style="margin-top:10px;">
            <el-alert :closable="false" title="工单流程" type="info" show-icon></el-alert>
            <el-steps style="text-align: left;margin-top:10px;" :active="workorder_current_state" finish-status="success">
                <el-step v-for="(val,index) in ordertypesteps"
                v-if="val.step_name == 'start'"
                :key="index"
                title="开始" 
                :description="val.step_info">
                </el-step>
                <el-step v-for="(val,index) in ordertypesteps"
                v-if="val.step_name != 'finsh' && val.step_name != 'start'"
                :key="index" 
                :title="val.step_name" 
                :description="val.step_info?val.step_info:val.approver_group_name">
                </el-step>
                <el-step v-for="(val,index) in ordertypesteps"
                v-if="val.step_name == 'finsh'"
                :key="index" 
                title="完成" 
                :description="val.step_info?val.step_info:'系统处理 [成功] 时间'">
                </el-step>
            </el-steps>
        </el-row>
        <el-row v-if="approver_group_hasuser.indexOf(username) > -1" style="margin-top:10px;">
            <el-alert :closable="false" title="操作" type="info" show-icon></el-alert>
            <div style="margin-top:10px;">
                <el-button :loading="loading" @click="handleAction('agree')" style="float:left;" size="small" type="primary">同意</el-button>
                <el-button :loading="loading" @click="handleAction('reject')" style="float:left;" size="small" type="danger">驳回</el-button>
            </div>
        </el-row>
    </div>
</template>

<script>
import moment from 'moment';
import store from '@/store/store.js';
import { getWorkOrder,getWorkOrderType,editWorkOrder,getApprovalGroup } from '@/api/api.js';
export default {
    // name: 'workorderdetail',
    data() {
        return {
            loading: false,
            username: '',
            workorderno: '',
            workorderid: '',
            workorderdata: {},
            content: {},
            ordertypesteps: [],
            workorderstate: [],
            workorder_current_state: 0,
            approver_group_id: '',
            approver_group_hasuser: [],
        }
    },
    methods: {
        handleAction(action) {
            this.loading = true
            let change_data = {};
            change_data.id = this.workorderid
            change_data.operator = store.getters.username
            if (action == 'agree') {
                change_data.status = 2
            }
            else if (action == 'reject') {
                change_data.status = 4
            }
            editWorkOrder(change_data).then((response) => {
                this.getWorkOrderDetail()
                this.$message.success('处理成功!');
                this.loading = false
            }).catch((error) => {
                console.log(error);
                this.$message.error('处理失败!');
                this.loading = false
            })
        },
        dateFormate(date) {
            return moment(date).format("YYYY-MM-DD HH:mm:ss");
        },
        getApproverGroupUsers(step_id) {
            this.approver_group_hasuser = []
            for (let i=0;i<this.ordertypesteps.length;i++) {
                if (this.ordertypesteps[i].step_id == step_id) {
                    if (this.ordertypesteps[i].approver_group_id) {
                        this.approver_group_id =  this.ordertypesteps[i].approver_group_id
                        getApprovalGroup({'id':this.approver_group_id}).then((response) => {
                            this.approver_group_hasuser = response.data.hasusername
                        })
                    }
                }
            }
        },
        getWorkOrderDetail() {
            this.workorderno = this.$route.params.workorderno
            this.workorderid = this.workorderno.split('-')[1]
            getWorkOrder({'id':this.workorderid}).then((response) => {
                if (response.data.ordertype) {
                    this.workorderdata = response.data
                    this.workorderstate = response.data.workorderstate
                    this.content = JSON.parse(response.data.content)
                    this.getWorkOrderTypeInfo(response.data.ordertype)
                }
            })
        },
        getWorkOrderTypeInfo(ordertype_id) {
            this.ordertypesteps = []
            getWorkOrderType({'id':ordertype_id}).then((response) => {
                for (let i=0;i<response.data.hasstep.length;i++) {
                    this.ordertypesteps.push(response.data.hasstep[i])
                }
                this.getWorkOrderState(this.workorderstate,this.ordertypesteps)
            }).catch((error) => {
                console.log(error);         
            })
        },
        getWorkOrderState(workorderstate,ordertypesteps) {
            this.workorder_current_state = workorderstate.length
            this.getApproverGroupUsers(this.workorder_current_state+1)
            for (let i=0;i<workorderstate.length;i++) {
                if (workorderstate[i].action == 'start') {
                    ordertypesteps[i].step_info = workorderstate[i].operator + ' [提交] ' + this.dateFormate(workorderstate[i].update_time)
                }
                else if (workorderstate[i].action == 'finsh') {
                    ordertypesteps[i].step_info = workorderstate[i].operator + ' [完成] ' + this.dateFormate(workorderstate[i].update_time)
                }
                else {
                    ordertypesteps[i].step_info = workorderstate[i].operator + ' [同意] ' + this.dateFormate(workorderstate[i].update_time)
                }
                
            }
        },
    },
    mounted() {
        this.getWorkOrderDetail()
        this.username = store.getters.username
    },
}
</script>

<style>
.workorderdetail .el-table__expanded-cell[class*=cell]{
    padding: 5px 62px;
}
.workorderdetail label {
    /* width: 100px; */
    font-size: 12px;
    color: #99a9bf;
}
.workorderdetail .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
}
.workorderdetail .el-form-item__content{
    text-align: left;
}
</style>
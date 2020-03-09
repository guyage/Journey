<template>
    <div class="autoorderdetail">
        <el-row>
            <el-divider content-position="left">{{autoorderno}}</el-divider>
        </el-row>
        <el-row>
            <el-col style="text-align:left;">
                <el-form size="mini" label-width="100">
                    <el-form-item label="主题:">
                        <span>{{autoorderdata['title']}}</span>
                    </el-form-item>
                    <el-form-item label="状态:">
                        <el-tag size="small"  v-if="autoorderdata['status'] == 0">待审批</el-tag>
                        <el-tag size="small" type="warning" v-else-if="autoorderdata['status'] == 1">已驳回</el-tag>
                        <el-tag size="small" type="success" v-else-if="autoorderdata['status'] == 2">已完成</el-tag>
                        <el-tag size="small" style="color:#fa8c16;background:#fff7e6;border-color:#ffd591;" type="warning" v-else-if="autoorderdata['status'] == 3">DBA-CHECK中</el-tag>
                        <el-tag size="small" style="color:#13c2c2;background:#e6fffb;border-color:#87e8de;" type="warning" v-else-if="autoorderdata['status'] == 4">待执行</el-tag>
                        <el-tag size="small" style="color:#faad14;background:#fffbe6;border-color:#ffe58f;" type="warning" v-else-if="autoorderdata['status'] == 5">已执行，待验证</el-tag>
                        <el-tag size="small" style="color:#722ed1;background:#f9f0ff;border-color:#d3adf7;" type="danger" v-else-if="autoorderdata['status'] == 6">已验证</el-tag>
                        <el-tag size="small" type="info" v-else-if="autoorderdata['status'] == 7">已取消</el-tag>
                        <el-tag size="small" type="danger" v-else="autoorderdata['status'] == -1">已失败</el-tag>
                    </el-form-item>
                    <el-form-item label="申请人:">
                        <span>{{autoorderdata['creator']}}</span>
                    </el-form-item>
                    <el-form-item v-for="(val, key, index) in content" :key="index" :label="key+':'">
                        <span>{{val}}</span>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
        <el-row style="margin-top:10px;">
            <el-alert :closable="false" title="工单流程" type="info" show-icon></el-alert>
            <el-steps style="text-align: left;margin-top:10px;" :active="autoorder_current_state" finish-status="success">
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
import { getApprovalGroup } from '@/api/workorder.js';
import { getAutoOrder,getAutoOrderType,editAutoOrder } from '@/api/autoorder.js';
export default {
    // name: 'autoorderdetail',
    data() {
        return {
            loading: false,
            username: '',
            autoorderno: '',
            autoorderid: '',
            autoorderdata: {},
            content: {},
            ordertypesteps: [],
            autoorderstate: [],
            autoorder_current_state: 0,
            approver_group_id: '',
            approver_group_hasuser: [],
        }
    },
    methods: {
        handleAction(action) {
            this.loading = true
            let change_data = {};
            change_data.id = this.autoorderid
            change_data.operator = store.getters.username
            if (action == 'agree') {
                change_data.status = 0
            }
            else if (action == 'reject') {
                change_data.status = 1
            }
            editAutoOrder(change_data).then((response) => {
                this.getAutoOrderDetail()
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
        getAutoOrderDetail() {
            this.autoorderno = this.$route.params.autoorderno
            this.autoorderid = this.autoorderno.split('-')[1]
            getAutoOrder({'id':this.autoorderid}).then((response) => {
                if (response.data.ordertype) {
                    this.autoorderdata = response.data
                    this.autoorderstate = response.data.autoorderstate
                    this.content = JSON.parse(response.data.content)
                    this.getAutoOrderTypeInfo(response.data.ordertype)
                }
            })
        },
        getAutoOrderTypeInfo(ordertype_id) {
            this.ordertypesteps = []
            getAutoOrderType({'id':ordertype_id}).then((response) => {
                for (let i=0;i<response.data.hasstep.length;i++) {
                    this.ordertypesteps.push(response.data.hasstep[i])
                }
                this.getAutoOrderState(this.autoorderstate,this.ordertypesteps)
            }).catch((error) => {
                console.log(error);         
            })
        },
        getAutoOrderState(autoorderstate,ordertypesteps) {
            this.autoorder_current_state = autoorderstate.length
            this.getApproverGroupUsers(this.autoorder_current_state+1)
            for (let i=0;i<autoorderstate.length;i++) {
                if (autoorderstate[i].action == 'start') {
                    ordertypesteps[i].step_info = autoorderstate[i].operator + ' [提交] ' + this.dateFormate(autoorderstate[i].update_time)
                }
                else if (autoorderstate[i].action == 'finsh') {
                    ordertypesteps[i].step_info = autoorderstate[i].operator + ' [完成] ' + this.dateFormate(autoorderstate[i].update_time)
                }
                else {
                    ordertypesteps[i].step_info = autoorderstate[i].operator + ' [同意] ' + this.dateFormate(autoorderstate[i].update_time)
                }
                
            }
        },
    },
    mounted() {
        this.getAutoOrderDetail()
        this.username = store.getters.username
    },
}
</script>

<style>
.autoorderdetail .el-table__expanded-cell[class*=cell]{
    padding: 5px 62px;
}
.autoorderdetail label {
    /* width: 100px; */
    font-size: 12px;
    color: #99a9bf;
}
.autoorderdetail .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
}
.autoorderdetail .el-form-item__content{
    text-align: left;
}
</style>
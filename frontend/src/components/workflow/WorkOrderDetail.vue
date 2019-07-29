<template>
    <div class="workorderdetail">
        <el-collapse v-model="activeNames">
            <el-collapse-item title="工单明细" name="1">
                <el-divider content-position="left">{{workordernum}}</el-divider>
                <div style="width:100%;" class="demo-table-expand">
                    <el-form label-width="100px">
                        <el-form-item style="float:left;" v-for="(val, key, index) in form_columns" v-if="key != 'status'" :key="index" :label="val+':'">
                            <span>{{workorderdata[key]}}</span>
                        </el-form-item>
                        <el-form-item style="float:left;" v-for="(val, key, index) in form_columns" v-if="key == 'status'" :key="index+20" :label="val+':'">
                            <el-tag size="small" type="danger" v-if="workorderdata[key] == -1">已失败</el-tag>
                            <el-tag size="small" type="danger" v-else-if="workorderdata[key] == 0">已终止</el-tag>
                            <el-tag size="small" v-else-if="workorderdata[key] == 1">申请中</el-tag>
                            <el-tag size="small" type="success" v-else-if="workorderdata[key] == 2">已同意</el-tag>
                            <el-tag size="small" type="success" v-else-if="workorderdata[key] == 3">已完成</el-tag>
                            <el-tag size="small" type="danger" v-else="workorderdata[key] == 4">已驳回</el-tag>
                        </el-form-item>
                        <el-form-item v-if="workorderdata['order_type'] == 'git'" style="float:left;" v-for="(val, key, index) in git_columns" :key="index+10" :label="val+':'">
                            <span v-if="key != 'git_project' && key != 'git_permission'">{{JSON.parse(workorderdata['content'])[key]}}</span>
                            <span v-else-if="key == 'git_project'">{{JSON.parse(workorderdata['content'])[key]}}</span>
                            <span v-else-if="JSON.parse(workorderdata['content'])[key] == 'None'">移除权限</span>
                            <span v-else-if="JSON.parse(workorderdata['content'])[key] == 'Developer'">读写</span>
                            <span v-else-if="JSON.parse(workorderdata['content'])[key] == 'Reporter'">只读</span>
                        </el-form-item>
                    </el-form>
                    <div style="padding: 10px 10px 10px 10px;">
                        <el-alert :closable="false" title="工单流" type="info" show-icon></el-alert>
                        <div>
                            <el-steps style="padding: 10px 10px 10px 10px;" :active="step" finish-status="success">
                            <el-step title="开始" :description="step1_description"></el-step>
                            <el-step title="审核" :description="step2_description"></el-step>
                            <el-step title="完成" :description="step3_description"></el-step>
                            </el-steps>
                        </div>
                    </div>
                    <div v-if="user_permissions.indexOf(workorderdata['operation_group']) > -1" style="padding: 10px 10px 10px 10px;">
                        <el-alert :closable="false" title="操作" type="info" show-icon></el-alert>
                        <div style="padding: 10px 10px 10px 10px;">
                            <el-button @click="handleAction('agree')" style="float:left;" size="small" type="primary">同意</el-button>
                            <el-button @click="handleAction('reject')" style="float:left;" size="small" type="danger">驳回</el-button>
                        </div>
                    </div>
                </div>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script>
import moment from 'moment';
import store from '@/store/store.js';
import { WorkOrderDetail,getWorkOrderStep,ChangeWorkOrderState } from '@/api/api.js';
export default {
    // name: 'workorderdetail',
    data() {
        return {
            loading: false,
            activeNames: ['1'],
            workordernum: '',
            form_columns: {
                title: '主题',
                order_type: '工单类型',
                status: '工单状态',
                creator: '申请人',
                // operator: '操作人',
                // create_time: '创建时间',
                // update_time: '更新时间',
            },
            user_permissions: [],
            username: '',
            git_columns: {
                git_user: 'Git账户',
                git_project: 'Git项目',
                git_permission: 'Git权限',

            },
            workorderdata: {},
            workorderid:0,
            comment: '',
            step: 1,
            step1_description: '',
            step2_description: '',
            step3_description: '',
        }
    },
    methods: {
        handleAction(action) {
            this.loading = true
            let change_data = {};
            change_data.workorderid = this.workorderid
            change_data.operator = this.username
            if (action == 'agree') {
                change_data.changetype = 'agree'
            }
            else if (action == 'reject') {
                change_data.changetype = 'reject'
            }
            ChangeWorkOrderState(change_data).then((response) => {
                this.getWorkOrderDetail()
                this.loading = false
            }).catch((error) => {
                console.log(error);
                this.loading = false
            })
        },
        getWorkOrderDetail () {
            this.workordernum = this.$route.params.workordernum
            this.workorderid = this.workordernum.split('-')[1]
            this.getWorkOrderState({'workorderid':this.workorderid})
            WorkOrderDetail({'workorderid':this.workorderid}).then((response) => {
                this.workorderdata = response.data.results
            }).catch((error) => {
                console.log(error);
            })
        },
        getWorkOrderState(workorderid) {
            getWorkOrderStep(workorderid).then((response) => {
                this.step = response.data.steps
                for (let i =0;i<this.step;i++) {
                    let dname = 'step'+(i+1)+'_description'
                    let operator = response.data.results[i].operator
                    let create_time = response.data.results[i].create_time
                    let status = response.data.results[i].step
                    if (status == 2) {
                        this.step2_description = operator + ' [同意] ' +this.dateFormate(create_time)
                    }
                    else if (status == 4) {
                        this.step2_description = operator + ' [驳回] ' +this.dateFormate(create_time)
                    }
                    else if (status == 1) {
                        this.step1_description = operator + ' [提交] ' + this.dateFormate(create_time)
                    }
                    else if (status == 3) {
                        this.step3_description = operator + ' [完成] ' + this.dateFormate(create_time)
                    }
                    else if (status == -1) {
                        this.step3_description = operator + ' [失败] ' + this.dateFormate(create_time)
                    }
                }
            }).catch((error) => {
                console.log(error);
            })
        },
        dateFormate(date) {
            return moment(date).format("YYYY-MM-DD HH:mm:ss");
        }
    },
    mounted () {
        this.getWorkOrderDetail()
        let userpermissionsgroup = store.getters.userpermissionsgroup
        this.username = store.getters.username
        if (typeof(userpermissionsgroup) == 'string') {
            this.user_permissions = userpermissionsgroup.split(',')
        }
        else {
            this.user_permissions = userpermissionsgroup
        }
    },

}
</script>

<style>
.workorderdetail .el-collapse-item__header.is-active,.workorderdetail .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
    border-bottom: 1px solid #dcdfe6;
}
.workorderdetail .el-table__expanded-cell[class*=cell]{
    padding: 5px 62px;
}
.workorderdetail .demo-table-expand {
    font-size: 0;
}
.workorderdetail .demo-table-expand label {
    /* width: 100px; */
    font-size: 12px;
    color: #99a9bf;
}
.workorderdetail .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
}
.workorderdetail .el-form-item__content{
    text-align: left;
}
.workorderdetail .el-step__head{
    text-align: left;
}
</style>

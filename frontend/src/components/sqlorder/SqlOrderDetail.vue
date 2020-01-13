<template>
    <div id="sqlorderdetail" class="sqlorderdetail">
        <el-row>
            <el-divider content-position="left">{{sqlorderno}}</el-divider>
        </el-row>
        <el-row>
            <el-tabs v-model="activeName" style="height:400px;">
                <el-tab-pane label="基本信息" name="1">
                    <el-col style="text-align:left;">
                        <el-form size="mini" label-width="100">
                            <el-form-item label="主题:"> 
                                <span>{{sqlorderdetail['title']}}</span>
                            </el-form-item>
                            <el-form-item label="工单类型:" v-if="sqlorderdetail['ordertypename']"> 
                                <span>{{sqlorderdetail['ordertypename']}}</span>
                            </el-form-item>
                            <el-form-item label="状态:"> 
                                <el-tag size="small"  v-if="sqlorderdetail['status'] == 0">待审批</el-tag>
                                <el-tag size="small" type="warning" v-else-if="sqlorderdetail['status'] == 1">已驳回</el-tag>
                                <el-tag size="small" type="success" v-else-if="sqlorderdetail['status'] == 2">已完成</el-tag>
                                <el-tag size="small" style="color:#fa8c16;background:#fff7e6;border-color:#ffd591;" type="warning" v-else-if="sqlorderdetail['status'] == 3">DBA-CHECK中</el-tag>
                                <el-tag size="small" style="color:#13c2c2;background:#e6fffb;border-color:#87e8de;" type="warning" v-else-if="sqlorderdetail['status'] == 4">待执行</el-tag>
                                <el-tag size="small" style="color:#faad14;background:#fffbe6;border-color:#ffe58f;" type="warning" v-else-if="sqlorderdetail['status'] == 5">已执行，待验证</el-tag>
                                <el-tag size="small" style="color:#722ed1;background:#f9f0ff;border-color:#d3adf7;" type="danger" v-else-if="sqlorderdetail['status'] == 6">已验证</el-tag>
                                <el-tag size="small" type="info" v-else-if="sqlorderdetail['status'] == 7">已取消</el-tag>
                                <el-tag size="small" type="danger" v-else="sqlorderdetail['status'] == -1">已失败</el-tag>
                            </el-form-item>
                            <el-form-item label="创建人:"> 
                                <span>{{sqlorderdetail['creator']}}</span>
                            </el-form-item>
                            <el-form-item v-if="sqlorderdetail['approvergroup_name']" label="经办人:"> 
                                <span>{{sqlorderdetail['approvergroup_name']}}</span>
                            </el-form-item>
                            <el-form-item label="创建时间:">
                                <span>{{sqlorderdetail['create_time'] | dateFormate}}</span>
                            </el-form-item>
                        </el-form>
                    </el-col>
                </el-tab-pane>
                <el-tab-pane v-if="sql_data.length > 0" label="SQL文本" name="2">
                    <el-table v-if="sql_data.length > 0" size="mini" style="width: 100%" height="300" border :data="sql_data.slice((currentPage-1)*pagesize,currentPage*pagesize)">
                        <el-table-column width="200" align="center" label="实例" prop="inst"></el-table-column>
                        <el-table-column width="200" align="center" label="数据库" prop="dbname"></el-table-column>
                        <el-table-column align="left" label="SQL" prop="sql"></el-table-column>
                        <el-table-column width="80" align="center" label="状态" prop="sql">
                            <template slot-scope="scope">
                                <el-tag size="small" type="success" v-if="scope.row.sqlstatus == 1">已执行</el-tag>
                                <el-tag size="small" v-else-if="scope.row.sqlstatus == 0">待执行</el-tag>
                                <el-tag size="small" type="danger" v-else-if="scope.row.sqlstatus == -1">已失败</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column width="200" align="center" label="执行信息">
                            <template slot-scope="scope">
                                <el-button v-if="scope.row.sqlstatus != 0"  @click="showExecInfo(scope.row)" size="mini" type="primary">Info</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    <el-pagination
                    v-if="sql_data.length > 0"
                    mini
                    background
                    layout="total, sizes,prev, pager, next, jumper"
                    :total="sql_data.length"
                    :page-sizes="[10, 20, 30]"
                    :page-size="pagesize"
                    @current-change="handleCurrentChange"
                    @size-change="handleSizeChange">
                    </el-pagination>
                </el-tab-pane>
                <el-tab-pane v-if="sql_file.length > 0" label="SQL附件" name="4">
                    <el-table v-if="sql_file.length > 0" size="mini" style="width: 100%" height="300" border :data="sql_file">
                        <el-table-column align="center" label="文件" prop="sqlfileurl">
                            <template slot-scope="scope">
                                <el-link :href="scope.row.sqlfileurl" type="info">{{scope.row.sqlfileurl|cutStr}}<i class="el-icon-paperclip el-icon--right"></i></el-link>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>
                <el-tab-pane label="备注" name="5"></el-tab-pane>
            </el-tabs>
        </el-row>
        <el-row>
            <el-alert :closable="false" title="流程" type="info" show-icon></el-alert>
            <el-steps style="text-align: left;margin-top:10px;"  finish-status="success">
                <el-step v-if="ordertype_info['create']" :title="ordertype_info['create']" :description="sqlorder_state['create']" :status="sqlorder_state_status['create']"></el-step>
                <el-step v-if="ordertype_info['first_approver']" :title="ordertype_info['first_approver']" :description="sqlorder_state['first_approver']" :status="sqlorder_state_status['first_approver']"></el-step>
                <el-step v-if="ordertype_info['second_approver']" :title="ordertype_info['second_approver']" :description="sqlorder_state['second_approver']" :status="sqlorder_state_status['second_approver']"></el-step>
                <el-step v-if="ordertype_info['dba_approver']" :title="ordertype_info['dba_approver']" :description="sqlorder_state['dba_approver']" :status="sqlorder_state_status['dba_approver']"></el-step>
                <el-step v-if="ordertype_info['exec']" :title="ordertype_info['exec']" :description="sqlorder_state['exec']" :status="sqlorder_state_status['exec']"></el-step>
                <el-step v-if="ordertype_info['check']" :title="ordertype_info['check']" :description="sqlorder_state['check']" :status="sqlorder_state_status['check']"></el-step>
                <el-step v-if="ordertype_info['done']" :title="ordertype_info['done']" :description="sqlorder_state['done']" :status="sqlorder_state_status['done']"></el-step>
            </el-steps>  
        </el-row>
        <el-row v-if="approver_group_hasuser.indexOf(username) > -1" style="margin-top:10px;">
            <el-alert :closable="false" title="操作" type="info" show-icon></el-alert>
                <div v-if="sqlorderdetail.status == 0" style="margin-top:10px;">
                    <el-button @click="handleAction('agree')" style="float:left;" size="small" type="primary">同意</el-button>
                    <el-button @click="handleAction('reject')" style="float:left;" size="small" type="danger">驳回</el-button>
                </div>
                <div v-if="sqlorderdetail.status == 3" style="margin-top:10px;">
                    <el-button @click="handleAction('agree')" style="float:left;" size="small" type="primary">CHECK通过</el-button>
                    <el-button @click="handleAction('reject')" style="float:left;" size="small" type="danger">CHECK不通过</el-button>
                </div>
                <div v-if="sqlorderdetail.status == 4" style="margin-top:10px;">
                    <div v-if="sql_data.length > 0">
                        <el-button @click="handleExec('agree','auto')" style="float:left;" size="small" type="primary">自动执行</el-button>
                        <div style="float:right;">
                            <el-button @click="handleExec('agree','manual')" style="float:left;" size="small" type="primary">手动执行</el-button>
                            <el-button @click="handleExec('reject')" style="float:left;" size="small" type="danger">取消执行</el-button>
                        </div>
                    </div>
                    <div v-if="sql_file.length > 0">
                        <el-button @click="handleExec('agree','manual')" style="float:left;" size="small" type="primary">手动执行</el-button>
                        <el-button @click="handleExec('reject')" style="float:right;" size="small" type="danger">取消执行</el-button>
                    </div>
                </div>
        </el-row>
        <el-row v-if="sqlorderdetail['creator'] == username && sqlorderdetail.status == 5" style="margin-top:10px;">
            <el-alert :closable="false" title="操作" type="info" show-icon></el-alert>
                <div v-if="sqlorderdetail.status == 5" style="margin-top:10px;">
                    <el-button @click="handleCheck('agree','success')" style="float:left;" size="small" type="primary">验证通过</el-button>
                    <el-button @click="handleCheck('agree','error')" style="float:left;" size="small" type="danger">验证失败</el-button>
                </div>
        </el-row>
        <el-row>
            <el-dialog
            title="执行结果"
            :visible.sync="dialogVisible"
            width="80%"
            :before-close="handleClose">
            <div>
                <!-- <el-alert v-if="checkinfo_data.length > 0" title="审核失败，请修改后重新审核!" type="error" effect="dark" :closable="false"></el-alert>
                <el-alert v-if="checkinfo_data.length == 0" title="审核通过!" type="success" effect="dark" :closable="false"></el-alert> -->
                <el-table size="mini" style="width: 100%" height="450" border :data="exec_info.slice((infocurrentPage-1)*infopagesize,infocurrentPage*infopagesize)">
                    <el-table-column width="100" align="center" label="步骤" prop="stage"></el-table-column>
                    <!-- <el-table-column width="80" align="center" label="步骤级别" prop="errlevel"></el-table-column> -->
                    <el-table-column width="200" align="center" label="步骤状态" prop="stagestatus"></el-table-column>
                    <el-table-column align="left" label="步骤信息" prop="errormessage"></el-table-column>
                    <el-table-column align="left" label="SQL" prop="SQL"></el-table-column>
                    <el-table-column width="100" align="center" label="影响行数" prop="Affected_rows"></el-table-column>
                </el-table>
                <el-pagination
                v-if="exec_info.length > 0"
                mini
                background
                layout="total, sizes,prev, pager, next, jumper"
                :infototal="exec_info.length"
                :page-sizes="[10, 20, 30]"
                :page-size="infopagesize"
                @current-change="handleInfoCurrentChange"
                @size-change="handleInfoSizeChange">
                </el-pagination>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button size="mini" @click="dialogVisible = false" type="primary">确定</el-button>
            </span>
            </el-dialog>
        </el-row>
    </div>
</template>

<script>
import moment from 'moment';
import store from '@/store/store.js';
import {getSqlOrderDetail,searchApprovalGroup,editSqlOrder,getSqlText} from '@/api/api.js';
export default {
    // name: sqlorderdetail,
    data () {
        return {
            username: '',
            sqlorderno: '',
            activeName: '1',
            sqlorderdetail : {},
            sql_data: [],
            sql_file: [],
            sqlorderid: '',
            // 分页参数
            total: 0,
            currentPage: 1,
            pagesize: 10,
            // info分页参数
            infototal: 0,
            infocurrentPage: 1,
            infopagesize: 10,
            ordertype_info: {},
            sqlorder_state: {},
            sqlorder_state_status: {},
            approver_group_hasuser: [],
            // 执行结果相关参数
            dialogVisible: false,
            exec_info: []
        }
    },
    filters: {
        dateFormate(date) {
            return moment(date).format("YYYY-MM-DD HH:mm:ss");
        },
        cutStr(str) {
            let index = str.lastIndexOf("\/");
            return str.substring(index + 1, str.length);
        }
    },
    methods: {
        dateFormate(date) {
            return moment(date).format("YYYY-MM-DD HH:mm:ss");
        },
        showExecInfo(row) {
            console.log(row);
            getSqlText({'id':row.id}).then((response) => {

                console.log(response.data.execinfo);
                this.exec_info = response.data.execinfo
                // console.log(this.exec_info);
                
                this.dialogVisible = true;
            })
        },
        handleClose(done) {
            this.$confirm('确认关闭？')
            .then(_ => {
                done();
            })
            .catch(_ => {});
        },
        handleExec(action,exectype) {
            let prompt = ''
            if (action == 'agree') {
                prompt = '执行'
            } else {
                prompt = '取消执行'
            }
            let change_data = {};
            change_data.id = this.sqlorderid
            change_data.operator = store.getters.username
            change_data.action = action
            change_data.exectype = exectype
            this.$confirm('确认'+prompt+'?')
            .then(_ => {
                editSqlOrder(change_data).then((response) => {
                    this.getSqlOrderDetail()
                    this.$message.success('处理成功!');
                    this.loading = false
                }).catch((error) => {
                    console.log(error);
                    this.$message.error('处理失败!');
                    this.loading = false
                })
            })
            .catch(_ => {});
            
        },
        handleCheck(action,checktype) {
            let prompt = ''
            if (checktype == 'success') {
                prompt = '验证成功'
            } else {
                prompt = '验证失败'
            }
            let change_data = {};
            change_data.id = this.sqlorderid
            change_data.operator = store.getters.username
            change_data.action = action
            change_data.checktype = checktype
            this.$confirm('确认'+prompt+'?')
            .then(_ => {
                editSqlOrder(change_data).then((response) => {
                    this.getSqlOrderDetail()
                    this.$message.success('处理成功!');
                    this.loading = false
                }).catch((error) => {
                    console.log(error);
                    this.$message.error('处理失败!');
                    this.loading = false
                })
            })
            .catch(_ => {});
            
        },
        handleAction(action) {
            let prompt = ''
            if (action == 'agree') {
                prompt = '通过'
            } else {
                prompt = '驳回'
            }
            let change_data = {};
            change_data.id = this.sqlorderid
            change_data.operator = store.getters.username
            change_data.action = action
            this.$confirm('确认'+prompt+'?')
            .then(_ => {
                editSqlOrder(change_data).then((response) => {
                    this.getSqlOrderDetail()
                    this.$message.success('处理成功!');
                    this.loading = false
                }).catch((error) => {
                    console.log(error);
                    this.$message.error('处理失败!');
                    this.loading = false
                })
            })
            .catch(_ => {});
        },
        getApproverGroupUsers(states,ortertype_info) {
            this.approver_group_hasuser = []
            let current_action = ''
            let next_action = ''
            console.log(states[states.length-1],ortertype_info);
            current_action = states[states.length-1].action
            if ( current_action == 'create' ) {
                next_action = 'first_approver'
            }
            else if (current_action == 'first_approver') {
                if (ortertype_info.second_approver) {
                    next_action = 'second_approver'
                } else {
                    next_action = 'dba_approver'
                }
            }
            else if (current_action == 'second_approver') {
                next_action = 'dba_approver'
            }
            else if (current_action == 'dba_approver') {
                next_action = 'dba_approver'
            }
            else {
                next_action = ''
            }
            if (next_action) {
                searchApprovalGroup({'searchcontent':ortertype_info[next_action]}).then((response) => {
                    this.approver_group_hasuser = response.data[0].hasusername                   
                })
            }
            
        },
        getSqlOrderDetail() {
            this.sqlorderno = this.$route.params.sqlorderno
            this.sqlorderid = this.sqlorderno.split('-')[1]
            getSqlOrderDetail({'sqlorderid':this.sqlorderid}).then((response) => {
                console.log(response.data);
                
                this.sqlorderdetail = response.data
                this.sql_data = this.sqlorderdetail['sql_data']
                this.ordertype_info = this.sqlorderdetail['ordertype_info']
                this.sql_file = this.sqlorderdetail['sql_file']
                // this.sqlorder_state = this.sqlorderdetail['sqlorderstate']
                this.initSqlOrderState(this.sqlorderdetail['sqlorderstate'])
                this.getApproverGroupUsers(this.sqlorderdetail['sqlorderstate'],this.ordertype_info)
            }).catch((error) => {
                console.log(error);
            })
        },
        initSqlOrderState(states) {
            for (let i=0;i<states.length;i++) {
                if (states[i].action == 'create') {
                    console.log(states[i]);
                    this.sqlorder_state.create =  states[i].operator + ' [创建] ' + this.dateFormate(states[i].create_time)
                    this.sqlorder_state_status.create = states[i].status
                }
                else if (states[i].action == 'first_approver') {
                    this.sqlorder_state_status.first_approver = states[i].status
                    if (states[i].status == 'success') {
                        this.sqlorder_state.first_approver =  states[i].operator + ' [同意] ' + this.dateFormate(states[i].create_time)
                    }
                    else {
                        this.sqlorder_state.first_approver =  states[i].operator + ' [驳回] ' + this.dateFormate(states[i].create_time)
                    }
                    
                }
                else if (states[i].action == 'second_approver') {
                    this.sqlorder_state_status.second_approver = states[i].status
                    if (states[i].status == 'success') {
                        this.sqlorder_state.second_approver =  states[i].operator + ' [同意] ' + this.dateFormate(states[i].create_time)
                    }
                    else {
                        this.sqlorder_state.second_approver =  states[i].operator + ' [驳回] ' + this.dateFormate(states[i].create_time)
                    }
                }
                else if (states[i].action == 'dba_approver') {
                    this.sqlorder_state_status.dba_approver = states[i].status
                    if (states[i].status == 'success') {
                        this.sqlorder_state.dba_approver =  states[i].operator + ' [check通过] ' + this.dateFormate(states[i].create_time)
                    }
                    else {
                        this.sqlorder_state.dba_approver =  states[i].operator + ' [check不通过] ' + this.dateFormate(states[i].create_time)
                    }
                    
                    
                }
                else if (states[i].action == 'exec') {
                    this.sqlorder_state.exec =  states[i].operator + ' [exec] ' + this.dateFormate(states[i].create_time)
                    this.sqlorder_state_status.exec = states[i].status
                }
                else if (states[i].action == 'check') {
                    this.sqlorder_state_status.check = states[i].status
                    if (states[i].status == 'success') {
                        this.sqlorder_state.check =  states[i].operator + ' [验证通过] ' + this.dateFormate(states[i].create_time)
                    }
                    else {
                        this.sqlorder_state.check =  states[i].operator + ' [验证失败] ' + this.dateFormate(states[i].create_time)
                    }
                    
                    
                }
                else if (states[i].action == 'done') {
                    this.sqlorder_state.done =  states[i].operator + ' [完成] ' + this.dateFormate(states[i].create_time)
                    this.sqlorder_state_status.done = states[i].status
                }
            }            
        },
        handleCurrentChange(currentPage){
            this.currentPage = currentPage;
        },
        handleSizeChange(val){
            this.pagesize = val;
        },
        handleInfoCurrentChange(currentPage){
            this.currentPage = currentPage;
        },
        handleInfoSizeChange(val){
            this.pagesize = val;
        },
    },
    mounted() {
        this.getSqlOrderDetail()
        this.username = store.getters.username
    },
}
</script>

<style>
.sqlorderdetail .el-table__expanded-cell[class*=cell]{
    padding: 5px 62px;
}
.sqlorderdetail label {
    /* width: 100px; */
    font-size: 12px;
    color: #99a9bf;
}
.sqlorderdetail .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
}
.sqlorderdetail .el-form-item__content{
    text-align: left;
}

/* 表格样式 */
.sqlorderdetail .el-table th{
    user-select: auto
}
.sqlorderdetail .el-table .cell{
    white-space: pre;
    overflow: auto;
    text-overflow: unset;
}
/* 设置滚动条的样式 */
.sqlorderdetail .el-table--border::-webkit-scrollbar,.sqlorderdetail .el-table .cell::-webkit-scrollbar {
    width: 4px;
    height: 6px;
}
/* 滚动槽 */
.sqlorderdetail .el-table--border::-webkit-scrollbar-track,.sqlorderdetail .el-table .cell::-webkit-scrollbar-track{
    border-radius: 2px;
    /* background: hsla(220,4%,58%,.3); */
    /* background: rgba(0, 0, 0, 0.3); */
}
/* 滚动条滑块 */
.sqlorderdetail .el-table--border::-webkit-scrollbar-thumb,.sqlorderdetail .el-table .cell::-webkit-scrollbar-thumb{
    border-radius: 2px;
    background: hsla(220,4%,58%,.3);
    /* background: rgba(0, 0, 0, 0.3); */
}
</style>
<template>
    <div id="sqlordertype" class="sqlordertype">
        <el-row style="padding-bottom:5px;">
            <div class="sqlordertype-operation">
                <el-button @click="handleAdd" style="float: left;" icon="el-icon-edit" size="small" type="primary">添加</el-button>
                <el-input v-model="searchcontent" @keyup.enter.native="searchData" style="width: 200px;float: right;" size="small" placeholder="Search">
                    <el-button @click="searchData" slot="append" icon="el-icon-search"></el-button>
                </el-input>
            </div>
        </el-row>
        <el-row>
            <el-table
            size="small"
            ref="multipleTable"
            :data="table_data.slice((currentPage-1)*pagesize,currentPage*pagesize)"
            border
            strip
            style="width: 100%"
            @selection-change="handleSelectionChange">
                <el-table-column align="center" type="selection" width="55"></el-table-column>
                <el-table-column align="center" type="index" label="序号" width="55">
                    <template slot-scope="scope"><span>{{scope.$index+(currentPage - 1) * pagesize + 1}} </span></template>
                </el-table-column>
                <el-table-column width="200" align="center" label="类型" prop="ordertype" >
                </el-table-column>
                <el-table-column align="center" label="一级审批" prop="first_approver" >
                </el-table-column>
                <el-table-column align="center" label="二级审批" prop="second_approver" >
                </el-table-column>
                <el-table-column align="center" width="100" label="自动执行" prop="is_auto" >
                    <template slot-scope="scope">
                        <el-tag size="small" v-if="scope.row.is_auto == 'ENABLE'" type="success">已开启</el-tag>
                        <el-tag size="small" v-else type="info">已停用</el-tag>
                    </template>
                </el-table-column>
                <el-table-column align="center" width="100" label="备注" prop="comment" ></el-table-column>
                <el-table-column align="center" width="100" label="是否启用" prop="is_enabled" >
                    <template slot-scope="scope">
                        <el-tag size="small" v-if="scope.row.is_auto == 'ENABLE'" type="success">启用</el-tag>
                        <el-tag size="small" v-else type="info">禁止</el-tag>
                    </template>
                </el-table-column>
                <el-table-column width="300" align="center" label="操作">
                <template slot-scope="scope">
                    <el-button @click="handleEdit(scope.$index,scope.row)" size="mini" type="primary">编辑</el-button>
                    <el-button @click="handleDelete(scope.$index,scope.row)" size="mini" type="danger">删除</el-button>
                </template>
                </el-table-column>
            </el-table>
        </el-row>
        <el-row>
            <el-pagination
            background
            layout="total, prev, pager, next, jumper"
            :total="table_data.length"
            :page-size="pagesize"
            @current-change="current_change">
            </el-pagination>
        </el-row>
        <el-row>
            <div class="sqlordertype-dialog">
                <el-dialog
                :title="isEdit?'编辑SQL工单类型':'添加SQL工单类型'"
                :visible.sync="dialogVisible"
                :before-close="handleClose">
                <el-card>
                    <el-form :model="form" ref="form">
                        <el-form-item label="工单类型 : " label-width="100px" prop="ordertype">
                            <el-input style="width: 300px; float: left;" v-model="form.ordertype" auto-complete="off"></el-input>
                        </el-form-item>
                        <el-form-item label="一级审核 : " label-width="100px" prop="first_approver">
                            <el-select clearable style="width: 300px; float: left;" v-model="form.first_approver" placeholder="请选择一级审核组">
                                <el-option v-for="(val,index) in approvalgroup_list" :key="index" :label="val.approver_group_name" :value="val.id" ></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="二级审核 : " label-width="100px" prop="second_approver">
                            <el-select clearable style="width: 300px; float: left;" v-model="form.second_approver" placeholder="请选择二级审核组">
                                <el-option v-for="(val,index) in approvalgroup_list" :key="index" :label="val.approver_group_name" :value="val.id" ></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="DBA审核 : " label-width="100px" prop="dba_approver">
                            <el-select clearable style="width: 300px; float: left;" v-model="form.dba_approver" placeholder="请选择DBA审核组">
                                <el-option v-for="(val,index) in approvalgroup_list" :key="index" :label="val.approver_group_name" :value="val.id" ></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label-width="100px">
                            <el-button style="float: left;" type="primary" @click="handleSumit">提交</el-button>
                            <el-button style="float: left;" @click="dialogVisible = false;">取消</el-button>
                        </el-form-item>
                    </el-form>
                </el-card>
                </el-dialog>
            </div>
        </el-row>
    </div>
</template>

<script>
import store from '@/store/store.js';
import { getSqlOrderType,getApprovalGroup } from '@/api/api.js';
export default {
    name: 'sqlordertype',
    data () {
        return {
            searchcontent: '',
            table_data: [],
            // 分页参数
            total: 0,
            currentPage: 1,
            pagesize: 20,
            // 添加编辑参数
            ordertypeid: '',
            approvalgroup_list: [],
            form: {
                ordertype: '',
                first_approver: '',
                second_approver: '',
                dba_approver: '',
                is_file: '',
            },
            initform: {
                ordertype: '',
                first_approver: '',
                second_approver: '',
                dba_approver: '',
                is_file: '',
            },
            isEdit: false,
            dialogVisible: false,
        }
    },
    methods: {
        resetForm() {
            this.form = this.initform
        },
        handleSelectionChange(val) {
            this.multipleSelection = val; 
        },
        current_change(currentPage){
            this.currentPage = currentPage;
        },
        handleClose(done) {
            this.$confirm('确认关闭？')
            .then(_ => {
                done();
            })
            .catch(_ => {});
        },
        handleSumit(){

        },
        handleAdd(){
            this.resetForm();
            this.dialogVisible = true;
            this.isEdit = false;
        },
        handleEdit($index,row) {
            this.ordertypeid = row.id
            getSqlOrderType({'id':this.ordertypeid}).then((response) => {
                console.log(response.data);
                this.form = response.data
                this.dialogVisible = true;
                this.isEdit = true;
            })  
        },
        saveData() {
            
        },
        searchData() {

        },
        getDataList() {
            getSqlOrderType().then((response) => {
                console.log(response.data);
                this.table_data = response.data
            }).catch((error) => {
                console.log(error);
            })
        },
        getApprovalGroupList() {
            getApprovalGroup().then((response) => {
                console.log(response.data);
                
                this.approvalgroup_list = response.data
            }).catch((error) => {
                console.log(error);
            })
        }
    },
    mounted() {
        this.getDataList()
        this.getApprovalGroupList()
    },
}
</script>

<style>
.sqlordertype .el-collapse-item__header.is-active,.sqlordertype .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
    border-bottom: 1px solid #dcdfe6;
}
.sqlordertype-dialog{
    text-align: left;
}
</style>
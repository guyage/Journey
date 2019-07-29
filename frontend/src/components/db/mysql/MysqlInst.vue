<template>
    <div id="mysqlinst" class="mysqlinst">
        <el-collapse v-model="activeNames">
            <el-collapse-item title="MySQL实例" name="1">
                <div class="mysqlinst-operation" style="padding: 0.8em 0em 1em;">
                    <el-button @click="addData" style="float: left;" icon="el-icon-edit" size="small" type="primary">添加</el-button>
                    <el-input v-model="searchcontent" @keyup.enter.native="searchData" style="width: 200px;float: right;" size="small" placeholder="Search">
                        <el-button @click="searchData" slot="append" icon="el-icon-search"></el-button>
                    </el-input>
                </div>
                <br>
                <MysqlInstTable
                ref="datatable"
                :TableData="table_data"
                :TableColumn="table_columns"
                :delData="delData"
                :editData="editData">
                </MysqlInstTable>
                <MysqlInstDialog
                ref="datadialog"
                :show.sync="show"
                :form="form"
                :rules="rules"
                :saveData="saveData">
                </MysqlInstDialog>
            </el-collapse-item>
        </el-collapse> 
    </div>
</template>

<script>
import MysqlInstTable from './MysqlInstTable.vue';
import MysqlInstDialog from './MysqlInstDialog.vue';
import { getMysqlInst, searchMysqlInst, addMysqlInst, delMysqlInst, editMysqlInst } from '@/api/api.js';
export default {
    name: 'mysqlinst',
    components:{
        MysqlInstTable,
        MysqlInstDialog,
    },
    data () {
        return {
            //控制弹出框
            show: false,
            activeNames: ['1'],
            searchcontent: '',
            table_data: [],
            table_columns: {
                id: 'id',
                inst_name: '实例名称',
                inst_host: '实例IP',
                inst_port: '实例端口',
                role: '角色',
                manage_user: '管理用户',
                read_user: '只读用户',
                services: '涉及服务',
                version: '版本',
                is_enabled: '是否启用',
                comment: '注释',
            },
            //添加，编辑用户form表单参数
            form: {
                inst_name: '',
                inst_host: '',
                inst_port: '',
                role: '',
                manage_user: '',
                manage_userpwd: '',
                read_user: '',
                read_userpwd: '',
                services: '',
                version: '',
                is_enabled: '',
                comment: '',
            },
            rules: {
                inst_name: [
                    { required: true, message: '请输入MySQL实例名', trigger: 'blur' }
                ],
                inst_host: [
                    { required: true, message: '请输入MySQL实例IP', trigger: 'blur' }
                ],
                inst_port: [
                    { required: true, message: '请输入MySQL实例端口', trigger: 'blur' }
                ],
                role: [
                    { required: true, message: '请选择MySQL实例角色', trigger: 'change' }
                ],
            },
        }
    },
    methods: {
        // 控制弹窗
        openDialog () {
            this.show = true;
        },
        closeDialog () {
            this.show = false;
        },
        getDataList() {
            getMysqlInst().then((response) => {
                if (response.data.length > 0) {
                    this.table_data = response.data
                }
            }).catch((error) => {
                console.log(error);
            })
        },
        saveData(isedit,data) {
            if (isedit) {
                editMysqlInst(data).then((response) => {
                    this.$message.success('保存成功!');
                    this.closeDialog();
                    this.getDataList()
                }).catch((error) => {
                    this.$message.error('保存失败!');
                    console.log(error);
                    this.closeDialog();
                })
            }
            else {
                addMysqlInst(data).then((response) => {
                    this.$message.success('保存成功!');
                    this.closeDialog();
                    this.getDataList()
                }).catch((error) => {
                    this.$message.error('保存失败!');
                    console.log(error);
                    this.closeDialog();
                })
            }
        },
        delData(id) {
            delMysqlInst({id:id}).then((response) => {
                this.$message.success('删除成功!');
            }).catch((error) => {
                this.$message.error('删除失败!');
                console.log(error);
            })
        },
        searchData() {
            if (this.searchcontent) {
                searchMysqlInst({searchcontent:this.searchcontent}).then((response) => {
                    this.table_data = response.data
                }).catch((error) => {
                    console.log(error);
                })
            }
            else {
                this.getDataList()
            }
        },
        addData() {
            for (var k in this.form) {
                this.form[k] = ''
            }
            this.$refs.datadialog.isEdit = false
            this.openDialog()
        },
        editData(id) {
            this.getDataDeatil(id)
        },
        getDataDeatil(id) {
            getMysqlInst({id:id}).then((response) => {
                this.$refs.datadialog.isEdit = true
                this.form = response.data
                this.openDialog()
            })
        },
    },
    mounted() {
        this.getDataList()
    },
}
</script>

<style>
.mysqlinst .el-collapse-item__header.is-active,.mysqlinst .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
    border-bottom: 1px solid #dcdfe6;
}   
</style>

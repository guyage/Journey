<template>
    <div id="mongodbinst" class="mongodbinst">
        <el-collapse v-model="activeNames">
            <el-collapse-item title="MongoDB实例" name="1">
                <div class="mongodbinst-operation" style="padding: 0.8em 0em 1em;">
                    <el-button @click="addData" style="float: left;" icon="el-icon-edit" size="small" type="primary">添加</el-button>
                    <el-input v-model="searchcontent" @keyup.enter.native="searchData" style="width: 200px;float: right;" size="small" placeholder="Search">
                        <el-button @click="searchData" slot="append" icon="el-icon-search"></el-button>
                    </el-input>
                </div>
                <br>
                <MongodbInstTable
                ref="datatable"
                :TableData="table_data"
                :TableColumn="table_columns"
                :delData="delData"
                :editData="editData">
                </MongodbInstTable>
                <MongodbInstDialog
                ref="datadialog"
                :show.sync="show"
                :form="form"
                :rules="rules"
                :saveData="saveData">
                </MongodbInstDialog>
            </el-collapse-item>
        </el-collapse> 
    </div>
</template>

<script>
import MongodbInstTable from './MongodbInstTable.vue';
import MongodbInstDialog from './MongodbInstDialog.vue';
import { getMongoDBInst, searchMongoDBInst, addMongoDBInst, delMongoDBInst, editMongoDBInst } from '@/api/api.js';
export default {
    name: 'mongodbinst',
    components:{
        MongodbInstTable,
        MongodbInstDialog,
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
            getMongoDBInst().then((response) => {
                if (response.data.length > 0) {
                    this.table_data = response.data
                }
            }).catch((error) => {
                console.log(error);
            })
        },
        saveData(isedit,data) {
            if (isedit) {
                editMongoDBInst(data).then((response) => {
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
                addMongoDBInst(data).then((response) => {
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
            delMongoDBInst({id:id}).then((response) => {
                this.$message.success('删除成功!');
            }).catch((error) => {
                this.$message.error('删除失败!');
                console.log(error);
            })
        },
        searchData() {
            if (this.searchcontent) {
                searchMongoDBInst({searchcontent:this.searchcontent}).then((response) => {
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
            getMongoDBInst({id:id}).then((response) => {
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
.mongodbinst .el-collapse-item__header.is-active,.mongodbinst .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
    border-bottom: 1px solid #dcdfe6;
}   
</style>

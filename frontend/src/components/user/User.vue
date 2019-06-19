<template>
    <div id="user" class="user">
        <el-collapse v-model="activeNames">
            <el-collapse-item title="用户" name="1">
                <div class="user-operation" style="padding: 0.8em 0em 1em;">
                    <el-button @click="addData" style="float: left;" icon="el-icon-edit" size="small" type="primary">添加</el-button>
                    <el-input v-model="searchcontent" @keyup.enter.native="searchData" style="width: 200px;float: right;" size="small" placeholder="Search">
                        <el-button @click="searchData" slot="append" icon="el-icon-search"></el-button>
                    </el-input>
                </div>
                <br>
                <UserTable
                :TableColumn="table_columns"
                :TableData="table_data"
                :delData="delData"
                :editData="editData">
                </UserTable>
                <UserDialog
                ref="userdialog"
                :show.sync="show"
                :form="form"
                :rules="rules"
                :saveData="saveData">
                </UserDialog>
            </el-collapse-item>
        </el-collapse> 
    </div>
</template>

<script>
import UserTable from './UserTable.vue';
import UserDialog from './UserDialog.vue';
import { getUserList,searchUser,addUser,delUser,editUser,getUserGroupList } from '@/api/api.js';
export default {
    name: 'user',
    components:{
        UserTable,
        UserDialog,
    },
    data () {
        return {
            activeNames: ['1'],
            searchcontent: '',
            //用户列表参数
            table_data: [],
            table_columns: {
                id: 'id',
                real_name: '姓名',
                group: '用户组',
                permissions_group: '权限组',
                is_active: '状态',
                is_superuser: 'isSuperUser',
                username: '用户组',
                comment: '备注'
            },
            //添加，编辑用户form表单参数
            form: {
                username: '',
                last_name: '',
                first_name: '',
                password: '',
                group: '',
                email: '',
                mobile: '',
                webcat: '',
                comment: ''
            },
            rules: {
                username: [
                    { required: true, message: '请输入用户名', trigger: 'blur' }
                ],
                last_name: [
                    { required: true, message: '请输入姓氏', trigger: 'blur' }
                ],
                first_name: [
                    { required: true, message: '请输入姓名', trigger: 'blur' }
                ],
                group: [
                    { required: true, message: '请选择用户组', trigger: 'change' }
                ],
                email: [
                    { required: true, message: '请输入邮箱', trigger: 'blur' }
                ],
            },
            //控制弹出框
            show: false,
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
        addData() {
            for (var k in this.form) {
                this.form[k] = ''
            }
            this.$refs.userdialog.isEdit = false
            this.openDialog()
        },
        saveData(isedit,user_data) {
            if (isedit) {
                editUser(user_data).then((response) => {
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
                addUser(user_data).then((response) => {
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
        editData(id) {
            this.getDataDeatil(id)
        },
        getDataDeatil(id) {
            getUserList({id:id}).then((response) => {
                this.$refs.userdialog.isEdit = true
                response.data.group = response.data.group.toString()
                this.form = response.data
                this.openDialog()
            })
        },
        searchData() {
            if (this.searchcontent) {
                searchUser({searchcontent:this.searchcontent}).then((response) => {
                    this.table_data = response.data
                }).catch((error) => {
                    console.log(error);
                })
            }
            else {
                this.getDataList()
            }
        },
        getDataList() {
            getUserList().then((response) => {
                this.table_data = response.data
            }).catch((error) => {
                console.log(error);
            })
        },
        delData(id) {
            delUser({id:id}).then((response) => {
                console.log(response);
            }).catch((error) => {
                console.log(error);
            })
        },
        
    },
    mounted () {
        this.getDataList()
    }
}
</script>

<style>
.user .el-collapse-item__header.is-active,.user .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
    border-bottom: 1px solid #dcdfe6;
}
</style>

<template>
    <div class="user">
        <el-row style="padding-bottom:5px;">
            <el-button v-if="user_has_perms.indexOf('user:user:add')>-1 || user_issuper" @click="addData" style="float: left;" icon="el-icon-edit" size="small" type="primary">添加</el-button>
            <el-input v-model="searchcontent" @keyup.enter.native="searchData" style="width: 200px;float: right;" size="small" placeholder="Search">
                <el-button @click="searchData" slot="append" icon="el-icon-search"></el-button>
            </el-input>
        </el-row>
        <el-row>
            <UserTable
            ref="datatable"
            :TableColumn="table_columns"
            :TableData="table_data"
            :editData="editData"
            :delData="delData">
            </UserTable>
        </el-row>
        <el-row>
            <UserDialog
            ref="userdialog"
            :show.sync="show"
            :saveData="saveData"
            :form="form"
            :rules="rules">
            </UserDialog>
        </el-row>
    </div>
</template>

<script>
import store from '@/store/store.js';
import UserTable from './UserTable.vue';
import UserDialog from './UserDialog.vue';
import { getUser,searchUser,addUser,delUser,editUser,getUserGroup } from '@/api/api.js';
export default {
    name: 'user',
    components: {
       UserTable,
       UserDialog
    },
    data() {
        return {
            // 用户按钮权限
            user_issuper: false,
            user_has_perms:[],
            searchcontent: '',
            //控制弹出框
            show: false,
            //用户列表参数
            table_data: [],
            table_columns: {
                id: 'id',
                username: '用户名',
                real_name: '姓名',
                email: '邮箱',
                group: '用户组',
                roles: '角色',
                is_active: '状态',
                is_superuser: 'isSuperUser',
                comment: '备注'
            },
            //添加，编辑用户form表单参数
            form: {
                username: '',
                last_name: '',
                first_name: '',
                password: '',
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
                email: [
                    { required: true, message: '请输入邮箱', trigger: 'blur' }
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
        addData() {
            this.$refs.userdialog.isEdit = false
            this.openDialog()
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
                this.getData()
            }
        },
        saveData(isedit,user_data) {
            if (isedit) {
                editUser(user_data).then((response) => {
                    this.$message.success('保存成功!');
                    this.closeDialog();
                    this.getData()
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
                    this.getData()
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
            getUser({id:id}).then((response) => {
                this.$refs.userdialog.isEdit = true
                this.form = response.data
                this.openDialog()
            })
        },
        delData(id) {
            delUser({id:id}).then((response) => {
                this.$message.success('删除成功!');
            }).catch((error) => {
                this.$message.error('删除失败!');
                console.log(error);
            })
        },
        getData() {
            getUser().then((response) => {
                this.table_data = response.data
            }).catch((error) => {
                console.log(error);
            })
        },
    },
    mounted() {
        this.getData()
        this.user_has_perms = store.getters.userperms 
        this.user_issuper = store.getters.userissuper           
    },
}
</script>

<style>

</style>

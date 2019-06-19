<template>
    <div id="usergroup" class="usergroup">
        <el-collapse v-model="activeNames">
            <el-collapse-item title="用户组" name="1">
                <div class="usergroup-operation" style="padding: 0.8em 0em 1em;">
                    <el-button @click="addData" style="float: left;" icon="el-icon-edit" size="small" type="primary">添加</el-button>
                    <el-input v-model="searchcontent" @keyup.enter.native="searchData" style="width: 200px;float: right;" size="small" placeholder="Search">
                        <el-button @click="searchData" slot="append" icon="el-icon-search"></el-button>
                    </el-input>
                </div>
                <br>
                <GeneralTable
                ref="datatable"
                :TableData="table_data"
                :TableColumn="table_columns"
                :delData="delData"
                :editData="editData">
                </GeneralTable>
                <UserGroupDialog
                ref="datadialog"
                :show.sync="show"
                :saveData="saveData">
                </UserGroupDialog>
            </el-collapse-item>
        </el-collapse> 
    </div>
</template>

<script>
import UserGroupDialog from './UserGroupDialog.vue';
import GeneralTable from '@/components/views/GeneralTable.vue';
import { getUserGroupList, searchUserGroup, delUserGroup, editUserGroup, addUserGroup } from '@/api/api.js';
export default {
    name: 'usergroup',
    components:{
        GeneralTable,
        UserGroupDialog,
    },
    data () {
        return {
            //弹框参数
            show: false,
            searchcontent: '',
            activeNames: ['1'],
            table_data: [],
            table_columns: {
                id: 'id',
                group_name: '用户组',
                usercount: '成员数目',
                comment: '备注'
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
        saveData(isedit,usergroup_data) {
            if (isedit) {
                editUserGroup(usergroup_data).then((response) => {
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
                addUserGroup(usergroup_data).then((response) => {
                    this.table_data.push(response.data)
                    this.$message.success('保存成功!');
                    this.closeDialog();
                }).catch((error) => {
                    this.$message.error('保存失败!');
                    console.log(error);
                    this.closeDialog();
                })
            }
        },
        addData() {
            this.$refs.datadialog.isEdit = false
            this.initUserGroupParams(this.$refs.datadialog.isEdit)
            this.openDialog()
        },
        editData(id) {
            this.getDataDeatil(id)
        },
        getDataDeatil(id) {
            getUserGroupList({id:id}).then((response) => {
                this.$refs.datadialog.isEdit = true
                this.initUserGroupParams(this.$refs.datadialog.isEdit,response.data)
                this.openDialog()
            })
        },
        searchData() {
            if (this.searchcontent) {
                searchUserGroup({searchcontent:this.searchcontent}).then((response) => {
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
            getUserGroupList().then((response) => {
                if (response.data.length > 0) {
                    this.table_data = response.data
                }
            }).catch((error) => {
                console.log(error);
            })
        },
        delData(id) {
            delUserGroup({id:id}).then((response) => {
                console.log(response);
            }).catch((error) => {
                console.log(error);
            })
        },
        initUserGroupParams (isedit,usergroupparams) {
            if (isedit) {
                this.$refs.datadialog.group_name = usergroupparams.group_name
                this.$refs.datadialog.comment = usergroupparams.comment
                this.$refs.datadialog.userselected = usergroupparams.userlist
                this.$refs.datadialog.usergroup_edit_id = usergroupparams.id
                this.$refs.datadialog.isEdit = true
            }
            else {
                this.$refs.datadialog.group_name = ''
                this.$refs.datadialog.comment = ''
                this.$refs.datadialog.isEdit = false
                this.$refs.datadialog.userselected = []
                this.$refs.datadialog.usergroup_edit_id = 0
            }
        }
    },
    mounted () {
        this.getDataList()
    }
}
</script>

<style>
.usergroup .el-collapse-item__header.is-active,.usergroup .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
    border-bottom: 1px solid #dcdfe6;
}
</style>

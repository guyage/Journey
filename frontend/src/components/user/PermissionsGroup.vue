<template>
    <div class="permissionsgroup">
        <el-collapse v-model="activeNames">
            <el-collapse-item title="权限组" name="1">
                <div class="permissionsgroup-operation" style="padding: 0.8em 0em 1em;">
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
                <PermissionsGroupDialog
                ref="datadialog"
                :show.sync="show"
                :saveData="saveData">
                </PermissionsGroupDialog>
            </el-collapse-item>
        </el-collapse> 
    </div>
</template>

<script>
import PermissionsGroupDialog from './PermissionsGroupDialog.vue';
import GeneralTable from '@/components/views/GeneralTable.vue';
import { getPermissionsGroupList, searchPermissionsGroup, delPermissionsGroup, editPermissionsGroup, addPermissionsGroup } from '@/api/api.js';
export default {
    name: 'permissionsgroup',
    components:{
        GeneralTable,
        PermissionsGroupDialog,
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
                permissions_name: '权限组',
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
        saveData(isedit,permissionsgroup_data) {
            if (isedit) {
                console.log(permissionsgroup_data);
                
                editPermissionsGroup(permissionsgroup_data).then((response) => {
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
                addPermissionsGroup(permissionsgroup_data).then((response) => {
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
            this.initpermissionsgroupParams(this.$refs.datadialog.isEdit)
            this.openDialog()
        },
        editData(id) {
            this.getDataDeatil(id)
        },
        getDataDeatil(id) {
            getPermissionsGroupList({id:id}).then((response) => {
                this.$refs.datadialog.isEdit = true
                this.initpermissionsgroupParams(this.$refs.datadialog.isEdit,response.data)
                this.openDialog()
            })
        },
        searchData() {
            if (this.searchcontent) {
                searchPermissionsGroup({searchcontent:this.searchcontent}).then((response) => {
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
            getPermissionsGroupList().then((response) => {
                if (response.data.length > 0) {
                    this.table_data = response.data
                }
            }).catch((error) => {
                console.log(error);
            })
        },
        delData(id) {
            delPermissionsGroup({id:id}).then((response) => {
                this.$message.success('删除成功!');
            }).catch((error) => {
                console.log(error);
            })
        },
        initpermissionsgroupParams (isedit,permissionsgroupparams) {
            if (isedit) {
                this.$refs.datadialog.permissions_name = permissionsgroupparams.permissions_name
                this.$refs.datadialog.comment = permissionsgroupparams.comment
                this.$refs.datadialog.userselected = permissionsgroupparams.userlist
                this.$refs.datadialog.permissionsgroup_edit_id = permissionsgroupparams.id
                this.$refs.datadialog.isEdit = true
            }
            else {
                this.$refs.datadialog.permissions_name = ''
                this.$refs.datadialog.comment = ''
                this.$refs.datadialog.isEdit = false
                this.$refs.datadialog.userselected = []
                this.$refs.datadialog.permissionsgroup_edit_id = 0
            }
        }
    },
    mounted () {
        this.getDataList()
    }
}
</script>

<style>
.permissionsgroup .el-collapse-item__header.is-active,.permissionsgroup .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
    border-bottom: 1px solid #dcdfe6;
}
</style>

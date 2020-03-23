<template>
    <div class="perms">
        <el-row style="padding-bottom:5px;">
            <el-button @click="addData" style="float: left;" icon="el-icon-edit" size="small" type="primary">添加</el-button>
            <!-- <el-input v-model="searchcontent" @keyup.enter.native="searchData" style="width: 200px;float: right;" size="small" placeholder="Search">
                <el-button @click="searchData" slot="append" icon="el-icon-search"></el-button>
            </el-input> -->
        </el-row>
        <el-row>
            <el-alert
            title="接口权限配置，配置后端接口请求权限(get,post,patch,del)!"
            type="success"
            effect="dark">
            </el-alert>
        </el-row>
        <el-row>
            <PermsTable
            ref="datatable"
            :TableColumn="table_columns"
            :TableData="table_data"
            :editData="editData"
            :delData="delData">
            </PermsTable>
        </el-row>
        <el-row>
            <PermsDialog
            ref="datadialog"
            :show.sync="show"
            :saveData="saveData">
            </PermsDialog>
        </el-row>
    </div>
</template>

<script>
import { getPerms,addPerms,editPerms,delPerms } from '@/api/user.js';
import PermsTable from './PermsTable.vue';
import PermsDialog from './PermsDialog.vue';
export default {
    name: 'perms',
    components: {
        PermsTable,
        PermsDialog
    },
    data () {
        return {
            //控制弹出框
            show: false,
            searchcontent: '',
            table_data: [],
            table_columns: {
                id: 'id',
                name: '接口名称',
                api: '接口',
                perms: '权限标识',
                del_flag: '禁用',
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
            this.openDialog()
        },
        getData() {
            getPerms().then((response) => {
                this.table_data = response.data
            }).catch((error) => {
                console.log(error); 
            })
        },
        editData(req_data) {
            editPerms(req_data).then((response) => {
                this.$message.success('处理成功!');
                this.getData()
            }).catch((error) => {
                console.log(error);
                this.$message.error('处理失败!');
            })
        },
        delData(req_data) {
            console.log(req_data);
            
            delPerms(req_data).then((response) => {
                this.$message.success('删除成功!');
                this.getData()
            }).catch((error) => {
                console.log(error);
                this.$message.error('删除失败!');
            })
        },
        saveData(req_data) {
            addPerms(req_data).then((response) => {
                this.$message.success('添加成功!');
                this.getData()
                this.closeDialog()
            }).catch((error) => {
                console.log(error);
                this.$message.error('添加失败!');
                this.closeDialog()
            })
        },
    },
    mounted() {
        this.getData()
    },
}
</script>

<style>

</style>
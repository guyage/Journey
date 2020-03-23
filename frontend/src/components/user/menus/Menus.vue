<template>
    <div class="menus">
        <el-row style="padding-bottom:5px;">
            <el-button @click="addData" style="float: left;" icon="el-icon-edit" size="small" type="primary">添加</el-button>
            <!-- <el-input v-model="searchcontent" @keyup.enter.native="searchData" style="width: 200px;float: right;" size="small" placeholder="Search">
                <el-button @click="searchData" slot="append" icon="el-icon-search"></el-button>
            </el-input> -->
        </el-row>
        <el-row>
            <el-alert
            title="菜单路由配置，配置左侧菜单及子路由(内部跳转使用)，路由均需与前端路由一致!"
            type="success"
            effect="dark">
            </el-alert>
        </el-row>
        <el-row>
            <MenusTable
            ref="datatable"
            :TableColumn="table_columns"
            :TableData="table_data"
            :editData="editData">
            </MenusTable>
        </el-row>
        <el-row>
            <MenusDialog
            ref="datadialog"
            :show.sync="show"
            :saveData="saveData">
            </MenusDialog>
        </el-row>
    </div>
</template>

<script>
import { getMenus,editMenus,addMenus,searchMenus } from '@/api/user.js';
import MenusTable from './MenusTable.vue';
import MenusDialog from './MenusDialog.vue';
export default {
    name: 'menus',
    components: {
        MenusTable,
        MenusDialog
    },
    data () {
        return {
            //控制弹出框
            show: false,
            searchcontent: '',
            table_data: [],
            table_columns: {
                id: 'id',
                name: '名称',
                icon: '图标',
                url: '路由',
                mtype: '类型',
                del_flag: '禁用',
            },
            initform: {
                name: '',
                url: '',
                parent_id: '',
                icon: '',
                mtype: 0,
                del_flag:0,
                creator: '',
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
        getData() {
            getMenus().then((response) => {
                this.table_data = response.data
            }).catch((error) => {
                console.log(error); 
            })
        },
        // searchData() {
        //     if (this.searchcontent) {
        //         searchMenus({searchcontent:this.searchcontent}).then((response) => {
        //             this.table_data = response.data
        //         }).catch((error) => {
        //             console.log(error);
        //         })
        //     }
        //     else {
        //         this.getData()
        //     }
        // },
        addData() {
            this.$refs.datadialog.form = this.initform
            this.$refs.datadialog.isEdit = false
            this.openDialog()

        },
        getDataDeatil(req_data) {
            getMenus(req_data).then((response) => {
                this.$refs.datadialog.isEdit = true
                this.$refs.datadialog.getSelectMenusList()
                this.$refs.datadialog.mtype = response.data.mtype
                this.$refs.datadialog.form = response.data
                this.openDialog()
            })
        },
        editData(req_data,type) {
            if (type == 'status') {
                editMenus(req_data).then((response) => {
                    this.$message.success('处理成功!');
                    this.getData()
                }).catch((error) => {
                    console.log(error);
                    this.$message.error('处理失败!');
                })
            }
            else if (type == 'content') {
                this.getDataDeatil(req_data)
            }
            
        },
        saveData(isedit,req_data) {
            if (isedit) {
                editMenus(req_data).then((response) => {
                    this.$message.success('编辑成功!');
                    this.getData()
                    this.closeDialog()
                }).catch((error) => {
                    console.log(error);
                    this.$message.error('编辑失败!');
                    this.closeDialog()
                })
            }
            else {
                addMenus(req_data).then((response) => {
                    this.$message.success('添加成功!');
                    this.getData()
                    this.closeDialog()
                }).catch((error) => {
                    console.log(error);
                    this.$message.error('添加失败!');
                    this.closeDialog()
                })
            }
            
        }
    },
    mounted () {
        this.getData()
    }
}
</script>

<style>

</style>
<template>
    <div class="mysqlinst">
        <div class="filter-container" style="overflow:hidden; padding-bottom:10px;">
            <el-button @click="changeUpdateButton" style="float: left;" icon="el-icon-edit" size="small" type="primary">添加</el-button>
            <el-input v-on:change="inputchange" v-model="searchcontent" @keyup.enter.native="searchData" style="width: 200px;float: right;" size="small" placeholder="Search">
                <el-button @click="searchData" slot="append" icon="el-icon-search"></el-button>
            </el-input>
        </div>
        <!-- // 对应table -->
        <Table 
        ref="datatable"
        v-bind:apiurl="api"
        :getDataDetail="getDataDetail"
        :openDataDialog="openDialog"                    
        :removeData="delData" 
        :TableData="results"
        :TableColumn="tablecolumns">
        </Table>
        <DataDialog
        ref="datadialog"
        :editurl="editapi"
        :editFun="updateData"
        :apiurl="api"
        :addFun="addData"
        :form="dataform"
        :formlabel="dataformlabel"
        :rules="datarules"
        :show.sync="show">
        </DataDialog>
    </div>
</template>

<script>
import Axios from '@/utils/axios.js';
import Table from '@/components/views/Table.vue';
import DataDialog from '@/components/views/DataDialog.vue';
export default {
    name: 'mysqlinst',
    data () {
        return {
            show: false,
            editapi: '',              // 编辑数据接口
            api: '/mysqlinst/',     // api定义对应后台接口
            results: [],              // results定义表数据
            searchcontent: '',        // input搜索框数据
            // table显示列定义
            tablecolumns: {           
                id: 'id',
                instname: '实例名称',
                host: 'IP地址',
                port: '端口',
                manageuser: '管理用户',
                readuser: '只读用户',
                version: '版本',
                comment: '备注',
                is_enabled: '是否启用'
            },
            resdetail: {},            // 数据明细根据id获取
            // 添加或修改数据时form表单行定义
            dataform: {
                instname: '',
                host: '',
                port: '',
                manageuser: '',
                manageuserpwd: '',
                readuser: '',
                readuserpwd: '',
                version: '',
                comment: '',
                is_enabled: ''
            },
            // 添加或修改数据时form表单对应中文别名
            dataformlabel: {
                instname: { label: 'Mongodb实例名称', selected: false},
                host: { label: 'IP地址', selected: false },
                port: { label: '端口', selected: false },
                manageuser: { label: '管理用户', selected: false },
                manageuserpwd: { label: '管理用户密码', selected: false },
                readuser: { label: '只读用户', selected: false },
                readuserpwd: { label: '只读用户密码', selected: false },
                version: { label: '版本', selected: false },
                comment: { label: '注释', selected: false },
                is_enabled: { label: '是否启用', selected: false },
            },
            // 添加或修改数据时form表单校验定义
            datarules: {
                instname: [
                    { required: true, message: '请输入数据库', trigger: 'blur' }
                ],
                host: [
                    { required: true, message: '请输入IP地址', trigger: 'blur' }
                ],
                port: [
                    { required: true, message: '请输入端口', trigger: 'blur' }
                ],
                version: [
                    { required: true, message: '请输入版本', trigger: 'blur' }
                ],
                is_enabled: [
                    { required: true, message: '请确认是否启用', trigger: 'blur' }
                ]
            },
            columns: {},
            
        }
    },
    components: {
        Table,
        DataDialog
    },
    mounted () {
        this.getDataList(this.api)
    },
    methods: {
        // 获取mongodbinst列表(方法名定义公共些，方便类似功能复制)
        getDataList(url) {
            Axios.oGet(url).then((response) => {
                if (response) {
                    this.results = response.data
                }
            }).catch((error) => {
                console.log(error);
            })
        },
        // 搜索数据
        searchData() {
            if (this.searchcontent) {
                var searchurl = this.api + '?search=' + this.searchcontent
                this.getDataList(searchurl)
            }
            else {
                this.getDataList(this.api)
            } 
        },
        // 添加功能
        addData(url,data) {
            Axios.oPost(url,data).then((response)=>{
                if (response) {
                    this.results.push(response.data)
                    this.$message.success('数据保存成功!');
                }
            }).catch((error)=>{
                console.log(error); 
            })
        },
        // 获取明细
        getDataDetail(id) {
            this.$refs.datadialog.isUpdate = true
            var url = this.api + id + '/'
            this.editapi = url
            Axios.oGet(url).then((response)=>{
                if (response) {
                    this.resdetail = response.data          
                    this.dataform = this.resdetail
                }               
            }).catch((error) => {
                console.log(error);
            }) 
        },
        // 修改数据
        updateData(url,data) {
            Axios.oUpdate(url,data).then((response)=>{
                if (response) {
                    this.getDataList(this.api)
                    this.$message.success('数据编辑成功!');
                }                
            }).catch((error)=>{
                console.log(error); 
            })
        },
        // 删除database
        delData(id) {
            var url = this.api + id + '/'
            Axios.oDelete(url).then((response)=>{
            }).catch((error)=>{
                console.log(error);                
            })
        },
        inputchange(value) {
            console.log(value);
        },
        openDialog () {
            this.show = true;
        },
        changeUpdateButton() {
            this.$refs.datadialog.isUpdate = false;
            this.openDialog()
            // this.$refs.dbdialog.resetForm('form');
        }
        
    },
    
}
</script>

<style>

</style>


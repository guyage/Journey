<template>
    <div id="dumpwhitelist" class="dumpwhitelist">
        <el-row style="padding-bottom:5px;">
            <div class="mysqlinst-operation">
                <el-button @click="addData" style="float: left;" icon="el-icon-edit" size="small" type="primary">添加</el-button>
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
                <el-table-column width="100" align="center" label="用户" prop="white_user" >
                    <template slot-scope="scope">
                        <template v-if="scope.row.isadd">
                            <el-input size="small" v-model="white_user_temp"></el-input>
                        </template>
                        <span v-if="!scope.row.isadd">{{scope.row.white_user}}</span>  
                    </template>
                </el-table-column>                
                <el-table-column align="left" label="白名单表" prop="white_table" >
                    <template slot-scope="scope">
                        <template v-if="scope.row.isedit">
                            <el-input style="width:80%;" size="small" v-model="white_table_temp"></el-input>
                            <div style="width:11em;float:right;">
                                <el-button v-if="!scope.row.isadd" @click="saveData('edit',scope.row)" size="mini" type="success">ok</el-button>
                                <el-button v-if="scope.row.isadd" @click="saveData('add',scope.row)" size="mini" type="success">ok</el-button>
                                <el-button v-if="!scope.row.isadd" @click="handleCancel('edit',scope.$index,scope.row)" size="mini" type="warning">cancel</el-button>
                                <el-button v-if="scope.row.isadd" @click="handleCancel('add',scope.$index,scope.row)" size="mini" type="warning">cancel</el-button>
                            </div>
                        </template>
                        <span v-if="!scope.row.isedit">{{scope.row.white_table}}</span>
                    </template>
                </el-table-column>
                <el-table-column width="200" align="center" label="操作">
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
                
    </div>
</template>

<script>
import store from '@/store/store.js';
import { getDumpWhiteList,delDumpWhiteList,editDumpWhiteList,addDumpWhiteList,searchDumpWhiteList } from '@/api/query.js';
export default {
    name: 'dumpwhitelist',
    data () {
        return {
            searchcontent: '',
            table_data: [],
            // 分页参数
            total: 0,
            currentPage: 1,
            pagesize: 20,
            white_table_temp: '',
            white_user_temp: '',
        }
    },
    methods: {
        handleSelectionChange(val) {
            this.multipleSelection = val; 
        },
        current_change(currentPage){
            this.currentPage = currentPage;
        },
        handleEdit($index,row) {
            row.isedit = true;
            this.white_table_temp = row.white_table
        },
        handleCancel(type,$index,row) {
            if (type == 'edit') {
                row.isedit = false
            }
            else if (type == 'add') {
                var real_index = $index+(this.currentPage - 1) * this.pagesize
                this.table_data.splice(real_index, 1)
            }
        },
        saveData(type,row) {
            let white_data = {}
            if (type == 'edit') {
                white_data.id = row.id
                white_data.white_table = this.white_table_temp
                editDumpWhiteList(white_data).then((response) => {
                    row.isedit = false
                    row.white_table = response.data.white_table
                    this.$message.success('编辑成功!');
                }).catch((error) => {
                    console.log(error);
                    this.$message.error('编辑失败!');
                })
            }
            else if (type == 'add') {
                white_data.white_user = this.white_user_temp
                white_data.white_table = this.white_table_temp
                addDumpWhiteList(white_data).then((response) => {
                    this.$message.success('添加成功!');
                    this.getDataList()
                }).catch((error) => {
                    console.log(error);
                    this.$message.error('添加失败!');
                })
            }
        },
        handleDelete($index,row) {
            this.$confirm('确认删除?', '提示',{
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            })
            .then(_=> {
                var real_index = $index+(this.currentPage - 1) * this.pagesize
                delDumpWhiteList({'id':row.id}).then((response) => {
                    if (response) {
                        this.table_data.splice(real_index, 1)
                        this.$message.success('删除成功!');
                        this.getDataList()
                    }
                }).catch((error) => {
                    console.log(error);
                    this.$message.error('删除失败!');
                })
            })
            .catch(_=>{})
        },
        addData() {
            this.white_table_temp = '';
            this.white_user_temp = '';
            this.table_data.unshift({white_user:'',white_table:'',isadd:true,isedit:true})
        },
        searchData() {
            if (this.searchcontent) {
                searchDumpWhiteList({searchcontent:this.searchcontent}).then((response) => {
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
            getDumpWhiteList().then((response) => {
                for (let i=0;i<response.data.length;i++) {
                    response.data[i].isedit = false
                    // response.data[i].isadd = false
                }
                this.table_data = response.data
            }).catch((error) => {
                console.log(error);
            })
        }

    },
    mounted() {
        this.getDataList()
    },
}
</script>

<style>
.dumpwhitelist .el-collapse-item__header.is-active,.dumpwhitelist .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
    border-bottom: 1px solid #dcdfe6;
}
</style>

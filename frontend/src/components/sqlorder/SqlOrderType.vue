<template>
    <div id="sqlordertype" class="sqlordertype">
        <el-row style="padding-bottom:5px;">
            <div class="sqlordertype-operation">
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
                <el-table-column width="200" align="center" label="类型" prop="ordertype" >
                    <template slot-scope="scope">
                        <template v-if="scope.row.isedit">
                            <el-input size="small" v-model="ordertype_temp"></el-input>
                        </template>
                        <span v-if="!scope.row.isedit">{{scope.row.ordertype}}</span>
                    </template>
                    
                </el-table-column>
                <el-table-column align="center" label="一级审批" prop="first_approver" >
                    <!-- <template slot-scope="scope">
                        <template v-if="scope.row.isadd">
                            <el-input size="small" v-model="white_user_temp"></el-input>
                        </template>
                        <span v-if="!scope.row.isadd">{{scope.row.white_user}}</span>  
                    </template> -->
                </el-table-column>
                <el-table-column align="center" label="二级审批" prop="second_approver" >
                    <!-- <template slot-scope="scope">
                        <template v-if="scope.row.isadd">
                            <el-input size="small" v-model="white_user_temp"></el-input>
                        </template>
                        <span v-if="!scope.row.isadd">{{scope.row.white_user}}</span>  
                    </template> -->
                </el-table-column>
                <el-table-column align="center" width="100" label="自动执行" prop="is_auto" >
                    <template slot-scope="scope">
                        <el-tag size="small" v-if="scope.row.is_auto == 'ENABLE'" type="success">已开启</el-tag>
                        <el-tag size="small" v-else type="info">已停用</el-tag>
                    </template>
                </el-table-column>
                <el-table-column align="center" width="100" label="备注" prop="comment" ></el-table-column>
                <el-table-column align="center" width="100" label="是否启用" prop="is_enabled" >
                    <template slot-scope="scope">
                        <el-tag size="small" v-if="scope.row.is_auto == 'ENABLE'" type="success">启用</el-tag>
                        <el-tag size="small" v-else type="info">禁止</el-tag>
                    </template>
                </el-table-column>
                <el-table-column width="300" align="center" label="操作">
                <template slot-scope="scope">
                    <div v-if="scope.row.isedit">
                        <el-button v-if="!scope.row.isadd" @click="saveData('edit',scope.row)" size="mini" type="success">ok</el-button>
                        <el-button v-if="scope.row.isadd" @click="saveData('add',scope.row)" size="mini" type="success">ok</el-button>
                        <el-button v-if="!scope.row.isadd" @click="handleCancel('edit',scope.$index,scope.row)" size="mini" type="warning">cancel</el-button>
                        <el-button v-if="scope.row.isadd" @click="handleCancel('add',scope.$index,scope.row)" size="mini" type="warning">cancel</el-button>
                    </div>
                    <div v-if="!scope.row.isedit">
                        <el-button @click="handleEdit(scope.$index,scope.row)" size="mini" type="primary">编辑</el-button>
                        <el-button @click="handleDelete(scope.$index,scope.row)" size="mini" type="danger">删除</el-button>
                    </div>
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
import { getSqlOrderType } from '@/api/api.js';
export default {
    name: 'sqlordertype',
    data () {
        return {
            searchcontent: '',
            table_data: [],
            // 分页参数
            total: 0,
            currentPage: 1,
            pagesize: 20,
            // 编辑参数
            ordertype_temp: '',
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
            console.log(row);
            this.ordertype_temp = row.ordertype
            
        },
        addData() {
            this.ordertype_temp = ''
            this.table_data.unshift({ordertype:'',isadd:true,isedit:true})
        },
        searchData() {

        },
        getDataList() {
            getSqlOrderType().then((response) => {
                console.log(response.data);
                
                for (let i=0;i<response.data.length;i++) {
                    response.data[i].isedit = false
                    // response.data[i].isadd = false
                }
                this.table_data = response.data
            }).catch((error) => {
                console.log(error);
            })
        },
    },
    mounted() {
        this.getDataList()
    },
}
</script>

<style>
.sqlordertype .el-collapse-item__header.is-active,.sqlordertype .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
    border-bottom: 1px solid #dcdfe6;
}
</style>
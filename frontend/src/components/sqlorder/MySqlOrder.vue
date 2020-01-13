<template>
    <div id="mysqlorder" class="mysqlorder">
        <el-row style="padding-bottom:5px;">
            <div class="mysqlorder-operation">
                <el-button @click="handleNeworder" style="float: left;" icon="el-icon-edit" size="small" type="primary">新建SQL工单</el-button>
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
                <!-- <el-table-column align="center" type="selection" width="55"></el-table-column> -->
                <el-table-column align="center" label="SQL工单号" width="150" prop="id">
                    <template slot-scope="scope">
                        <el-link :href="'#/sqlorderdetail/'+'SQLOnline'+'-'+scope.row.id" type="primary">SQLOnline-{{scope.row.id}}</el-link>
                    </template>
                </el-table-column>
                <el-table-column align="center" label="主题" prop="title"></el-table-column>
                <el-table-column width="150" align="center" label="工单类型" prop="ordertypename">
                    <template slot-scope="scope">
                        <el-tag size="small" style="color:#ffffff;background:#19be6b;border-color:#19be6b;"  v-if="scope.row.ordertypename == 'DDL'">{{scope.row.ordertypename}}</el-tag>
                        <el-tag size="small" style="color:#ffffff;background:#f90;border-color:#f90;"  v-else-if="scope.row.ordertypename == 'DML'">{{scope.row.ordertypename}}</el-tag>
                        <el-tag size="small" style="color:#ffffff;background:#ffa2d3;border-color:#ffa2d3;"  v-else="scope.row.ordertypename != 'DDL' || scope.row.ordertypename != 'DML'">{{scope.row.ordertypename}}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column width="150" align="center" label="状态" prop="status" :filters="status_filters" :filter-method="filterStatus">
                    <template slot-scope="scope">
                        <el-tag size="small"  v-if="scope.row.status == 0">待审批</el-tag>
                        <el-tag size="small" type="warning" v-else-if="scope.row.status == 1">已驳回</el-tag>
                        <el-tag size="small" type="success" v-else-if="scope.row.status == 2">已完成</el-tag>
                        <el-tag size="small" style="color:#fa8c16;background:#fff7e6;border-color:#ffd591;" type="warning" v-else-if="scope.row.status == 3">DBA-CHECK中</el-tag>
                        <el-tag size="small" style="color:#13c2c2;background:#e6fffb;border-color:#87e8de;" type="warning" v-else-if="scope.row.status == 4">待执行</el-tag>
                        <el-tag size="small" style="color:#faad14;background:#fffbe6;border-color:#ffe58f;" type="warning" v-else-if="scope.row.status == 5">已执行，待验证</el-tag>
                        <el-tag size="small" style="color:#722ed1;background:#f9f0ff;border-color:#d3adf7;" type="danger" v-else-if="scope.row.status == 6">已验证</el-tag>
                        <el-tag size="small" type="info" v-else-if="scope.row.status == 7">已取消</el-tag>
                        <el-tag size="small" type="danger" v-else="scope.row.status == -1">已失败</el-tag>
                    </template>
                </el-table-column>
                <el-table-column align="center" width="100" label="创建人" prop="creator"></el-table-column>
                <el-table-column align="center" width="100" label="操作人" prop="operator"></el-table-column>
                <el-table-column width="200" align="center" label="创建时间" prop="create_time" >
                    <template slot-scope="scope">
                        {{scope.row.create_time | dateFormate}}
                    </template>
                </el-table-column>
                <el-table-column width="200" align="center" label="修改时间" prop="update_time" >
                    <template slot-scope="scope">
                        {{scope.row.update_time | dateFormate}}
                    </template>
                </el-table-column>
                <!-- <el-table-column width="200" align="center" label="流程" prop="update_time" >
                    <template slot-scope="scope">
                        <el-badge :value="1" class="item">
                            <el-button size="mini">流程</el-button>
                        </el-badge>
                    </template>
                </el-table-column> -->
            </el-table>
        </el-row>
        <el-row>
            <el-pagination
            background
            layout="total, sizes,prev, pager, next, jumper"
            :total="table_data.length"
            :page-size="pagesize"
            :page-sizes="[10, 15, 20, 30]"
            @current-change="current_change"
            @size-change="handleSizeChange">
            </el-pagination>
        </el-row> 
    </div>
</template>

<script>
import moment from 'moment';
import store from '@/store/store.js';
import { getMySqlOrder } from '@/api/api.js';
export default {
    // name: 'mysqlorder',
    data () {
        return {
            searchcontent: '',
            table_data: [],
            // 分页参数
            total: 0,
            currentPage: 1,
            pagesize: 15,
            // 编辑参数
            ordertype_temp: '',
            // 筛选数据参数
            status_filters: [{text:'待审批',value:0}, {text:'已驳回', value:1}]
        }
    },
    filters: {
        dateFormate(date) {
            return moment(date).format("YYYY-MM-DD HH:mm:ss");
        }
    },
    methods: {
        handleSelectionChange(val) {
            this.multipleSelection = val; 
        },
        handleSizeChange(val){
            this.pagesize = val;
        },
        current_change(currentPage){
            this.currentPage = currentPage;
        },
        filterStatus(value, row) {
            return row.status === value;
        },
        handleNeworder() {
            this.$router.push({ path: '/newsqlorder'})
        },
        searchData() {

        },
        getDataList() {
            getMySqlOrder().then((response) => {
                console.log(response.data);
                this.table_data = response.data.results
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
.mysqlorder .el-collapse-item__header.is-active,.mysqlorder .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
    border-bottom: 1px solid #dcdfe6;
}
</style>
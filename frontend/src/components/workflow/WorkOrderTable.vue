<template>
    <div id="workordertable" class="workordertable">
        <el-table
        size="mini"
        ref="multipleTable"
        :data="TableData.slice((currentPage-1)*pagesize,currentPage*pagesize)"
        strip
        style="width: 100%"
        @selection-change="handleSelectionChange">
            <!-- <el-table-column type="expand">
                <template slot-scope="props">
                    <el-form size="mini" label-position="left" inline class="demo-table-expand">
                        <el-form-item v-for="(val, key, index) in JSON.parse(props.row['content'])" :key="index" :label="key">
                            <span>{{val}}</span>
                        </el-form-item>
                    </el-form>
                </template>
            </el-table-column> -->
            <el-table-column align="center" type="index" label="序号" width="55">
                <template slot-scope="scope"><span>{{scope.$index+(currentPage - 1) * pagesize + 1}} </span></template>
            </el-table-column>
            <el-table-column align="center" label="工单号" width="150" prop="id">
                <template slot-scope="scope">
                    <el-link :href="'#/workorderdetail/'+scope.row.order_prefix+'-'+scope.row.id" type="primary">{{scope.row.order_prefix}}-{{scope.row.id}}</el-link>
                </template>
            </el-table-column>
            <el-table-column align="center" v-for="(val, key, index) in TableColumn" v-if=" key != 'id' && key != 'status' && key !='create_time' && key !='update_time' && key !='content'" :key="index" :label="val" :prop="key" ></el-table-column>
            <el-table-column v-else-if="key =='status'" align="center" :label="TableColumn.status" prop="status" >
                <template slot-scope="scope">
                    <el-tag size="small" type="danger" v-if="scope.row.status == 0">已终止</el-tag>
                    <el-tag size="small" type="danger" v-else-if="scope.row.status == -1">已失败</el-tag>
                    <el-tag size="small" v-else-if="scope.row.status == 1">申请中</el-tag>
                    <el-tag size="small" type="success" v-else-if="scope.row.status == 2">已同意</el-tag>
                    <el-tag size="small" type="success" v-else-if="scope.row.status == 3">已完成</el-tag>
                    <el-tag size="small" type="danger" v-else="scope.row.status == 4">已驳回</el-tag>
                </template>
            </el-table-column>
            <el-table-column v-else-if="key =='create_time'" align="center" :label="TableColumn.create_time" prop="create_time" >
                <template slot-scope="scope">
                    {{scope.row.create_time | dateFormate}}
                </template>
            </el-table-column>
            <el-table-column v-else-if="key =='update_time'" align="center" :label="TableColumn.update_time" prop="update_time" >
                <template slot-scope="scope">
                    {{scope.row.update_time | dateFormate}}
                </template>
            </el-table-column>
            <el-table-column  align="center" label="操作">
            <template slot-scope="scope">
                <el-button @click="handleDetail(scope.$index,scope.row)" size="mini" type="primary">详情</el-button>
            </template>
            </el-table-column>
        </el-table>
        <el-pagination
        background
        layout="total, prev, pager, next, jumper"
        :total="TableData.length"
        :page-size="pagesize"
        @current-change="current_change">
        </el-pagination>
    </div>
</template>

<script>
import moment from 'moment';
import store from '@/store/store.js';
import { getWorkOrder } from '@/api/api.js';
export default {
    name: 'workordertable',
    data () {
        return {
            // 分页参数
            total: 0,
            currentPage: 1,
            pagesize: 15,
            
        }
    },
    props: {
        TableData: {
            type: Array
        },
        TableColumn: {
            type: Object
        },
        editData: {
            type: Function
        },
        delData: {
            type: Function
        },
    },
    filters: {
        dateFormate(date) {
            return moment(date).format("YYYY-MM-DD HH:mm:ss");
        }
    },
    methods: {
        handleDetail($index,row) {
            let params_data = {'workordernum':row.order_prefix+'-'+row.id,'workorderdata':row}
            this.$router.push({name:'workorderdetail',params:params_data})
        },
        handleSelectionChange(val) {
            this.multipleSelection = val; 
        },
        current_change(currentPage){
            this.currentPage = currentPage;
        },

    },
    mounted() {
        
    },
}
</script>

<style>
.workordertable .el-table__expanded-cell[class*=cell]{
    padding: 5px 62px;
}
.workordertable .demo-table-expand {
    font-size: 0;
}
.workordertable .demo-table-expand label {
    /* width: 100px; */
    font-size: 12px;
    color: #99a9bf;
}
.workordertable .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
}
.workordertable .el-table th{
    user-select: auto
}
</style>

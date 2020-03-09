<template>
    <div class="syslog">
        <el-row style="padding-bottom:5px;">
            <el-button @click="getDataList" style="float: left;" size="mini" type="primary" plain>重置</el-button>
            <div style="float: left;">
                <el-date-picker
                size="mini"
                v-model="timerange"
                type="datetimerange"
                value-format="yyyy-MM-dd H:mm:ss"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                @change="handleSearch('time')">
                </el-date-picker>
            </div>
            <el-input v-model="searchcontent" @keyup.enter.native="searchData" style="width: 200px;float: right;" size="small" placeholder="Search">
                <el-button @click="searchData" slot="append" icon="el-icon-search"></el-button>
            </el-input>
        </el-row>
        <el-row>
            <el-table
            size="small"
            ref="multipleTable"
            :data="table_data.slice((currentPage-1)*pagesize,currentPage*pagesize)"
            border
            strip
            style="width: 100%">
                <!-- <el-table-column align="center" type="selection" width="55"></el-table-column> -->
                <el-table-column align="center" type="index" label="序号" width="55">
                    <template slot-scope="scope"><span>{{scope.$index+(currentPage - 1) * pagesize + 1}} </span></template>
                </el-table-column>
                <el-table-column align="center" label="操作用户" prop="user"></el-table-column>
                <el-table-column align="center" label="操作类型" prop="event_type">
                    <template slot-scope="scope">
                        <el-tag size="small"  v-if="scope.row.event_type == 1">Create</el-tag>
                        <el-tag size="small" style="color:#fa8c16;background:#fff7e6;border-color:#ffd591;" type="warning" v-else-if="scope.row.event_type == 2">Update</el-tag>
                        <el-tag size="small" style="color:#13c2c2;background:#e6fffb;border-color:#87e8de;" type="warning" v-else-if="scope.row.event_type == 4">Many-to-Many Change</el-tag>
                        <el-tag size="small" style="color:#faad14;background:#fffbe6;border-color:#ffe58f;" type="warning" v-else-if="scope.row.event_type == 5">Reverse Many-to-Many Change</el-tag>
                        <el-tag size="small" type="danger" v-else="scope.row.event_type == 3">Delete</el-tag>
                    </template>
                </el-table-column>
                <el-table-column align="center" label="Models" prop="content_type"></el-table-column>
                <el-table-column align="center" label="Models-PK" prop="object_id"></el-table-column>
                <el-table-column align="center" label="时间" prop="datetime" >
                    <template slot-scope="scope">
                        {{scope.row.datetime | dateFormate}}
                    </template>
                </el-table-column>
                <el-table-column align="center" width="200" label="操作详情" >
                    <template slot-scope="scope">
                        <el-button plain @click="handleShow(scope.row.object_json_repr,scope.row.changed_fields)" size="mini" type="success">Show Info</el-button>
                        <!-- <el-button plain @click="handleShow('object',scope.row.object_json_repr)" size="mini" type="success">Models Object</el-button>
                        <el-button plain v-if="scope.row.changed_fields != null" @click="handleShow('fields',scope.row.changed_fields)" size="mini" type="warning">Changed Fields</el-button> -->
                    </template>
                </el-table-column>
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
        <el-row>
            <el-dialog
            title="操作详情" 
            :visible.sync="dialogVisible">
                <div class="syslog-results">
                    <!-- <pre v-if="showdata" class="syslog-results-content">{{JSON.stringify(JSON.parse(showdata.replace(/\s*/g,"")), null,4)}}</pre> -->
                    
                    <el-col :span="12" style="border-right:1px solid #dcdfe6">
                        <p>Models Object:</p>
                        <br>
                        <pre v-if="object_data" class="syslog-results-content">{{JSON.stringify(JSON.parse(object_data.replace(/\s*/g,"")), null,4)}}</pre>
                    </el-col>
                    <el-col style="padding-left: 8px;" v-if="change_fields" :span="12">
                        <p>Changed Fields:</p>
                        <br>
                        <pre class="syslog-results-content">{{JSON.stringify(JSON.parse(change_fields.replace(/\s*/g,"")), null,4)}}</pre>
                    </el-col>
                </div>
            </el-dialog>
        </el-row>
    </div>
</template>

<script>
import moment from 'moment';
import { getCrudEvent } from '@/api/conf.js';
export default {
    name:'syslog',
    data () {
        return {
            searchcontent: '',
            table_data: [],
            // 分页参数
            total: 0,
            currentPage: 1,
            pagesize: 15,
            //
            timerange: [],
            dialogVisible: false,
            object_data: '',
            change_fields: '',
            title: '',
        }
    },
    filters: {
        dateFormate(date) {
            return moment(date).format("YYYY-MM-DD HH:mm:ss");
        }
    },
    methods: {
        handleSizeChange(val){
            this.pagesize = val;
        },
        current_change(currentPage){
            this.currentPage = currentPage;
        },
        handleShow(object,fields) {
            this.object_data = object
            this.change_fields = fields
            this.dialogVisible = true
        },
        // handleShow(type,data) {
        //     this.title = ''
        //     if (type == 'object') {
        //         this.title = 'Models Object'
        //     }
        //     else if (type == 'fields') {
        //         this.title = 'Changed Fields'
        //     }
        //     this.dialogVisible = true
        //     this.showdata = data            
        // },
        handleSearch(searchtype) {
            let filter_data = {}
            filter_data.timerange = this.timerange
            getCrudEvent(filter_data).then((response) => {
                console.log(response.data);
                this.table_data = response.data.results
            }).catch((error) => {
                console.log(error);
            })
        },
        searchData() {

        },
        getDataList() {
            getCrudEvent().then((response) => {
                console.log(response);
                this.table_data = response.data.results
            })
        }
    },
    mounted() {
        this.getDataList()
    },
}
</script>

<style>
/* 结果样式 */
.syslog .syslog-results{
    text-align: left;
    border:1px solid #dcdfe6;
    /* height: 630px; */
    background-color: #494c4e;
    color: #b7e16b;
    padding-left: 8px;
    overflow: auto;
}
.syslog .syslog-results-index{
    font-size: 5px;
    padding-bottom: 4px;
    padding-left: 4px;
}
.syslog .syslog-results-content{
    /* padding: 1 */
}
/* 结果样式 */
.syslog .syslog-results::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
</style>
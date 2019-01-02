<template>

    <div id="query" class="query">
        <div id="query-db" class="query-db">
            <el-select v-model="selectdb" placeholder="请选择查询数据库" @change="handleSelect">
                <el-option 
                v-for="item in dblist" 
                :key="item.id"
                :label="item.dbname"
                :value="item.dbname">
                </el-option>
            </el-select>
        </div>
        <div id="query-sql" class="query-sql">
            <el-tabs v-model="sqltabsvalue" type="border-card" editable @edit="handleTabsEdit" @tab-click="handleClick">
                <el-tab-pane 
                v-for="(item,index) in sqltabs"
                :key="index"
                :label="item.title"
                :name="item.name">
                    <div class="query-sql-input-help">
                        <el-input class="query-sql-input" v-model="item.sql" type="textarea" placeholder="输入SQL语句，以分号结束，注意添加schema">
                        </el-input>
                        <div class="query-sql-help">
                            <el-alert title="SQL查询注意事项:" :closable="false" type="warning"></el-alert>
                            <el-alert title="Query标签可添加，最多添加5个" :closable="false" type="warning" show-icon></el-alert>
                            <el-alert title="支持单条语句查询" :closable="false" type="warning" show-icon></el-alert>
                            <el-alert title="查询语句默认添加limit 100，也可指定limit" :closable="false" type="warning" show-icon></el-alert>
                            <el-alert title="建议在所有的表名前加上库名限定，如dbname.tablename" :closable="false" type="warning" show-icon></el-alert>
                            <el-alert title="查询字段中无.符号，可采用别名，否则数据无法渲染" :closable="false" type="warning" show-icon></el-alert>
                        </div>
                    </div>
                    
                    <div id="query-sql-button" class="query-sql-button">
                        <el-button title="Exec" class="query-sql-button-exec" @click="execSQL" size="mini" circle>
                            <icon-svg class="query-sql-button-exec-icon" iconClass="icon-zhihangzhong"></icon-svg>
                        </el-button>
                        <el-button title="Explain" class="query-sql-button-exec" @click="explainSQL" size="mini" circle>
                            <icon-svg class="query-sql-button-exec-icon" iconClass="icon-explain"></icon-svg>
                        </el-button>
                        <el-button title="导出Excel" class="query-sql-button-exec" @click="exportExcel" size="mini" circle>
                            <icon-svg class="query-sql-button-exec-icon" iconClass="icon-excel"></icon-svg>
                        </el-button>
                    </div>
                    <div  class="query-sql-results-table">
                        <el-table element-loading-text="拼命加载中" v-loading="loading" style="width: 100%" highlight-current-row max-height="500" border :data="item.results.slice((currentPage-1)*pagesize,currentPage*pagesize)">
                            <el-table-column  align="center" v-for="(val, key) in item.col" :fixed="key===0?true:false" :key="key" :label="val" :prop="val">
                                <!-- <template slot-scope="scope">
                                    <span v-if="scope.row[val] == null ">NULL</span>
                                    <span v-else-if="scope.row[val] == '\u0001' ">b'1'</span>
                                    <span v-else-if="scope.row[val] == '\u0000' ">b'0'</span>
                                    <span v-else>{{scope.row[val]}}</span>
                                </template> -->
                            </el-table-column>
                        </el-table>
                        <el-pagination
                        background
                        layout="total, sizes,prev, pager, next, jumper"
                        :total="item.results.length"
                        :page-sizes="[10, 20, 30]"
                        :page-size="pagesize"
                        @current-change="handleCurrentChange"
                        @size-change="handleSizeChange">
                        </el-pagination>
                    </div>
                </el-tab-pane>
            </el-tabs>  
        </div>
    </div>
</template>

<script>
import store from '@/store/store.js'
import FileSaver from 'file-saver'
import XLSX from 'xlsx'
import Axios from '@/utils/axios.js';
export default {
    data() {
        return {
            loading: false,
            // 分页参数
            total: 0,
            currentPage: 1,
            pagesize: 20,
            currenttab: 0,
            sql: '',
            selectdb: '',
            dblist: [],
            sqltabsvalue: '1',
            sqltabs: [
                { title: 'Query', name: '1', sql:'',selectdb:'',col:[], results: []},
            ],
            tabIndex: 1
        }
    },
    methods: {
        generateExcelFileName(){
            var username = this.$store.getters.username
            var myDate = new Date();
            var fileDate = myDate.getFullYear().toString() + (myDate.getMonth() + 1).toString() + myDate.getDate().toString()
            var fileTime = myDate.getHours().toString() + myDate.getMinutes().toString() + myDate.getSeconds().toString()
            let ExcelFileName = username + '-' + fileDate + '-' + fileTime + '.xlsx'
            return ExcelFileName
        },
        exportExcel(){
            if (this.sqltabs[this.currenttab].results.length > 0) {
                // var tableid = '#' + this.sqltabs[this.currenttab].tableid
                // let wb = XLSX.utils.table_to_book(document.querySelector(tableid));
                // let wbout = XLSX.write(wb, { bookType: 'xlsx', bookSST: true, type: 'array' });
                let wb = { SheetNames: ['Sheet1'], Sheets: {}, Props: {} };
                wb.Sheets['Sheet1'] = XLSX.utils.json_to_sheet(this.sqltabs[this.currenttab].results);
                let wbout = XLSX.write(wb, { bookType: 'xlsx', bookSST: true, type: 'array' });
                var ExcelFileName = this.generateExcelFileName()
                try {
                    FileSaver.saveAs(new Blob([wbout], { type: 'application/octet-stream' }), ExcelFileName);
                } catch (e)
                {
                    if (typeof console !== 'undefined')
                        console.log(e, wbout)
                }
                return wbout
            }
            
        },
        requestSQL(querydata) {
            this.loading = true
            Axios.oPost('/query',querydata).then((response)=>{
                if (response) {
                    this.sqltabs[this.currenttab].col = response.data.col
                    this.sqltabs[this.currenttab].results = response.data.results
                    this.loading = false
                }                        
            }).catch((error) => {
                console.log(error);
            })
        },
        execSQL() {
            if(this.sqltabs[this.currenttab].selectdb.length > 0) {
                this.sql =  this.sqltabs[this.currenttab].sql
                var querydata = {}
                querydata.sql = this.sql
                querydata.dbname = this.sqltabs[this.currenttab].selectdb
                querydata.exectype = 'exec'
                this.requestSQL(querydata)
            }  
        },
        explainSQL() {
            if(this.sqltabs[this.currenttab].selectdb.length > 0) {
                this.sql =  this.sqltabs[this.currenttab].sql
                var querydata = {}
                querydata.sql = this.sql
                querydata.dbname = this.sqltabs[this.currenttab].selectdb
                querydata.exectype = 'explain'
                this.requestSQL(querydata)
            }  
        },
        handleCurrentChange(currentPage){
            this.currentPage = currentPage;
        },
        handleSizeChange(val){
            this.pagesize = val;
        },
        handleSelect(val){
            this.sqltabs[this.currenttab].selectdb = val
        },
        handleTabsEdit(targetName, action) {
            if(action === 'add') {
                if (this.sqltabs.length <5) {
                    let newTabName = ++this.tabIndex + ''
                    let newTitle = 'Query'
                    this.sqltabs.push({title:newTitle,name:newTabName,sql:'',selectdb:'',col:[], results: []})   
                }    
            }
            if(action === 'remove') {
                if (this.sqltabs.length >1) {
                    let tabs = this.sqltabs
                    let activeName = this.sqltabsvalue
                    if (activeName === targetName) {
                        tabs.forEach((tab,index) => {
                            if(tab.name === targetName) {
                                let nextTab = tabs[index + 1] || tabs[index - 1]
                                if(nextTab) {
                                    activeName = nextTab.name
                                }
                            }
                        });
                    }
                    this.sqltabsvalue = activeName
                    this.selectdb = this.sqltabs[this.sqltabsvalue -1 ].selectdb
                    this.sqltabs = tabs.filter(tab => tab.name !== targetName)
                }   
            }
        },
        handleClick(tab) {
            this.currenttab = tab.index
            this.selectdb = this.sqltabs[this.currenttab].selectdb
            // this.sqltabs[this.currenttab].tableid = 'reseltstable' + this.currenttab.toString()
        },
        getDbList() {
            var url = '/userinfo/' + this.$store.getters.username + '/'
            Axios.oGet(url).then((response)=>{
                if (response) {
                    var dblist = response.data.accessdb.split(",")
                    for (var i =0; i< dblist.length;i++) {
                        var useraccessdb = {}
                        useraccessdb.id = i
                        useraccessdb.dbname = dblist[i]
                        this.dblist.push(useraccessdb)
                    }
                }                        
            }).catch((error) => {
                console.log(error);
            })
        }
    },
    mounted() {
        this.getDbList()
    },
}
</script>

<style>
.query .el-table .cell{
    word-break:normal;
    white-space: nowrap;
}
.query .el-tabs__new-tab{
    position: absolute;
    z-index: 999;
}
.query .el-alert--warning {
    background-color: #fef0f0;
    color: #f56c6c;
    padding: 5px 16px;
}
.query .el-alert__title {
    font-size: 14px;
}
.query .query-sql-input-help{
   height: 190px; 
}
.query .el-textarea{
    float: left;
    width: 50%;
}
.query .query-sql-help{
    /* position: absolute; */
    top: 18px;
    /* margin-left: 820px; */
    float: left;

}
.el-select-dropdown .el-scrollbar .el-scrollbar__wrap{
    overflow: scroll;
}
.query .query-sql-button-exec.el-button{
    border: 0px;
    margin-left: 0px;
}
.query .query-sql-button-exec-icon.svg-icon{
    width:30px;
    height:30px;
}
.query .query-db{
    float: left;
    margin-top: 10px
}
.query .query-sql-button{
    float: left;
    /* margin-top: 10px;
    position: absolute; */
}
.query .el-textarea__inner{
    height: 190px;
    /* width: 50%; */
    float: left;
}
/* .query-sql-input{
    width: 50%;
    float: left;
} */
.query .query-sql{
    width: 96%;
    position: absolute;
    margin-top: 60px
}
.query .query-sql-results-table{
    margin-top: 50px;
}
.query .el-tabs__new-tab .el-icon-plus{
    /* font-size: 13px; */
    /* color: #f56c6c; */
    transform: scale(1.3,1.3);
    font-weight:bold;
}

</style>

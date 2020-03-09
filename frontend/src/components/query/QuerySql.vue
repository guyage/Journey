<template>
    <div class="querysql" id="querysql">
        <el-row>
            <div class="querysql-inst" >
                <div style="text-align:left;">
                    <label style="text-align:right;width:100px;display:inline-block;padding-left: 1px;font-size: 12px;">MySQL实例：</label>
                    <el-select size="small" style="width:300px;" v-model="selectinst" placeholder="请选择查询实例" @change="handleSelect">
                        <el-option 
                        v-for="item in instlist" 
                        :key="item.instid"
                        :label="item.instname"
                        :value="item.instid">
                        </el-option>
                    </el-select>
                </div>
                <div class="querysql-db" style="text-align:left;padding: 0.8em 0.2em 1em;">
                    <label style="text-align:right;width:100px;display:inline-block;font-size: 12px;">MySQL数据库：</label>
                    <el-radio-group size="small"  v-model="selectdb">
                        <el-radio border v-for="(val, key) in dblist" :key="key" :label="val"></el-radio>
                    </el-radio-group>
                </div>
            </div>
        </el-row>
        <el-row >
            <el-col :span="12">
                <div class="querysql-sql-input">
                    <Editor ref="sqleditor"></Editor>
                </div>
            </el-col>
            <el-col :span="12">
                <div class="querysql-sql-help">
                    <el-alert title="SQL查询注意事项:" :closable="false" type="warning"></el-alert>
                    <el-alert title="SQL提示功能，可通过Alt+c键开启提示，或者点击输入框右上角提示按钮开启提示" :closable="false" type="warning" show-icon></el-alert>
                    <el-alert title="支持单条语句查询，查询语句默认添加limit 500，也可指定limit" :closable="false" type="warning" show-icon></el-alert>
                    <el-alert title="建议在所有的表名前加上库名限定，如dbname.tablename" :closable="false" type="warning" show-icon></el-alert>
                    <el-alert title="查询字段中带.符号，可采用别名，否则数据渲染有问题" :closable="false" type="warning" show-icon></el-alert>
                </div>
            </el-col>
        </el-row>
        <el-row>
            <div id="querysql-sql-button" class="querysql-sql-button">
                <el-button :loading="loading" title="Exec" class="querysql-sql-button-exec" @click="handleSql('exec')" size="mini" circle>
                    <icon-svg class="querysql-sql-button-exec-icon" iconClass="iconzhihangzhong"></icon-svg>
                </el-button>
                <el-button title="Explain" class="query-sql-button-exec" @click="handleSql('explain')" size="mini" circle>
                    <icon-svg class="querysql-sql-button-exec-icon" iconClass="iconexplain"></icon-svg>
                </el-button>
                <el-button title="导出Excel" class="query-sql-button-exec" @click="exportExcel" size="mini" circle>
                    <icon-svg class="querysql-sql-button-exec-icon" iconClass="iconexcel"></icon-svg>
                </el-button>
            </div>
        </el-row>
        <el-row>
            <div class="querysql-sql-results-table">
                <el-table size="small" :element-loading-text="loadingtext" v-loading="loading" style="width: 100%" highlight-current-row height="450" border :data="results.slice((currentPage-1)*pagesize,currentPage*pagesize)">
                    <el-table-column :width="val.length<5?((val.length+3)*13):val.length*13" align="center" v-for="(val, key) in col" :fixed="key===0?true:false" :key="key" :label="val" :prop="val">
                    </el-table-column>
                </el-table>
                <el-pagination
                small
                background
                layout="total, sizes,prev, pager, next, jumper"
                :total="results.length"
                :page-sizes="[10, 20, 30]"
                :page-size="pagesize"
                @current-change="handleCurrentChange"
                @size-change="handleSizeChange">
                </el-pagination>
            </div>
        </el-row>
        
    </div>
</template>

<script>
import FileSaver from 'file-saver';
import XLSX from 'xlsx';
import store from '@/store/store.js';
import Editor from '@/components/common/Editor.vue';
import { getUserAccessDb,getMysqlMeta } from '@/api/db.js';
import { execQuerySql } from '@/api/query.js';
export default {
    name: 'querysql',
    components: {
      Editor  
    },
    data () {
        return {
            loading: false,
            loadingtext: '拼命加载中...',
            // 分页参数
            total: 0,
            currentPage: 1,
            pagesize: 10,
            activeNames: ['1'],
            instlist: [],
            dblist: [],
            //查询结果
            selectinst: '',
            selectdb: '',
            sql: '',
            results:[],
            col: [],
        }
    },
    watch: {
        selectdb (val) {
            let meta_data = {}
            let tables_hint = {}
            meta_data.type = 'table'
            meta_data.instid = this.selectinst
            meta_data.dbname = this.selectdb
            if (val) {
                getMysqlMeta(meta_data).then((response) => {
                    if (response) {
                        let colname = response.data.col[0]
                        for (let i=0;i<response.data.results.length;i++) {
                            let tablename = response.data.results[i][colname];
                            tables_hint[tablename] = []
                        }
                    }
                    this.$refs.sqleditor.cmOption.hintOptions.tables = tables_hint
               }).catch((error) => {
                   console.log(error);
               })
            }
        }
    },
    methods: {
        generateExcelFileName(){
            let username = this.$store.getters.username
            let myDate = new Date();
            let fileDate = myDate.getFullYear().toString() + (myDate.getMonth() + 1).toString() + myDate.getDate().toString()
            let fileTime = myDate.getHours().toString() + myDate.getMinutes().toString() + myDate.getSeconds().toString()
            let ExcelFileName = username + '-' + fileDate + '-' + fileTime + '.xlsx'
            return ExcelFileName
        },
        exportExcel() {
            if (this.results.length > 0) {
                let wb = { SheetNames: ['Sheet1'], Sheets: {}, Props: {} };
                wb.Sheets['Sheet1'] = XLSX.utils.json_to_sheet(this.results);
                let wbout = XLSX.write(wb, { bookType: 'xlsx', bookSST: true, type: 'array' });
                let ExcelFileName = this.generateExcelFileName()
                try {
                    FileSaver.saveAs(new Blob([wbout], { type: 'application/octet-stream' }), ExcelFileName);
                } catch (e)
                {
                    if (typeof console !== 'undefined')
                        console.log(e, wbout)
                }
                return wbout
            }
            else {
                this.$notify({title: '提示',message:'无数据，导出Excel异常！',type: 'warning'})
            }
        },
        handleSql(action) {
            if (this.selectinst > 0 && this.selectdb.length > 0) {
                let querysql_data = {}
                querysql_data.instid = this.selectinst
                querysql_data.dbname = this.selectdb
                querysql_data.sql = this.$refs.sqleditor.code
                if (action == 'exec') {
                    this.loading = true
                    querysql_data.exectype = 'exec'
                    querysql_data.username = this.$store.getters.username 
                }
                else if (action == 'explain') {
                    querysql_data.exectype = 'explain'
                }
                execQuerySql(querysql_data).then((response) => {
                    if (response) {
                        this.col = response.data.col;
                        this.results = response.data.results
                        this.loading = false
                    }
                }).catch((error) =>{
                    console.log(error);
                    this.loading = false
                })
            }
            else {
                this.$notify({title: '提示',message:'数据库和SQL语句不能为空！',type: 'warning'})
            }
        },
        handleCurrentChange(currentPage){
            this.currentPage = currentPage;
        },
        handleSizeChange(val){
            this.pagesize = val;
        },
        handleSelect(val){
            this.selectinst = val
            this.dblist = []
            getUserAccessDb({'dbtype':'mysqldb','mysqlinst':{'id':val},'username':store.getters.username}).then((response) => {
                if (response) {
                    for (let i=0;i<response.data.results.length;i++) {
                        this.dblist.push(response.data.results[i].dbname)
                    }
                }
            }).catch((error) => {
                console.log(error);
            })
            
        },
        getUserAccessInst() {
            getUserAccessDb({'dbtype':'mysqlinst','username':store.getters.username}).then((response) => {
                if (response.data.results.length > 0) {
                    for (let i =0; i< response.data.results.length;i++) {
                        this.instlist.push({'instid':response.data.results[i].instid,'instname':response.data.results[i].instname})
                    }
                }
                else {
                    this.$notify({title: '提示',message:'无可访问数据库，请先申请数据库权限！',type: 'warning'})
                }
            }).catch((error) => {
                console.log(error);
            })
        }
    },
    mounted () {
        this.getUserAccessInst()
    }

}
</script>

<style>
/* 选择框样式 */
.querysql .querysql-inst{
    float: left;
    /* margin-top: 10px; */
}
.querysql .editor .cm-s-solarized.cm-s-light{
    height: 200px;
}
.querysql .querysql-sql-input{
    /* width: 50%; */
    text-align: left;
    /* float: left;  */
    /* clear: both; */
}
.querysql .querysql-sql-help{
    /* width: 50%; */
    /* float: right;  */
    height: 200px;
    text-align: left;
    
}
.querysql .querysql-sql-button{
    float: left;
    padding: 0.5em 0.1em 0.5em;
    clear: both;
}
/* 表格样式 */
.querysql .el-table th{
    user-select: auto
}
.querysql .el-table .cell{
    white-space: nowrap
}
.querysql .el-radio{
   margin-right: 0px!important; 
}


</style>

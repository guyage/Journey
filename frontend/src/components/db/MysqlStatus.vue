<template>
    <div class="mysqlstatus">
        <div class="mysqlstatus-inst">
            <el-select v-model="selectinst" placeholder="请选择MySQL实例" @change="handleSelect">
                <el-option 
                v-for="item in instlist" 
                :key="item.instid"
                :label="item.instname"
                :value="item.instid">
                </el-option>
            </el-select>
        </div>
        <div class="mysqlstatus-button">
            <el-button @click="getMysqlInstStatus('full')" type="primary">SHOW FULL PROCESSLIST</el-button>
            <el-button @click="getMysqlInstStatus('active')" type="primary">SHOW ACTIVE</el-button>
            <el-button @click="getMysqlInstStatus('innodb')" type="primary">SHOW ENGINE INNODB STATUS</el-button>
            <el-button @click="getMysqlInstStatus('master')" type="primary">SHOW MASTER STATUS</el-button>
            <el-button @click="getMysqlInstStatus('slave')" type="primary">SHOW SLAVE STATUS</el-button>
        </div>
        <div class="mysqlstatus-results">
            <el-table v-if="results.length > 0 && type != 'innodb' && type != 'slave'" size="mini" style="width: 100%" highlight-current-row show-overflow-tooltip="true" max-height="700" border :data="results.slice((currentPage-1)*pagesize,currentPage*pagesize)">
                <el-table-column  align="center" v-for="(val, key) in col"  :key="key" :label="val" :prop="val">
                </el-table-column>
                <el-table-column v-if="type == 'full' || type == 'active'" width="100px" align="center" label="操作">
                <template slot-scope="scope">
                    <el-button size="mini" type="danger" @click="handleKillSession(scope.$index,scope.row)">KILL</el-button>
                </template>
                </el-table-column>
            </el-table>
            <el-table  v-if="results.length > 0 && type == 'slave'" size="mini" style="width: 100%" highlight-current-row show-overflow-tooltip="true" max-height="700" border :data="results.slice((currentPage-1)*pagesize,currentPage*pagesize)">
                <el-table-column :width="val.length*12" align="center" v-for="(val, key) in col"  :key="key" :label="val" :prop="val">
                </el-table-column>
            </el-table>
            <div class="mysqlstatus-innodbresults">
                <el-table  v-if="results.length > 0 && type == 'innodb'" size="mini" style="width: 100%" highlight-current-row max-height="700" border :data="results.slice((currentPage-1)*pagesize,currentPage*pagesize)">
                    <el-table-column align="center" v-for="(val, key) in col" v-if="val == 'Status'" :fixed="key===0?true:false" :key="key" :label="val" :prop="val">
                    </el-table-column>
                </el-table>
            </div>
            
            <el-pagination
            v-if="results.length > 0"
            background
            layout="total, sizes,prev, pager, next, jumper"
            :total="results.length"
            :page-sizes="[10, 20, 30]"
            :page-size="pagesize"
            @current-change="handleCurrentChange"
            @size-change="handleSizeChange">
            </el-pagination>
        </div>
    </div>
</template>

<script>
import store from '@/store/store.js';
import { getUserAccessDb,getMysqlStatus } from '@/api/api.js';
export default {
    name: 'mysqlstatus',
    data () {
        return {
            // 分页参数
            total: 0,
            currentPage: 1,
            pagesize: 20,
            currenttab: 0,
            instlist: [],
            selectinst: '',
            results: [],
            col: [],
            type: ''
        }
    },
    methods: {
        handleCurrentChange(currentPage){
            this.currentPage = currentPage;
        },
        handleSizeChange(val){
            this.pagesize = val;
        },
        handleSelect(val){
            this.selectinst = val
        },
        handleKillSession($index,row){
            console.log(row);
            var real_index = $index+(this.currentPage - 1) * this.pagesize
            this.results.splice(real_index, 1)
            let dropinfo = '确认删除<strong style="color:red;">会话ID:'+row.ID+'</strong>'
            this.$confirm(dropinfo, '提示',{
                dangerouslyUseHTMLString: true,
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
            })
            .then(_=> {
                let request_data = {}
                request_data.instid = this.selectinst
                request_data.sessionid = row.ID
                request_data.type = 'kill'
                getMysqlStatus(request_data).then((response) => {
                    if (response) {
                        this.$message.success('KILL成功!');
                    }
                }).catch((error) => {
                    console.log(error);
                })
            })
            .catch(_=>{})
        },
        getMysqlInstStatus(type){
            if (this.selectinst) {
                let request_data = {}
                request_data.instid = this.selectinst
                if (type=='full') {
                    request_data.type = 'full'
                }
                else if (type=='active') {
                    request_data.type = 'active'
                }
                else if (type=='innodb') {
                    request_data.type = 'innodb'
                }
                else if (type=='master') {
                    request_data.type = 'master'
                }
                else if (type=='slave') {
                    request_data.type = 'slave'
                }
                getMysqlStatus(request_data).then((response)=>{
                    if (response) {
                        this.col = response.data.col
                        this.results = response.data.results
                        this.type = request_data.type
                        if (this.results == 0) {
                            this.$notify({title: '提示',message:'无结果返回!',type: 'info'})
                        }
                    }                        
                }).catch((error) => {
                    console.log(error);
                })
                }
            
        },
        getInstList() {
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
    mounted() {
        this.getInstList()
    },
    
}
</script>

<style>
/* 表格样式 */
.mysqlstatus .el-table th{
    user-select: auto
}
.mysqlstatus .el-table .cell{
    white-space: nowrap
}
.el-select-dropdown .el-scrollbar .el-scrollbar__wrap{
    overflow: scroll;
}
.mysqlstatus .mysqlstatus-inst{
    float: left;
}
.mysqlstatus .mysqlstatus-button{
    clear: both;
    float: left;
    margin-top: 0.5em;
    margin-bottom: 1em;
}
.mysqlstatus .el-button+.el-button{
    margin-left: 0px!important;
}
.mysqlstatus .el-table--mini, .el-table--small, .el-table__expand-icon{
    font-size: 13px;
}
.mysqlstatus-innodbresults .el-table .cell{
    white-space: pre;
    text-align: left;
    font-size: 13px
}
</style>


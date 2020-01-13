<template>
    <div class="newsqlorder">
        <el-row>
            <div >
                <el-form size="small" ref="form" :rules="rules" :model="form" label-position="right" label-width="100px">
                    <el-col :span="6">
                    <div>
                    <el-form-item label="工单类型:" prop="ordertype">
                        <el-select style="width:100%;" @change="handleSelectOrderType($event)" v-model="form.ordertype" placeholder="请选择工单类型">
                            <el-option 
                            v-for="item in ordertypelist"
                            :key="item.id"
                            :label="item.ordertype"
                            :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    </div>
                    </el-col >
                    <el-col :span="12">
                        <div>
                            <el-form-item label="工单主题:" prop="title">
                                <el-input style="width:80%;float:left;" v-model="form.title" placeholder="请输入工单主题"></el-input>
                                <el-button size="mini" type="primary" @click="addSqlText">新增SQL</el-button>
                            </el-form-item>
                            <!-- <el-form-item label="">
                                <el-button type="primary" @click="addSqlText">新增SQL内容</el-button>
                            </el-form-item> -->
                        </div>
                    </el-col >
                </el-form>
            </div>
        </el-row>
        <div v-if="is_file == 'DISABLED'">
            <el-row>
            
            <el-col :span="6">
                <div>
                    <el-form size="small" ref="dbnameform" :model="sqlform" label-position="right" label-width="100px">
                        <el-form-item
                        style="height:100px;"
                        v-for="(item,index) in sqlform.sqlcontent"
                        :key = "index"
                        :label="'数据库-' + index + ':'"
                        :prop="'sqlcontent.' + index + '.dbname'"
                        :rules="[
                            { required: true, message: '请选择数据库', trigger: 'blur' },
                        ]">
                            <el-cascader
                            clearable
                            style="width:100%;"
                            v-model="item.dbname"
                            :options="instlist"
                            :props="dblist"></el-cascader>
                        </el-form-item>
                    </el-form>
                </div>
            </el-col>
            <el-col :span="12">
                <div>
                    <el-form size="small" ref="sqlform" :model="sqlform" label-position="right" label-width="100px">
                        <el-form-item
                        style="height:100px;"
                        v-for="(item,index) in sqlform.sqlcontent"
                        :key = "index + 100"
                        :label="'SQL-' + index + ':'"
                        :prop="'sqlcontent.' + index + '.sqltext'"
                        :rules="[
                            { required: true, message: '请输入SQL，以分号结尾', trigger: 'blur' },
                        ]">
                            <el-input  rows="4" style="width:80%;float:left;" type="textarea" v-model="item.sqltext"></el-input><el-button v-if="index > 0" @click.prevent="removeSqlText(item)">删除</el-button>
                            <!-- <div class="sql-order-editor" style="text-align:left;">
                                <codemirror ref="editor" @keyup.alt.67.native="showSqlHint"  v-model="item.sqltext" :options="cmOption"></codemirror>
                                <el-button v-if="index > 0" @click.prevent="removeSqlText(item)">删除</el-button>
                            </div> -->
                        </el-form-item>
                    </el-form>
                </div>
            </el-col>
        </el-row>
        <el-row>
            <el-button style="float:left;" size="mini" type="primary" @click="handleCheck()">审核</el-button>
        </el-row>
        <el-row>
            <el-dialog
            title="审核结果"
            :visible.sync="dialogVisible"
            width="80%"
            :before-close="handleClose">
            <div v-if="is_show">
                <el-alert v-if="checkinfo_data.length > 0" title="审核失败，请修改后重新审核!" type="error" effect="dark" :closable="false"></el-alert>
                <el-alert v-if="checkinfo_data.length == 0" title="审核通过!" type="success" effect="dark" :closable="false"></el-alert>
                <el-table v-if="checkinfo_data.length > 0" size="mini" style="width: 100%" highlight-current-row height="450" border :data="checkinfo_data.slice((currentPage-1)*pagesize,currentPage*pagesize)">
                    <!-- <el-table-column align="center" v-for="(val, key, index) in checkinfo_col" :key="index" :label="val" :prop="key"></el-table-column> -->
                    <!-- <el-table-column width="50" align="center" label="ID" prop="ID"></el-table-column> -->
                    <el-table-column width="100" align="center" label="步骤" prop="stage"></el-table-column>
                    <!-- <el-table-column width="80" align="center" label="步骤级别" prop="errlevel"></el-table-column> -->
                    <el-table-column width="150" align="center" label="步骤状态" prop="stagestatus"></el-table-column>
                    <el-table-column align="left" label="步骤信息" prop="errormessage"></el-table-column>
                    <el-table-column align="left" label="SQL" prop="SQL"></el-table-column>
                    <el-table-column width="100" align="center" label="影响行数" prop="Affected_rows"></el-table-column>
                </el-table>
                <el-pagination
                v-if="checkinfo_data.length > 0"
                mini
                background
                layout="total, sizes,prev, pager, next, jumper"
                :total="checkinfo_data.length"
                :page-sizes="[10, 20, 30]"
                :page-size="pagesize"
                @current-change="handleCurrentChange"
                @size-change="handleSizeChange">
                </el-pagination>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button size="mini" @click="dialogVisible = false">取消</el-button>
                <el-button v-loading="loading" size="mini" v-if="checkinfo_data.length == 0" type="primary" @click="handleSumit()">提交SQL工单</el-button>
            </span>
            </el-dialog>
        </el-row>
        </div>
        <div v-if="is_file == 'ENABLED'">
            <el-row style="margin-top:20px;">
                <SqlFile ref="sqlfile"></SqlFile>
            </el-row>
            <el-row style="float:left;margin-top:50px;">
                <el-button size="mini" type="primary" @click="handleSumitSqlFile()">提交SQL工单</el-button>
            </el-row>
        </div>
    </div>
</template>



<script>
import store from '@/store/store.js';
import SqlFile from './SqlFile.vue';
import { getSqlOrderType,getMysqlInst,getMysqlMeta,addSqlOrder,Inception } from '@/api/api.js';
export default {
    name: 'newsqlorder',
    components: {
        SqlFile
    },
    data () {
        return {
            dblist: {
                lazy: true,
                lazyLoad (node, resolve) {
                    if (node.level == 1 ) {
                        getMysqlMeta({'type':'database','instid':node.data.value}).then((response) => {
                            const dbnames = response.data.results.map(item => ({
                                value: item.table_schema,
                                label: item.table_schema,
                                leaf: node.level >= 1
                            }))
                            resolve(dbnames)
                        })
                    }
                    
                }
            },
            is_file: 'DISABLED',
            // 分页参数
            total: 0,
            currentPage: 1,
            pagesize: 10,
            form: {
                title: '',
                ordertype: '',
                creator: '',
                operator: '',
            },
            sqlform: {
                sqlcontent: [{dbname: '',sqltext: ''}]
            },
            rules: {
                ordertype: [
                    { required: true, message: '请选择工单类型', trigger: 'change' }
                ],
                title: [
                    { required: true, message: '请输入工单主题', trigger: 'blur' },
                ],
            },
            dialogVisible: false,
            ordertypelist: [],
            instlist: [],
            checkinfo_data: [],
            is_show: false,
            loading: false,
        }
    },
    methods: {
        handleSumitSqlFile() {
            this.$refs['form'].validate((valid) => {
                if (valid) {
                    this.loading = true;
                    addSqlOrder(this.form).then((response) => {
                        this.loading = false;
                        this.$message.success('提交成功!');
                        if (response) {
                            this.$refs.sqlfile.submitUpload(response.data.id)
                            this.$router.push({ path: '/mysqlorder'})
                        }
                    }).catch((error) => {
                        this.$message.error('提交失败!');
                        console.log(error);
                        this.dialogVisible = false;
                        this.loading = false;
                    })
                } else {
                    return false;
                }
            })
        },
        handleSumit() {
            this.loading = true;
            this.form.sql_data = this.sqlform
            this.$confirm('确认提交?')
            .then(_ => {
                addSqlOrder(this.form).then((response) => {
                    this.$message.success('提交成功!');
                    this.dialogVisible = false;
                    this.loading = false;
                    this.$router.push({ path: '/mysqlorder'})
                }).catch((error) => {
                    this.$message.error('提交失败!');
                    console.log(error);
                    this.dialogVisible = false;
                    this.loading = false;
                })
            })
            .catch(_ => {});
            
        },
        handleSelectOrderType(val) {
            let selectordertype = []
            selectordertype = this.ordertypelist.filter(item => item.id === val);
            this.is_file = selectordertype[0].is_file
            console.log(this.is_file);
            
        },
        handleCheck() {
            this.$refs['form'].validate((valid) => {
                if (valid) {
                    this.$refs['dbnameform'].validate((valid) => {
                        if (valid) {
                            this.$refs['sqlform'].validate((valid) =>{
                                if (valid) {
                                    this.checkSql()
                                } else {
                                    return false;
                                }
                            })
                        }
                        else {
                            return false;
                        }
                    })
                } else {
                    return false;
                }
            })
        },
        handleClose(done) {
            this.$confirm('确认关闭？')
            .then(_ => {
                done();
            })
            .catch(_ => {});
        },
        checkSql() {
            this.is_show = false,
            this.checkinfo_data = []
            for (let i=0;i<this.sqlform.sqlcontent.length;i++) {
                let check_data = {}
                check_data.type = 'check'
                check_data.sql_data = this.sqlform.sqlcontent[i]
                console.log(check_data);
                
                Inception(check_data).then((response) => {
                    this.checkinfo_data.push(...response.data.results)
                    this.is_show = true                    
                })
            }
            console.log(this.checkinfo_data);
            
            this.dialogVisible = true;
        },  
        addSqlText() {
            this.sqlform.sqlcontent.push({dbname: '',sqltext: ''})
        },
        removeSqlText(item) {
            let index = this.sqlform.sqlcontent.indexOf(item)
            if (index !== -1) {
            this.sqlform.sqlcontent.splice(index, 1)
            }
        },
        getMySQLInst() {
            getMysqlInst().then((response) => {
                for (let i=0;i<response.data.length;i++) {
                    this.instlist.push({'value':response.data[i].id,'label':response.data[i].inst_name})
                }
            }).catch((error) => {
                console.log(error);
            })
        },
        getSqlOrderType() {
            getSqlOrderType().then((response) => {
                this.ordertypelist = response.data
            }).catch((error) => {
                console.log(error);
            })
        },
        handleCurrentChange(currentPage){
            this.currentPage = currentPage;
        },
        handleSizeChange(val){
            this.pagesize = val;
        },
    },
    mounted() {
        this.getSqlOrderType()
        this.getMySQLInst()
        this.form.creator = store.getters.username
        this.form.operator = store.getters.username
    },
}
</script>

<style>
/* 表格样式 */
.newsqlorder .el-table th{
    user-select: auto
}
.newsqlorder .el-table .cell{
    white-space: pre;
    overflow: auto;
    text-overflow: unset;
}
/* 设置滚动条的样式 */
.newsqlorder .el-table--border::-webkit-scrollbar,.newsqlorder .el-table .cell::-webkit-scrollbar {
    width: 4px;
    height: 6px;
}
/* 滚动槽 */
.newsqlorder .el-table--border::-webkit-scrollbar-track,.newsqlorder .el-table .cell::-webkit-scrollbar-track{
    border-radius: 2px;
    /* background: hsla(220,4%,58%,.3); */
    /* background: rgba(0, 0, 0, 0.3); */
}
/* 滚动条滑块 */
.newsqlorder .el-table--border::-webkit-scrollbar-thumb,.newsqlorder .el-table .cell::-webkit-scrollbar-thumb{
    border-radius: 2px;
    background: hsla(220,4%,58%,.3);
    /* background: rgba(0, 0, 0, 0.3); */
}
/* 编辑器样式 */
/* .sql-order-editor .cm-s-solarized.cm-s-light .CodeMirror-gutters{
    background-color: #eee; 
}
.sql-order-editor .cm-s-solarized.cm-s-light{
  background-color: #f4f4f5;
  height: 150px;
}
.sql-order-editor .editor-sqlformat{
    position: absolute;
    top: 7px;
    right: 15px;
}
.sql-order-editor .el-alert{
    padding: 1px 1px;
} */
</style> 
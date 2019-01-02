<template>
    <div class="sqlsoar">
        <div class="sqlsoar-input">
            <el-select v-model="selectdb" placeholder="请选择查询数据库" @change="handleSelect">
                <el-option 
                v-for="item in dblist" 
                :key="item.id"
                :label="item.dbname"
                :value="item.dbname">
                </el-option>
            </el-select>
            <!-- <el-input type="textarea" v-model="sql" placeholder="输入SQL语句，以分号结束，注意添加schema">
            </el-input> -->
            <div class="sqlsoar-input-codemirror">
                <SQLEditor ref="sqleditor"></SQLEditor>
                <!-- <codemirror v-model="code" :options="cmOption"></codemirror> -->
            </div>
            <div class="sqlsoar-button">
                <!-- <el-button type="primary" @click="handlesql('pretty')">语句美化</el-button> -->
                <el-button type="primary" @click="handlesql('optimize')">优化建议</el-button>
            </div>
        </div>
        <div class="sqlsoar-results">
            <el-alert
            title="结果说明：此结果仅提供优化建议，如执行后无Explain信息，则可能SQL语句有错误，或联系管理员。"
            type="info"
            show-icon
            :closable="false">
            </el-alert>
            <div class="sqlsoar-results-report" v-html="results"></div>
        </div>
    </div>
</template>

<script>
import marked from 'marked';
import Axios from '@/utils/axios.js';
import SQLEditor from './SQLEditor.vue';
export default {
    name: 'sqlsoar',
    components: {
      SQLEditor  
    },
    data () {
        return {
            dblist: [],
            selectdb: '',
            results: '',
            sql: ''
        }
    },
    methods: {
        handlesql(soar_type) {
            console.log('code',this.$refs.sqleditor.code);
            this.sql = this.$refs.sqleditor.code
            var soar_data = {}
            if (this.selectdb.length > 0 && this.sql.length> 0 ) {
                soar_data.dbname = this.selectdb
                soar_data.sql = this.sql
                if (soar_type === 'optimize') {
                    soar_data.soartype = 'optimize'
                    this.execSQLSoar(soar_data)
                }                
            }
            else {
              this.$notify({title: '提示',message:'数据库和SQL语句不能为空！',type: 'warning'})  
            }
        },
        execSQLSoar(soar_data) {
            Axios.oPost('sqlsoar',soar_data).then((response)=>{
                if (response) {
                    this.results = marked(response.data.results, { sanitize: true })
                }                        
            }).catch((error) => {
                console.log(error);
            })
        },
        handleSelect(val){
            this.selectdb = val
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
.sqlsoar{
    /* width: 500px;
    height: 90%;
    border: 10px; */
}
.sqlsoar .sqlsoar-results{
    float: right;
    width: 63%;
}
.sqlsoar .sqlsoar-input-codemirror{
    float: left;
    width: 100%;
    margin-top: 1em;
    text-align: left;
}
.el-select-dropdown .el-scrollbar .el-scrollbar__wrap{
    overflow: scroll;
}
.sqlsoar .sqlsoar-button{
    margin-top: 1em;
    float: left;
}
.sqlsoar .el-select{
    float: left;
}
.sqlsoar .sqlsoar-input{
    float: left;
    width: 35%; 
}
.sqlsoar .el-textarea__inner{
    height: 500px;
    margin-top: 20px;
}
/* soar结果样式 */
.sqlsoar .sqlsoar-results-report h1{
    margin-top: 1em;
    margin-bottom: 25px;
    font-size: 24px;
    text-align: left;
}
.sqlsoar .sqlsoar-results-report p{
    margin-top: 0;
    margin-bottom: 10px;
    text-align: left;
}
.sqlsoar .sqlsoar-results-report{
    font-style: normal;
    font-variant-ligatures: normal;
    font-variant-caps: normal;
    font-variant-numeric: normal;
    font-variant-east-asian: normal;
    font-weight: normal;
    font-stretch: normal;
    font-size: 13px;
    line-height: normal;
    font-family: "Myriad Pro", "Lucida Grande", Lucida, Verdana, sans-serif;
    text-align: left;
}
.sqlsoar .sqlsoar-results-report pre{
    border: 1px solid #dcdfe6;
    background: #f1f5f9;
    margin: 20px 0;
    padding: 8px;
    font-size: 11px;
}

.sqlsoar .sqlsoar-results-report h2{
    margin-top: 1em;
    font-size: 20px;
    padding-bottom: 2px;
    border-bottom: 1px solid #dcdfe6;
}
.sqlsoar .sqlsoar-results-report h3{
    font-size: 16px;
}
.sqlsoar .sqlsoar-results-report h3,.sqlsoar .sqlsoar-results-report h4{
    margin-top: 1em;
}
.sqlsoar .sqlsoar-results-report h3,.sqlsoar .sqlsoar-results-report h4,.sqlsoar .sqlsoar-results-report h5,.sqlsoar .sqlsoar-results-report h6{
    margin-bottom: .5em;
}

.sqlsoar .sqlsoar-results-report ul{
    list-style: square;
    margin: 0 0 0 30px;
    padding: 0 0 12px 6px;
}
.sqlsoar .sqlsoar-results-report ol{
    margin: 0 0 0 30px;
    padding: 0 0 12px 6px;
}
.sqlsoar .sqlsoar-results-report li{
    margin-top: 7px;
}
.sqlsoar .sqlsoar-results-report table{
    margin-top: 1em;
    border-top: 1px solid #dcdfe6;
    border-left: 1px solid #dcdfe6;
    border-spacing: 0;
    width: 100%;
    text-align: center;
}
.sqlsoar .sqlsoar-results-report thead,.sqlsoar .sqlsoar-results-report tbody{
    display: table-header-group;
    vertical-align: middle;
    border-color: inherit;
}
.sqlsoar .sqlsoar-results-report table th{
    padding: 4px 8px;
    background: #f4f4f5;
}
.sqlsoar .sqlsoar-results-report table td, table th{
    font-size: 14px;
    border-bottom: 1px solid #dcdfe6;
    border-right: 1px solid #dcdfe6;
}
</style>

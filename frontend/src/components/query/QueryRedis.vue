<template>
    <div class="queryredis">
        <div id="query-redis" class="query-redis">
            <el-tag>Redis实例：</el-tag>
            <el-select v-model="selectredis" placeholder="请选择Redis实例" @change="handleSelectredis" @visible-change="handleDropDown($event)">
                <el-option 
                v-for="item in redislist" 
                :key="item.id"
                :label="item.name"
                :value="item.name">
                </el-option>
            </el-select>
            <el-tag>Redis数据库：</el-tag>
            <el-select v-model="selectdb" @change="handleSelectdb" placeholder="请选择Redis数据库">
                <el-option
                v-for="item in redisdbcount"
                :key="item-1"
                :label="item-1"
                :value="item-1">
                </el-option>
            </el-select>
            <el-tag>Key：</el-tag>
            <el-input v-model="rediskey" style="width: 50em;" placeholder="请输入Key"></el-input>
            <el-button @click="execGet" type="primary" >Get</el-button>
        </div>
        <div v-if="results" class="query-redis-results">
            {{rediskey}} : {{results}}
        </div>

    </div>
</template>

<script>
import Axios from '@/utils/axios.js';
export default {
    name: 'queryredis',
    data () {
        return {
            redislist: [],
            selectredis: '',
            redisdbcount: 16,
            selectdb: '',
            results: '',
            rediskey: ''
        }
    },
    mounted() {
        this.getDbList()
    },
    methods: {
        execGet() {
            var querydata = {}
            querydata.rediskey = this.rediskey
            querydata.selectdb = this.selectdb
            querydata.selectredis = this.selectredis
            querydata.exectype = 'getkey'
            Axios.oPost('/redisdbquery',querydata).then((response)=>{
                if (response.data) {
                    this.results = response.data.results
                }
                else if (response.readyState ==4 )  {
                    this.loading = false
                    this.$notify({title: '提示',message:'查询超时，请重新查询！',type: 'error'})
                }                  
            }).catch((error) => {
                console.log(error);
            })
        },
        handleSelectdb(val){
            this.selectdb = val
        },
        handleSelectredis(val){
            this.selectredis = val
        },
        handleDropDown(event){
            if (event) {
                if (!this.redislist[0].name) {
                    this.$notify({title: '提示',message:'请先联系管理员配置可访问数据库！',type: 'warning'})
                }
            }
        },
        getDbList() {
            // var url = '/redisdb/' + this.$store.getters.username + '/'
            var url = '/redisdb/'
            Axios.oGet(url).then((response)=>{
                if (response) {
                    for (var i = 0;i< response.data.length;i++) {
                        var useraccessredis = {}
                        useraccessredis.id = i
                        useraccessredis.name = response.data[i].name
                        this.redislist.push(useraccessredis)
                    }
                    
                }                        
            }).catch((error) => {
                console.log(error);
            })
        }
    }
}
</script>

<style>
.queryredis .el-select-dropdown .el-scrollbar .el-scrollbar__wrap{
    overflow: scroll;
}
.queryredis .query-redis{
    float: left;
}
.queryredis .query-redis-results{
    clear:both;
    float: left;
    border:1px solid #dcdfe6;
    min-height: 100px;
    background-color: #494c4e;
    padding-left: 8px;
    color: #b7e16b;
    text-align: left;
    width: 87%;
    margin-top: 1em;
}
</style>

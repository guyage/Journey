<template>
    <div class="queryredis">
        <el-row>
            <div id="query-redis" class="query-redis">
                <el-tag>Redis实例：</el-tag>
                <el-select v-model="selectinst" placeholder="请选择Redis实例" @change="handleSelectredis">
                    <el-option 
                    v-for="item in instlist" 
                    :key="item.instid"
                    :label="item.instname"
                    :value="item.instid">
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
                {{results}}
            </div>
        </el-row>
    </div>
</template>

<script>
import store from '@/store/store.js';
import { getUserAccessDb } from '@/api/db.js';
import { execQueryRedis } from '@/api/query.js';
export default {
    name: 'queryredis',
    data () {
        return {
            activeNames: ['1'],
            instlist: [],
            selectinst: '',
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
            let querydata = {}
            querydata.rediskey = this.rediskey
            querydata.selectdb = this.selectdb
            querydata.selectredis = this.selectinst
            querydata.exectype = 'getkey'
            execQueryRedis(querydata).then((response) => {
                if (response.data.results) {
                    this.results = response.data.results
                }
                else {
                    this.results = "no results."
                }
            }).catch((error) => {
                console.log(error);
            })
        },
        handleSelectdb(val){
            this.selectdb = val
        },
        handleSelectredis(val){
            this.selectinst = val
        },
        getInstList() {
            getUserAccessDb({'dbtype':'redisinst','username':store.getters.username}).then((response) => {
                if (response) {
                    if (response.data.results.length > 0) {
                        for (let i =0; i< response.data.results.length;i++) {
                            this.instlist.push({'instid':response.data.results[i].instid,'instname':response.data.results[i].instname})
                        }
                    }
                    else {
                        this.$notify({title: '提示',message:'无可访问实例，请先申请实例权限！',type: 'warning'})
                    }
                    
                }
            }).catch((error) => {
                console.log(error); 
            })
            // var url = '/redisdb/' + this.$store.getters.username + '/'
            // var url = '/redisdb/'
            // Axios.oGet(url).then((response)=>{
            //     if (response) {
            //         for (var i = 0;i< response.data.length;i++) {
            //             var useraccessredis = {}
            //             useraccessredis.id = i
            //             useraccessredis.name = response.data[i].name
            //             this.redislist.push(useraccessredis)
            //         }
                    
            //     }                        
            // }).catch((error) => {
            //     console.log(error);
            // })
        }
    },
    mounted() {
        this.getInstList()
    }
}
</script>

<style>
/* .queryredis .el-select-dropdown .el-scrollbar .el-scrollbar__wrap{
    overflow: scroll;
} */
.queryredis .el-collapse-item__header.is-active,.queryredis .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
    border-bottom: 1px solid #dcdfe6;
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

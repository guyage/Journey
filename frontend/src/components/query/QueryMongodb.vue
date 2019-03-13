<template>

    <div id="querymongodb" class="querymongodb">
        <div id="querymongodb-sql" class="querymongodb-sql">
            <div id="querymongodb-db" class="querymongodb-db">
            <el-input
            class="dbmeta-filterinput"
            placeholder="输入关键字进行过滤"
            v-model="filterText">
            </el-input>
            <el-tree
            class="filter-tree"
            ref="tree"
            :data="treedata"
            lazy
            accordion
            :load="loadTreeData"
            highlight-current
            :props="treeprops"
            :filter-node-method="filterNode"
            @node-click="handleNodeClick">
            </el-tree>
            </div>
            <div class="querymongodb-input-results">
                <div class="querymongodb-input-db">
                    <span>当前选中db：</span>
                    <span>{{db}}</span>
                    <!-- <el-tag>{{db}}</el-tag> -->
                </div>
                <div class="querymongodb-input">
                    <el-input  v-model="sql" style="width: 90em;" placeholder="输入MongoDB查询">
                    </el-input>
                    <el-button type="primary" @click="execQuery">查询</el-button>
                </div>
                
                <div class="querymongodb-results">
                    <label v-for="(item, index) in results" :key="index">
                        <p class="querymongodb-results-index">/* {{index + 1}} */</p>
                        <pre class="querymongodb-results-content">{{JSON.stringify(JSON.parse(item.replace(/\s*/g,"")), null,4)}}</pre>
                        <br>
                    </label>
                    <!-- <pre v-for="(item, index) in results" :key="index">{{JSON.stringify(JSON.parse(item.replace(/\s*/g,"")), null,4)}}</pre>  -->
                </div>
            </div>
            
        </div>
    </div>
</template>

<script>
import Axios from '@/utils/axios.js';
export default {
    name: 'querymongodb',
    data () {
        return {
            // tree组件参数
            treeprops: {
                children: 'children',
                label: 'label'
            },
            treedata: [],
            filterText: '',
            db: '',
            collection: '',
            sql: '',
            results: ''
        }
    },
    watch: {
        filterText (val) {
            this.$refs.tree.filter(val);
        },
    },
    methods: {
        handleNodeClick(data) {
            if (!data.id) {
                console.log(data);
                this.db = data.label
            }
        },
        filterNode(value, data) {
            if (!value) return true;
            return data.label.indexOf(value) !== -1;
        },
        execQuery() {
            console.log(this.sql);
            var request_data = {}
            request_data.exectype = 'sql'
            request_data.dbname = this.db
            request_data.sql = this.sql
            console.log(request_data);
            
            Axios.oPost('/mongodbquery/',request_data).then((respone) => {
                if(respone) {
                    console.log(respone.data);
                    
                    // var str_pretty = JSON.stringify(respone.data.results, null, 4)
                    this.results = respone.data.results
                }
            }).catch((error) => {
                console.log(error);
            })
        },
        getDbList() {
            // var url = '/userinfo/' + this.$store.getters.username + '/'
            var url = '/mongodbdb/'
            Axios.oGet(url).then((response)=>{
                if (response) {
                    // this.treedata.push(response.data.accessdb.split(","))
                    // var dblist = response.data.accessdb.split(",")
                    for (var i =0; i< response.data.length;i++) {
                        var treedb = {}
                        // treedb.label = dblist[i]
                        treedb.label = response.data[i].dbname
                        this.treedata.push(treedb)
                    }                    
                }                        
            }).catch((error) => {
                console.log(error);
            })
        },
        loadTreeData (node,resolve) {
            if (node.level ==1) {
                var treetable = []
                var meta_data = {}
                meta_data.exectype = 'table'
                meta_data.dbname = node.data.label
                Axios.oPost('/mongodbquery/',meta_data).then((respone) => {
                    if(respone) {
                        for (var i = 0; i< respone.data.results.length; i++) {
                            var treetablenode = {}
                            treetablenode.id = i + 1
                            treetablenode.label = respone.data.results[i]
                            treetable.push(treetablenode)
                        }
                        return resolve(treetable)
                    }
                }).catch((error) => {
                    console.log(error);
                })
            }
            else {
                return resolve([])
            }
        },
    },
    mounted() {
        this.getDbList()
    },
}
</script>

<style>
/* 设置滚动条的样式 */
.querymongodb .querymongodb-db::-webkit-scrollbar {
    width: 4px;
    height: 6px;
}
/* 滚动槽 */
.querymongodb .querymongodb-db::-webkit-scrollbar-track{
    border-radius: 2px;
    /* background: hsla(220,4%,58%,.3); */
    /* background: rgba(0, 0, 0, 0.3); */
}
/* 滚动条滑块 */
.querymongodb .querymongodb-db::-webkit-scrollbar-thumb{
    border-radius: 2px;
    background: hsla(220,4%,58%,.3);
    /* background: rgba(0, 0, 0, 0.3); */
}
.querymongodb .el-tree-node>.el-tree-node__children{
    overflow: inherit;
    
}
.querymongodb .el-tree{
    /* border: 1px solid #dcdfe6; */
    height: 700px;
    margin-left: 1px;
}
.querymongodb .el-tree-node__content{
    position: relative;
}
.querymongodb .el-tree-node__label{
    font-size: 17px;
    position: absolute;
    padding-left: 30px;
}
.querymongodb .el-tree-node__content>.el-tree-node__expand-icon{
    position: absolute;
    top:4px;
}
.querymongodb .querymongodb-db{
    height: 700px;
    overflow:auto;
    float: left;
    /* margin-top: 55px; */
    width: 250px;
}
.querymongodb .querymongodb-sql{
    width: 98%;
    position: absolute;
    /* margin-top: 60px; */
    /* right: 10px; */
}
.querymongodb-input-results{
    width: 80%;
    margin-left: 15%;
    /* float: left; */
    /* height: 190px; */
}
.querymongodb .el-textarea__inner{
    height: 10px;
    text-decoration:none;
}
.querymongodb .querymongodb-input-db{
   float: left;
}
/* 结果样式 */
.querymongodb .querymongodb-results{
    text-align: left;
    border:1px solid #dcdfe6;
    height: 580px;
    background-color: #494c4e;
    color: #b7e16b;
    padding-left: 8px;
    overflow: auto;
}
.querymongodb .querymongodb-results-index{
    font-size: 5px;
    padding-bottom: 4px;
    padding-left: 4px;
}
.querymongodb .querymongodb-results-content{
    /* padding: 1 */
}
/* 结果样式 */
</style>

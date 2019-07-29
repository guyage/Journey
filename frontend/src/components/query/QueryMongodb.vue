<template>
    <div id="querymongodb" class="querymongodb">
        <el-collapse v-model="activeNames">
            <el-collapse-item title="QueryMongoDB" name="1">
                <div id="querymongodb-sql" class="querymongodb-sql" style="padding: 0.8em 0.2em 1em;">
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
                        </div>
                        <div class="querymongodb-input" style="padding: 2em 0em 0em;">
                            <el-input  v-model="sql" style="max-width:80%;float:left;" placeholder="输入MongoDB查询">
                            </el-input>
                            <el-button :loading="loading" type="primary" @click="execQuery">查询</el-button>
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
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script>
import store from '@/store/store.js';
import { getUserAccessDb,execQueryMongodb } from '@/api/api.js';
export default {
    name: 'querymongodb',
    data () {
        return {
            loading: false,
            activeNames: ['1'],
            // tree组件参数
            treeprops: {
                children: 'children',
                label: 'label'
            },
            treedata: [],
            filterText: '',
            selectinst: 0,
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
            if (data.type == 'inst') {
                this.selectinst = data.instid
            }
            else if (data.type == 'db') {
                this.db = data.label
            }

        },
        filterNode(value, data) {
            if (!value) return true;
            return data.label.indexOf(value) !== -1;
        },
        execQuery() {
            this.loading = true
            let request_data = {}
            request_data.exectype = 'sql'
            request_data.collectionname = this.db
            request_data.instid = this.selectinst
            request_data.sql = this.sql
            execQueryMongodb(request_data).then((response) => {
                    if (response) {
                        this.results = response.data.results
                    }
                    this.loading = false
                }).catch((error) => {
                    console.log(error);
                    this.loading = false
                })
        },
        getInstList() {
            getUserAccessDb({'dbtype':'mongodbinst','username':store.getters.username}).then((response) => {
                if (response) {
                    if (response.data.results.length > 0) {
                        for (let i =0; i< response.data.results.length;i++) {
                            let treedb = {}
                            treedb.type = 'inst'
                            treedb.instid = response.data.results[i].instid
                            treedb.label = response.data.results[i].instname
                            this.treedata.push(treedb)
                        }
                    }
                    else {
                        this.$notify({title: '提示',message:'无可访问实例，请先申请实例权限！',type: 'warning'})
                    }
                    
                }
            }).catch((error) => {
                console.log(error); 
            })
        },
        loadTreeData (node,resolve) {
            if (node.level == 1) {
                let treedb = []
                let meta_data = {}
                meta_data.exectype = 'db'
                meta_data.instid = node.data.instid
                meta_data.instname = node.data.label
                execQueryMongodb(meta_data).then((response) => {
                    if (response) {
                        for (let i=0;i<response.data.results.length;i++) {
                            if (response.data.results[i] != 'admin' && response.data.results[i] != 'local') {
                                let treenode = {}
                                treenode.type = 'db'
                                treenode.label = response.data.results[i]
                                treedb.push(treenode)
                            } 
                        }
                        return resolve(treedb)
                    }
                }).catch((error) => {
                    console.log(error);
                })
            }
            else if (node.level == 2) {
                let treecollection = []
                let meta_data = {}
                meta_data.exectype = 'collection'
                meta_data.instid = node.parent.data.instid
                meta_data.instname = node.parent.data.label
                meta_data.collectionname = node.data.label
                execQueryMongodb(meta_data).then((response) => {
                    if (response) {
                        for (let i=0;i<response.data.results.length;i++) {
                            if (response.data.results[i] != 'admin') {
                                let treenode = {}
                                treenode.type = 'collection'
                                treenode.label = response.data.results[i]
                                treecollection.push(treenode)
                            } 
                        }
                        return resolve(treecollection)
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
        this.getInstList()
    },
}
</script>

<style>
.querymongodb .el-collapse-item__header.is-active,.querymongodb .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
    border-bottom: 1px solid #dcdfe6;
}
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
    height: 600px;
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
    /* position: absolute; */
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
    height: 630px;
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
.querymongodb .querymongodb-results::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
/* 滚动槽 */
.querymongodb .querymongodb-results::-webkit-scrollbar-track{
    border-radius: 2px;
    /* background: hsla(220,4%,58%,.3); */
    /* background: rgba(0, 0, 0, 0.3); */
}
/* 滚动条滑块 */
.querymongodb .querymongodb-results::-webkit-scrollbar-thumb{
    border-radius: 2px;
    background: hsla(220, 16%, 87%, 0.3);
    /* background: rgba(0, 0, 0, 0.3); */
}
</style>

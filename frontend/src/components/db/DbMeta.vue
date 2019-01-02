<template>
    <div id="dbmeta" class="dbmeta">
        <div class="dbmeta-tree">
            <el-input
            class="dbmeta-filterinput"
            placeholder="输入关键字进行过滤"
            v-model="filterText">
            </el-input>
            <!-- <el-scrollbar> -->
                <div class="dbmeta-tree-data">
                    <el-tree
                    class="filter-tree"
                    ref="tree"
                    :data="treedata"
                    lazy
                    accordion
                    highlight-current
                    :load="loadTreeData"
                    :props="treeprops"
                    @node-click="handleNodeClick"
                    :filter-node-method="filterNode">
                    </el-tree>
                </div>
            <!-- </el-scrollbar> -->
        </div>
        <div class="dbmeta-table">
            <el-table border :data="tablecol.results">
                <el-table-column align="left" v-for="(val, key) in tablecol.col" v-if="key == 0" width="300px" :key="key" :label="val" :prop="val">
                </el-table-column>
                <el-table-column align="left" v-for="(val, key) in tablecol.col" v-if="key != 0" :key="key" :label="val" :prop="val">
                </el-table-column>
                <!-- <el-table-column align="left" label="Table" prop="Table">
                </el-table-column>
                <el-table-column align="left" label="Create Table" prop="Create Table">
                </el-table-column> -->
            </el-table>
        </div>
    </div>
</template>

<script>
import store from '@/store/store.js';
import Axios from '@/utils/axios.js';
export default {
    name: 'dbmeta',
    data() {
        return {
            parent_dbname:'',
            tablecol: {},
            filterText: '',
            treedata: [],
            treeprops: {
                children: 'children',
                label: 'label'
            }
        }
    },
    watch: {
        filterText (val) {
            this.$refs.tree.filter(val);
        },
    },
    methods: {
        loadTreeData (node,resolve) {
            if (node.level ==1) {
                var treetable = []
                var meta_data = {}
                meta_data.type = 'db'
                meta_data.dbname = node.data.label
                Axios.oPost('/dbmeta',meta_data).then((respone) => {
                    if(respone) {
                        var colname = respone.data.col[0]
                        for (var i = 0; i< respone.data.results.length; i++) {
                            var treetablenode = {}
                            treetablenode.id = i + 1
                            treetablenode.label = respone.data.results[i][colname]
                            treetable.push(treetablenode)
                        }
                        return resolve(treetable)
                    }
                }).catch((error) => {
                    console.log(error);
                })
            }
            if (node.level >1) {
                return resolve([]);
            }
        },
        handleNodeClick(data) {
            if (!data.id) {
                this.parent_dbname = data.label
            }
            else {
                var meta_data = {}
                meta_data.type = 'table'
                meta_data.dbname = this.parent_dbname
                meta_data.tablename = data.label
                Axios.oPost('/dbmeta',meta_data).then((respone) => {
                    if(respone) {
                        this.tablecol = respone.data
                        
                    }
                }).catch((error) => {
                    console.log(error);
                })
            }
        },
        filterNode(value, data) {
            if (!value) return true;
            return data.label.indexOf(value) !== -1;
        },
        getDbList() {
            var url = '/userinfo/' + this.$store.getters.username + '/'
            Axios.oGet(url).then((response)=>{
                if (response) {
                    // this.treedata.push(response.data.accessdb.split(","))
                    var dblist = response.data.accessdb.split(",")
                    for (var i =0; i< dblist.length;i++) {
                        var treedb = {}
                        treedb.label = dblist[i]
                        this.treedata.push(treedb)
                    }
                }                        
            }).catch((error) => {
                console.log(error);
            })
            // Axios.oGet('/db/').then((response)=>{
            //     if (response) {
            //         var dblist = response.data
            //         for (var i =0; i< dblist.length;i++) {
            //             var treedb = {}
            //             treedb.label = dblist[i].dbname
            //             this.treedata.push(treedb)
            //         }
            //     }                        
            // }).catch((error) => {
            //     console.log(error);
            // })
        },
    },
    mounted() {
        this.getDbList()
    },
}
</script>

<style>
/* .el-scrollbar{
  height: 100%;
}
.el-scrollbar__wrap{
  overflow: scroll;
  overflow-x:auto
} */
.dbmeta .el-table--border{
    max-height: 800px;
    overflow: auto;
}
.dbmeta .el-table::before{
    bottom: inherit;
}
.dbmeta .el-table .cell{
    white-space: pre;
    overflow: auto;
    text-overflow: unset;
}
.dbmeta .dbmeta-tree-data{
    max-height: 800px;
    overflow:auto;
}
.dbmeta .el-tree-node__label{
    font-size: 17px;
    position: absolute;
    padding-left: 30px;
}
.dbmeta .el-tree-node__content>.el-tree-node__expand-icon{
    position: absolute;
    top:4px;
}

.dbmeta .el-tree-node__content{
    position: relative;
}
.dbmeta .el-input__inner{
    width: 100%;
    float: left;
}
.dbmeta .dbmeta-tree{
    width: 20%;
    float: left;
}
.dbmeta .dbmeta-table{
    /* float: right; */
    /* margin-top: 45px; */
    width: 78%;
    display:inline-block;
}
.dbmeta .el-tree-node>.el-tree-node__children{
    overflow: inherit;
    
}
/* 设置滚动条的样式 */
.dbmeta .dbmeta-tree-data::-webkit-scrollbar,.dbmeta .el-table--border::-webkit-scrollbar,.dbmeta .el-table .cell::-webkit-scrollbar {
    width: 4px;
    height: 6px;
}
/* 滚动槽 */
.dbmeta .dbmeta-tree-data::-webkit-scrollbar-track,.dbmeta .el-table--border::-webkit-scrollbar-track,.dbmeta .el-table .cell::-webkit-scrollbar-track{
    border-radius: 2px;
    /* background: hsla(220,4%,58%,.3); */
    /* background: rgba(0, 0, 0, 0.3); */
}
/* 滚动条滑块 */
.dbmeta .dbmeta-tree-data::-webkit-scrollbar-thumb,.dbmeta .el-table--border::-webkit-scrollbar-thumb,.dbmeta .el-table .cell::-webkit-scrollbar-thumb{
    border-radius: 2px;
    background: hsla(220,4%,58%,.3);
    /* background: rgba(0, 0, 0, 0.3); */
}
</style>

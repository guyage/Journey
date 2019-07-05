<template>
    <div class="mysqlmeta" id="mysqlmeta">
        <el-collapse v-model="activeNames">
            <el-collapse-item title="MySQL元数据" name="1">
                <div class="mysqlmeta-tree" style="padding: 0.8em 0em 1em;">
                    <el-input
                    class="mysqlmeta-filterinput"
                    placeholder="输入关键字进行过滤"
                    v-model="filterText">
                    </el-input>
                        <div class="mysqlmeta-tree-data">
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
                </div>
                <div class="mysqlmeta-table" style="padding: 0.8em 0em 1em;">
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
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script>
import store from '@/store/store.js';
import { getUserAccessDb,getMysqlMeta } from '@/api/api.js';
export default {
    name: 'mysqlmeta',
    data () {
        return {
            activeNames: ['1'],
            instid: 0,
            dbname: '',
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
            if (node.level == 1) {
                getUserAccessDb({'dbtype':'mysqldb','mysqlinst':node.data,'username':store.getters.username}).then((response) => {
                    if (response) {
                        let treedb = []
                        for (let i=0;i<response.data.results.length;i++) {
                        treedb.push({'label':response.data.results[i].dbname,'type':'db'})
                        }
                        return resolve(treedb);
                    }
                }).catch((error) => {
                    console.log(error);
                })
            }
            else if (node.level == 2) {
                let treetable = []
                let meta_data = {}
                meta_data.type = 'table'
                meta_data.instid = node.parent.data.id
                meta_data.dbname = node.data.label
                getMysqlMeta(meta_data).then((response) => {
                    let colname = response.data.col[0]
                    for (let i = 0; i< response.data.results.length; i++) {
                            let treetablenode = {}
                            treetablenode.id = i + 1
                            treetablenode.label = response.data.results[i][colname]
                            treetablenode.type = 'table'
                            treetablenode.isLeaf = true
                            treetable.push(treetablenode)
                        }
                    return resolve(treetable)
                }).catch((error) => {
                    console.log(error);
                })
            }
            else {
                return resolve([]);
            }
        },
        handleNodeClick(data) {
            if (data.type == 'inst') {
                this.instid = data.id
            }
            else if (data.type == 'db') {
                this.dbname = data.label                
            }
            else if (data.type == 'table') {
                let meta_data = {'type':'tablemeta','instid':this.instid,'dbname':this.dbname,'tablename':data.label}
                getMysqlMeta(meta_data).then((response) => {
                    this.tablecol = response.data
                }).catch((error) => {
                    console.log(error);
                })
            }
        },
        filterNode(value, data) {
            if (!value) return true;
            return data.label.indexOf(value) !== -1;
        },
        getData () {
            getUserAccessDb({'dbtype':'mysqlinst','username':store.getters.username}).then((response) => {
                if (response.data.results.length > 0) {
                    for (let i=0;i<response.data.results.length;i++) {
                        this.treedata.push({'id':response.data.results[i].instid,'label':response.data.results[i].instname,'type':'inst'})
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
        this.getData()
    }

}
</script>

<style>
.mysqlmeta .el-collapse-item__header.is-active,.mysqlmeta .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
    border-bottom: 1px solid #dcdfe6;
}  
.mysqlmeta .el-table--border{
    max-height: 800px;
    overflow: auto;
}
.mysqlmeta .el-table::before{
    bottom: inherit;
}
.mysqlmeta .el-table .cell{
    white-space: pre;
    overflow: auto;
    text-overflow: unset;
}
.mysqlmeta .mysqlmeta-tree-data{
    max-height: 800px;
    overflow:auto;
}
.mysqlmeta .el-tree-node__label{
    font-size: 17px;
    position: absolute;
    padding-left: 30px;
}
.mysqlmeta .el-tree-node__content>.el-tree-node__expand-icon{
    position: absolute;
    top:4px;
}

.mysqlmeta .el-tree-node__content{
    position: relative;
}
.mysqlmeta .el-input__inner{
    width: 100%;
    float: left;
}
.mysqlmeta .mysqlmeta-tree{
    width: 20%;
    float: left;
}
.mysqlmeta .mysqlmeta-table{
    /* float: right; */
    /* margin-top: 45px; */
    width: 78%;
    display:inline-block;
}
.mysqlmeta .el-tree-node>.el-tree-node__children{
    overflow: inherit;
    
}
/* 设置滚动条的样式 */
.mysqlmeta .mysqlmeta-tree-data::-webkit-scrollbar,.mysqlmeta .el-table--border::-webkit-scrollbar,.mysqlmeta .el-table .cell::-webkit-scrollbar {
    width: 4px;
    height: 6px;
}
/* 滚动槽 */
.mysqlmeta .mysqlmeta-tree-data::-webkit-scrollbar-track,.mysqlmeta .el-table--border::-webkit-scrollbar-track,.mysqlmeta .el-table .cell::-webkit-scrollbar-track{
    border-radius: 2px;
    /* background: hsla(220,4%,58%,.3); */
    /* background: rgba(0, 0, 0, 0.3); */
}
/* 滚动条滑块 */
.mysqlmeta .mysqlmeta-tree-data::-webkit-scrollbar-thumb,.mysqlmeta .el-table--border::-webkit-scrollbar-thumb,.mysqlmeta .el-table .cell::-webkit-scrollbar-thumb{
    border-radius: 2px;
    background: hsla(220,4%,58%,.3);
    /* background: rgba(0, 0, 0, 0.3); */
}
</style>

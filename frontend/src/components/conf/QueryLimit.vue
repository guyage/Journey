<template>
    <div id="querylimit" class="querylimit">
        <el-row>
            <el-divider content-position="left">QueryLimit</el-divider>
            <div class="querylimit-list">
                <div class="querylimit-list-mysql" style="float:left;padding: 0.8em 0em 1em;">
                    <el-tag  style="width:100px;">MySQL</el-tag>
                    <el-input-number size="small" style="left:10px;rigth:10px;" v-model="mysqllimit" :step="100" :min="0" :max="1000" label="描述文字"></el-input-number>
                    <el-button type="primary" size="small" style="margin-left:10px;" @click="setData('mysql')">修改</el-button>
                </div>
                <div class="querylimit-list-mongodb" style="float:left;clear: both;padding: 0.8em 0em 1em;">
                    <el-tag style="width:100px;" >MongoDB</el-tag>
                    <el-input-number size="small" style="left:10px;" v-model="mongodblimit" :step="10" :min="0" :max="500" label="描述文字"></el-input-number>
                    <el-button type="primary" size="small" style="margin-left:10px;" @click="setData('mongodb')">修改</el-button>
                </div>
            </div>
        </el-row> 
    </div>
</template>

<script>
import { getQueryLimit, setQueryLimit } from '@/api/api.js';
export default {
    name: 'querylimit',
    data () {
        return {
            mysqllimit: 0,
            mongodblimit: 0,
            mysqllimitid: 0,
            mongodblimitid: 0,
        }
    },
    methods: {
        setData(dbtype) {
            let querylimit_data = {}
            if (dbtype == 'mysql') {
                querylimit_data.id = this.mysqllimitid
                querylimit_data.query_type = 'mysql'
                querylimit_data.query_limit = this.mysqllimit
                
            }
            else if (dbtype == 'mongodb') {
                querylimit_data.id = this.mongodblimitid
                querylimit_data.query_type = 'mongodb'
                querylimit_data.query_limit = this.mongodblimit
            }
            setQueryLimit(querylimit_data).then((response) => {
                this.getDataList()
                this.$message.success('修改成功!');
            }).catch((error) => {
                console.log(error);
            })
        },
        getDataList() {
            getQueryLimit().then((response) => {
                for (let i=0;i<response.data.length;i++) {
                    if (response.data[i].query_type == 'mysql') {
                        this.mysqllimitid = response.data[i].id 
                        this.mysqllimit = response.data[i].query_limit 
                    }
                    else if (response.data[i].query_type == 'mongodb') {
                        this.mongodblimitid = response.data[i].id 
                        this.mongodblimit = response.data[i].query_limit
                    }
                }
            }).catch((error) => {
                console.log(error);
            })
        },
    },
    mounted () {
        this.getDataList()
    }
}
</script>

<style>
.querylimit .el-collapse-item__header.is-active,.querylimit .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
    border-bottom: 1px solid #dcdfe6;
}
</style>

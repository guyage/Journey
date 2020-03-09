<template>
    <div id="useraccessmongodb" class="useraccessmongodb">
        <div v-if="!isapply" class="useraccessmongodb-list">
            <el-row style="padding-bottom:5px;">
                <div class="user-operation" style="padding: 0.8em 0em 1em;">
                    <el-button @click="applyData" style="float: left;" icon="el-icon-edit" size="small" type="primary">申请权限</el-button>
                    <el-input v-model="searchcontent" @keyup.enter.native="searchData" style="width: 200px;float: right;" size="small" placeholder="Search">
                        <el-button @click="searchData" slot="append" icon="el-icon-search"></el-button>
                    </el-input>
                </div>
            </el-row>
            <el-row>
                <UserAccessTable
                :TableColumn="table_columns"
                :TableData="table_data"
                :editData="editData"
                :delData="delData">
                </UserAccessTable>
            </el-row>
        </div>
        <div v-if="isapply" class="useraccessmongodb-apply">
            <el-row>
                <div style="padding-top: 10px;">
                    <el-form  ref="form" :model="form" :rules="rules">
                        <el-form-item label="申请用户：" label-width="150px" prop="username">
                            <el-input style="width: 300px; float: left;" v-model="form.username"></el-input>
                        </el-form-item>
                        <el-form-item label="申请访问实例：" label-width="150px" prop="mongodbinst">
                            <el-select style="width: 300px; float: left;" v-model="form.mongodbinst" placeholder="请选择MongoDB实例">
                                <el-option v-for="(val,index) in instlist" :key="index" :label="val.inst" :value="val.id" ></el-option>
                            </el-select>
                        </el-form-item>
                        <!-- <el-form-item  label="申请访问数据库：" label-width="150px">
                            <el-checkbox-group style="float: left;" v-model="form.user_access_db">
                                <el-checkbox v-for="(val,index) in instdb" :key="index" :label="val"></el-checkbox>
                            </el-checkbox-group>
                        </el-form-item> -->
                        <el-form-item label="申请说明：" label-width="150px">
                            <el-input style="width: 300px; float: left;" v-model="form.comment"></el-input>
                        </el-form-item>
                        <el-form-item label-width="150px">
                            <el-button style="float: left;" type="primary" @click="handleApply">提交</el-button>
                            <el-button style="float: left;" @click="isapply = false;">取消</el-button>
                        </el-form-item>
                    </el-form>
                </div>
            </el-row>
        </div>
    </div>
</template>



<script>
import store from '@/store/store.js';
import UserAccessTable from '../mysql/UserAccessTable.vue';
import { getUserAccessMongoDB,getMongoDBInst,execQueryMongodb,editUserAccessMongoDB,delUserAccessMongoDB,addUserAccessMongoDB,searchUserAccessMongoDB } from '@/api/db.js';
export default {
    name: "useraccessmongodb",
    components: {
        UserAccessTable,
    },
    data () {
        return {
            activeNames: ['1'],
            searchcontent: '',
            //用户列表参数
            table_data: [],
            table_columns: {
                id: 'id',
                username: '用户名',
                mongodbinst: 'MongoDB实例',
                create_time: '申请时间',
                status: '状态',
                comment: '备注'
            },
            //用户申请相关参数
            instlist: [],
            instdb: [],
            form: {
                username: '',
                mongodbinst: '',
                comment: '',
            },
            rules: {
                username: [
                    { required: true, message: '请输入用户名', trigger: 'blur' }
                ],
                mongodbinst: [
                    { required: true, message: '请选择MongoDB实例', trigger: 'change' }
                ],
            },
            isapply: false,
        }
    },
    methods: {
        applyData() {
            this.isapply = true
        },
        handleApply() {
            this.$refs['form'].validate((valid)=>{
                if(valid){
                    addUserAccessMongoDB(this.form).then((response) => {
                        if (response) {
                            this.$message.success('申请成功!');
                            this.getDataList()
                            this.isapply = false;
                        }
                    }).catch((error) => {
                        this.$message.error('申请失败，请确认是否重复申请!');
                        console.log('请勿重复申请!');
                    })
                }
                else {
                    this.$message.error('数据不合法!');
                }
            })
        },
        delData(id) {
            delUserAccessMongoDB({id:id}).then((response) => {
                // console.log(response);
                this.$message.success('删除成功!');
            }).catch((error) => {
                console.log(error);
            })
        },
        editData (data) {
            editUserAccessMongoDB(data).then((response) => {
                this.$message.success('处理成功!');
            }).catch((error) => {
                console.log(error);
            })
        },
        searchData() {
            if (this.searchcontent) {
                searchUserAccessMongoDB({searchcontent:this.searchcontent}).then((response) => {
                    this.table_data = response.data
                }).catch((error) => {
                    console.log(error);
                })
            }
            else {
                this.getDataList()
            }
        },
        getDataList() {
            getUserAccessMongoDB({'username':store.getters.username}).then((response) => {
                if (response) {
                    this.table_data = response.data
                }
            }).catch((error) => {
                console.log(error);
            })
        },
        getInstList() {
            getMongoDBInst().then((response) => {
                if (response.data.length > 0) {
                    if (store.getters.userissuper) {
                        for (var i = 0; i < response.data.length;i++) {
                            this.instlist.push({'id':response.data[i].id,'inst':response.data[i].inst_name})
                        }
                    }
                    else {
                        for (var i = 0; i < response.data.length;i++) {
                            if (response.data[i].role == 'Slave' ) {
                                this.instlist.push({'id':response.data[i].id,'inst':response.data[i].inst_name})  
                            }
                        }
                    }
                }
            }).catch((error) => {
                console.log(error);
            })
        },
        // getInstDb (val) {
        //     this.instdb = []
        //     let req_data = {}
        //     req_data.exectype = 'table'
        //     req_data.instid = val
        //     execQueryMongodb(req_data).then((response) => {
        //         for (let i=0;i<response.data.results.length;i++) {
        //             this.instdb.push(response.data.results[i].table_schema)
        //         }
        //     }).catch((error) => {
        //         console.log(error);
        //     })
            
        // },
        initUserApplyData() {
            this.form.username = store.getters.username
        },
    },
    mounted() {
        this.getDataList()
        this.getInstList()
        this.initUserApplyData()
    },

}
</script>


<style>
.useraccessmongodb .el-collapse-item__header.is-active,.useraccessmongodb .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
    border-bottom: 1px solid #dcdfe6;
}
</style>

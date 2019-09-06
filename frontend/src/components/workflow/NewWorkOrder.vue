<template>
    <div class="newworkorder">
        <el-row>
            <el-col :span="8">
                <div>
                    <el-form size="small" ref="form" :rules="rules" :model="form" label-position="right" label-width="100px">
                        <el-form-item label="工单类型:" prop="ordertype">
                            <el-select style="width:100%;" v-model="form.ordertype" @change="handleChange($event)" placeholder="请选择工单类型">
                                <el-option 
                                v-for="item in ordertypelist"
                                :key="item.id"
                                :label="item.ordertype"
                                :value="item.id">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="工单主题:" prop="title">
                            <el-input v-model="form.title" placeholder="请输入工单主题"></el-input>
                        </el-form-item>
                    </el-form>
                </div>
            </el-col>
        </el-row>
        <el-row>
            <el-col v-loading="loading" :span="8">
                <div style="font-size: 14px;">
                    <fm-generate-form
                    :data="formjson"
                    :remote="remoteFuncs"
                    ref="generateForm">
                    </fm-generate-form>
                </div>
                <div v-if="formjson.list.length > 0" style="text-align:left;">   
                    <el-form size="mini" label-width="100px">
                        <el-form-item>
                            <el-button @click="handleSubmit" type="primary">提交工单</el-button>
                        </el-form-item>
                    </el-form>
                </div>
            </el-col>
        </el-row>
        <!-- <el-row >
            <el-col :span="8">
                <div v-if="formjson.list.length > 0" style="text-align:left;">   
                    <el-form size="mini" label-width="100px">
                        <el-form-item>
                            <el-button @click="handleSubmit" type="primary">提交工单</el-button>
                        </el-form-item>
                    </el-form>
                </div>
            </el-col>
        </el-row> -->
    </div>
</template>

<script>
import store from '@/store/store.js';
import { getWorkOrderType,getGitLabInfo,addWorkOrder} from '@/api/api.js';
export default {
    // name: 'newworkorder',
    data () {
        var that = this
        return {
            loading: false,
            ordertypelist: [],
            form: {
                title: '',
                ordertype: '',
                creator: '',
                operator: '',
                content: '',
            },
            rules: {
                ordertype: [
                    { required: true, message: '请选择工单类型', trigger: 'change' }
                ],
                title: [
                    { required: true, message: '请输入工单主题', trigger: 'blur' },
                ],
            },
            formjson: {
                "list": [],
                "config": {},
            },
            initjson: {
                "list": [],
                "config": {},
            },
            remoteFuncs: {
                getGitProjectGroups (resolve) {
                    // that.loading = true
                    getGitLabInfo({'reqtype':'groups'}).then((response) => {
                        resolve(response.data.results)
                        // that.loading = false
                    }).catch((error) => {
                        console.log(error);
                        // that.loading = false
                    })
                },
                getGitUsers (resolve) {
                    that.loading = true
                    getGitLabInfo({'reqtype':'users'}).then((response) => {
                        resolve(response.data.results)
                        that.loading = false
                    }).catch((error) => {
                        console.log(error);
                        that.loading = false
                    })
                },
                getGitUsersList (resolve) {
                    // that.loading = true
                    getGitLabInfo({'reqtype':'users'}).then((response) => {
                        resolve(response.data.results)
                        // that.loading = false
                    }).catch((error) => {
                        console.log(error);
                        // that.loading = false
                    })
                },
                getGitProjectProjects (resolve) {
                    that.loading = true
                    getGitLabInfo({'reqtype':'projects'}).then((response) => {
                        resolve(response.data.results)
                        that.loading = false
                    }).catch((error) => {
                        console.log(error);
                        that.loading = false
                    })
                }
            },
        }
    },
    methods: {
        handleSubmit () {
            // this.form = this.initform
            this.$refs.generateForm.getData().then((data) => {
                this.form.content = JSON.stringify(data)
                this.form.creator = store.getters.username
                this.form.operator = store.getters.username
                // console.log(this.form);
                addWorkOrder(this.form).then((response) => {
                    this.$router.push({ path: '/myworkorder'})
                    this.$message.success('提交成功!');
                }).catch((error) => {
                    console.log(error);
                    this.$message.error('提交失败!');
                })
            }).catch((error) => {
                console.log(error);
                this.$message.error('数据不合法!');
            })
        },
        handleChange(val) {
            this.formjson = this.initjson
            getWorkOrderType({'id':val}).then((response) => {
                if (response.data.formconfig) {
                    this.formjson = JSON.parse(response.data.formconfig)                    
                }
                else {
                    this.$notify({title: '提示',message:'请先联系管理员配置工单参数!',type: 'warning'})
                }
            }).catch((error) => {
                console.log(error);
            })
        },
        getData() {
            getWorkOrderType().then((response) => {
                this.ordertypelist = response.data
            }).catch((error) => {
                console.log(error);
            })
        },
    },
    mounted () {
        this.getData()
    }
}
</script>

<style>

</style>
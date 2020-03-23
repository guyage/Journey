<template>
    <div class="permsdialog">
        <el-dialog
        :title="'添加菜单'"
        :visible.sync="visible"
        @close="$emit('update:show', false)"
        :show="show"
        :before-close="handleClose">
            <el-card>
                <el-form ref="form" :model="form" label-width="150px">
                    <el-form-item label="接口名称：" prop="name">
                        <el-input size="small" style="width: 300px; float: left;" placeholder="接口名称" v-model="form.name"></el-input>
                    </el-form-item>
                    <el-form-item label="接口地址：" prop="api">
                        <el-input size="small" style="width: 300px; float: left;" placeholder="接口对应url(从api开始写，如/api/docs/)" v-model="form.api"></el-input>
                    </el-form-item>
                     <el-form-item label="接口标识：" prop="api">
                        <el-input size="small" style="width: 300px; float: left;" placeholder="接口对应views中module_perms值" v-model="form.module_perms"></el-input>
                    </el-form-item>
                    <el-form-item label="接口请求类型：">
                        <el-checkbox-group v-model="form.api_type">
                        <el-checkbox label="get">GET</el-checkbox>
                        <el-checkbox label="post">POST</el-checkbox>
                        <el-checkbox label="patch">PATCH</el-checkbox>
                        <el-checkbox label="deletel">DELETEL</el-checkbox>
                        </el-checkbox-group>
                    </el-form-item>
                    <el-form-item>
                        <el-button size="small" type="primary" @click="handleSumit('form')">确定</el-button>
                        <el-button size="small" @click="visible = false;resetForm('form')">取消</el-button>
                        <el-button size="small" @click="resetForm('form')">重置</el-button>
                    </el-form-item>
                </el-form>
            </el-card>
        </el-dialog>
    </div>
</template>

<script>
import store from '@/store/store.js';
export default {
    name: 'permsdialog',
    data () {
        return {
            visible: this.show,
            selectdatalist: [],
            form: {
                name: '',
                api:'',
                module_perms: '',
                api_type: [],
                del_flag:0,
                creator: ''
            },
            rules: {

            }
        }
    },
    props: {
        show: {
            type: Boolean,
            default: false
        },
        saveData: {
            type: Function
        }
    },
    watch: {
        show () {
            this.visible = this.show;
        }
    },
    methods: {
        handleSumit(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    console.log(this.form);
                    let req_data = {}
                    req_data = this.form
                    req_data.creator = store.getters.username
                    this.saveData(req_data)
                } else {
                    console.log('数据不合法!!');
                    return false;
                }
            });
        },
        resetForm(formName) {
            this.$refs[formName].resetFields();
        },
        handleClose(done) {
            this.$confirm('确认关闭!')
            .then(_=> {
                done();
            })
            .catch(_=>{})
        },
    }
}
</script>

<style>
.permsdialog{
    text-align: left;
}
</style>
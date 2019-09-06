<template>
    <div class="menusdialog">
        <el-dialog
        :title="'添加菜单'"
        :visible.sync="visible"
        @close="$emit('update:show', false)"
        :show="show"
        :before-close="handleClose">
            <el-card>
                <el-form ref="form" :model="form" label-width="100px">
                    <el-form-item label="类型：">
                        <el-radio-group v-model="form.mtype" @change="handleSelect($event)">
                            <el-radio :label="0">目录</el-radio>
                            <el-radio :label="1">菜单</el-radio>
                            <el-radio :label="2">按钮</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <div v-if="mtype == 0">
                        <el-form-item label="目录名称：" prop="name">
                            <el-input size="small" style="width: 300px; float: left;" v-model="form.name"></el-input>
                        </el-form-item>
                        <el-form-item label="目录图标：" prop="icon">
                            <el-input size="small" style="width: 300px; float: left;" v-model="form.icon"></el-input>
                        </el-form-item>
                    </div>
                    <div v-else-if="mtype == 1">
                        <el-form-item label="菜单名称：" prop="name">
                            <el-input size="small" style="width: 300px; float: left;" v-model="form.name"></el-input>
                        </el-form-item>
                        <el-form-item label="上级目录：" prop="parent_id">
                            <el-select style="width: 300px;" v-model="form.parent_id" placeholder="请选菜单所属目录">
                                <el-option 
                                v-for="item in selectdatalist" 
                                :key="item.id"
                                v-if="item.name != '仪表盘'"
                                :label="item.name"
                                :value="item.id">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="菜单路由：" prop="url">
                            <el-input size="small" style="width: 300px; float: left;" v-model="form.url"></el-input>
                        </el-form-item>
                        <el-form-item label="菜单图标：" prop="icon">
                            <el-input size="small" style="width: 300px; float: left;" v-model="form.icon"></el-input>
                        </el-form-item>
                    </div>
                    <div v-else-if="mtype == 2">
                        <el-form-item label="按钮名称：" prop="name">
                            <el-input size="small" style="width: 300px; float: left;" v-model="form.name"></el-input>
                        </el-form-item>
                        <el-form-item label="上级菜单：" prop="parent_id">
                            <el-select style="width: 300px;" v-model="form.parent_id" placeholder="请选按钮所属菜单">
                                <el-option 
                                v-for="item in selectdatalist" 
                                :key="item.id"
                                :label="item.name"
                                :value="item.id">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="授权标识：" prop="perms">
                            <el-input size="small" style="width: 300px; float: left;" v-model="form.perms"></el-input>
                        </el-form-item>
                    </div>
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
import { getMenus } from '@/api/api.js';
export default {
    name: 'menusdialog',
    data () {
        return {
            visible: this.show,
            mtype: 0,
            selectdatalist: [],
            form: {
                name: '',
                url: '',
                parent_id: '',
                icon: '',
                perms: '',
                mtype: 0,
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
                    let req_data = {}
                    if (this.mtype == 0) {
                        req_data = this.form
                        req_data.parent_id = 0
                    }
                    else if (this.mtype == 1) {
                        req_data = this.form
                    }
                    else if (this.mtype == 2) {
                        req_data = this.form
                    }
                    req_data.creator = store.getters.username
                    this.saveData(req_data)
                } else {
                    console.log('数据不合法!!');
                    return false;
                }
            });
        },
        handleSelect(val) {
            this.mtype = val
            this.resetForm('form')
            if (this.mtype == 0) {
                this.selectdatalist = []
            }
            else if (this.mtype == 1) {
                this.selectdatalist = []
                getMenus().then((response) => {
                    this.selectdatalist = response.data.filter( i => i.mtype === 0)  
                })
            }
            else if (this.mtype == 2){
                this.selectdatalist = []
                getMenus().then((response) => {
                    for (let i in response.data) {
                        if (response.data[i].children.length>0) {
                            this.selectdatalist.push.apply(this.selectdatalist,response.data[i].children.filter(i => i.mtype === 1))                        }
                    }
                })
            }
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
.menusdialog{
    text-align: left;
}
</style>
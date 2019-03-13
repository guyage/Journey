<template>
    <div class="datadialog">
        <el-dialog
            :title="isUpdate?'修改数据库':'添加数据库'"
            :visible.sync="visible"
            @close="$emit('update:show', false)"
            :show="show"
            :before-close="handleClose">           
            <el-form :model="form" :rules="rules" ref="form">
                <el-form-item v-for="(val, key, index) in formlabel"  v-if="key != 'is_enabled'" :label="val.label" label-width="150px" :key="index" :prop="key">
                    <el-input style="width: 300px; float: left;" v-model="form[key]" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="是否启用 : " label-width="150px" prop="is_enabled">
                    <el-select style="width: 300px; float: left;" v-model="form.is_enabled" placeholder="请选择是否启用">
                        <el-option label="启用" value="1"></el-option>
                        <el-option label="禁用" value="0"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button v-if="!isUpdate" type="primary" @click="addDataFun">添加</el-button>
                    <el-button v-if="isUpdate" type="primary" @click="editDataFun">编辑</el-button>
                    <el-button @click="visible = false;resetForm('form')">取消</el-button>
                    <el-button @click="resetForm('form')">重置</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>
    </div>
</template>

<script>
export default {
    name: 'datadialog',
    data () {
        return {
            visible: this.show,
            isUpdate: false
        };
    },
    props: {
        show: {
            type: Boolean,
            default: false
        },
        apiurl: '',
        form: {
            type: Object,
        },
        formlabel: {
            type: Object,
        },
        rules: {
            type: Object,
        },
        addFun: {
            type: Function
        },
        editFun: {
            type: Function
        },
        editurl: '',
    },
    watch: {
        show () {
            this.visible = this.show;
        }
    },
    methods: {
        handleClose(done) {
            this.$confirm('确认关闭!')
                .then(_=> {
                    done();
                })
                .catch(_=>{})
        },
        resetForm(formName) {
            this.$refs[formName].resetFields();
        },
        addDataFun() {
            // console.log('123',this.form);
            
            this.$refs['form'].validate((valid)=>{
                if(valid){
                    this.addFun(this.apiurl,this.form)
                    this.visible = false
                    this.$message.success('数据保存成功!');
                }
                else {
                    this.$message.error('数据库不合法!');
                }
            })
                       
        },
        editDataFun() {
            this.$refs['form'].validate((valid)=>{
                if(valid){
                    this.editFun(this.editurl,this.form)
                    this.visible = false
                    this.$message.success('编辑成功!');
                
                }
                else {
                    this.$message.error('数据不合法!');
                }
            })    
        },
    },
}
</script>

<style>

</style>

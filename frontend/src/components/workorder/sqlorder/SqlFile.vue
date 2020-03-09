<template>
    <div class="sqlfile">
        <el-col :span="10">
            <div style="float:left;text-align:left;">
                <el-upload
                class="upload-demo"
                ref="upload"
                multiple
                :action="uploadTo"
                name="sqlfile"
                :limit="1"
                :on-preview="handlePreview"
                :on-success="handleSuccess"
                :on-remove="handleRemove"
                :on-exceed="handleExceed"
                :file-list="fileList"
                :auto-upload="false"
                :headers="headers"
                :data="uploadData">
                <el-button size="small" type="warning">选取SQL文件</el-button>
                <!-- <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传SQL文件</el-button> -->
                <div slot="tip" class="el-upload__tip">只能上传sql/txt/zip文件，限制一个</div>
                </el-upload>
            </div>
        </el-col>
    </div>
</template>

<script>
import store from '@/store/store.js';
import { getCookies } from '@/utils/auth.js';
import { editSqlFile } from '@/api/sqlorder.js';
export default {
    name: 'sqlfile',
    data () {
        return {
            fileList: [],
            uploadTo: 'http://127.0.0.1:8888/api/sqlfile/',
            uploadData: {
                sqlorder_id: '',
            },
        }
    },
    computed: {
        headers () {
            return {
                'Authorization': 'JWT ' + getCookies('Authorization'),
            }
        }
    },
    methods: {
        submitUpload(sqlorderid) {
            this.uploadData.sqlorder_id = sqlorderid;
            if (this.uploadData.sqlorder_id) {
                this.$refs.upload.submit();
            }
            
        },	
        handleExceed() {
            this.$notify({title: '提示',message:'限制上传一个附件！',type: 'warning'})
        },
        handleSuccess(file, fileList) {
            let sqlfiledata = {}
            sqlfiledata.id = fileList.response.id
            sqlfiledata.sqlfileurl = fileList.response.sqlfile
            editSqlFile(sqlfiledata).then((response) => {
                this.$message.success('提交成功!');
            }).catch((error) => {
                console.log(error);
                this.$message.error('提交失败!');
            })
            
        },
        handleRemove(file, fileList) {
            console.log(file, fileList);
        },
        handlePreview(file) {
            console.log(file);
        }
    },
}
</script>

<style>

</style>
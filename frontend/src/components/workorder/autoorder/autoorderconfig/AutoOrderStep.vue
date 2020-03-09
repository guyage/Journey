<template>
    <div class="autoorderstep">
        <el-row>
            <el-col :span="2" style="text-align:left;">
                <el-button @click="isadd = true;" size="mini" type="primary">添加审批流程</el-button>
            </el-col>
            <div v-if="isadd">
                <el-col :span="20" style="text-align:left;">
                    <el-form ref="stepform" size="mini" :inline="true" :form="stepform">
                        <!-- <el-form-item label="步骤ID:" prop="step_id">
                            <el-input-number v-model="stepform.step_id" controls-position="right" :min="2" :max="5"></el-input-number>
                        </el-form-item> -->
                        <el-form-item label="流程名称:" prop="step_name">
                            <el-input v-model="stepform.step_name"></el-input>
                        </el-form-item>
                        <el-form-item label="审批组:" prop="approver_group_id">
                            <el-select v-model="stepform.approver_group_id" placeholder="请选择流程审批组">
                                <el-option 
                                v-for="item in approvalgrouplist" 
                                :key="item.id"
                                :label="item.approver_group_name"
                                :value="item.id">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item>
                            <el-button @click="handleAddStep" size="mini" type="primary" plain >save</el-button>
                            <el-button @click="isadd = false;" size="mini" type="danger" plain >cancel</el-button>
                        </el-form-item>
                    </el-form>
                </el-col>
            </div>
        </el-row>

        <el-row>
            <el-divider content-position="left">工单流程</el-divider>
            <el-steps style="text-align: left;" :active="ordertypestepscount">
                <el-step v-for="(val,index) in ordertypesteps"
                v-if="val.step_name == 'start'"
                :key="index" 
                title="开始" 
                description="用户 [提交] 时间">
                </el-step>
                <el-step v-for="(val,index) in ordertypesteps"
                v-if="val.step_name != 'finsh' && val.step_name != 'start'"
                :key="index" 
                :title="val.step_name" 
                :description="val.approver_group_name">
                </el-step>
                <el-step v-for="(val,index) in ordertypesteps"
                v-if="val.step_name == 'finsh'"
                :key="index" 
                title="完成" 
                description="系统处理 [成功] 时间">
                </el-step>
            </el-steps>
        </el-row>
    </div>
</template>

<script>
import { getApprovalGroup,} from '@/api/workorder.js';
import { addAutoOrderStep } from '@/api/autoorder.js';
export default {
    name: 'autoorderstep',
    data() {
        return {
            approvalgrouplist: [],
            selectapprovalgroup: '',
            isadd: false,
            stepform: {
                step_id: 2,
                ordertype_id: 0,
                approver_group_id: '',
                step_name: '',
            },
        }
    },
    props: {
        ordertypeid: {
            type: Number,
        },
        ordertypesteps: {
            type: Array,
        },
        ordertypestepscount: {
            type: Number,
        },
        getAutoOrderTypeFun: {
            type: Function,
        }
    },
    methods: {
        handleAddStep() {
            this.stepform.ordertype_id = this.ordertypeid
            this.stepform.step_id = this.ordertypestepscount
            addAutoOrderStep(this.stepform).then((response) => {
                this.isadd = false;
                this.getAutoOrderTypeFun(this.ordertypeid)
            })
        },
        getApprovalGroupData() {
            getApprovalGroup().then((response) => {
                this.approvalgrouplist = response.data
            }).catch((error) => {
                console.log(error);
            })
        },
    },
    mounted () {
        this.getApprovalGroupData()
    }
}
</script>

<style>

</style> 
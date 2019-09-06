<template>
    <div class="workorderconfig">
        <el-col class="workorderconfig-col" :span="6">
            <el-card class="workorderconfig-card" shadow="hover">
                <div slot="header" class="clearfix">
                    <span>工单类型</span>
                    <el-button @click="isadd = true;newordertype = ''" style="float: right; padding: 3px 0" type="text">添加</el-button>
                </div>
                <div class="ordertypelist" >
                    <el-tree 
                    :data="ordertypelist" 
                    :props="OrderTypeProps" 
                    @node-click="handleOrderTypeTree">
                    <span class="custom-tree-node" slot-scope="{ node, data }">
                        <span >
                            <icon-svg style="vertical-align:middle;" class="menus-tree-icon" iconClass="icondian"></icon-svg>
                            {{ node.label }}
                        </span>
                        <span >
                            <el-button type="text" size="mini" @click="handleDel(node, data)">Delete</el-button>
                        </span>
                    </span>
                    </el-tree>
                    <div v-if="isadd" style="margin-top:5px;">
                        <el-input v-model="newordertype" size="mini" placeholder="请输入工单类型"></el-input>
                        <div style="margin-top:5px;">
                            <el-button @click="handleSaveOrderType" size="mini" type="primary" plain >save</el-button>
                            <el-button @click="isadd = false;" size="mini" type="danger" plain >cancel</el-button>
                        </div>
                    </div>
                </div>
            </el-card>
        </el-col>
        <el-col class="workorderconfig-col" :span="18">
            <div>
                <el-tabs type="card">
                    <el-tab-pane label="工单表单">
                        <DynamicForm
                        ref="dynamicform"
                        :saveWorkOrderForm="saveWorkOrderForm">
                        </DynamicForm>
                    </el-tab-pane>
                    <el-tab-pane label="工单流程步骤">
                        <WorkOrderStep
                        :ordertypeid="selectordertype"
                        :ordertypesteps="ordertypesteps"
                        :ordertypestepscount="ordertypestepscount"
                        :getWorkOrderTypeFun="getWorkOrderTypeDetail">
                        </WorkOrderStep>
                    </el-tab-pane>
                    <el-tab-pane label="工单脚本">
                        <WorkOrderScript
                        :saveWorkOrderScript="saveWorkOrderScript"
                        :ordertypescript="ordertypescript">
                        </WorkOrderScript>
                    </el-tab-pane>
                </el-tabs>
            </div>
        </el-col>
    </div>
</template>

<script>
import DynamicForm from './dynamicform/DynamicForm.vue';
import WorkOrderStep from './WorkOrderStep.vue';
import WorkOrderScript from './WorkOrderScript.vue';
import WorkOrderFuncs from './WorkOrderFuncs.vue';
import { getWorkOrderType,editWorkOrderType,addWorkOrderType,getWorkOrderStep,delWorkOrderType} from '@/api/api.js';
export default {
    name: 'workorderconfig',
    components: {
        DynamicForm,
        WorkOrderStep,
        WorkOrderFuncs,
        WorkOrderScript
    },
    data () {
        return {
            isadd: false,
            newordertype: '',
            selectordertype: 0,
            ordertypelist: [],
            OrderTypeProps: {
                label: 'ordertype'
            },
            ordertypesteps: [],
            ordertypestepscount: 0,
            ordertypefuncs: '',
            ordertypescript: '',
            initwidgetForm: {
                list: [],
                config: {
                    labelWidth: 100,
                    labelPosition: 'left',
                    size: 'small'
                },
            },
        }
    },
    methods: {
        handleDel(node, data) {
            this.$confirm('确认删除!')
            .then(_=> {
                let parent = node.parent;
                let children = parent.data.children || parent.data;
                let index = children.findIndex(d => d.id === data.id);
                children.splice(index, 1);
                delWorkOrderType({'id':data.id}).then((response) => {
                    this.$message.success('删除成功!');
                }).catch((error) => {
                    console.log(error);
                    this.$message.error('删除失败!');
                })
            })
            .catch(_=>{})
            
            
        },
        handleOrderTypeTree(data) {
            this.selectordertype = data.id
            this.getWorkOrderTypeDetail(this.selectordertype)
        },
        getWorkOrderTypeDetail(ordertypeid) {
            getWorkOrderType({'id':ordertypeid}).then((response) => {
                this.ordertypesteps = response.data.hasstep
                this.ordertypestepscount = response.data.stepscount
                this.ordertypefuncs = response.data.remotefuncs
                this.ordertypescript = response.data.script
                if (response.data.formconfig) {
                    this.$refs.dynamicform.widgetForm = JSON.parse(response.data.formconfig)
                    this.$refs.dynamicform.widgetFormSelect = JSON.parse(response.data.formconfig).list[0]
                }
                else {
                    this.$refs.dynamicform.widgetForm = this.initwidgetForm
                }
            })
        },  
        handleSaveOrderType() {
            if (this.newordertype) {
                addWorkOrderType({'ordertype':this.newordertype}).then((response) => {
                    this.isadd = false
                    this.$message.success('添加成功!');
                    this.getData()
                }).catch((error) => {
                    console.log(error);
                    this.$message.error('添加失败!');
                });
            }
        },
        getData() {
            getWorkOrderType().then((response) => {
                this.ordertypelist = response.data
            }).catch((error) => {
                console.log(error);
            })
        },
        saveWorkOrderForm(form_data) {
            let req_data = {}
            req_data.id = this.selectordertype
            req_data.formconfig = JSON.stringify(form_data)
            editWorkOrderType(req_data).then((response) => {
                this.$message.success('保存成功!');
            }).catch((error) => {
                console.log(error);
                this.$message.error('保存失败!');
            });
        },
        saveWorkOrderScript(script) {
            let req_data = {}
            req_data.id = this.selectordertype
            req_data.script = script
            editWorkOrderType(req_data).then((response) => {
                this.$message.success('保存成功!');
            }).catch((error) => {
                console.log(error);
                this.$message.error('保存失败!');
            });
        }
    },
    mounted () {
        this.getData()
    }

}
</script>

<style>
.workorderconfig{
    font-size: 14px;
}
.workorderconfig .el-card__header {
    padding: 5px 5px;
}
.workorderconfig  .el-card__body {
    padding: 10px;
}
.workorderconfig  .clearfix {
    text-align: left;
    padding-left: 10px;
}
.ordertypelist .el-tree-node__expand-icon.is-leaf{
    display: none;
}
.workorderconfig .el-tree-node.is-current.is-focusable {
    color:#409EFF;
}
.workorderconfig .workorderconfig-col{
    padding-right: 5px;
}
.workorderconfig .custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
}
</style>
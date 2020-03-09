<template>
    <div class="dynamicform">
        <el-col :span="2">
            <el-card class="dynamicform-card" shadow="hover">
                <div slot="header" class="clearfix">
                    <span>字段类型</span>
                </div>
                <div>
                    <draggable
                    v-bind="{group:{ name:'people', pull:'clone',put:false},sort:false, ghostClass: 'ghost'}"
                    :list="fieldComponents"
                    @end="handleMoveEnd"
                    @start="handleMoveStart"
                    :move="handleMove">
                        <el-button size="mini" v-for="(item, index) in fieldComponents" :key="index">
                            <span>{{item.name}}</span>
                        </el-button>
                    </draggable>
                </div>
            </el-card>
        </el-col>
        <el-col :span="16">
            <el-card class="dynamicform-card" shadow="hover">
                <div slot="header" class="clearfix">
                    <span>表单</span>
                    <el-button type="text" size="mini" style="float: right; padding: 3px 0" @click="handleSaveFormConfig">保存</el-button>
                </div>
                <div class="" >
                    <FormField style="position:unset" v-if="!resetJson"  ref="widgetForm" :data="widgetForm" :select.sync="widgetFormSelect"></FormField>
                </div>
            </el-card>
        </el-col>
        <el-col :span="6">
            <el-card class="dynamicform-card" shadow="hover">
                <div slot="header" class="clearfix">
                    <span>表单属性</span>
                </div>
                <div class="" style="text-align:left;">
                    <el-tabs>
                        <el-tab-pane label="字段属性">
                            <FieldConfig :data="widgetFormSelect"></FieldConfig>
                        </el-tab-pane>
                        <el-tab-pane label="表单属性">
                            <FormConfig :data="widgetForm.config"></FormConfig>
                        </el-tab-pane>
                    </el-tabs>
                </div>
            </el-card>
        </el-col>
    </div>
</template>

<script>
import { fieldComponents } from './formfieldComponents.js';
import draggable from 'vuedraggable';
import FormField from './FormField.vue';
import FieldConfig from './FieldConfig.vue';
import FormConfig from './FormConfig.vue';
export default {
    name: 'dynamicform',
    components: {
        draggable,
        FormField,
        FieldConfig,
        FormConfig
    },
    props: {
        saveAutoOrderForm: {
            type: Function
        },
    },
    data() {
        return {
            fieldComponents,
            num: 80,
            resetJson: false,
            type: '',
            values: {},
            jsonVisible: false,
            fieldlist: ['输入框','单选框','多选框'],
            selectfield: [],
            widgetForm: {
                list: [],
                config: {
                    labelWidth: 100,
                    labelPosition: 'left',
                    size: 'small'
                },
            },
            widgetFormSelect: null,
        }
    },
    methods: {
        handleSaveFormConfig () {
            this.saveAutoOrderForm(this.widgetForm)
        },
        handleMoveEnd (evt) {
        // console.log('end', evt)
        },
        handleMoveStart ({oldIndex}) {
        // console.log('start', oldIndex, this.basicComponents)
        },
        handleMove () {
            return true
        },
    },
    watch: {
        widgetForm: {
        deep: true,
        handler: function (val) {
            // console.log(this.$refs.widgetForm)
        }
        }
    },
   
}
</script>

<style>
.dynamicform .el-button+.el-button{
    margin-left: 0px;
}
.dynamicform .el-form-item.is-success.el-form-item--small{
    outline: 2px solid #409eff;
    border: 1px solid #409eff;
}

</style>
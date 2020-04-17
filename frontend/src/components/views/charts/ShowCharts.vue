<template>
    <div class="showcharts">
        <el-row>
            <el-col :span="8" style="margin-right:10px;">
                <div class="showcharts-card">
                    <el-card style="height:100px;" class="box-card" shadow="hover">
                        <div style="float:left;">
                            <icon-svg iconClass="iconwodedingdan"></icon-svg>
                        </div>
                        <div style="display:inline-block;margin-top:20px;">
                            <!-- <p style="color:rgb(64, 158, 255);font-size:32px;">{{todo_workorder}}/{{done_workorder}}/{{exception_workorder}}/{{workorder_total}}</p> -->
                            <div style="color:rgb(64, 158, 255);font-size:32px;">
                                <span style="color:#E6A23C">{{todo_workorder}}</span>/<span style="color:#67C23A">{{done_workorder}}</span>/<span style="color:#F56C6C">{{exception_workorder}}</span>/<span>{{workorder_total}}</span>
                            </div>
                            <p style="color:#99a9bf;">待处理/已处理/异常/工单总数</p>
                        </div>
                    </el-card>
                </div>
            </el-col>
            <el-col :span="5" style="margin-right:10px;">
                <div class="showcharts-card">
                    <el-card style="height:100px;" class="box-card" shadow="hover">
                        <div style="float:left;">
                            <icon-svg iconClass="iconwodedingdan"></icon-svg>
                        </div>
                        <div style="display:inline-block;margin-top:20px;">
                            <p style="color:rgb(64, 158, 255);font-size:32px;"></p>
                            <p style="color:#99a9bf;"></p>
                        </div>
                    </el-card>
                </div>
            </el-col>
            <el-col :span="5" style="margin-right:10px;">
                <div class="showcharts-card">
                    <el-card style="height:100px;" class="box-card" shadow="hover">
                        <div style="float:left;">
                            <icon-svg iconClass="iconxingzhuanggongnengtubiao-1"></icon-svg>
                        </div>
                        <div style="display:inline-block;margin-top:20px;">
                            <!-- <p style="color:rgb(36, 170, 125);font-size:32px;">{{server_total}}</p>
                            <p style="color:#99a9bf;">主机</p> -->
                        </div>
                    </el-card>
                </div>
            </el-col>
            <el-col :span="5">
                <div class="showcharts-card">
                    <el-card style="height:100px;" class="box-card" shadow="hover">
                        <div style="float:left;">
                            <icon-svg iconClass="icon-yonghuguanli"></icon-svg>
                        </div>
                        <div style="display:inline-block;margin-top:20px;">
                            <p style="color:rgb(215, 119, 255);font-size:32px;">{{user_total}}</p>
                            <p style="color:#99a9bf;">用户数</p>
                        </div>
                        
                    </el-card>
                </div>
            </el-col>
        </el-row>
        <el-row style="margin-top:10px;">
          <el-col :span="6" style="margin-right:10px;">
              <DrawLine v-if="isshow" :elementid="WorkOrderPieCharts" :title="WorkOrderPietitle" :options="WorkOrderPieOptions"></DrawLine>
          </el-col>
          <!-- <el-col :span="6">
              <DrawLine v-if="isshow" :elementid="IdcPieCharts" :title="IdcPieTitle" :options="IdcPieOptions"></DrawLine>
          </el-col> -->
        </el-row>
        <el-row style="margin-top:10px;">
            <el-col>
                <DrawLine v-if="isshow" :elementid="laste_order" :title="Linetitle" :options="LineOptions"></DrawLine>
            </el-col>
            
        </el-row>
    </div>
</template>

<script>
import DrawLine from './DrawLine.vue';
import { ShowCharts } from '@/api/charts.js';
export default {
    components: {
        DrawLine
    },
    data () {
        return {
            //
            laste_order : 'laste_order',
            WorkOrderPieCharts: 'workorderpiecharts',
            IdcPieCharts: 'serverpiecharts',
            isshow: false,
            // 工单数据
            workorder_total: '',
            done_workorder: '',
            exception_workorder: '',
            todo_workorder: '',
            user_total: '',
            server_total: '',
            IdcPieTitle: '主机分布',
            WorkOrderPietitle: '工单统计',
            Linetitle: '最近7天工单数(个)',
            LineOptions: {
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: []
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    data: []
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                ]
            },
            WorkOrderPieOptions: {
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b} : {c} ({d}%)'
                },
                legend: {
                    bottom: 10,
                    left: 'center',
                    data: ['Sql工单', 'Ops工单', 'Auto工单']
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                series: [
                    {
                        name: '工单统计',
                        color:['#5ab1ef','#b6a2de', '#2ec7c9','#ffb980', '#d87a80', '#7EC0EE','#FF9F7F', ],
                        type: 'pie',
                        radius: '60%',
                        center: ['50%', '40%'],
                        selectedMode: 'single',
                        data: [],
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        },
                        label:{
                            normal: {
                                // 设置标签位置，默认在饼状图外 可选值：'outer' ¦ 'inner（饼状图上）'
                                // position: 'inner',
                                // formatter: '{a} {b} : {c}个 ({d}%)'   设置标签显示内容 ，默认显示{b}
                                // {a}指series.name  {b}指series.data的name
                                // {c}指series.data的value  {d}%指这一部分占总数的百分比
                                formatter: '{b}:{c}'
                            }
                        },
                    }
                ]
            },
            IdcPieOptions: {
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b} : {c} ({d}%)'
                },
                legend: {
                    bottom: 10,
                    left: 'center',
                    data: []
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                series: [
                    {
                        name: '主机分布',
                        type: 'pie',
                        radius: '60%',
                        center: ['50%', '40%'],
                        selectedMode: 'single',
                        data: [],
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        },
                        label:{
                            normal: {
                                // 设置标签位置，默认在饼状图外 可选值：'outer' ¦ 'inner（饼状图上）'
                                // position: 'inner',
                                // formatter: '{a} {b} : {c}个 ({d}%)'   设置标签显示内容 ，默认显示{b}
                                // {a}指series.name  {b}指series.data的name
                                // {c}指series.data的value  {d}%指这一部分占总数的百分比
                                formatter: '{b}:{c}'
                            }
                        }
                    }
                ]
            },
        }
    },
    methods: {
        showInitCharts() {
            ShowCharts().then((response) => {
                this.done_workorder = response.data.results.done_workorder
                this.exception_workorder = response.data.results.exception_workorder
                this.todo_workorder = response.data.results.todo_workorder
                this.workorder_total = response.data.results.workorder_total
                this.user_total = response.data.results.user_total
                // this.server_total = response.data.results.server_total
                //idc主机分布饼图
                // this.showIdcPieCharts(response.data.results.idc_dis_count)
                // 工单饼图
                this.showWorkOrderPieCharts(response.data.results.hissql_total,response.data.results.hisops_total,response.data.results.hisauto_total)
                // 折线图数据
                this.showLineCharts(response.data.results.laste_data,response.data.results.laste_sql,response.data.results.laste_ops,response.data.results.laste_auto)
                
            })
        },
        // 工单饼图
        showWorkOrderPieCharts(hissql_total,hisops_total,hisauto_total) {
            this.WorkOrderPieOptions.series[0].data.push({value: hissql_total, name: 'Sql工单'})
            this.WorkOrderPieOptions.series[0].data.push({value: hisauto_total, name: 'Auto工单'})
            this.WorkOrderPieOptions.series[0].data.push({value: hisops_total, name: 'Ops工单'})
            this.isworkorderpiechart = true
        },
        // idc主机分布饼图
        showIdcPieCharts(idc_dis_count) {
            console.log(idc_dis_count);
            for (let i=0;i<idc_dis_count.length;i++) {
                let idc_name = idc_dis_count[i].idc_name
                let idc_server_count = idc_dis_count[i].idc_server_count
                this.IdcPieOptions.legend.data.push(idc_name)
                this.IdcPieOptions.series[0].data.push({value: idc_server_count, name: idc_name})
            }
        },
        // 折线图数据
        showLineCharts(laste_data,laste_sql,laste_ops,laste_auto) {
            this.LineOptions.xAxis.data =  laste_data
            this.LineOptions.legend.data.push('Ops工单','Auto工单','Sql工单')
            this.LineOptions.series.push({ name: 'Ops工单',type: 'line',stack: '总量',data: laste_ops})
            this.LineOptions.series.push({ name: 'Sql工单',type: 'line',stack: '总量',data: laste_sql})
            this.LineOptions.series.push({ name: 'Auto工单',type: 'line',stack: '总量',data: laste_auto})
            this.isshow = true
        },

    },
    mounted() {
        this.showInitCharts()
        // this.showlaste_sqlOrder()

    },
    created() {
        // this.showlaste_sqlOrder()
    },
}
</script>

<style>
.showcharts .svg-icon {
  width: 100px;
  height: 100px;
  /* float: left; */
  /* vertical-align: -0.2em; */
  fill: currentColor;
  overflow: hidden;
}
.showcharts-card .el-card__body{
    padding-left: 0;
    padding-top: 0;
}
</style>
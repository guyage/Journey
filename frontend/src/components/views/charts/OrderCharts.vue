<template>
    <div class="ordercharts">
        <el-row>
            <el-col :span="8" style="margin-right:10px;">
                <div class="ordercharts-card">
                    <el-card style="height:100px;" class="box-card" shadow="hover">
                        <div style="float:left;">
                            <icon-svg iconClass="iconwodedingdan"></icon-svg>
                        </div>
                        <div style="display:inline-block;margin-top:20px;">
                            <p style="color:rgb(64, 158, 255);font-size:32px;">{{sqlorder_total}}/{{sqlorder_total}}/{{sqlorder_total}}/{{sqlorder_total}}</p>
                            <p style="color:#99a9bf;">待处理/已处理/异常/工单总数(今日)</p>
                        </div>
                    </el-card>
                </div>
            </el-col>
            <el-col :span="5" style="margin-right:10px;">
                <div class="ordercharts-card">
                    <el-card style="height:100px;" class="box-card" shadow="hover">
                        <div style="float:left;">
                            <icon-svg iconClass="iconwodedingdan"></icon-svg>
                        </div>
                        <div style="display:inline-block;margin-top:20px;">
                            <p style="color:rgb(64, 158, 255);font-size:32px;">{{sqlorder_total}}</p>
                            <p style="color:#99a9bf;">工单总数</p>
                        </div>
                    </el-card>
                </div>
            </el-col>
            <el-col :span="5" style="margin-right:10px;">
                <div class="ordercharts-card">
                    <el-card style="height:100px;" class="box-card" shadow="hover">
                        <div style="float:left;">
                            <icon-svg iconClass="iconxingzhuanggongnengtubiao-1"></icon-svg>
                        </div>
                        <div style="display:inline-block;margin-top:20px;">
                            <p style="color:rgb(36, 170, 125);font-size:32px;">{{sqlorder_total}}</p>
                            <p style="color:#99a9bf;">已处理工单</p>
                        </div>
                    </el-card>
                </div>
            </el-col>
            <el-col :span="5">
                <div class="ordercharts-card">
                    <el-card style="height:100px;" class="box-card" shadow="hover">
                        <div style="float:left;">
                            <icon-svg iconClass="icon-yonghuguanli"></icon-svg>
                        </div>
                        <div style="display:inline-block;margin-top:20px;">
                            <p style="color:rgb(215, 119, 255);font-size:32px;">{{sqlorder_total}}</p>
                            <p style="color:#99a9bf;">用户数</p>
                        </div>
                        
                    </el-card>
                </div>
            </el-col>
        </el-row>
        <el-row style="margin-top:10px;">
            <!-- <div class="ordercharts-hissqlorder">
                <el-card class="hissqlorder-card" shadow="hover">
                <div slot="header" class="clearfix">
                    <span>最近7天工单数(个)</span>
                </div>
                <div id="hisSqlOrder" style="width:100%;height:300px;"></div>
            </el-card>
            </div> -->
            <DrawLine v-if="isshow" :title="title" :options="options"></DrawLine>
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
            isshow: false,
            sqlorder_total: '',
            title: '最近7天工单数(个)',
            options: {
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
        }
    },
    methods: {
        ShowInitCharts() {
            ShowCharts({'flag':0}).then((response) => {
                let col = ''
                col = response.data.col[0]
                this.sqlorder_total = response.data.results[0][col]
                console.log('sqlorder_total',this.sqlorder_total);
            })
        },
        showHisSqlOrder() {
            ShowCharts({'flag':1}).then((response) => {
                if (response) {
                    this.options.legend.data.push('SQL工单')
                    let hissqlorder = { name: 'SQL工单',type: 'line',stack: '总量',data: response.data.results.histotal}
                    this.options.series.push(hissqlorder)
                    this.options.xAxis.data = response.data.results.hisdate
                    this.isshow = true
                }
            })
        },
        // dateList() {
        //     let dateArray = [];
        //     let myDate = new Date(); //获取今天日期
        //     myDate.setDate(myDate.getDate() - 7);
        //     let dateTemp;  // 临时日期数据
        //     let flag = 1; 
        //     for (let i = 0; i < 7; i++) {
        //         dateTemp = myDate.getFullYear() + '-' +(myDate.getMonth()+1)+"-"+myDate.getDate();
        //         dateArray.push(dateTemp);
        //         myDate.setDate(myDate.getDate() + flag);
        //     }
        //     console.log(dateArray);
        //     this.options.xAxis.data = dateArray
        //     console.log(this.options.xAxis.data);
            
            
        // },
    },
    mounted() {
        this.ShowInitCharts()
        this.showHisSqlOrder()
    },
    created() {
        // this.showHisSqlOrder()
    },
}
</script>

<style>
.ordercharts .svg-icon {
  width: 100px;
  height: 100px;
  /* float: left; */
  /* vertical-align: -0.2em; */
  fill: currentColor;
  overflow: hidden;
}
.ordercharts-card .el-card__body{
    padding-left: 0;
    padding-top: 0;
}
</style>
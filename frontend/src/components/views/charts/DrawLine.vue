<template>
    <div class="drawline">
        <div v-if="title" class="drawline-card">
                <el-card class="drawline-card" shadow="hover">
                <div slot="header" class="clearfix">
                    <span>{{title}}</span>
                </div>
                <div id="show-drawline" style="width:100%;height:300px;"></div>
            </el-card>
        </div>
    </div>
</template>

<script>
export default {
    name: '',
    props: {
        title: {
            type: String
        },
        options: {
            type: Object
        }
    },
    methods: {
        // 画图函数
        drawLine(options){
            // 基于准备好的dom，初始化echarts实例
            let myChart = this.$echarts.init(document.getElementById('show-drawline'))
            // 绘制图表
            myChart.setOption(options);
        },
    },
    mounted() {
        console.log(this.options);
        
        this.drawLine(this.options)
    },
}
</script>

<style>
.drawline .el-card__header {
    padding: 5px 5px;
}
.drawline  .el-card__body {
    padding: 10px;
}
.drawline  .clearfix {
    text-align: left;
    padding-left: 10px;
}
</style>
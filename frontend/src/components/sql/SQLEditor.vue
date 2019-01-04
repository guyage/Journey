<template>
    <div class="sqleditor">
        <el-alert title="请输入SQL语句：" type="info" :closable="false">
            <div class="sqleditor-sqlformat">
               <icon-svg @click.native="sqlFormat" iconClass="icon-moshubang" slot="suffix"></icon-svg> 
            </div>
        </el-alert>
        <codemirror ref="sqleditor" v-model="code" :options="cmOption"></codemirror>
    </div>
    
</template>

<script>
import sqlFormatter from "sql-formatter";
import 'codemirror/mode/sql/sql.js';
import 'codemirror/theme/solarized.css';
export default {
    data () {
        return {
            code: '',
            cmOption: {
                tabSize: 4,
                styleActiveLine: true,
                viewportMargin: Infinity,
                lineNumbers: true,
                line: true,
                mode: 'text/x-mysql',
                theme: 'solarized light'
                // theme: 'xq-light'   
            }
        }
    },
    methods: {
        sqlFormat() {
            if (this.code.length > 0) {
                let sqlContent = this.code
                this.code = sqlFormatter.format(sqlContent)
            }
            
        }
    }
}
</script>

<style>
.sqleditor .cm-s-solarized.cm-s-light .CodeMirror-gutters{
    background-color: #eee; 
}
.sqleditor .cm-s-solarized.cm-s-light{
  background-color: #f4f4f5;
  height: 400px;
}
.sqleditor .sqleditor-sqlformat{
    position: absolute;
    top: 7px;
    right: 15px;
}
</style>

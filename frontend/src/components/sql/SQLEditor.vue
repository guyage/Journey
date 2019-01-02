<template>
    <div class="sqleditor">
        <el-alert title="请在输入框输入SQL语句：" type="info" :closable="false"></el-alert>
        <codemirror v-model="code" :options="cmOption"></codemirror>
    </div>
    
</template>

<script>
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
    }
}
</script>

<style>
.cm-s-solarized.cm-s-light .CodeMirror-gutters{
    background-color: #eee; 
}
.cm-s-solarized.cm-s-light{
  background-color: #f4f4f5; 
}
</style>

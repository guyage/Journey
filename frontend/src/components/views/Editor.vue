<template>
    <div class="editor">
        <el-alert title="请输入SQL语句：" type="info" :closable="false">
            <div class="editor-sqlformat">
               <icon-svg @click.native="sqlFormat" iconClass="icon-moshubang" slot="suffix"></icon-svg> 
            </div>
        </el-alert>
        <codemirror ref="editor" v-model="code" :options="cmOption"></codemirror>
        <!-- <textarea ref="editor" class="codesql" v-model="code" style="height:200px;width:600px;"></textarea> -->
    </div>
    
</template>

<script>
import sqlFormatter from "sql-formatter";
import 'codemirror/mode/sql/sql.js';
import 'codemirror/theme/solarized.css';
import "codemirror/addon/hint/show-hint.css";
require("codemirror/addon/edit/matchbrackets");
require("codemirror/addon/selection/active-line");
require("codemirror/mode/sql/sql");
require("codemirror/addon/hint/show-hint");
require("codemirror/addon/hint/sql-hint");

export default {
    data () {
        // const generateTablesHint = () => {
        //     return { student: ['name']}
        // }
        return {
            code: '',
            cmOption: {
                tabSize: 4,
                styleActiveLine: true,
                viewportMargin: Infinity,
                lineWrapping: true,
                lineNumbers: true,
                line: true,
                mode: 'text/x-mysql',
                theme: 'solarized light',
                extraKeys: {"Ctrl":"autocomplete"},
                matchBrackets: true,
                hintOptions: {
                    completeSingle: false,
                    tables: {},
                }
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
    },
    mounted() {
        let editor = this.$refs.editor.codemirror
        editor.on('cursorActivity', function() {
            editor.showHint()
        })
    },
}
</script>

<style>
.editor .cm-s-solarized.cm-s-light .CodeMirror-gutters{
    background-color: #eee; 
}
.editor .cm-s-solarized.cm-s-light{
  background-color: #f4f4f5;
  height: 400px;
}
.editor .editor-sqlformat{
    position: absolute;
    top: 7px;
    right: 15px;
}
.editor .el-alert{
    padding: 1px 1px;
}
</style>

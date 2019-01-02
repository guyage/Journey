<template>
    <div id="nav" class="nav">
      <el-container>       
        <el-aside >
          <el-scrollbar style="height:100%;">
            <el-menu 
            :default-active="$router.path" 
            background-color="#545c64" 
            text-color="#fff" 
            active-text-color="#ffd04b"
            ref="navmenu" 
            router>
              <NavMenu></NavMenu>
              
            </el-menu>
          </el-scrollbar>
        </el-aside>
        <el-container>
            <el-header>
            <Breadcrumb></Breadcrumb>
            <TagsView></TagsView>
            </el-header>
          <el-main>
            <transition :name="transitionName">
              <keep-alive :include="cachedViews">
                <router-view></router-view>
              </keep-alive>
            </transition>
            
          </el-main>
        </el-container>
      </el-container>
    </div>
</template>


<script>
import NavMenu from './NavMenu.vue';
import Breadcrumb from './Breadcrumb.vue';
import TagsView from './TagsView.vue';
import Axios from '@/utils/axios.js';
import store from '@/store/store.js';
export default {
    data() {
      return {
        msg: '',
        transitionName: 'slide-fade',
        // breads: []
      }
    },
    components: {
      Breadcrumb,
      NavMenu,
      TagsView
    },
    computed: {
      cachedViews() {
        return this.$store.state.tagsview.cachedViews
      }
    },
    // watch: {
      
    // }
  };
</script>

<style>
*{
  margin: 0;
  padding: 0;
}
.el-container{
  min-height: 100%;
  position: absolute;
  width: 100%;
}
.el-header {
  background-color: rgb(255,255,255);
  color: #333;
  text-align: center;
  line-height: 60px;
  box-shadow: 0 1px 3px 0 rgba(0,0,0,.12), 0 0 3px 0 rgba(0,0,0,.04);
  border-bottom: 1px solid #d8dce5;
  position: relative;
  height: 80px!important;
  
}
  
  .el-aside {
    color: #333;
    text-align: center;
    line-height: 200px;
    width: 200px!important;
    height: 100%;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 999;
    background-color: rgb(84, 92, 100);
    overflow: hidden;
  }
  
  .el-main {
    background-color: #ffffff;
    color: #333;
    text-align: center;
    /* line-height: 160px; */
  }
  .is-vertical{
    margin-left:200px;
    position: relative;
    min-height: 100%;
  }

.el-scrollbar__wrap {
   overflow-x: hidden;
}
/* 可以设置不同的进入和离开动画 */
/* 设置持续时间和动画函数 */
/* .slide-fade-enter-active {
  transition: all .9s ease;
}
.slide-fade-leave-active {
  transition: all .8s cubic-bezier(1.0, 0.5, 0.8, 1.0);
}
.slide-fade-enter, .slide-fade-leave-to
{
  transform: translateX(10px);
  opacity: 0;
} */
</style>
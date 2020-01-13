![Image text](https://github.com/guyage/Journey/blob/master/frontend/src/assets/logo.png)
# Journey DB平台
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/build-release-brightgreen.svg)
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/version-0.1.0-brightgreen.svg)
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/python-3.6.5-brightgreen.svg)
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/Django-2.0.4-brightgreen.svg)
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/djangorestframework-3.8.2-brightgreen.svg)
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/vue.js-2.5.2-brightgreen.svg)
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/element--ui-2.4.6-brightgreen.svg)
## 功能简介
* 全局配置
  * 邮件配置：配置平台邮件服务
  * QueryLimit：设置查询返回行数限制
  * 导出白名单：提供个别需求需要查询超出limit限制数据，针对用户的白名单
  * 工单配置：配置工单(添加不同的工单需求，可定制工单参数，审批流程，执行脚本)
  * 审批组：工单相关的审批组
* 用户权限
  * 菜单：系统菜单配置，分为一级目录，二级菜单对应相应路由(内部跳转路由不配置图标即可不显示)，三级按钮(实际为对应二级菜单路由的post、patch、delete请求)
  * 用户组：用户所属用户组，便于公司内部人员分组，跟其他功能无相关
  * 角色：角色控制权限(通过用户->角色->权限)，默认新用户只可访问仪表盘，超级用户，可访问所有权限
  * 用户：用户管理
* MySQL
  * MySQL实例：管理MySQL实例(以前为以数据为单位管理，后面发现使用不方便)
  * 数据库用户：管理MySQL用户
  * 数据库实例状态：管理MySQL实例状态(processlist、innodb状态、master/slave状态)
* MongoDB
  * MongoDB实例：管理MongoDB实例
* Redis
  * Redis实例：管理Redis实例
* 数据库权限
  * MySQL权限：用户默认无可访问MySQL权限，通过申请，待管理员同意后，方可访问
  * MongoDB权限：用户默认无可访问MongoDB权限，通过申请，待管理员同意后，方可访问
  * Redis权限：用户默认无可访问Redis权限，通过申请，待管理员同意后，方可访问
* Query
  * 数据库元数据：显示MySQL表结构
  * QuerySql：mysql查询功能，提供语法提示功能，导出查询结果功能，limit限制可通过QueryLimit动态调整
  * QueryMongoDB：MongoDB查询功能
  * QueryRedis：Redis查询功能
* 自助工单申请：
  * 新建工单：创建工单
  * 我创建的：查看自己创建的工单
  * 我待办的：待办工单
* SQL工单：
  * 新建SQL工单：新建SQL工单(审核部分集成inception，inception已闭源，见个人fork项目)
  * 我的SQL工单：我创建的SQL工单
  * 待办SQL工单：我待办的SQL工单
  * 全部SQL工单：全部历史工单，默认显示近7日的工单，可通过时间搜索
## 环境
* 后端
  * python 3.6
  * Django 2.0
  * djangorestframework 3.8
* 前端
  * Vue.js 2.5
  * element-ui 2.4.6
  * vue-router 3.0.1
  * vuex 3.0.1
## 安装文档
[安装文档](https://github.com/guyage/Journey/blob/master/install.md)
## 部分功能展示
登录界面(支持LADP和普通登陆)：
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/1.png)
dashboard页面：
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/111.png)
菜单管理：
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/12.png)
角色管理：
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/2.png)
SQL工单功能页面：
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/112.png)
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/113.png)
MySQL功能页面：
MySQL用户列表页面：
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/6.png)
MySQL实例状态页面：
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/7.png)
MySQL元数据页面：
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/8.png)
QueryLimit页面：
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/9.png)
QuerySQL页面：
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/5.png)
工单相关页面：
工单配置：
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/3.png)
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/4.png)
工单页面：
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/10.png)
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/11.png)
## 其他
工单配置功能中动态Form功能参考(https://github.com/GavinZhuLei/vue-form-making)
## 使用交流
* QQ群：521745114

说明：项目目前在重构，重构原因：主要涉及后端models设计，后面添加功能发现使用不方便，还有前端请求后端部分，添加了统一的api文件，方便管理，另外样式部分需要调整

备注：项目是个人在满足公司需求时做的，也希望能帮助到其他人，项目刚开始，后期会增加其他功能。

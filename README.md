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
* 用户管理
  * 用户：管理平台用户，设置用户禁用及超级帐号
  * 用户组：管理用户组
* MySQL管理
  * MySQL实例：管理MySQL实例(以前为以数据为单位管理，后面发现使用不方便)
  * 数据库用户：管理MySQL用户
  * 数据库元数据：显示MySQL表结构
  * 数据库实例状态：管理MySQL实例状态(processlist、innodb状态、master/slave状态)
* 数据库权限
  * MySQL权限：用户默认无可访问MySQL权限，通过申请，待管理员同意后，方可访问
* 全局配置
  * 邮件配置：配置平台邮件服务
* MongoDB管理
  * 待重构
* Redis管理
  * 待重构
* SQL
  * 待重构
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
用户管理：
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/2.png)
用户组页面：
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/3.png)
添加用户组页面：
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/4.png)
MySQL权限页面：
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/5.png)
申请MySQL权限页面：
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/6.png)
邮件配置页面：
![Image text](https://github.com/guyage/Journey/blob/master/frontend/github_img/7.png)
## 使用交流
* QQ群：521745114

说明：项目目前在重构，重构原因：主要涉及后端models设计，后面添加功能发现使用不方便，还有前端请求后端部分，添加了统一的api文件，方便管理，另外样式部分需要调整

备注：项目是个人在满足公司需求时做的，也希望能帮助到其他人，项目刚开始，后期会增加其他功能。

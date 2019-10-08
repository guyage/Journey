# Journey DB平台安装步骤
## 环境准备
python 3.6+
mysql 5.6+
## 安装步骤
1. 克隆代码
```bash
cd /tmp/
git clone https://github.com/guyage/Journey.git
mkdir -p /app/
将后端Django程序拷贝至单独目录
mv /tmp/Journey/backend /app/Journey
或者直接下载zip包，上传到创建目录
```
2. 安装项目后端依赖包
```bash
cd /app/Journey/backend
pip install -r requirements.txt
```
其中ldap相关包，参照后面安装方式，因ldap相关包直接安装问题较多
3. 创建项目数据库及用户(项目所需MySQL数据库)
安装MySQL后，进入MySQL命令行
创建数据库
```bash
create database journey;
```
创建用户
```
grant all privileges on journey.* to journey@'项目后端Django服务所在IP' identified by 'journey';
```
4. 配置配置文件
```bash
cd /app/Journey
vim Journey.conf
```
配置文件说明如下：
项目访问地址：可自定义(需注意，自定义修改前端项目配置文件对应域名，Journey/frontend/config/下env.js文件)
配置完配置文件后初始化django models到数据库
```bash
cd /app/Journey
python manage.py makemigrations
python manage.py migrate
成功后
导入菜单
source 在项目backend/initsql/menus.sql
```
5. 配置gunicorn
```bash
cd /app/Journey/Journey
vim gunicorn_config.py
```
gunicorn配置文件如下：
```ini
import multiprocessing

bind = "0.0.0.0:8888"  
workers = 8
errorlog = '/logs/Journey/gunicorn.error.log'
accesslog = '/logs/Journey/gunicorn.access.log'
#loglevel = 'debug'
proc_name = 'Journey'
```
6. 创建用户后并启动后端Django服务，确认是否启动成功
这里测试的时候可以通过python manage.py runserver 0.0.0.0:8888启动，生产建议用下面方式启动

创建用户
```bash
cd /app/Journey
python manage.py createsuperuser
根据提示创建用户，用户后续使用普通登录方式
```
启动后端Django服务
```bash
cd /app/Journey
gunicorn Journey.wsgi:application -c ./Journey/gunicorn_config.py
```
通过访问http://xxx.xxx.xxx.xxx:8888/ 确认是否安装成功
7. 前端项目
这里需要node环境，先安装node
node版本需要注意一下，可能会出现版本问题
```bash
node -v
v8.11.3
```
### 开发模式下：
需注意，前端项目服务器需要配置hosts，解析journey.api(可修改，前端项目config下dev.env.js文件中)域名到后端Django实际ip
127.0.0.1(后端Django实际ip) journey.api
```bash
这里需要注意一点，最好提前安装vue脚手架，因为可能存在后续安装依赖包出现环境问题
安装vue脚手架
npm install -g vue-cli
然后安装项目依赖
cd /tmp/Journey/frontend
npm install
npm run dev
然后访问http://xxx.xxx.xxx.xxx:8080/
```
### 生产模式下：
生产模式需要先部署nginx
```bash
安装vue脚手架
npm install -g vue-cli
打包前端vue项目
cd /tmp/Journey/frontend
npm install
npm run build
将生成dist文件夹，拷贝到/app/Journey下
cp -rf dist /app/Journey/
```
配置nginx：
```ini
server {
        # 项目访问域名，需与配置文件中一致，还有前端项目config下prod.env.js中域名一致
        server_name  journey.xs.jf; 
        listen 80;
        access_log /logs/nginx/journey.access.log main;
        error_log  /logs/nginx/journey.error.log;

        location /api {
            # 配置后端Django服务访问地址
            proxy_pass http://X.X.X.X:8888;
            # 此为upstream配置方式，需添加upstream配置文件
            #proxy_pass http://journey.api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location / {
            root /app/Journey/dist;  # 注意此项，前端开发完成后，会做打包处理，此文件夹为打包后的文件夹
            index index.html;
        }

        location ~.*\.(js|css|png|jpg)$ {
            root /app/Journey/dist;
            expires 3h;
        }
}
```
配置完后，启动nginx
访问http://journey.xs.jf
使用前面创建的用户登陆系统


## 可能遇到的问题
#### centos安装django-auth-ldap遇到的问题
安装django_auth_ldap需要依赖python_ldap,  openldap
CentOS要实现openLDAP必须先安装openldap,  openldap-servers,  openldap-clients三个包。第一个默认已经安装好了。
默认easy_install或者pip install很容易遇到这个错误

/usr/include/sasl/sasl.h:349: 警告：函数声明不是一个原型
Modules/ldapcontrol.c: In function ‘encode_assertion_control’:
Modules/ldapcontrol.c:352: 警告：隐式声明函数 ‘ldap_create_assertion_control_value’
Modules/constants.c: In function ‘LDAPinit_constants’:
Modules/constants.c:155: 错误：‘LDAP_OPT_DIAGNOSTIC_MESSAGE’ 未声明 (在此函数内第一次使用)
Modules/constants.c:155: 错误：(即使在一个函数内多次出现，每个未声明的标识符在其
Modules/constants.c:155: 错误：所在的函数内只报告一次。)
Modules/constants.c:365: 错误：‘LDAP_CONTROL_RELAX’ 未声明 (在此函数内第一次使用)
error: Setup script exited with error: command 'gcc' failed with exit status 1

原因是版本不兼容，centos默认装了个2.3的。以下指令好使
```bash
yum install openldap openldap24-libs openldap-clients openldap-devel openldap24-libs-devel
export CPATH=/usr/include/openldap24
export LIBRARY_PATH=/usr/lib/openldap24/     (以上为安装openldap)
pip install python-ldap

pip install django-auth-ldap(依赖python_ldap)
```
验证OK了

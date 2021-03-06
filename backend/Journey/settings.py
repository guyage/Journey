"""
Django settings for Journey project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import configparser
import sys
import datetime
#ldap认证相关
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, PosixGroupType, LDAPGroupQuery, LDAPSearchUnion

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'utils'))

# 获取配置文件信息
config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR,'Journey.conf'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o5q&8jpgjc0va&ji^t8el&&k7s67i!pvc$#gif$44*923z15c('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# 修改django默认使用用户表
AUTH_USER_MODEL = 'user.Users'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 解决跨域
    'corsheaders',
    'rest_framework',
    'user',
    'common',
    'conf',
    'db',
    'query',
    'charts',
    'easyaudit',
    'workorder',
]

MIDDLEWARE = [
    # 解决跨域
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# 解决跨域
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'Journey.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# 上传路径
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")
MEDIA_URL = "/uploads/"

WSGI_APPLICATION = 'Journey.wsgi.application'
# 配置认证方式
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    #  配置默认的认证方式  帐号密码认证
    'DEFAULT_AUTHENTICATION_CLASSES' : (  
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# JWT 配置
JWT_AUTH = {
    # token 有效期
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 有效期内可以利用旧token刷新新token
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 自定义登陆返回结果
    'JWT_RESPONSE_PAYLOAD_HANDLER':'user.utils.jwt_response_payload_handler',
    'JWT_GET_USER_SECRET_KEY': 'user.models.jwt_get_secret_key',
    'JWT_ALLOW_REFRESH': True,
}

# ldap认证相关配置
# ladp连接信息(参数在Journey.conf中设置)
LDAP_URI = config.get('ldap', 'ldap_uri')
LADP_BASE_DN = config.get('ldap', 'ldap_base_dn')
LADP_BIND_DN = config.get('ldap', 'ldap_bind_dn')
LADP_BIND_PASSWD = config.get('ldap', 'ldap_bind_passwd')

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_LDAP_SERVER_URI = LDAP_URI  # 服务器地址
# ldap查找用户,可以为任一用户
AUTH_LDAP_BIND_DN = LADP_BIND_DN + ',' + LADP_BASE_DN
AUTH_LDAP_BIND_PASSWORD = LADP_BIND_PASSWD
# key为数据库字段名，value为ldap中字段名，此字典解决django model与ldap字段名可能出现的不一致问题
AUTH_LDAP_USER_ATTR_MAP = {
    "username": "sAMAccountName",
    'email': 'mail',
    "first_name": "givenName",
    "last_name": "sn",
}

AUTH_LDAP_USER_SEARCH = LDAPSearch(
    LADP_BASE_DN,
    ldap.SCOPE_SUBTREE,
    '(sAMAccountName=%(user)s)',    
)

AUTH_LDAP_GROUP_SEARCH = LDAPSearch(LADP_BASE_DN,ldap.SCOPE_SUBTREE, "(objectClass=group)" )  #搜索某个OU下组信息
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn") #返回的组的类型，并用来判断用户与组的从属关系
# AUTH_LDAP_MIRROR_GROUPS = True #导入用户的组信息，在用户登录的时候把用户的域组关系同步过来。每次用户登录时，都会把用户的组关系删除，重新从ldap中进行同步（解决办法参考后面）
AUTH_LDAP_ALWAYS_UPDATE_USER = True #是否同步LDAP修改



# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# 获取配置文件信息
# config = configparser.ConfigParser()
# config.read(os.path.join(BASE_DIR,'Journey.conf'))
# django 数据库连接信息
DB_HOST = config.get('db', 'host')
DB_PORT = config.getint('db', 'port')
DB_USER = config.get('db', 'user')
DB_PASSWORD = config.get('db', 'password')
DB_DATABASE = config.get('db', 'database')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_DATABASE,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# -*- coding: utf-8 -*-
import os
import sys
import logging
import hashlib
import requests
import hmac
import time
import base64
import json
import uuid
import urllib3
import datetime
from urllib import parse

# from .models import AccessKey
# from utils.cryption import decypt


class Sign(object):
    """
    签名机制
    https://help.aliyun.com/document_detail/29747.html?spm=a2c4g.11186623.6.620.600111b6pEpZjE
    """

    def __init__(self, secretKey):
        self.secretKey = secretKey

    def url_encoder(self, s):
        ret = parse.quote(s)
        ret = ret.replace('+', '%20')
        ret = ret.replace('*', '%2A')
        ret = ret.replace('%7E', '~')
        return ret

    # 生成签名串
    def make(self, params, method='GET'):
        params_join = "&".join(
            k + "=" + str(self.url_encoder(str(params[k]))) for k in sorted(params.keys()))
        srcStr = method.upper() + '&%2F&' + self.url_encoder(params_join)
        hashed = hmac.new(
            bytes(
                self.secretKey, encoding='utf8'), bytes(
                srcStr, encoding='utf8'), hashlib.sha1)
        return base64.b64encode(hashed.digest())


class QyCloud(object):
    """
    iaas相关操作类
    """
    requestHost = 'api.qingcloud.com'
    requestUri = '/iaas'





    def __init__(self,zone,ak,sk):

        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        now = (datetime.datetime.now() - datetime.timedelta(minutes=480)).strftime("%Y-%m-%d %H:%M:%S")
        five_min_ago = (datetime.datetime.now() - datetime.timedelta(minutes=485)).strftime("%Y-%m-%d %H:%M:%S")
        # 转换时间格式 "2011-07-11T11:07:00Z"
        start = five_min_ago[0:10] + 'T' + five_min_ago[11:] + 'Z'
        end = now[0:10] + 'T' + now[11:] + 'Z'
        self.access_key_id = ak
        self.zone = zone
        # 用于加密的Secret为 AccessKeySecret加上&字符
        self.AccessKeySecret = sk + '&'
        self.params = {
            "zone": self.zone,
            "signature_version": 1,
            "signature_method": "HmacSHA256",
            "version": 1,
            'access_key_id': self.access_key_id,
            'time_stamp': timestamp
            # "start_time": start,
            # "end_time": end,
            # "time_stamp": end,
        }
        self.url = 'https://%s%s' % (QyCloud.requestHost,
                                     QyCloud.requestUri)


    def get_instance(self):
        """
        获取主机列表

        """
        self.params['action'] = 'DescribeInstances'
        # self.params['status'] = status
        # self.params['limit'] = limit
        self.params['signature'] = Sign(self.AccessKeySecret).make(self.params)

        ret = requests.get(self.url, params=self.params)

        print(self.url)
        print(self.params)
        return json.loads(ret.text)



if __name__ == "__main__":
    qy_access_key_id = 'OLNWYAUNKRHMGTYSFUTT'
    qy_secret_access_key = 'qIDTz6JF9PHhe7EooAq5SgfkRUTGfQ7ZbUX1std6'
    zone = 'pek3b'

    qy = QyCloud(zone=zone, ak=qy_access_key_id,sk=qy_secret_access_key)
    status = ['Running']
    ins = qy.get_instance()

    print(ins)



# -*- coding:utf-8 -*-

import os
import time
import json
import sys
import textwrap
import argparse
import qingcloud.iaas
import inspect
import logging
import ssl
from qingcloud.iaas.actions.instance import InstanceAction

logger = logging.getLogger('default')
#青云API key


class QyCloud(object):
    """qingyun cloud management"""

    def __init__(self, ak, sk, zone, conn):
        self.ak = ak
        self.sk = sk
        self.zone = zone

        self.conn = qingcloud.iaas.connect_to_zone(zone=self.zone, access_key_id=self.ak, secret_access_key=self.sk)
        ssl._create_default_https_context = ssl._create_unverified_context
    def get_all_server_info(self):
        res = {}
        try:
            # res = instances.describe_instances(status=["running"])
            res = self.conn.describe_instances(status=['running', 'stopped'],limit=50)["instance_set"]
        except Exception as e:
            print("获取失败，错误日志为:{}".format(e))
        return res




# if __name__ == "__main__":
#     qy = QyCloud(ak=qy_access_key_id, sk=qy_secret_access_key, zone=zone, conn=None)
#     res = qy.get_all_server_info()
#     print(res)

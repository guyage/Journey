# -*- coding: utf-8 -*-
#加盐解密


import os
import sys
import logging
from cryptography.fernet import Fernet
from alidns.models import AccessKey


logger = logging.getLogger('default')

class decypt(object):

	def __init__(self,saltkey):

		#获取环境变量中的加盐密钥
		saltkey_temp = os.environ.get("saltkey")
		if saltkey_temp is None:
			logger.error('环境变量中获取saltkey失败')
			sys.exit(1)
		else:
			self.saltkey = bytes(saltkey_temp, encoding='utf8')


	def decryptV(self,encrypted_key):
		cipher = Fernet(self.saltkey)
		k = bytes(encrypted_key, encoding='utf8')
		decrypted_value = cipher.decrypt(k)
		return str(decrypted_value, encoding='utf8')

	def get_encrypted_key(self,realkey):
		self.realkey = bytes(realkey,encoding='utf8')
		cipher = Fernet(self.saltkey)
		encrypted_text = cipher.encrypt(self.realkey)

		return encrypted_text

	def get_decrypeted_key(self,accountname):
		ret = {}
		self.accountname = accountname
		accesskey = AccessKey.objects.filter(account_name=self.accountname)
		if accesskey:
			for i in accesskey:
				ak = self.decryptV(i.accesskey_id)
				sk = self.decryptV(i.accesskey_secret)
				ret['ak'] = ak
				ret ['sk'] = sk
			return ret

		else:
			logger.error("获取key配置失败,{}".format(self.accountname))
			return False




# if __name__ == '__main__':
#
# 	de =decypt(saltkey=None)
# 	ret = de.get_decrypeted_key('qy_api_key')
#
# 	print(ret)
# real_key = 'Z'
# ret = de.get_encrypted_key(real_key)
# print(ret)
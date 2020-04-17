# -*- coding: utf-8 -*-
#加盐解密
import os
import sys
import logging
from cryptography.fernet import Fernet
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
		return str(encrypted_text, encoding='utf8')
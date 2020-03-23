# -*- coding: utf-8 -*-
import paramiko
import logging

logger = logging.getLogger('views')


class Ssh(object):
    """
    SSH 连接
    """

    def __init__(
            self,
            ip,
            port,
            key,
            username="root",
            auth_type="passwd",
            timeout=10):
        self.ip = ip
        self.port = port
        self.username = username
        self.auth_type = auth_type
        self.key = key

        #ssh & sftp
        self.transport = None
        self.ssh = None
        self.sftp = None
        self.timeout = timeout
        # self.sock = (self.ip, self.port)

        # self._try_times = 1 #重试次数为3

    # 建立连接
    def connect(self):
        # while True:
        # 尝试连接
        try:
            self.transport = paramiko.Transport(sock=(self.ip, self.port))
            if self.auth_type == "passwd":
                self.transport.connect(
                    username=self.username, password=self.key)
                # 如果没有异常，直接返回

                self.ssh = paramiko.SSHClient()
                self.ssh.transport = self.transport
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())# 通过公共方式进行认证 (不需要在known_hosts 文件中存在)

                logger.info(
                    "ssh IP:{} Port:{}连接成功 ".format(
                        self.ip, self.port))
                # sftp连接
                # self.sftp = paramiko.SFTPClient()

                return True
            elif self.auth_type == "pkey":

                self.transport.connect(username=self.username, pkey=self.key)
                # 如果没有异常，直接返回

                self.ssh = paramiko.SSHClient()
                self.ssh.transport = self.transport

                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())# 通过公共方式进行认证 (不需要在known_hosts 文件中存在)
                logger.info(
                    "ssh IP:{} Port:{}连接成功 ".format(
                        self.ip, self.port))
                # sftp连接
                self.sftp = paramiko.SFTPClient()

                return True
        except Exception as e:
            # if self._try_times != 0:
            #     print("第{}次连接IP:{},失败原因{}".format(4 - self._try_times ,self.ip, e))
            #     print("开始重试")
            #     self._try_times -= 1
            # else:
            #     print("第{}次连接IP:{},失败原因{}".format(4 - self._try_times, self.ip, e))
            #     print("ssh IP:{} Port:{}连接失败".format(self.ip, self.port))
            #     print("结束重试")
            print(
                "ssh连接 IP:{0} Port:{1}失败，失败原因{2}".format(
                    self.ip, self.port, e))
            return False

    # 断开连接
    def close(self):
        if self.transport:
            self.transport.close()

    # 发送要执行的命令
    def exec_cmd(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_cmd(cmd)
        return stdout.read().decode(), stderr.read().decode()

    # sftp get单个文件

    def sftp_get(self, remotefile, localfile):
        try:
            self.sftp.get(remotefile, localfile)
            print("文件{}下载成功".format(remotefile))
        except Exception as e:
            print("下载失败,原因:{}".format(e))

    # sftp put单个文件
    def sftp_put(self, localfile, remotefile):
        try:
            self.sftp.put(localfile, remotefile)
            print("文件{}上传成功".format(localfile))
        except Exception as e:
            print("下载失败,原因:{}".format(e))

    def __del__(self):
        print("{}连接已关闭".format(self.ip))


# # 创建SSH对象
# ssh = paramiko.SSHClient()

# # 连接服务器
# ssh.connect(hostname='c1.salt.com', port=22, username='GSuser', password='123')
# # 执行命令
# stdin, stdout, stderr = ssh.exec_command('ls')
# # 获取命令结果
# result = stdout.read()
# # 关闭连接
# ssh.close()

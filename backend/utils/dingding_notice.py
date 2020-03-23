# -*- coding: UTF-8 -*-
from dingtalkchatbot.chatbot import DingtalkChatbot


class DDNotice(object):
    def __init__(self, token, msg):
        self.token = token
        self.msg = msg

    def send_msg(self):
        webhook = ('https://oapi.dingtalk.com/robot/send?access_token=%s'
                   % (self.token))
        # 初始化机器人
        bot = DingtalkChatbot(webhook)
        # 发送消息
        bot.send_text(msg=self.msg, is_at_all=True)

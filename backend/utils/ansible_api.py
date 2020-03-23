#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通过ansible API动态生成ansible资产信息但不产生实际的hosts文件
主机信息都可以通过数据库获得，然后生成指定格式，最后调用这个类来
生成主机信息。
"""

import sys
# 用于读取YAML和JSON格式的文件
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.parsing.dataloader import DataLoader
# 用于存储各类变量信息
from ansible.vars.manager import VariableManager
# 用于导入资产文件
from ansible.inventory.manager import InventoryManager
# 操作单个主机信息
from ansible.inventory.host import Host
# 操作单个主机组信息
from ansible.inventory.group import Group
# 状态回调，各种成功失败的状态
from ansible.plugins.callback import CallbackBase
from collections import namedtuple
from ansible.executor.task_queue_manager import TaskQueueManager

from ansible.playbook.play import Play

from ansible import context
from ansible.module_utils.common.collections import ImmutableDict


#根据list生成ansible inventory
def gen_inventory(oblist):
    #返回inventory格式
    # temphosts_dict = {
    #     "Group1": {
    #         "hosts": [{"ip": "192.168.160.12", "port": "22", "username": "root"},
    #                   {"ip": "192.168.160.121", "port": "22", "username": "root"},
    #                   {"ip": "192.168.160.155", "port": "8000", "username": "root"},
    #                   {"ip": "192.168.160.247", "port": "8000", "username": "root"},],
    #         "group_vars": {"var1": "ansible"}
    #     },
    # }

    res = {}
    if len(oblist) > 0:
        res = {"Group1": {"hosts": "", "group_vars": ""}}
        tmp_list = []
        for j in oblist:
            # 动态构造inventory
            tmp_dict = {}
            tmp_dict["ip"] = j["ip"]
            tmp_dict["port"] = j["ssh_port"]
            tmp_dict["username"] = "root"
            tmp_list.append(tmp_dict)

        res["Group1"]["hosts"] = tmp_list
        res["Group1"]["group_vars"] = {"var1": "ansible"}

    return res


class CallbackResultCollector(CallbackBase):
    """
    callback改写，格式化输出playbook执行结果
    """
    CALLBACK_VERSION = 2.0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_ok = {}
        self.task_unreachable = {}
        self.task_failed = {}
        self.task_skipped = {}
        self.task_status = {}

    def v2_runner_on_unreachable(self, result):
        """
        重写 unreachable 状态
        :param result:  这是父类里面一个对象，这个对象可以获取执行任务信息
        """
        self.task_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        """
        重写 ok 状态
        :param result:
        """
        self.task_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        """
        重写 failed 状态
        :param result:
        """
        self.task_failed[result._host.get_name()] = result

    def v2_runner_on_skipped(self, result):
        self.task_skipped[result._host.get_name()] = result


class MyInventory:
    """
    动态生成/etc/ansible/hosts文件
    """
    def __init__(self, hosts_resource):
        #  hosts_resource = {
        #         "Group1": {
        #             "hosts": [{"ip": "10.0.0.62", "port": "22", "username": "root", "password": "123456"},
        #                       {"ip": "10.0.0.61", "port": "22", "username": "root", "password": "123456"}],
        #             "group_vars": {"var1": "ansible"}
        #         },
        #         # "Group2": {}
        #     }
        self.hosts_resource = hosts_resource
        self.loader = DataLoader()
        self.hosts_file = [""]
        """
        sources这个我们知道这里是设置hosts文件的地方，它可以是一个列表里面包含多个文件路径且文件真实存在，在单纯的执行ad-hoc的时候这里的
        文件里面必须具有有效的hosts配置，但是当通过动态生成的资产信息的时候这个文件必须存在但是它里面可以是空的，如果这里配置成None那么
        它不影响资产信息动态生成但是会有一个警告
         [WARNING]: No inventory was parsed, only implicit localhost is available
         {'all': [], 'ungrouped': [], 'Group1': ['10.0.0.62', '10.0.0.61']}
        """
        self.inventory = InventoryManager(loader=self.loader, sources=self.hosts_file)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.dynamic_inventory()

    def add_hosts_group(self, hosts_list, group_name, group_vars=None):
        """
        动态添加主机到指定的主机组
        完整的HOSTS文件格式
        [test1]
        hostname ansible_ssh_host=192.168.1.111 ansible_ssh_user="root" ansible_ssh_pass="123456"
        但通常我们都省略hostname，端口也省略因为默认是22，这个在ansible配置文件中有，除非有非22端口的才会配置
        [test1]
        192.168.100.10 ansible_ssh_user="root" ansible_ssh_pass="123456" ansible_python_interpreter="/usr/bin/python3"
        [test2]
        192.168.100.10 ansible_ssh_user="root" ansible_ssh_pass="123456" ansible_python_interpreter="/usr/bin/python3"
        [parent_group:children]
        test1
        test2
        [test2:vars]
        touch_file=new_file
        :param hosts_list: 主机列表 [{"hostname":"m01","ip": "192.168.100.10", "port": "22",
                                     "username": "root", "password": None}, {}]
        :param group_name:  组名称
        :param group_vars:  组变量，格式为字典group_vars={"var1": "ansible"}
        :return:
        """
        # 如果主机组不存在，就添加主机组，如果存在，就直接获取
        if not self.inventory.groups.get(group_name):
            self.inventory.add_group(group_name)
        # 返回值是Group对象，注意这里一定要保证是同一个对象
        inventory_group = self.inventory.groups.get(group_name)
        # 如果组变量存在，就设置组变量，可用于playbook中
        if group_vars:
            for key, value in group_vars.items():
                inventory_group.set_variable(key, value)
        for host in hosts_list:
            ip = host.get("ip", None)
            hostname = host.get("hostname", ip)
            port = host.get("port", "22")
            username = host.get("username")
            password = host.get("password", None)
            ssh_key = host.get("ssh_key", None)
            python_interpreter = host.get("python_interpreter", None)

            try:
                host_obj = Host(name=hostname, port=port)
                self.variable_manager.set_host_variable(host=host_obj, varname="ansible_ssh_host", value=ip)
                self.variable_manager.set_host_variable(host=host_obj, varname="ansible_ssh_port", value=port)
                self.variable_manager.set_host_variable(host=host_obj, varname="ansible_ssh_user", value=username)
                if password:
                    self.variable_manager.set_host_variable(host=host_obj,
                                                            varname="ansible_ssh_pass",
                                                            value=password)
                if ssh_key:
                    self.variable_manager.set_host_variable(host=host_obj,
                                                            varname="ansible_ssh_private_key_file",
                                                            value=ssh_key)
                if python_interpreter:
                    self.variable_manager.set_host_variable(host=host_obj,
                                                            varname="ansible_python_interpreter",
                                                            value=python_interpreter)

                # 添加其他变量
                for key, value in host.items():
                    if key not in ["ip", "hostname", "port", "username", "password", "ssh_key", "python_interpreter"]:
                        self.variable_manager.set_host_variable(host=host_obj, varname=key, value=value)

                # 添加主机到主机组
                self.inventory.add_host(host=hostname, group=group_name, port=port)
            except Exception as e:
                print(e)

    def dynamic_inventory(self):
        # 为了以后扩展，我们先把该段内容写在这里
        for group_name, hosts_and_vars in self.hosts_resource.items():
            self.add_hosts_group(hosts_and_vars.get("hosts"), group_name, hosts_and_vars.get("group_vars"))

    @property
    def inventory_obj(self):
        """
        返回inventory對象
        :return:
        """
        return self.inventory

    @property
    def variable_manager_obj(self):
        """
       返回variable_manager對象
       :return:
       """
        return self.variable_manager


class AdhocRunner(object):
    def __init__(self, hostsresource):

        context.CLIARGS = ImmutableDict(connection='smart', remote_user=None, ack_pass=None, sudo_user=None, forks=5, sudo=None,
                          ask_sudo_pass=False,
                          verbosity=5, module_path="", become=None, become_method=None, become_user=None, check=False,
                          diff=False,
                          listhosts=None, listtasks=None, listtags=None, syntax=None, remote_tmp="/tmp/.ansible")

        self._passwords = dict(sshpass=None, becomepass=None)  # 这个可以为空，因为在hosts文件中
        self._loader = DataLoader()
        myinven = MyInventory(hosts_resource=hostsresource)
        self._inventory = myinven.inventory_obj
        self._variable_manager = myinven.variable_manager_obj


    def run_adhoc(self, hosts, tasks_list, extra_vars=None):
        """
        执行playbook
        :param playbook_path: playbook的yaml文件路径
        :param extra_vars: 额外变量
        :return: 无返回值
        """
        try:
            if extra_vars:
                self._variable_manager.extra_vars = extra_vars
            play_source = dict(name="Ansible Play",  # 任务名称
                               hosts=hosts,  # 目标主机，可以填写具体主机也可以是主机组名称
                               gather_facts="yes",  # 是否收集配置信息
                               # tasks是具体执行的任务，列表形式，每个具体任务都是一个字典
                               tasks=tasks_list)
            play = Play().load(play_source, variable_manager=self._variable_manager, loader=self._loader)
            self._callback = CallbackResultCollector()  # 实例化自定义callback
            tqm = TaskQueueManager(
                inventory=self._inventory,
                variable_manager=self._variable_manager,
                loader=self._loader,
                # options=self._options,
                passwords=self._passwords,
                stdout_callback=self._callback  # 配置使用自定义callback
            )
            tqm.run(play)
            # return self._callback
        except Exception as err:
            print(err)

    def get_adhoc_result(self):
        """
        获取playbook执行结果
        :return:
        """
        result_raw = {"ok": {}, "failed": {}, "unreachable": {}, "skipped": {}, "status": {}}
        for host, result in self._callback.task_ok.items():
            result_raw["ok"][host] = result._result

        for host, result in self._callback.task_failed.items():
            result_raw["failed"][host] = result._result

        for host, result in self._callback.task_unreachable.items():
            result_raw["unreachable"][host] = result._result

        for host, result in self._callback.task_skipped.items():
            result_raw["skipped"][host] = result._result

        for host, result in self._callback.task_status.items():
            result_raw["status"][host] = result._result

        return result_raw


class PlaybookRunner(object):
    def __init__(self, hostsresource):

        context.CLIARGS = ImmutableDict(connection='smart', remote_user=None, ack_pass=None, sudo_user=None, forks=5, sudo=None,
                          ask_sudo_pass=False,
                          verbosity=5, module_path="", become=None, become_method=None, become_user=None, check=False,
                          diff=False,
                          listhosts=None, listtasks=None, listtags=None, syntax=None, remote_tmp="/tmp/.ansible")
        self._passwords = dict(sshpass=None, becomepass=None)  # 这个可以为空，因为在hosts文件中
        self._loader = DataLoader()
        myinven = MyInventory(hosts_resource=hostsresource)
        self._inventory = myinven.inventory_obj
        self._variable_manager = myinven.variable_manager_obj

    def run_playbook(self, playbook_path, extra_vars=None):
        """
        执行playbook
        :param playbook_path: playbook的yaml文件路径
        :param extra_vars: 额外变量
        :return: 无返回值
        """
        try:
            if extra_vars:
                self._variable_manager.extra_vars = extra_vars
            playbook = PlaybookExecutor(playbooks=[playbook_path], inventory=self._inventory,
                                        variable_manager=self._variable_manager, loader=self._loader,
                                        passwords=self._passwords)
            # 配置使用自定义callback
            self._callback = CallbackResultCollector()
            playbook._tqm._stdout_callback = self._callback
            # 执行playbook
            playbook.run()
        except Exception as err:
            print(err)

    def get_playbook_result(self):
        """
        获取playbook执行结果
        :return:
        """
        result_raw = {"ok": {}, "failed": {}, "unreachable": {}, "skipped": {}, "status": {}}
        for host, result in self._callback.task_ok.items():
            result_raw["ok"][host] = result._result

        for host, result in self._callback.task_failed.items():
            result_raw["failed"][host] = result._result

        for host, result in self._callback.task_unreachable.items():
            result_raw["unreachable"][host] = result._result

        for host, result in self._callback.task_skipped.items():
            result_raw["skipped"][host] = result._result

        for host, result in self._callback.task_status.items():
            result_raw["status"][host] = result._result

        return result_raw


def main():
    temphosts_dict = {
        "Group1": {
            "hosts": [{"ip": "192.168.160.12", "port": "22","username": "root"},
                      {"ip": "192.168.160.121", "port": "22","username": "root"}],
            "group_vars": {"var1": "ansible"}
        },
        # "Group2": {}
    }


    # my_inventory_obj = MyInventory(temphosts_dict)
    # print(my_inventory_obj.inventory_obj.get_groups_dict())


    # print(type(my_inventory_obj.inventory_obj.get_groups_dict()))
    # # <class 'dict'>，组内的主机信息就通过操作字典来获取数据了
    # # 2.获取主机对象
    # print(my_inventory_obj.inventory_obj.get_hosts())  # []
    # host = my_inventory_obj.inventory_obj.get_host("192.168.160.12")
    # print()  # 10.0.0.61
    # print(type(host))  # <class 'ansible.inventory.host.Host'>
    # # 3.获取主机的变量
    # print(host.get_vars())
    # # {'ansible_port': 22, 'inventory_file': None, 'inventory_dir': None,
    # # 'inventory_hostname': '10.0.0.61', 'inventory_hostname_short': '10', 'group_names': ['Group1']}
    # print(type(host.get_vars()))  # <class 'dict'>
    # # 4.获取主机所在的组
    # print(host.get_groups())  # [Group1]
    # print(type(host.get_groups()))  # <class 'list'>
    # # 5.获取组对象
    # group_obj = my_inventory_obj.inventory.groups.get("Group1")
    # # group_obj = Group(name="Group2")
    # print(type(group_obj))  # <class 'ansible.inventory.group.Group'>
    # # 6.把主机添加到组中，但这样并没有添加到inventory中
    # my_inventory_obj.inventory.add_group("Group2")
    # group_obj2 = my_inventory_obj.inventory.groups.get("Group2")
    # new_host = Host(name="10.0.0.63", port="22")
    # new_host.add_group(group_obj2)
    # print(new_host.groups)  # [Group2]
    # print(my_inventory_obj.inventory.get_groups_dict())
    # # {'all': [], 'ungrouped': [], 'Group1': ['10.0.0.62', '10.0.0.61'], 'Group2': []}
    # # 添加主机到主机组
    # # 添加主机到主机组
    # my_inventory_obj.inventory.add_host(host="10.0.0.63", group="Group2", port="22")
    # print(my_inventory_obj.inventory.get_groups_dict())
    # # {'all': [], 'ungrouped': [], 'Group1': ['10.0.0.62', '10.0.0.61'], 'Group2': ['10.0.0.63']}

    # # 7.获取主机的变量
    # print(my_inventory_obj.variable_manager.get_vars(host=host))
#     {'var1': 'ansible', 'ansible_port': 22, 'inventory_file': None, 'inventory_dir': None,
#     'inventory_hostname': '10.0.0.61', 'inventory_hostname_short': '10',
#     'group_names': ['Group1'], 'ansible_facts': {}, 'ansible_ssh_host': '10.0.0.61', 'ansible_ssh_port': '22',
#     'ansible_ssh_user': 'root', 'ansible_ssh_pass': '123456',
#     'playbook_dir': '/project/CMDB/task_manage/my_ansible',
#     'ansible_playbook_python': '/usr/bin/python3',
#     'groups': {'all': [], 'ungrouped': [], 'Group1': ['10.0.0.62', '10.0.0.61'], 'Group2': []},
#     'omit': '__omit_place_holder__3a96c0f711c926b0ece7e5caf5d969d656ddfbe0'}


    # # for group, hosts in mi.INVENTORY.get_groups_dict().items():
    # #     print(group, hosts)

    # host = mi.INVENTORY.get_host("192.168.160.12")
    # print(mi.VARIABLE_MANAGER.get_vars(host=host))
    # # mi = MyInventory(hostsresource=temphosts_dict)
    # # for group, hosts in mi.INVENTORY.get_groups_dict().items():
    # #     print(group, hosts)
    # # host = mi.INVENTORY.get_host("192.168.200.12")
    # # print(mi.VARIABLE_MANAGER.get_vars(host=host))


    tasks = []
    tasks.append(dict(action=dict(module="setup",patterns="*",)))
    # tasks.append(dict(action=dict(module="script", args='/project/CMDB/tmp_dir/10.0.0.61应用1.sh', warn=False)))
    hosts = "Group1"
    ar = AdhocRunner(temphosts_dict)
    ar.run_adhoc(hosts, tasks)
    print(ar.get_adhoc_result())
    print("changed==============", ar.get_adhoc_result().get("changed"))
    print("status==============", ar.get_adhoc_result().get("status"))
    print("skipped==============", ar.get_adhoc_result().get("skipped"))
    print("failed==============", ar.get_adhoc_result().get("failed"))


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit()

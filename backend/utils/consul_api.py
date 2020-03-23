import consul

class Consul(object):
    def __init__(self, host, port):
        '''初始化，连接consul服务器'''
        self._consul = consul.Consul(host, port)

    def RegisterService(self, name, host, port, tags=None):
        tags = tags or []
        # 注册服务
        self._consul.agent.service.register(
            name,
            name,
            host,
            port,
            tags,
            # 健康检查ip端口，检查时间：5,超时时间：30，注销时间：30s
            check=consul.Check().tcp(host, port, "5s", "30s", "30s"))

    def GetService(self, name):
        services = self._consul.agent.services()

        service = services.get(name)
        if not service:
            return None, None
        addr = "{0}:{1}".format(service['Address'], service['Port'])
        return service, addr

    def GetAllServiceIpByCatelog(self, service_name):
        services = self._consul.catalog.service(service=service_name)
        ips = [ i["ServiceAddress"] for i in services[1] ]
        return ips

    def GetAllCatalogs(self):
        svc = self._consul.catalog.services()
        if svc:
            service = svc[1]
        return service


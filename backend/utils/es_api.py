# -*- coding: utf-8 -*-
#ElasticSearch API
from elasticsearch6 import Elasticsearch

class Es(object):
    """
    ElasticSearch相关所有操作
    """

    def __init__(self, host, port):
        """初始化"""
        self.host = host
        self.port = port
        self._es = Elasticsearch([{'host':self.host, 'port':self.port}])

    def GetText(self,index, query):
        res = self._es.search(index, body=query)
        # resp_docs = resp["hits"]["hits"]

        return res



if __name__ == '__main__':
    index = 'system-log-2020.03.04'
    query = {
        "query": {
            "match": {"host.ip": "192.168.160.1"}
        }
    }

    es = Es(host="172.25.1.5", port="30122")
    res = es.GetText(index=index,query=query)
    filebeat_status = 1 if res['hits']['total'] == 0 else 0

    print(res)
    print(filebeat_status)

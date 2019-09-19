# -*- coding: utf-8 -*-
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint
import json
from tools.getconfig import K8sApi
template = """{'apiVersion': '{{api}}',
  'kind': 'Service',
  'metadata':
   { 'labels': {'app': 'bxg-cms' },
     'name': 'bxg-cms',
     'namespace': 'test' },
  'spec':
   { 'ports': [ { 'name': 'http', 'port': '8080' } ],
     'selector': { 'app': 'bxg-cms' },
     'sessionAffinity': 'None',
     'type': 'NodePort' } }"""
class configMap():
    def __init__(self):
        """
        k8s api地址后期需要动态获取
        """
        configuration = kubernetes.client.Configuration()
        configuration.api_key['authorization'] = K8sApi['test']['token']
        configuration.host = K8sApi['test']['address']
        configuration.verify_ssl = False
        configuration.api_key_prefix['authorization'] = 'Bearer'
        self.api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
        self.namespace = 'kube-system'
    def setTemplate(self,name:str,template:str) ->None:
        """
        :param name: 模板名字
        :param template:  模板内容
        :return:
        """
        body = { 'apiVersion': 'v1',
                  'data': { 'template': template },
                  'kind': 'ConfigMap',
                  'metadata':
                   {
                     'name': name, } }
        try:
            api_response = self.api_instance.create_namespaced_config_map(self.namespace, body,)
            return True
        except ApiException as e:
            print(e)
            print("存储configmap异常")
            return False
    def getTemplate(self, name:str) ->json:
        """
        :param name: 模板名字
        :return:模板
        """
        try:
            field_selector = "metadata.name=={}".format(name)
            api_response = self.api_instance.list_namespaced_config_map(self.namespace, pretty='true',field_selector=field_selector)
            #长度等于0表示没有这个模板
            if len(api_response.items) ==0:
                return None
            return api_response.items[0].data['template']
        except ApiException as e:
            print("获取configmap异常")
            return None
    def deleteTemplate(self,name):
        try:
            api_response = self.api_instance.delete_namespaced_config_map(name, self.namespace)
            return True
        except ApiException as e:
            print(e)
            return False
    def getTemplateList(self):
        try:
            configMapList = []
            field_selector = "data=={}".format('template')
            api_response = self.api_instance.list_namespaced_config_map(self.namespace, pretty='true',)
            for i in api_response.items:
                for k in i.data.keys():
                    if k == 'template':
                        configMapList.append(i.metadata.name)
            return configMapList
        except ApiException as e:
            print("获取configmap异常")
            return {}
configMap = configMap()




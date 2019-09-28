# -*- coding: utf-8 -*-
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint
import json
from tools.getconfig import kubeconfig
from tools.log import logecho
class configMap():
    def __init__(self):
        """
        k8s api地址后期需要动态获取
        """
        self.configuration = kubeconfig()
        self.api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
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
            logecho.info(e)
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
            logecho.info(e)
            return None
    def deleteTemplate(self,name):
        try:
            api_response = self.api_instance.delete_namespaced_config_map(name, self.namespace)
            return True
        except ApiException as e:
            logecho.info(e)
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
            logecho.info(e)
            return {}
configMap = configMap()




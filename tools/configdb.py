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
            return []
class Rule():
    def __init__(self):
        self.configuration = kubeconfig()
        self.api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
        self.namespace = 'kube-system'
        # comfigmap的名字
        self.ruleName = 'rule'
        self.body = {'apiVersion': 'v1',
                     'data': {},
                     'kind': 'ConfigMap',
                     'metadata':
                         {
                             'name': self.ruleName, }}

    def set(self, rule, ruletype):
        field_selector = "metadata.name=={}".format('rule')
        api_response = self.api_instance.list_namespaced_config_map(self.namespace, pretty='true',
                                                                    field_selector=field_selector)
        # 如果等于0那么需要先创建这个configmap在添加规则
        if len(api_response.items) == 0:
            try:
                api_response = self.api_instance.create_namespaced_config_map(self.namespace, self.body, )
                self.set(rule, ruletype)
            except:
                pass
        else:
            ##更新rule
            oldrule = api_response.items[0].data
            if oldrule != None:
                newrule = json.loads(oldrule["rule"])
                if ruletype not in json.loads(oldrule["rule"]).keys():
                    newrule[ruletype] = []
                newrule[ruletype].append(rule)
            else:
                newrule = {
                    ruletype: [rule],
                }
            body = self.body
            body["data"] = {'rule': json.dumps(newrule)}
            api_response = self.api_instance.patch_namespaced_config_map(self.ruleName, self.namespace, body)

    def delete(self):
        pass

    def get(self):
        try:
            field_selector = "metadata.name=={}".format(self.ruleName)
            api_response = self.api_instance.list_namespaced_config_map(self.namespace, pretty='true',
                                                                        field_selector=field_selector)
            # 长度等于0表示没有这个模板
            if len(api_response.items) == 0:
                return None
            return json.loads(api_response.items[0].data['rule'])
        except ApiException as e:
            logecho.info(e)
            return None

    def getList(self):
        pass


class intoTemplate():
    def __init__(self):
        self.configuration = kubeconfig()
        self.api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
        self.namespace = 'kube-system'
        # comfigmap的名字
        self.ruleName = 'intotemplate'
        self.body = {'apiVersion': 'v1',
                     'data': {},
                     'kind': 'ConfigMap',
                     'metadata':
                         {'name': self.ruleName, }}

    def set(self, name, body):
        field_selector = "metadata.name=={}".format(self.ruleName)
        api_response = self.api_instance.list_namespaced_config_map(self.namespace, pretty='true',
                                                                    field_selector=field_selector)
        # 如果等于0那么需要先创建这个configmap在添加规则
        if len(api_response.items) == 0:
            try:
                api_response = self.api_instance.create_namespaced_config_map(self.namespace, self.body, )
                self.set(name)
            except:
                pass
        else:
            oldrule = api_response.items[0].data
            print(oldrule)
            if oldrule != None:
                newrule = json.loads(oldrule[self.ruleName])
                newrule[name] = body
            else:
                newrule = {
                    name: body,
                }
            body = self.body
            body["data"] = {self.ruleName: json.dumps(newrule)}
            api_response = self.api_instance.patch_namespaced_config_map(self.ruleName, self.namespace, body)

    def delete(self):
        pass

    def get(self):
        try:
            field_selector = "metadata.name=={}".format(self.ruleName)
            api_response = self.api_instance.list_namespaced_config_map(self.namespace, pretty='true',
                                                                        field_selector=field_selector)
            # 长度等于0表示没有这个模板
            if len(api_response.items) == 0:
                return None
            return json.loads(api_response.items[0].data[self.ruleName])
        except ApiException as e:
            logecho.info(e)
            return None

    def getList(self):
        pass


configMap = configMap()
Rule = Rule()
# Rule.set({"name":"caojiaoyue","template":"caojiaoyue"},"containers")
intoTemplate = intoTemplate()
intoTemplate.set("caojiaoyue", {'name': 'tomcat', 'image': 'tomcat', 'imagePullPolicy': 'Always'})

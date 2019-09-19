# -*- coding: utf-8 -*-
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
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

class ConfigMap():
    def __init__(self):
        """
        k8s api地址后期需要动态获取
        """
        self.K8sApi={
            "test":{"address":"https://172.16.1.51:6443",
                    "token":"eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi10b2tlbi04NXd4YiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJhZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjA0YjlhYzFkLWJmMTEtMTFlOS1iZjIyLWFjMWY2YmQ2ZDk4ZSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTphZG1pbiJ9.mX8tBopids-RjgxM30ZGnTY6zTVes8eAxgI_51lTh7lgLfzLQIeHPuaBNKb9DJhsPIloVA3JlcTFEGYcYuU_sUJg9jGLgIeviXN4g4oNNXuNnFDIc0FtRvf7xe4zwNAUxCEwfSHRVAADbWWcUutBQLWVk2HIGQ1-Sj3UxdgqfnCgxFd3mfi8ULanyNe2dE9DqlL7Saz-ujR3jZ5v2TTw17E7AnaoPcDhJMUaWj29Xu5j7EtDlhWJNqWCeEvYhDtB82DTZ_jwixxF7wggEgfuWb6punx8dKErltBmQXwqZmilzSPWB1Q5MNVwDQ0sIppda7kJ2CCyW7XQrA_HNeVTfg"
                    },
        }
        configuration = kubernetes.client.Configuration()
        configuration.api_key['authorization'] = self.K8sApi['test']['token']
        configuration.host = self.K8sApi['test']['address']
        configuration.verify_ssl = False
        configuration.api_key_prefix['authorization'] = 'Bearer'
        self.api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
        self.namespace = 'kube-system'
    def set(self,name:str,template:str) ->None:
        """
        :param name: 模板名字
        :param template:  模板内容
        :return:
        """
        body = { 'apiVersion': 'v1',
                  'data': { 'test': template },
                  'kind': 'ConfigMap',
                  'metadata':
                   {
                     'name': name, } }
        try:
            api_response = self.api_instance.create_namespaced_config_map(self.namespace, body,)
        except ApiException as e:
            print("存储configmap异常")

    def get(self, name:str) ->str:
        """
        :param name: 模板名字
        :return:模板
        """
        pass

s = ConfigMap()
s.set('caojiaoyue',template)
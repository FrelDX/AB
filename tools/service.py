# -*- coding: utf-8 -*-
import kubernetes.client
from kubernetes.client.rest import ApiException
from tools.getconfig import kubeconfig
from  tools.log import logecho
import json
s = """
{'apiVersion': 'v1',
  'kind': 'Service',
  'metadata':
   { 'labels': {'app': 'bxg-cms' },
     'name': 'bxg-cms1',
     'namespace': 'test' },
  'spec':
   { 'ports': [ { 'name': 'http', 'port': 8080 } ],
     'selector': { 'app': 'bxg-cms' },
     'sessionAffinity': 'None',
     'type': 'NodePort' } }
"""
configuration = kubeconfig()
class svc():
    @staticmethod
    def create(body:json):
        """
        :return:
        """
        namespace=body['metadata']['namespace']
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
        try:
            api_response = api_instance.create_namespaced_service(namespace,body)
            return True
        except ApiException as e:
            logecho.info("Exception when calling CoreV1Api->create_namespaced_service: %s\n" % e)
            return False
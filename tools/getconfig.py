# encoding=utf8
import kubernetes.client
from kubernetes.client.rest import ApiException
import urllib3
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getAddress():
    host = os.environ["KUBERNETES_SERVICE_HOST"]
    return "https://" + host
def getToken():
    token = open('/run/secrets/kubernetes.io/serviceaccount/token','r')
    return token.read()
def kubeconfig():
    configuration = kubernetes.client.Configuration()
    configuration.api_key['authorization'] = getToken()
    configuration.host = getAddress()
    configuration.verify_ssl = False
    configuration.api_key_prefix['authorization'] = 'Bearer'
    return configuration

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


Token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhYi10b2tlbi1qeGM2dCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJhYiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjVmZmNhY2RlLWUxMWQtMTFlOS1hNDUzLWFjMWY2YmQ2ZDk4ZSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTphYiJ9.JA0UMq-OjFiGebVuqbLq31XgTRjIx0pm-WeP8i09n6ix_8B_dhXIYIhIULxga4_oB-Mo2-LHmccII6oENJY3FAC8vBYEuqOo366IgwW3lurs9ae2FT1ZncIG1vNbqdXrDQxc7KO1UtTnvs0bLhxkhheuAOLs-f9eSYSPK5CqxqJcPMzDo6QwfbG5RF7xGtKWUBxNZqZBUqm86R4y-_1O0mmI6wqqSWqpYb2arFPRFakf4OO1hsTwISyQTvHoQwPWN06lfuvljZfbCS9uJJEYECVlpm0Wn-_phMusRAX4926oF2ukGqkRBWbiSwge5q1F0PYVYS0KDj3YVBby0gwpWg"
def kubeconfig():
    configuration = kubernetes.client.Configuration()
    configuration.api_key['authorization'] = Token
    configuration.host = 'https://172.16.1.51:6443'
    configuration.verify_ssl = False
    configuration.api_key_prefix['authorization'] = 'Bearer'
    return configuration

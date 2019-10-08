# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, request
from tools.configdb import configMap
from tools.log import logecho
import json
import base64

dbMap = configMap


class MutatingWebhookConfiguration(Resource):
    def __init__(self):
        super(MutatingWebhookConfiguration, self).__init__()

    def post(self):
        j_data = request.get_json()
        process = pipline(j_data)
        path = process.toInto()
        if path != None:
            body = {
                "apiVersion": "admission.k8s.io/v1beta1",
                "kind": "AdmissionReview",
                "response": {
                    # 回调uid
                    "uid": j_data['request']['uid'],
                    "allowed": True,
                    "patchType": "JSONPatch",
                    "patch": path
                }}
            return body


class pipline():
    def __init__(self, body: json):
        self.body = body
        # 命名空间
        self.namespace = self.body["request"]["namespace"]
        self.template = None
        # deploy名字
        self.name = self.body["request"]["object"]["metadata"]["name"]
        self.intoPath = {
            "containers": {"op": "replace", "path": "/spec/template/spec/containers", "value": None},
            "volumes": {"op": "replace", "path": "/spec/template/spec/volumes", "value": None},
        }
        self.sourceBody = self.body["request"]["object"]["spec"]["template"]["spec"]["containers"]

    def getInto(self, templateName: str) -> dict:
        """
        :return:  获取注入的body
        """
        template = {
            "nginx": {'name': 'nginx', 'image': 'nginx', 'imagePullPolicy': 'Always'},
            "tomcat": {'name': 'tomcat', 'image': 'tomcat', 'imagePullPolicy': 'Always'}
        }
        if templateName in template.keys():
            return template[templateName]
        return None

    def filtration(self) -> dict:
        """
        :return:  根据注入条件匹配注入的body。
        """
        intoBody = []
        Body = {}
        rule = {
            "containers": [{"name": "caojiaoyue", "template": "nginx"}, {"name": "caojiaoyue1", "template": "tomcat"}],
            "volumes": [{"name": "caojiaoyue", "template": "tomcat"}],
        }
        logecho.info(self.namespace)
        logecho.info(self.name)
        ###先判断容器注入
        for i in rule["containers"]:
            #
            if i.get("name") == self.name or i.get("namespace") == self.namespace:
                template = self.getInto(i.get("template"))
                if template == None:
                    continue
                intoBody.append(template)
                Body["containers"] = intoBody
                break
        return Body
    def toInto(self):
        """
        :return: 注入
        """
        # 需要注入的containers
        into = []
        try:
            needInto = self.filtration()
            if needInto == None:
                return None
        except Exception as e:
            logecho.info(e)
            return None
        for i in self.sourceBody:
            into.append(i)
        for i in needInto.keys():
            if i == "containers":
                for i in needInto:
                    into.append(i)
                containersPath = self.intoPath["containers"]
                containersPath["value"] = into
                jsonpath = [].append(containersPath)
        logecho.info(into)
        logecho.info(jsonpath)
        jsonpath = json.dumps(jsonpath)
        logecho.info(jsonpath)
        body = base64.b64encode(jsonpath.encode('utf8'))
        body = str(body, encoding='utf8')
        return body

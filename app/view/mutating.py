# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, request
from tools.configdb import configMap, Rule, intoTemplate
from tools.log import logecho
import base64
import json
class MutatingWebhookConfiguration(Resource):
    def __init__(self):
        super(MutatingWebhookConfiguration, self).__init__()

    def post(self):
        j_data = request.get_json()
        process = Pipline(j_data)
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


class IntoRule(Resource):
    def __init__(self):
        super(IntoRule, self).__init__()

    def post(self):
        data = request.get_json()
        logecho.info(data)


class IntoTemplate():
    def __init__(self):
        super(IntoRule, self).__init__()

    def post(self):
        pass
class Pipline():
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
        template = intoTemplate.get()
        logecho.info("注入的模板")
        logecho.info(template)
        if templateName in template.keys():
            return template[templateName]

        return None

    def filtration(self) -> dict:
        """
        :return:  根据注入条件匹配注入的body。
        """
        intoBody = []
        Body = {}
        rule = Rule.get()
        logecho.info("注入规则")
        logecho.info(rule)
        logecho.info(self.namespace)
        logecho.info(self.name)
        ###先判断容器注入
        for i in rule["containers"]:
            #
            if i.get("name") == self.name or i.get("namespace") == self.namespace:
                logecho.info("要注入的模板名字")
                template = self.getInto(i.get("template"))
                logecho.info(template)
                if template == None:
                    continue
                intoBody.append(template)
                Body["containers"] = intoBody
                break
        logecho.info(Body)
        return Body
    def toInto(self):
        """
        :return: 注入
        """
        # 需要注入的containers
        into = []
        jsonpath = []
        try:
            needInto = self.filtration()
            if len(needInto) == 0:
                return None
        except Exception as e:
            logecho.info(e)
            return None
        # 用户自己定义的资源
        for i in self.sourceBody:
            into.append(i)
        if "containers" in needInto.keys():
            for containers in needInto["containers"]:
                into.append(containers)
            containersPath = self.intoPath["containers"]
            containersPath["value"] = into
            logecho.info(containersPath)
            jsonpath.append(containersPath)
        logecho.info(jsonpath)
        jsonpath = json.dumps(jsonpath)
        logecho.info(jsonpath)
        body = base64.b64encode(jsonpath.encode('utf8'))
        body = str(body, encoding='utf8')
        return body

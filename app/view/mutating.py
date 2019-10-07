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
        body = {
            "apiVersion": "admission.k8s.io/v1beta1",
            "kind": "AdmissionReview",
            "response": {
                "uid": j_data['request']['uid'],
                "allowed": True,
                "patchType": "JSONPatch",
                "patch": process.toInto()
            }}
        return body


class pipline():
    def __init__(self, body: json):
        self.body = body
        logecho.info(self.body)

    @classmethod
    def getInto(self) -> list:
        """
        :return:  获取注入的body
        """
        return [{'name': 'nginx', 'image': 'nginx', 'imagePullPolicy': 'Always'}]

    @classmethod
    def filtration(self):
        """
        :return:  根据注入条件匹配注入的body，返回注入的jsonpath。和需要注入的模板名字。
        """
        rule = [

            {"name": "caojiaoyue", "template": "caojiaoyue"},
            {"namespace": "test", "template": "caojiaoyue"},

        ]
        namespace = self.body["request"]["namespace"]
        name = self.body["request"]["object"]["metadata"]["name"]
        logecho.info(name)
        logecho.info(namespace)
    def toInto(self):
        """
        :return: 注入
        """
        try:
            namespace = self.body["request"]["namespace"]
            name = self.body["request"]["object"]["metadata"]["name"]
            logecho.info(name)
            logecho.info(namespace)
        except:
            logecho.info("报错了")
        # 用户自定义的containers
        sourceBody = self.body["request"]["object"]["spec"]["template"]["spec"]["containers"]
        logecho.info(sourceBody)
        # 需要注入的containers
        intoBody = self.getInto()
        logecho.info(intoBody)
        # 最终注入体
        for i in intoBody:
            sourceBody.append(i)
        jsonpath = [
            {"op": "replace", "path": "/spec/template/spec/containers", "value": sourceBody}
        ]
        jsonpath = json.dumps(jsonpath)
        logecho.info(jsonpath)
        body = base64.b64encode(jsonpath.encode('utf8'))
        body = str(body, encoding='utf8')
        return body

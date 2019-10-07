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
    def __init__(self,body:json):
        self.body = body
    def getInto(self):
        """
        :return:  获取注入的body
        """
        return {'name': 'nginx', 'image': 'nginx:1.12.2', 'imagePullPolicy': 'Always'}
    def filtration(self):
        """
        :return:  根据注入条件匹配注入的body
        """
    def toInto(self):
        """
        :return: 注入
        """
        ###用户自定义的containers
        sourceBody = self.body["request"]["object"]["spec"]["template"]["spec"]["containers"]
        ###需要注入的containers
        intoBody = self.getInto()
        #最终注入体
        newInto = sourceBody.append(intoBody)
        jsonpath = [
            {"op": "replace", "path": "/spec/template/spec/containers", "value": newInto}
        ]
        jsonpath = json.dumps(jsonpath)
        body = base64.b64encode(jsonpath.encode('utf8'))
        body = str(body, encoding='utf8')
        return body












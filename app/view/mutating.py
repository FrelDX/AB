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
        logecho.info(j_data)
        for i in j_data.keys():
            logecho.info(i)
        logecho.info(j_data["request"]["uid"])
        logecho.info(j_data["request"]["object"])

        into = j_data["request"]["object"]["spec"]["template"]["spec"]["containers"]
        logecho.info("-----------------into-------------")
        logecho.info(into)
        logecho.info("-----------------into-------------")
        intobody = {'name': 'nginx', 'image': 'nginx', 'imagePullPolicy': 'Always'}
        into .append(intobody)
        logecho.info("-----------------into add -------------")
        logecho.info(into)
        logecho.info("-----------------into add -------------")
        jsonpath = [
            {"op": "replace", "path": "/spec/template/spec/containers", "value": into}
        ]
        pathc2 = json.dumps(jsonpath)
        srt = base64.b64encode(pathc2.encode('utf8'))
        srt = str(srt, encoding='utf8')
        logecho.info(srt)
        s = {
        "apiVersion": "admission.k8s.io/v1beta1",
        "kind": "AdmissionReview",
        "response": {
        "uid": j_data['request']['uid'],
        "allowed": True,
        "patchType": "JSONPatch",
        "patch": srt
         }}
        return s



# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, request
from tools.configdb import configMap
from tools.log import logecho
import json

dbMap = configMap


class MutatingWebhookConfiguration(Resource):
    def __init__(self):
        super(MutatingWebhookConfiguration, self).__init__()
    def post(self):
        data = request.data
        j_data = json.loads(data)
        for i in j_data.keys():
            logecho.info(i)
        logecho.info(j_data["request"]["uid"])
        logecho.info(j_data["request"]["object"])


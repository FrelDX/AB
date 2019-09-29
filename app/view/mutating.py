# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, request
from tools.configdb import configMap
dbMap  =configMap
class MutatingWebhookConfiguration(Resource):
    def __init__(self):
            super(MutatingWebhookConfiguration, self).__init__()
    def post(self):
        print('+_____________________________')
        print(request.data)
        print('+_____________________________')
        print( request.form)
        print('+_____________________________')
        print('+_____________________________')
        print('+_____________________________')

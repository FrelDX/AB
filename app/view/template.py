# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, request
from tools.configdb import configMap
class templateCreate(Resource):
    def __init__(self):
            super(templateCreate, self).__init__()
    def post(self):
        dbMap  =configMap
        if request.form.get("name")==None or request.form.get("name") ==None:
            return {'code':'1','msg':'参数缺失'}
        dbMap.setTemplate(request.form['name'],request.form['body'])
        return {'code':'1','msg':'None'}








class templateDelete(Resource):
    def __init__(self):
            super(templateDelete, self).__init__()
    def post(self):
        return 1234

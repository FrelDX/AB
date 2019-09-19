# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, request
import jinja2
from tools.configdb import configMap
dbMap  =configMap
class templateApi(Resource):
    def __init__(self):
            super(templateApi, self).__init__()
    def post(self,name, operaton):
        action = ['create','delete','update']
        if operaton not in action:
            return {'code':'1','msg':'不支持的操作{}'.format(operaton)}
        data = request.form
        body = dbMap.getTemplate(name)
        if body is None:
            return {'code':'1','msg':'模板没有找到'}
        try:
            _t = jinja2.Template(body)
            _text = _t.render(data)
            _text.encode('utf-8')
        except:
            return {'code': '1', 'msg': '后台异常'}
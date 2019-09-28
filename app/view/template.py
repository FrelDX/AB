# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, request
from tools.configdb import configMap
dbMap  =configMap
class templateCreate(Resource):
    def __init__(self):
            super(templateCreate, self).__init__()
    def post(self):
        if request.form.get("name")==None or request.form.get("body") ==None:
            return {'code':'1','msg':'参数缺失'}
        if dbMap.setTemplate(request.form['name'],request.form['body']):
            return {'code':'0','msg':'None'}
        return {'code': '1', 'msg': '创建异常'}
class templateDelete(Resource):
    def __init__(self):
            super(templateDelete, self).__init__()
    def delete(self):
        if request.form.get("name") == None:
            return {'code': '1', 'msg': '参数缺失'}
        if dbMap.deleteTemplate(request.form['name']):
             return {'code':'0','msg':'None'}
        return {'code': '1', 'msg': '删除异常'}
class templateGet(Resource):
    def __init__(self):
            super(templateGet, self).__init__()
    def get(self):
        """获取模板列表.
            ---
            definitions:
              Palette:
                type: object
                properties:
                  palette_name:
                    type: array
                    items:
                      $ref: '#/definitions/Color'
              Color:
                type: string
            responses:
              200:
                description: A list of colors (may be filtered by palette)
                schema:
                  $ref: '#/definitions/Palette'
                examples:
                  rgb: ['red', 'green', 'blue']
            """
        dbMap  =configMap
        templateList = dbMap.getTemplateList()
        return {'code':'0','templateList':templateList}
    def post(self):
        dbMap = configMap
        if request.form.get("name")==None:
            return {'code':'1','msg':'参数缺失'}
        templateList = dbMap.getTemplate(request.form.get("name"))
        if templateList is None:
            return {'code': '1', 'msg': "没有找到模板"}
        return {'code': '0', 'templateList': templateList}


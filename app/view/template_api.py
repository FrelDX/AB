# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, request
import jinja2
s = """
{'apiVersion': '{{api}}',
  'kind': '{{kind}}',
  'metadata':
   { 'labels': {'app': 'bxg-cms' },
     'name': 'bxg-cms',
     'namespace': 'test' },
  'spec':
   { 'ports': [ { 'name': 'http', 'port': '8080' } ],
     'selector': { 'app': 'bxg-cms' },
     'sessionAffinity': 'None',
     'type': 'NodePort' } }
"""
a = """
{'apiVersion': '{{api}}',
  'kind': '{{kind}}',
  'metadata':
   { 'labels': {'app': '{{app}}' },
     'name': 'bxg-cms',
     'namespace': '{{namespace}}' },
  'spec':
   { 'ports': [ { 'name': 'http', 'port': '8080' } ],
     'selector': { 'app': 'bxg-cms' },
     'sessionAffinity': 'None',
     'type': 'NodePort' } }
"""
templateList = {
    'svc':s,
    'a':a
}
class templateApi(Resource):
    def __init__(self):
            super(templateApi, self).__init__()
    def post(self,name, operation):
        data = request.form
        if name in templateList.keys():
            _t = jinja2.Template(templateList[name])
            _text = _t.render(data)
            _text.encode('utf-8')
            print(_text)
        else:
            return '模板没有找到'
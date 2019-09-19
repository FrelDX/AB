# -*- coding: utf-8 -*-
import os, jinja2
s = """
{'apiVersion': '{{name}}',
  'kind': 'Service',
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
_t = jinja2.Template(s)
_text = _t.render(name='曹交月')
_text.encode('utf-8')
print(_text)
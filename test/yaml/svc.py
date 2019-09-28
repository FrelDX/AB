# -*- coding: utf-8 -*-
import jsonpatch
doc = { 'apiVersion': 'apps/v1',
  'kind': 'Deployment',
  'metadata': { 'name': 'centos', 'labels': { 'app': 'centos' },'namespace':'test' },
  'spec':
   { 'replicas': 1,
     'template':
      { 'metadata': { 'name': 'centos', 'labels': { 'app': 'centos' } },
        'spec':
         { 'nodeSelector': { 'gogs': 'true' },
           'containers':
            [ { 'name': 'centos',
                'image': 'centos',
                'command': [ '/bin/bash' ],
                'ports': [ { 'containerPort': '9200' } ],
                'env':
                 [ { 'name': 'ES_JAVA_OPTS', 'value': '-Xms2048m -Xmx2048m' },
                   { 'name': 'discovery.type', 'value': 'single-node' } ] } ] } },
     'selector': { 'matchLabels': { 'app': 'centos' } } } }

body  = {"containers":
   [{"name": 'ab',
       "image": 'registry.cn-hangzhou.aliyuncs.com/caojiaoyue/ab:test7',
       "imagePullPolicy": 'IfNotPresent',
       "ports": [ { "containerPort": "5000" } ] } ],
  "serviceAccountName": {'ab':234},
  "restartPolicy": 'Always' }
path = '/spec/template/spec'
pathc = [{'op': 'add', 'path': '/spec/template/spec/containers', 'value': body},{'op': 'add', 'path': '/spec/template/spec/containers', 'value': body}]


a = jsonpatch.JsonPatch(pathc)

result = a.apply(doc)
print(result)


s = """

{'apiVersion': 'apps/v1', 'kind': 'Deployment', 'metadata': {'name': 'centos', 'labels': {'app': 'centos'}, 'namespace': 'test'}, 'spec': {'replicas': 1, 'template': {'metadata': {'name': 'centos', 'labels': {'app': 'centos'}}, 'spec': {'containers': [{'name': 'ab', 'image': 'registry.cn-hangzhou.aliyuncs.com/caojiaoyue/ab:test7', 'imagePullPolicy': 'IfNotPresent', 'ports': [{'containerPort': '5000'}]}], 'serviceAccountName': {'ab': 234}, 'restartPolicy': 'Always'}}, 'selector': {'matchLabels': {'app': 'centos'}}}}

"""


print(s.replace("'","\""))
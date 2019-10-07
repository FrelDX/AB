# -*- coding: utf-8 -*-
import jsonpatch

import base64
import json
import struct

path = '/spec/template/spec'
pathc1 = '[{"op": "add", "path": "/spec/replicas", "value": 3}]'
pathc2 = [{"op": "add", "path": "/spec/replicas", "value": 3}]
pathc2 = json.dumps(pathc2)
print(pathc1 == pathc2)
# print(base64.b64encode(pathc1))
# print(base64.b64encode(pathc2))
print(base64.b64encode(pathc1.encode('utf8')))
srt = base64.b64encode(pathc2.encode('utf8'))
srt = str(srt, encoding='utf8')
print(srt)

s = [{'name': 'test', 'image': 'tomcat', 'resources': {}, 'terminationMessagePath': '/dev/termination-log',
      'terminationMessagePolicy': 'File', 'imagePullPolicy': 'Always'},
     {'name': 'nginx', 'image': 'nginx', 'resources': {}, 'terminationMessagePath': '/dev/termination-log',
      'terminationMessagePolicy': 'File', 'imagePullPolicy': 'Always'}]
s = [{'name': 'test', 'image': 'tomcat', 'resources': {}, 'terminationMessagePath': '/dev/termination-log',
      'terminationMessagePolicy': 'File', 'imagePullPolicy': 'Always'},
     {'name': 'nginx', 'image': 'nginx', 'resources': {}, 'terminationMessagePath': '/dev/termination-log',
      'terminationMessagePolicy': 'File', 'imagePullPolicy': 'Always'},
     {'name': 'nginx', 'image': 'nginx', 'resources': {}, 'terminationMessagePath': '/dev/termination-log',
      'terminationMessagePolicy': 'File', 'imagePullPolicy': 'Always'}]

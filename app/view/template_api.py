# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, request
import jinja2,json,re
from tools.configdb import configMap
from tools import resource
from  tools.log import logecho
dbMap  =configMap
class templateApi(Resource):
    def __init__(self):
            super(templateApi, self).__init__()
    def post(self,name, operaton):
        action = ['create']
        if operaton not in action:
            return {'code':'1','msg':'不支持的操作{}'.format(operaton)}
        body = dbMap.getTemplate(name)
        if body is None:
            return {'code':'1','msg':'模板没有找到'}
        op = pipline(body)
        ##解析模板中资源类型
        kind = op.toResourceTest()
        logecho.info(kind)
        if kind:
            #解析模板中的参数
            parameter = op.toParameterTest()
            if len(parameter) > 0:
                data = request.form
                for i in parameter:
                    if i not in data:
                        return {"code":"模板中{}参数缺失".format(i)}
                # # 渲染
                try:
                    _t = jinja2.Template(body)
                    _text = _t.render(data)
                    _text.encode('utf-8')
                    body = _text
                    if op.toExecute(operaton, kind, body,):
                        return {'code': '0', 'msg': '创建成功'}
                    return {'code': '1', 'msg': '后台异常'}
                except Exception as e:
                    logecho.info(e)
                    return {'code': '1', 'msg': '后台异常'}
            else:
                op.toExecute(operaton,kind,body,)
        else:
            logecho.info("模板解析错误")
            return {"code":"1","msg":"模板解析错误"}


class pipline():
    def __init__(self,body):
        self.body = body
    def toResourceTest(self,):
        """
        主要用于自动检测yaml文件内容是否合法，以及对应的资源类型。
        :return:  资源类型
        """
        body = self.body.replace("\'","\"")
        body=body[1:-1]
        print(body)
        try:
            s = json.loads(body)
            return s['kind']
        except Exception as  e:
            logecho.info(e)
            return False
    def toParameterTest(self):
        """
        主要用于检测body中的环境变量个数，用于验证用户传的参数是否和预定的一致。
        :return:
        """
        body = self.body
        s = re.sub('Service', '',body)
        #返回的参数列表
        pa = []
        while True:
            parameter = re.search(r'{{.*}}', body)
            if parameter is not None:
                Str = parameter.group()
                body = re.sub(Str, '', body)
                pa.append(re.sub('[{{|}}]', '', Str))
            else:
                break
        return pa
    def toExecute(self,operaton,kind,body,):
        """
        :operaton: 操作的类型
        :kind：操作的资源对象
        :return: true or false
        """
        print(operaton)
        print(kind)
        body = json.loads(body.replace('\'','"')[1:-1])
        if hasattr(resource, kind):
            hand = getattr(resource, kind)()
            if hasattr(hand, operaton):
                if operaton == "create":
                    if getattr(hand, operaton)(body):
                        logecho.info("{}成功".format(operaton))
                        return True
                    else:
                        logecho.info("{}失败".format(operaton))
                        return False
            logecho.info("{}失败,没有找到对应的资源方法".format(operaton))
            return False
        logecho.info("{}失败,没有找到对应的资源类".format(operaton))
        return False
# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Api
from app.view.template import templateCreate
from app.view.template import templateDelete
from app.view.template import templateGet
from app.view.template_api import templateApi
from flask import Flask, jsonify
from flasgger import Swagger
from app.view.mutating import MutatingWebhookConfiguration
def createApp():
    app = Flask(__name__)
    swagger = Swagger(app)
    return app
App=createApp()
def makeUrl():
    api = Api(App)
    api.add_resource(templateCreate, '/ab/template/create')
    api.add_resource(templateDelete, '/ab/template/delete')
    api.add_resource(templateGet, '/ab/template/get')
    #name:template name operation: create delete patch
    api.add_resource(templateApi, '/ab/template/api/<name>/<operaton>')
    api.add_resource(MutatingWebhookConfiguration, '/ab/webhook')
makeUrl()

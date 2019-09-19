# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Api
from app.view.template import templateCreate
from app.view.template import templateDelete
def createApp():
    app = Flask(__name__)
    return app
App=createApp()
def makeUrl():
    api = Api(App)
    api.add_resource(templateCreate, '/template/create')
    api.add_resource(templateDelete, '/template/delete')

makeUrl()
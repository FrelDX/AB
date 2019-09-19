# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, request



class templateApi(Resource):
    def __init__(self):
            super(templateApi, self).__init__()
    def post(self):
        return 1234

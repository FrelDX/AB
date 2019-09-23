# -*- coding: utf-8 -*-
from tools.service import svc
from tools.deployment import deploy
import time
class resource():
    @staticmethod
    def Service() -> svc:
        return svc
    @staticmethod
    def Deployment() -> deploy:
        return deploy
# middleware.py

from django.conf import settings
from django.utils import timezone

import traceback
import json
import requests

from datetime import datetime

APP_IDE = settings.APP_TRACESCOPIO_IDE
URL = '{server}/reports/novo'.format(server=settings.TRACERSCOPIO_SERVER)
AGORA = timezone.now()

class TelemetryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):        
        self.enviar_telemetria(exception)


    def enviar_telemetria(self, traceback_info):
        print('capturando excecao')
        timestamp = datetime.timestamp(AGORA)        
        dados = {
            'erro': 'Middleware: Erro ao processar view',
            'traceback': traceback_info,
            'timestamp': timestamp,
        }
        headers = {
            'TRACER-APP-IDE': APP_IDE
        }
                
        try:
            requests.post(url=URL, data=dados, headers=headers)
        except Exception as e:
            pass
            #print(f"Erro ao enviar telemetria: {e}")

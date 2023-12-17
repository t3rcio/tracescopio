'''
Decorators para tracerscopio
'''
from django.conf import settings
from django.utils import timezone

from datetime import datetime
import traceback
import requests


APP_IDE = settings.APP_TRACESCOPIO_IDE
URL = '{server}/reports/novo'.format(server=settings.TRACERSCOPIO_SERVER)

def traceme(view):
    '''
    Registra eventos de erro
    '''
    def wrapper(request, *args, **kwargs):
        agora = timezone.now()
        try:
            return view(request, *args, **kwargs)
        except Exception as _error:
            _ts = datetime.timestamp(agora)
            error = 'Erro na view: ' + view.__name__
            trace = str(error) + ':\n' + traceback.format_exc()
            headers = {
                'TRACER-APP-IDE': APP_IDE
            }
            data = {
                'erro': error,
                'traceback': trace,
                'timestamp': _ts
            }
            res = requests.post(
                url=URL,
                data=data,
                headers=headers
            )
    return wrapper

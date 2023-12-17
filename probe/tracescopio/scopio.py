
from django.conf import settings

import requests

URL = '{server}/apps/novo'.format(server=settings.TRACERSCOPIO_SERVER)

class TracescopioApp:

    @staticmethod
    def new(name:str, url:str, **kwargs):
        if '' in [name, url]:
            return 'Indique nome e/ou url da aplicacao'        
        
        data = {
            'nome': name,
            'url': url
        }
        res = requests.post(
            url = URL,
            data = data,
        )
        return res.text
    
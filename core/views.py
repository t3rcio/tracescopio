
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
from core.models import Aplicacao, Report

@login_required
def home(request):
    aplicacoes = Aplicacao.objects.all()
    contexto = {
        'aplicacoes': aplicacoes
    }
    return render(request, 'core/index.html', contexto)

@csrf_exempt
def novo_app(request):
    res = {}
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome', '')
            url = request.POST.get('url', '')
            if '' in [nome, url]:
                return HttpResponseBadRequest('Parametros incompletos')
            
            if not Aplicacao.objects.filter(url=url,nome=nome).exists():
                _app = Aplicacao.objects.create(nome=nome, url=url)
                res = {
                    'ide': _app.ide,
                    'msg': 'Success'
                }
                return JsonResponse(res)
            return HttpResponseBadRequest('Jah existe app com mesmo nome e url')
        
        except Exception as error:            
            return HttpResponseServerError(content=str(error))
    return HttpResponseBadRequest('Parametros incompletos')


@csrf_exempt
def novo_report(request):
    res = {            
            'error': 'ide app error',
            'msg': 'Aplicacao inexistente'
        }
    tracer_app_ide = request.META.get('HTTP_TRACER_APP_IDE', '')    
    if not tracer_app_ide:        
        return HttpResponseBadRequest('header incompleto')
    
    if request.method == 'POST':
        try:
            app = Aplicacao.objects.get(ide=tracer_app_ide)
            _error = request.POST.get('erro', '')
            _traceback =  request.POST.get('traceback', '')
            _ts =  float(request.POST.get('timestamp', ''))
            data_hora = datetime.fromtimestamp(_ts)
            if '' in [_error, _traceback, data_hora]:
                res['error'] = ''
                res['msg'] = ''
                return HttpResponseBadRequest('parametros incompletos')
            
            Report.objects.create(
                aplicacao = app,
                erro = _error,
                traceback = _traceback,
                data_hora = data_hora
            )
            res = {
                'reports': app.reports.all().count()
            }
        except:
            import traceback
            import sys
            traceback.print_exc(file=sys.stdout)
            return HttpResponseBadRequest('app nao encontrada')
    return JsonResponse(res)

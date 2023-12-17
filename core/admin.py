from django.contrib import admin

from core.models import Aplicacao, Report

@admin.register(Aplicacao)
class AplicacaoAdmin(admin.ModelAdmin):
    list_display = [
        'ide',
        'nome',
        'url',
        'apelido',
        'descricao'
    ]

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = [
        'aplicacao',
        'erro',
        'data_hora'
    ]


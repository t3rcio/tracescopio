
from django.db import models
from django.utils import timezone
from uuid import uuid4

class Aplicacao(models.Model):
    nome = models.CharField(max_length=256, default='')
    url = models.CharField(max_length=1024, default='')
    apelido = models.CharField(max_length=512)
    descricao = models.TextField(default='')
    ide = models.UUIDField(default=uuid4)

    def __str__(self):
        return '{nome} ({url})'.format(nome=self.nome, url=self.url)
    
    def __repr__(self) -> str:
        return 'Aplicacao <{ide}>'.format(ide=self.ide)
    
    class Meta:
        verbose_name = 'Aplicação'
        verbose_name_plural = 'Aplicações'        
    

class Report(models.Model):
    aplicacao = models.ForeignKey(Aplicacao, related_name='reports', on_delete=models.CASCADE)
    erro = models.CharField(max_length=512, default='')
    traceback = models.TextField()
    nivel = models.IntegerField(default=0)
    data_hora = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ['-data_hora']


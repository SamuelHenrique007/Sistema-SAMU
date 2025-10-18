

from django.db import models
from django.contrib.auth.models import User

class SenhaUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    senha_plana = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.usuario.username} - senha'
    

class Arquivo(models.Model):
    nome_paciente = models.CharField(max_length=255)
    data_arquivo = models.DateField()
    arquivo = models.FileField(upload_to='arquivos/')

    def __str__(self):
        return f"{self.nome_paciente} - {self.data_arquivo}"
    
    


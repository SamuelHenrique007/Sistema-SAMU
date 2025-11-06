

from django.db import models


class Arquivo(models.Model):
    nome_paciente = models.CharField(max_length=255)
    data_arquivo = models.DateField()
    arquivo = models.FileField(upload_to='arquivos/')

    def __str__(self):
        return f"{self.nome_paciente} - {self.data_arquivo}"
    
    


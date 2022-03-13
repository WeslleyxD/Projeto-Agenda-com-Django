from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import DateField


# Create your models here.


class Contatos(models.Model):
    choices_categoria = [
        ('Amigo', 'Amigo'),
        ('Família', 'Família'),
        ('Trabalho', 'Trabalho'),
        ('Desconhecido', 'Desconhecido'),
    ]

    nome_contato = models.CharField (max_length=50)
    sobrenome_contato = models.CharField (max_length=50)
    data_criacao = models.DateTimeField (auto_now_add=True)
    aniversario = models.DateField ()
    telefone = models.CharField (max_length=20)
    email = models.CharField (max_length=100)
    descricao = models.CharField (max_length=2000, blank=True)
    categoria = models.CharField (max_length=12, choices=choices_categoria, default='AMIGO')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome_contato
        
    class Meta:
        verbose_name_plural = 'Contatos'

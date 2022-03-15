from django.db import models

from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True, error_messages={'unique': "O email cadastrado já existe."})
    created_at = models.DateField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def get_username(self):
        return self.email

class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    documento = models.CharField(max_length=20)
    created_at = models.DateField(auto_now_add=True)
    cep = models.CharField(max_length=9, default=None)

    def __str__(self) -> str:
        return f'{self.usuario.email} - {self.documento}'
    
class Gateway(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=25)
    nome = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
    mac_adress = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f'{self.cliente.usuario.email} - {self.nome}'

class Device(models.Model):
    gateway = models.ForeignKey(Gateway, on_delete=models.CASCADE)
    ip = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
    mac_adress = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=20)
    tipo_device = models.CharField(max_length=30)


    def __str__(self) -> str:
        return f'{self.gateway.cliente.usuario.email} - {self.nome}'
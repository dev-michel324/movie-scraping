from django.db import models

# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Movies(models.Model):
    fonte = models.CharField(max_length=255, null=True)
    categoria = models.ForeignKey(to=Categoria, on_delete=models.CASCADE, null=False)
    nome = models.CharField(max_length=255)
    embed = models.URLField(null=True)
    description = models.TextField(null=True)
    link = models.URLField(unique=False)
    image = models.URLField(unique=False)
    added = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.nome
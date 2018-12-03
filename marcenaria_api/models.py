from django.core.exceptions import ValidationError
from django.db import models
import math


# Create your models here.
class Fornecedor(models.Model):
    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'

    nome = models.CharField(max_length=128)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    cidade = models.CharField(max_length=64)
    uf = models.CharField(max_length=2)

    def __str__(self):
        return self.nome


class Material(models.Model):
    nome = models.CharField(max_length=128)

    def __str__(self):
        return self.nome


class Placa(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name='placas')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='+')
    largura = models.PositiveIntegerField()
    altura = models.PositiveIntegerField()
    preco = models.DecimalField('Preço', max_digits=8, decimal_places=2)

    @property
    def area(self):
        return self.largura * self.altura

    @property
    def preco_total(self):
        return self.preco * self.area

    def __str__(self):
        return str(self.id)


class Recorte(models.Model):
    placa = models.ForeignKey(Placa, on_delete=models.CASCADE, related_name='recortes')

    @property
    def area(self):
        return 0

    @property
    def preco(self):
        return self.area * self.placa.preco

    def clean(self):
        soma_areas_recortes = 0
        for recorte in Recorte.objects.select_related('recorteretangular', 'recortetriangular',
                                                      'recortecircular').all():
            if hasattr(recorte, 'recorteretangular'):
                soma_areas_recortes += recorte.recorteretangular.area
            if hasattr(recorte, 'recortetriangular'):
                soma_areas_recortes += recorte.recortetriangular.area
            if hasattr(recorte, 'recortecircular'):
                soma_areas_recortes += recorte.recortecircular.area
        if self.placa.area - soma_areas_recortes - self.area < 0:
            raise ValidationError('Área da placa insuficiente para o recorte', 'placa-sem-area')

    def __str__(self):
        return str(self.id)


class RecorteRetangular(Recorte):
    largura = models.PositiveIntegerField()
    altura = models.PositiveIntegerField()

    @property
    def area(self):
        return self.largura * self.altura


class RecorteTriangular(Recorte):
    altura = models.PositiveIntegerField()
    base = models.PositiveIntegerField()

    @property
    def area(self):
        return (self.base * self.altura) / 2


class RecorteCircular(Recorte):
    raio = models.FloatField()

    @property
    def area(self):
        return math.pi * math.pow(self.raio, 2)

from django.db import models


class Livro(models.Model):
    nome_aluno = models.CharField(max_length = 200)
    livro = models.CharField(max_length = 200)
    nome_autor = models.CharField(max_length = 200)
    nome_genero = models.CharField(max_length = 200)
    nome_editora = models.CharField(max_length = 200)
    num_paginas = models.CharField(max_length = 200)

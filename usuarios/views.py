from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django, logout as logout_django
from .models import Livro

def login(request):
    if request.method == "GET":
        return render(request, 'usuarios/login.html')
    else:
        username = request.POST.get('email')
        senha = request.POST.get('senha')
        user = authenticate(username = username, password = senha) 

        if user:
            login_django(request, user)
            return render(request, 'usuarios/home.html')
        else:
            return HttpResponse('E-mail ou senha inválidos')
        
def logout(request):
    if request.user.is_authenticated:
        logout_django(request)
        return render(request, 'usuarios/login.html')
    else:
        return HttpResponse("Você não acessou sua conta ainda!")
        
def cadastro(request):
    if request.method == "GET":
        return render(request, 'usuarios/cadastro.html')
    else:
        username = request.POST.get('email')
        email= request.POST.get('email')
        password = request.POST.get('senha')
        first_name = request.POST.get('nome')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse("Usuário ja existente!")
        else:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
            user.save()
            return render(request, 'usuarios/login.html')
        
def home(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/home.html')
    else:
        return HttpResponse("Faça o login para acessar!")

def lancar(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, 'usuarios/lancar.html')
        else:
            return HttpResponse("Faça o login para acessar!")
    else:
        livro = Livro()
        livro.nome_aluno = request.user.first_name
        livro.livro = request.POST.get('livro')
        livro.nome_autor = request.POST.get('nome_autor')
        livro.nome_genero = request.POST.get('nome_genero')
        livro.nome_editora = request.POST.get('nome_editora')
        livro.num_paginas = request.POST.get('num_paginas')

        livro_verificado = Livro.objects.filter(livro=livro.livro).first()

        if livro_verificado:
            return HttpResponse("Disciplina já possui notas cadastradas!")
        else:
            livro.save()
            return render( request, 'usuarios/home.html')


def alterar(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            lista_livros = Livro.objects.all()
            dicionario_livros = {'lista_livros':lista_livros}
            return render(request, 'usuarios/alterar.html', dicionario_livros)
        else:
            return HttpResponse("Faça o login para acessar!")

def visualizar(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            lista_livros = Livro.objects.all()
            dicionario_livros = {'lista_livros':lista_livros}
            return render(request, 'usuarios/visualizar.html', dicionario_livros)
        else:
            return HttpResponse("Faça o login para acessar!")
    else:
        livro = request.POST.get('livro')
        if livro == "Todas as disciplinas":
            lista_livros = Livro.objects.all()
            dicionario_livros = {'lista_livros':lista_livros}
            return render(request, 'usuarios/visualizar.html', dicionario_livros)   
        else:
            lista_livros = Livro.objects.filter(livro = livro)
            discionario_livros_filtrados = {'lista_livros':lista_livros}
            return render(request, 'usuarios/visualizar.html', discionario_livros_filtrados)
        
def excluir_verificacao(request, pk):
    if request.method == "GET":
        if request.user.is_authenticated:
            lista_livros = Livro.objects.get(pk=pk)
            dicionario_livros  = {'lista_livros':lista_livros}
            return render(request, 'usuarios/excluir.html', dicionario_livros)
        else:
            return HttpResponse("Faça o login para acessar!")
        
def excluir(request, pk):
    if request.method == "GET":
        if request.user.is_authenticated:
            livro_selecionado = Livro.objects.get(pk=pk)
            livro_selecionado.delete()
            return HttpResponseRedirect(reverse('alterar'))
        else:
            return HttpResponse("Faça o login para acessar!")
            

def editar_verificacao(request, pk):
    if request.method == "GET":
        if request.user.is_authenticated:
            lista_livros = Livro.objects.get(pk=pk)
            dicionario_livros ={'lista_livros':lista_livros}
            return render(request, 'usuarios/editar.html', dicionario_livros)
    else:
        return HttpResponse("Faça o login para acessar!")
    
def editar(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            nome_aluno = request.user.first_name
            livro = request.POST.get('livro')
            nome_autor = request.POST.get('nome_autor')
            nome_genero = request.POST.get('nome_genero')
            nome_editora = request.POST.get('nome_editora')
            num_paginas = request.POST.get('num_paginas')
            Livro.objects.filter(pk=pk).update(nome_aluno=nome_aluno, livro=livro, nome_autor=nome_autor, nome_genero=nome_genero, nome_editora=nome_editora, num_paginas=num_paginas)

            return HttpResponseRedirect(reverse('alterar'))
        
    else:
        return HttpResponse("Faça o login para acessar!")



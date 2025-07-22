from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django, logout as logout_django
from django.db.models.functions import Lower
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
            return render( request, 'usuarios/login.html')
        
def logout(request):
    if request.user.is_authenticated:
        logout_django(request)
        return render(request, 'usuarios/login.html')
    else:
        return render( request, 'usuarios/login.html')
        
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

        elif username == "" and email=='' and password =='':            
            return render( request, 'usuarios/cadastro.html')

        else:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
            user.save()
            return render(request, 'usuarios/login.html')
        
def home(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/home.html')
    else:
        return render( request, 'usuarios/login.html')

def lancar(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, 'usuarios/lancar.html')
        else:
            return render(request, 'usuarios/login.html')

    elif request.method == "POST":
        livro = Livro()
        livro.nome_usuario = request.user.first_name
        livro.livro = request.POST.get('livro')
        livro.nome_autor = request.POST.get('nome_autor')
        livro.nome_genero = request.POST.get('nome_genero')
        livro.nome_editora = request.POST.get('nome_editora')
        livro.num_paginas = request.POST.get('num_paginas')
        livro.imagem = request.FILES.get('imagem')  # <- já está correto!

        # Verifica se já existe livro com esse nome
        livro_verificado = Livro.objects.filter(livro=livro.livro).first()

        # Validação de campos obrigatórios
        if livro_verificado:
            return HttpResponse("Livro já cadastrado!")
        
        elif not all([livro.livro, livro.nome_autor, livro.nome_genero, livro.nome_editora, livro.num_paginas]):
            return render(request, 'usuarios/lancar.html', {
                'erro': 'Preencha todos os campos obrigatórios!'
            })

        else:
            livro.save()
            return render(request, 'usuarios/home.html')


def alterar(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            lista_livros = Livro.objects.all()
            dicionario_livros = {'lista_livros':lista_livros}
            return render(request, 'usuarios/alterar.html', dicionario_livros)
        else:
            return render( request, 'usuarios/login.html')

from django.db.models.functions import Lower
from .models import Livro

def visualizar(request):
    if request.user.is_authenticated:
        livros = Livro.objects.all()

        # FILTRO
        genero = request.GET.get('genero')
        if genero:
            livros = livros.filter(nome_genero=genero)

        
        ordenar = request.GET.get('ordenar')
        if ordenar == 'titulo':
            livros = livros.order_by(Lower('livro'))
        elif ordenar == 'paginas':
            livros = livros.order_by('num_paginas')

        
        generos_unicos = Livro.objects.values_list('nome_genero', flat=True).distinct()

        contexto = {
            'lista_livros': livros,
            'generos_unicos': generos_unicos,
            'genero_selecionado': genero,
            'ordenar_selecionado': ordenar,
        }
        return render(request, 'usuarios/visualizar.html', contexto)
    else:
        return render(request, 'usuarios/login.html')
    
def excluir_verificacao(request, pk):
    if request.method == "GET":
        if request.user.is_authenticated:
            lista_livros = Livro.objects.get(pk=pk)
            dicionario_livros  = {'lista_livros':lista_livros}
            return render(request, 'usuarios/excluir.html', dicionario_livros)
        else:
            return render( request, 'usuarios/login.html')
        
def excluir(request, pk):
    if request.method == "GET":
        if request.user.is_authenticated:
            livro_selecionado = Livro.objects.get(pk=pk)
            livro_selecionado.delete()
            return HttpResponseRedirect(reverse('alterar'))
        else:
            return render( request, 'usuarios/login.html')
            

def editar_verificacao(request, pk):
    if request.method == "GET":
        if request.user.is_authenticated:
            lista_livros = Livro.objects.get(pk=pk)
            dicionario_livros ={'lista_livros':lista_livros}
            return render(request, 'usuarios/editar.html', dicionario_livros)
    else:
        return render( request, 'usuarios/login.html')
    
def editar(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            nome_usuario = request.user.first_name
            livro = request.POST.get('livro')
            nome_autor = request.POST.get('nome_autor')
            nome_genero = request.POST.get('nome_genero')
            nome_editora = request.POST.get('nome_editora')
            num_paginas = request.POST.get('num_paginas')

            obj = Livro.objects.get(pk=pk)
            obj.nome_usuario = nome_usuario
            obj.livro = livro
            obj.nome_autor = nome_autor
            obj.nome_genero = nome_genero
            obj.nome_editora = nome_editora
            obj.num_paginas = num_paginas

            # Se uma nova imagem for enviada
            if 'imagem' in request.FILES:
                obj.imagem = request.FILES['imagem']

            obj.save()
            return HttpResponseRedirect(reverse('alterar'))

    return render(request, 'usuarios/login.html')


def sobre(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/sobre.html')
    else:
        return render( request, 'usuarios/login.html')
    
def contato(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/contato.html')
    else:
        return render( request, 'usuarios/login.html')
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.contrib.auth.models import User
from .models import Contatos
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request, 'index.html')



def sobre(request):
    return render(request, 'index.html')
    


def cadastrar(request):
    #Pega os dados enviados do formulário
    if request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        senha2 = request.POST.get('senha2')

        #Erro se algum campo estiver vazio
        if not nome or not sobrenome or not email or not usuario or not senha:
            messages.error(request, 'Preencha todos os campos!')
            return render(request, 'cadastrar.html')

        #Erro se a senha possuir menos de seis caracteres
        if len(senha) < 6:
            messages.error(request, 'Senha deve conter pelo menos seis caracteres!')
            return render(request, 'cadastrar.html')

        #Erro se senhas são diferentes
        if senha != senha2:
            messages.warning(request, 'Senha de confirmação inválida! ')
            return render(request, 'cadastrar.html')

        #Erro de validador de e-mail
        try:
            validate_email(email)
        except:
            messages.error(request, 'E-mail inválido!')
            return render(request, 'cadastrar.html')

        #Erro se o usuário ou email já tiver cadastro no bd User.
        if User.objects.filter(username=usuario).exists():
            messages.warning(request, 'Usuário existente. Por favor, insira outro usuário!')
            return render(request, 'cadastrar.html')

        if User.objects.filter(email=email).exists():
            messages.warning(request, 'E-mail existente. Por favor, insira outro e-mail!')
            return render(request, 'cadastrar.html')

        #Se não houver erros, segue para salvar o formulário.
        user = User.objects.create_user(username=usuario, password=senha, email=email, first_name=nome,
        last_name=sobrenome)
        user.save()

        messages.success(request, 'Cadastro realizado com sucesso. Por gentileza, faça o login!')
        return redirect('login')

    return render(request, 'cadastrar.html')



def login_view(request):
    #Pega os dados enviados do formulário para fazer o login
    if request.method == 'POST':    
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')

        #Autentica no bd User padrão do django
        user = authenticate(request, username=usuario, password=senha)

        #Verifica se a autenticação funcionou, senão retorna ao login exibindo a msg de erro
        if user is not None:
            login(request, user)
            return redirect ('contatos')
        else:
            messages.error(request, 'Usuário ou Senha inválido!')
            return render(request, 'login.html')

    return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect ('login')
    


@login_required(login_url='login')
def contatos(request):

    contatos = Contatos.objects.all()

    context = {
        'contatos' : contatos,
    }

    return render(request, 'contatos.html', context)



@login_required(login_url='login')
def cadastrar_contato(request):
    #Pega os dados enviados do formulário
    if request.method == 'POST':
        nome_contato = request.POST.get('nome')
        sobrenome_contato = request.POST.get('sobrenome')
        aniversario = request.POST.get('aniversario')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        descricao = request.POST.get('descricao')
        categoria = request.POST.get('categoria')
        usuario_logado = request.user

        #Erro se tentar salvar sem a data de aniversário
        if aniversario == "":
            messages.error(request, "O aniversário tem um formato de data inválido. Deve ser no formato  DD-MM-YYYY")
            return render(request, 'cadastrar.html')

        #Validação manual do formulário
        if not nome_contato or not telefone:
            messages.error(request, 'Preencha todos os campos!')
            return render(request, 'cadastrar_contato.html')
        
        #Validação manual do formulário
        if len(telefone)<=8:
            messages.error(request, 'Número pequeno!')
            return render(request, 'cadastrar_contato.html')

        messages.success(request, 'Contato criada com sucesso!')

        contato = Contatos.objects.create(nome_contato=nome_contato, sobrenome_contato=sobrenome_contato,
        telefone=telefone, email=email, descricao=descricao, categoria=categoria, aniversario=aniversario,
        usuario=usuario_logado)        
        contato.save()
        
        return redirect('cadastrar_contato')

    return render(request, 'cadastrar_contato.html')
    


@login_required(login_url='login')
def ver_contato(request, contato_id):
    contato = Contatos.objects.get(id=contato_id)

    context =  {
            'contato' : contato,
        }

    return render(request, 'ver_contato.html', context)



@login_required(login_url='login')
def excluir_contato(request, contato_id):
    contato = Contatos.objects.get(id=contato_id)

    context =  {
        'contato' : contato,
    }

    if request.method == 'POST':
        contato.delete()
        return redirect ('contatos')

    return render(request, 'excluir_contato.html', context)



@login_required(login_url='login')
def update_contato(request, contato_id):
    contato = Contatos.objects.get(id=contato_id)

    context =  {
        'contato' : contato,
    }
    if request.method=="POST":
        nome_contato = request.POST.get('nome')
        sobrenome_contato = request.POST.get('sobrenome')
        aniversario = request.POST.get('aniversario')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        descricao = request.POST.get('descricao')
        categoria = request.POST.get('categoria')
        contato = Contatos.objects.filter(id=contato_id).update(nome_contato=nome_contato, sobrenome_contato=sobrenome_contato,
        telefone=telefone, email=email, descricao=descricao, categoria=categoria, aniversario=aniversario,)

        return redirect('contatos')
    
    return render(request, 'update_contato.html', context)



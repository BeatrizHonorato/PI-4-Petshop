from pyexpat.errors import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from Aplicativo.forms import VacinaForm, cadastroTutorForm,VeterinarioCadastroForm, cadastroAnimalForm, AgendamentoForm
#from Aplicativo.forms import TutoresCadastroForm
from .models import VeterinarioCadastroModel, cadastroTutorModel,cadastroAnimalModel , AgendamentoModel, ServicoModel, cadastroVacinaModel
#from validate_docbr import CPF, CNPJ
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from . import views
from django.shortcuts import render, redirect


def index(request):
    return render(request, 'index.html')

def cadastro(request):
    return render(request, 'cadastro.html')

@login_required
def home(request):
    return render(request, 'home.html')

def cadastroServicos(request):
    return render(request, 'cadastroServicos.html')

def cadastrarVacinas(request):
    return render(request, 'cadastrarVacinas.html')

def agendar_cliente(request):
    return render(request, 'agendar_cliente.html')

def visualizar_cartaoVacina(request):
    return render(request, 'visualizar_cartaoVacina.html')

def autenticacao_cliente(request):
    return render(request, 'autenticacao_cliente.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html') 
    else:
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username = username , password = password)
        if user:
            login_django(request, user)
            return render(request, 'home.html', {'username': username})
        else:
            return render(request, 'index.html')
    
    return render(request, 'criar_agendamento.html')  

#CRUD VETERINARIO

def cadastroVet(request):
    if request.method == 'POST':
        form = VeterinarioCadastroForm(request.POST)
        vet = VeterinarioCadastroModel()
        vet.nome = form.data['nome']
        vet.email = form.data['email']
        vet.logradouro = form.data['logradouro']
        vet.bairro = form.data['bairro']
        vet.cep = form.data['cep']
        vet.numero = form.data['numero']
        vet.cidade = form.data['cidade']
        vet.estado = form.data['estado']
        vet.telefone = form.data['telefone']
        vet.crmv = form.data['crmv']
        vet.password = form.data['password']
        vet.save()
        vet = User.objects.create_user(username= form.data['email'], password = form.data ['password'])
        vet.save()
    return render(request, 'cadastroVet.html')

def atualizacaoVet(request):
    # Recupera todos os veterinários cadastrados
    veterinarios = VeterinarioCadastroModel.objects.all()
    return render(request, 'atualizacaoVet.html', {'veterinarios': veterinarios})

def updateVet(request, id):
    veterinario = get_object_or_404(VeterinarioCadastroModel, pk=id)
    
    if request.method == 'POST':
        form = VeterinarioCadastroForm(request.POST, instance=veterinario)
        if form.is_valid():
            form.save()
            return redirect('atualizacaoVet')
    else:
        form = VeterinarioCadastroForm(instance=veterinario)
    
    return render(request, 'updateVet.html', {'form': form, 'veterinario': veterinario})

def deleteVet(request, id):
     # Buscar o veterinário pelo ID
    veterinario = get_object_or_404(VeterinarioCadastroModel, pk=id)
    veterinario.delete()
    return redirect('index.html')

#CRUD TUTOR
def cadastroTutor(request):
    if request.method == 'POST':
        form = cadastroTutorForm(request.POST)
        tutor = cadastroTutorModel()
        tutor.nometutor = form.data['nometutor']
        tutor.email = form.data['email']
        tutor.logradouro = form.data['logradouro']
        tutor.bairro = form.data['bairro']
        tutor.cep = form.data['cep']
        tutor.numero = form.data['numero']
        tutor.cidade = form.data['cidade']
        tutor.estado = form.data['estado']
        tutor.telefone = form.data['telefone']
        tutor.cpf = form.data['cpf']
        tutor.save()
        tutor = User.objects.create_user(username= form.data['email'], password = form.data ['password'])
        tutor.save()
    return render(request, 'cadastroTutor.html')

def atualizacaoTutor(request):
    # Recupera todos os Tutores cadastrados
    tutores = cadastroTutorModel.objects.all()
    return render(request, 'atualizacaoTutor.html', {'tutor': tutores})

def updateTutor(request, id):
    tutor = get_object_or_404(cadastroTutorModel, pk=id)
    
    if request.method == 'POST':
        form = cadastroTutorForm(request.POST, instance=tutor)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = cadastroTutorForm(instance=tutor)
    
    return render(request, 'updateTutor.html', {'form': form, 'tutor': tutor})

def deleteTutor(request, id):
     # Buscar o Tutor pelo ID
    tutor = get_object_or_404(cadastroTutorModel, pk=id)
    tutor.delete()
    return redirect('/')


#CRUD ANIMAL

def cadastroAnimal(request):
    if request.method == 'POST':
        form = cadastroAnimalForm(request.POST)
        animal= cadastroAnimalModel()
        animal.nomepet = form.data['nomepet']
        animal.especie = form.data['especie']
        animal.porte = form.data['porte']
        animal.raca = form.data['raca']
        animal.sexo = form.data['sexo']
        animal.datanascimento = form.data['datanascimento']
        animal.cpftutor = form.data['cpftutor']
        animal.save()
        

    return render(request, 'cadastroAnimal.html')

def atualizacaoAnimal(request):
    animais = cadastroAnimalModel.objects.all()  # Recupera todos os animais do banco de dados
    context = {
        'animais': animais
    }
    return render(request, 'atualizacaoAnimal.html', context)

def updateAnimal(request, id):
    animal = get_object_or_404(cadastroAnimalModel, pk=id)
    
    if request.method == 'POST':
        form = cadastroAnimalForm(request.POST, instance=animal)
        if form.is_valid():
            form.save()
            return redirect('atualizacaoAnimal')
    else:
        form = cadastroAnimalForm(instance=animal)
    
    return render(request, 'updateAnimal.html', {'form': form, 'animal': animal})

def deleteAnimal(request, id):
     # Buscar o animal pelo ID
    animal = get_object_or_404(cadastroAnimalModel, pk=id)
    animal.delete()
    return redirect('index.html')



def dashatualizacao(request):
    return render(request, 'dashatualizacao.html')



from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Field

def criar_agendamento(request):
    # Obter todos os objetos ServicoModel
    servicos = ServicoModel.objects.all()

    if request.method == "POST":
        tutor_id = request.POST['tutor']
        animal_id = request.POST['animal']
        servico_id = request.POST['servico']
        data = request.POST['data']
        horario = request.POST['horario']

        # Verificar se o serviço existe
        servico = ServicoModel.objects.filter(id=servico_id).first()
        if not servico:
            # Definir a mensagem de erro
            error_message = "O serviço selecionado não está disponível. Por favor, selecione outro serviço."
            # Passar a mensagem de erro para o template
            context = {
                'error_message': error_message,
                'tutores': cadastroTutorModel.objects.all(),
                'animais': cadastroAnimalModel.objects.all(),
                'servicos': servicos
            }
            # Renderizar a mesma página com a mensagem de erro
            return render(request, 'criar_agendamento.html', context)

        # Criar uma nova instância de AgendamentoModel com o serviço correto
        agendamento = AgendamentoModel(
            tutor_id=tutor_id,
            animal_id=animal_id,
            servico_id=servico_id,
            data=data,
            horario=horario
        )
        agendamento.save()
        return redirect('criar_agendamento')  # redirecionar para onde for necessário

    tutores = cadastroTutorModel.objects.all()
    animais = cadastroAnimalModel.objects.all()

    context = {
        'tutores': tutores,
        'animais': animais,
        'servicos': servicos
    }
    return render(request, 'criar_agendamento.html', context)


def visualizar_agendamentos(request):
    # Obtenha os agendamentos em aberto para o tutor atual
    tutor_id = request.user.id  # Supondo que o tutor esteja logado
    agendamentos = AgendamentoModel.objects.filter(tutor_id=tutor_id, status='aberto')
    
    context = {
        'agendamentos': agendamentos
    }
    return render(request, 'visualizar_agendamentos.html', context)

# @login_required
def criarservicos(request):
    if request.method == 'POST':
        servicos_selecionados = request.POST.getlist('servicos')
        for nome_servico in servicos_selecionados:
            ServicoModel.objects.create(nome=nome_servico)
        return redirect('success')  # Redireciona para uma página de sucesso após cadastrar
    
    # Busca todos os serviços cadastrados
    servicos_cadastrados = ServicoModel.objects.all()
    
    return render(request, 'criarservicos.html', {'servicos_cadastrados': servicos_cadastrados})

def cadastrarvacina(request):
    if request.method == 'POST':
        form = VacinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redireciona para uma página de sucesso após cadastrar

    # Busca todas as vacinas cadastradas
    vacinas_cadastradas = cadastroVacinaModel.objects.all()

    # Inicializa um novo formulário para ser usado na página
    form = VacinaForm()

    return render(request, 'cadastrarVacina.html', {'form': form, 'vacinas_cadastradas': vacinas_cadastradas})

def cancelarvacina(request, id_vacina):
    vacina = get_object_or_404(cadastroVacinaModel, id=id_vacina)
    if request.method == 'POST':
        vacina.delete()
        return redirect('success')  # Redireciona para uma página de sucesso após deletar

    return render(request, 'cancelarvacina.html', {'vacina': vacina})

def updateVacinas(request, id_vacina):
    vacina = get_object_or_404(cadastroVacinaModel, id=id_vacina)
    if request.method == 'POST':
        form = VacinaForm(request.POST, instance=vacina)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redireciona para uma página de sucesso após atualizar

    else:
        form = VacinaForm(instance=vacina)

    return render(request, 'atualizarvacina.html', {'form': form})

# views.py
def visualizarvacinas(request):
    vacinas = cadastroVacinaModel.objects.all()
    return render(request, 'visualizarvacinas.html', {'vacinas': vacinas})
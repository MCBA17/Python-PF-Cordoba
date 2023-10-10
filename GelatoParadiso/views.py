from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate, logout
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
import random
import string
from django.http import JsonResponse
from datetime import datetime, timedelta

# Cuenta
        
def registro(request):
    if request.user.is_authenticated:
        return redirect('Inicio')
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            asignar_avatar_predeterminado(user)
            login(request, user)
            return redirect('Inicio')
    else:
        form = CustomRegistrationForm()
    return render(request, 'registro.html', {'form': form})


def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Inicio')
    else:
        form = AuthenticationForm()
    return render(request, 'iniciar_sesion.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('Inicio')

@login_required
def editarPerfil(request):

    usuario = request.user

    if request.method == 'POST':

        miFormulario = UserEditForm(request.POST)

        if miFormulario.is_valid():

            informacion = miFormulario.cleaned_data

            usuario.email = informacion['email']
            usuario.last_name = informacion['last_name']
            usuario.first_name = informacion['first_name']


            usuario.save()

            return render(request, "iniciologeado.html")

    else:

        miFormulario = UserEditForm(initial={'email': usuario.email, 'last_name': usuario.last_name, 'first_name': usuario.first_name})

    return render(request, "editar_perfil.html", {"miFormulario": miFormulario, "usuario": usuario})

@login_required
def cambiar_avatar(request):
    
    if request.method == "POST":
        
        formulario = cambiarAvatar(request.POST, request.FILES)
        
        if formulario.is_valid():
            
            u = request.user
            new_avatar = formulario.cleaned_data["imagen"]
            
            if Avatar.objects.filter(user=u).exists():

                old_avatar = Avatar.objects.get(user=u)
                old_avatar.delete()
            
            avatar = Avatar(user=u, imagen=new_avatar)
            avatar.save()
            
            return redirect("Inicio")
    
    else:
        formulario = cambiarAvatar()
    
    return render(request, "cambiaravatar.html", {"formulario": formulario})

        
def asignar_avatar_predeterminado(user):
    try:
        avatar, created = Avatar.objects.get_or_create(user=user)

        if not avatar.imagen:
            avatar.imagen = 'avatar_predeterminado.png'
            avatar.save()
    except Avatar.DoesNotExist:
        print("El usuario no tiene un avatar.")
       
# Vistas de paginas       
        
def inicio(request):
    context = {}
    if request.user.is_authenticated:
        context['user_info'] = request.user
        return render(request, 'iniciologeado.html', context)
    else:
        return render (request, "inicio.html")
    
def inicioredirect(request):
    return redirect ("Inicio")
        
def about(request):
    return render(request, "about.html")

def services(request):
    return render (request, "services.html")

def buscar_helado(request):
    query = request.GET.get('q')

    if query:
        resultados_helados = Helado.objects.filter(Q(nombre__icontains=query) | Q(descripcion_corta__icontains=query))
        resultados_pasteles = Pastel.objects.filter(Q(nombre__icontains=query) | Q(descripcion_corta__icontains=query))
        resultados_batidos = Batido.objects.filter(Q(nombre__icontains=query) | Q(descripcion_corta__icontains=query))
        resultados_infantil = Infantil.objects.filter(Q(nombre__icontains=query) | Q(descripcion_corta__icontains=query))
    else:
        resultados_helados = []
        resultados_pasteles = []
        resultados_batidos = []
        resultados_infantil = []

    return render(request, 'busqueda.html', {'resultados_helados': resultados_helados, 'resultados_pasteles': resultados_pasteles, 'resultados_batidos' : resultados_batidos, 'resultados_infantil' : resultados_infantil})

def resultados_busqueda(request):

    query = request.GET.get('q')

    resultados_helados = []
    resultados_pasteles = []
    resultados_batidos = []
    resultados_infantil = []

    if query:
        resultados_helados = Helado.objects.filter(Q(nombre__icontains=query))
        resultados_pasteles = Pastel.objects.filter(Q(nombre__icontains=query))
        resultados_batidos = Batido.objects.filter(Q(nombre__icontains=query))
        resultados_infantil = Infantil.objects.filter(Q(nombre__icontains=query))

    return render(request, 'resultados_busqueda.html', {'resultados_helados': resultados_helados, 'resultados_pasteles': resultados_pasteles, 'resultados_batidos' : resultados_batidos, 'resultados_infantil' : resultados_infantil})

def detalle_helado(request, helado_id):

    helado = get_object_or_404(Helado, id=helado_id)
    
    return render(request, 'detalle_helado.html', {'helado': helado})

def detalle_batido(request, batido_id):

    batido = get_object_or_404(Batido, id=batido_id)
    
    return render(request, 'detalle_batido.html', {'batido': batido})

def detalle_infantil(request, infantil_id):

    infantil = get_object_or_404(Infantil, id=infantil_id)
    
    return render(request, 'detalle_infantil.html', {'infantil': infantil})

def detalle_pastel(request, pastel_id):

    pastel = get_object_or_404(Pastel, id=pastel_id)
    
    return render(request, 'detalle_pastel.html', {'pastel': pastel})

# CRUD HELADO

@login_required
def crear_helado(request):
    if request.method == 'POST':
        form = HeladoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Lista Helados')
    else:
        form = HeladoForm()
    return render(request, 'crear_helado.html', {'form': form})

def lista_helados(request):
    helados = Helado.objects.all()
    return render(request, 'lista_helados.html', {'helados': helados})

@login_required
def editar_helado(request, helado_id):
    helado = get_object_or_404(Helado, id=helado_id)

    if request.method == 'POST':
        form = HeladoForm(request.POST, request.FILES, instance=helado)
        if form.is_valid():
            form.save()
            return redirect('Lista Helados')
    else:
        form = HeladoForm(instance=helado)

    return render(request, 'editar_helado.html', {'form': form, 'helado': helado})

@login_required
def borrar_helado(request, helado_id):
    helado = get_object_or_404(Helado, id=helado_id)
    
    if request.method == 'POST':
        helado.delete()
        return redirect('Lista Helados')
    
    return render(request, 'borrar_helado.html', {'helado': helado})

# CRUD PASTEL

@login_required
def crear_pastel(request):
    if request.method == 'POST':
        form = PastelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Lista Pasteles')
    else:
        form = PastelForm()

    return render(request, 'crear_pastel.html', {'form': form})

def lista_pasteles(request):
    pasteles = Pastel.objects.all()
    return render(request, 'lista_pasteles.html', {'pasteles': pasteles})

@login_required
def editar_pastel(request, pastel_id):
    pastel = Pastel.objects.get(id=pastel_id)

    if request.method == 'POST':
        form = PastelForm(request.POST, request.FILES, instance=pastel)
        if form.is_valid():
            form.save()
            return redirect('Lista Pasteles')
    else:
        form = PastelForm(instance=pastel)

    return render(request, 'editar_pastel.html', {'form': form, 'pastel': pastel})

@login_required
def borrar_pastel(request, pastel_id):
    pastel = get_object_or_404(Pastel, id=pastel_id)
    
    if request.method == 'POST':
        pastel.delete()
        return redirect('Lista Pasteles')
    
    return render(request, 'borrar_pastel.html', {'pastel': pastel})

# CRUD BATIDO

@login_required
def crear_batido(request):
    if request.method == 'POST':
        form = BatidoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Lista Batidos')
    else:
        form = BatidoForm()

    return render(request, 'crear_batido.html', {'form': form})

def lista_batidos(request):
    batidos = Batido.objects.all()
    return render(request, 'lista_batidos.html', {'batidos': batidos})

@login_required
def editar_batido(request, batido_id):
    batido = Batido.objects.get(id=batido_id)

    if request.method == 'POST':
        form = BatidoForm(request.POST, request.FILES, instance=batido)
        if form.is_valid():
            form.save()
            return redirect('Lista Batidos')
    else:
        form = BatidoForm(instance=batido)

    return render(request, 'editar_batido.html', {'form': form, 'batido': batido})

@login_required
def borrar_batido(request, batido_id):
    batido = get_object_or_404(Batido, id=batido_id)
    
    if request.method == 'POST':
        batido.delete()
        return redirect('Lista Batidos')
    
    return render(request, 'borrar_batido.html', {'batido': batido})

# CRUD INFANTIL

@login_required
def crear_infantil(request):
    if request.method == 'POST':
        form = InfantilForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Lista Infantil')
    else:
        form = InfantilForm()

    return render(request, 'crear_infantil.html', {'form': form})

def lista_infantil(request):
    infantiles = Infantil.objects.all()
    return render(request, 'lista_infantil.html', {'infantiles': infantiles})

ultimo_generado = None

@login_required
def editar_infantil(request, infantil_id):
    infantil = Infantil.objects.get(id=infantil_id)

    if request.method == 'POST':
        form = InfantilForm(request.POST, request.FILES, instance=infantil)
        if form.is_valid():
            form.save()
            return redirect('Lista Infantil')
    else:
        form = InfantilForm(instance=infantil)

    return render(request, 'editar_infantil.html', {'form': form, 'infantil': infantil})

@login_required
def borrar_infantil(request, infantil_id):
    infantil = get_object_or_404(Infantil, id=infantil_id)
    
    if request.method == 'POST':
        infantil.delete()
        return redirect('Lista Infantil')
    
    return render(request, 'borrar_infantil.html', {'infantil': infantil})

# Otros

@login_required
def generar_cupon(request):
    global ultimo_generado


    tiempo_limite = timedelta(minutes=5)
    ahora = datetime.now()

    if ultimo_generado is None or (ahora - ultimo_generado) >= tiempo_limite:

        cupon = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        cupon_formateado = '-'.join([cupon[i:i+4] for i in range(0, len(cupon), 4)])
        

        ultimo_generado = ahora


        data = {'cupon': cupon_formateado}
    else:

        tiempo_restante = tiempo_limite - (ahora - ultimo_generado)
        minutos_restantes = tiempo_restante.total_seconds() // 60
        data = {'cupon': f'Debes esperar {minutos_restantes:.0f} minutos antes de generar otro cupón.'}

    return JsonResponse(data)

@login_required
def comprar(request):
    return render (request, "compra.html")

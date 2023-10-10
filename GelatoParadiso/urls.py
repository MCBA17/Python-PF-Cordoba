"""
URL configuration for Heladeria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.contrib import admin
from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Vista de Paginas
    path("inicio/", inicio, name= "Inicio"),
    path("about/", about, name= "About"),
    path("services/", services, name = "Services"),
    
    # Cuenta
    path("registrarse/", registro, name="Registro"),
    path("login/", iniciar_sesion, name="IniciarSesion"),
    path("logout/", logout_view, name="Logout"),
    path("avatar/", cambiar_avatar, name="Cambiar Avatar"),
    path("editar_perfil/", editarPerfil, name="EditarPerfil"),
    
    # Búsqueda
    path("resultados/", resultados_busqueda, name="Resultados"),
    path("detalle_helado/<int:helado_id>/", detalle_helado, name="Detalle Helado"),
    path("detalle_pastel/<int:pastel_id>/", detalle_pastel, name="Detalle Pastel"),
    path("detalle_batido/<int:batido_id>/", detalle_batido, name="Detalle Batido"),
    path("detalle_infantil/<int:infantil_id>/", detalle_infantil, name="Detalle Infantil"),
    
    # CRUD Helado
    path("crear_helado/", crear_helado, name="Crear Helado"),
    path("lista_helados/", lista_helados, name= "Lista Helados"),
    path("editar_helado/<int:helado_id>/", editar_helado, name="Editar Helado"),
    path("borrar_helado/<int:helado_id>/", borrar_helado, name="Borrar Helado"),
    
    # CRUD Pastel
    path("crear_pastel/", crear_pastel, name="Crear Pastel"),
    path("lista_pasteles/", lista_pasteles, name= "Lista Pasteles"),
    path("editar_pastel/<int:pastel_id>/", editar_pastel, name="Editar Pastel"),
    path("borrar_pastel/<int:pastel_id>/", borrar_pastel, name="Borrar Pastel"),
    
    # CRUD Batido
    path("crear_batido/", crear_batido, name="Crear Batido"),
    path("editar_batido/<int:batido_id>/", editar_batido, name="Editar Batido"),
    path("lista_batidos/", lista_batidos, name= "Lista Batidos"),
    path("borrar_batido/<int:batido_id>/", borrar_batido, name="Borrar Batido"),
    
    # CRUD Infantil
    path("crear_infantil/", crear_infantil, name="Crear Infantil"),
    path("lista_infantil/", lista_infantil, name= "Lista Infantil"),
    path("editar_infantil/<int:infantil_id>/", editar_infantil, name="Editar Infantil"),
    path("borrar_infantil/<int:infantil_id>/", borrar_infantil, name="Borrar Infantil"),
    
    # Otros
    path("934fj9k9sdf9k090k230320f", generar_cupon, name="generar_cupon"),
    path("compra/", comprar, name="Comprar"),   
]

urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
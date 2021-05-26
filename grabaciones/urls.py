from django.urls import path
from . import views

app_name = 'grabaciones'

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('grabaciones/inicio.html', views.grabaciones, name="grabacion"),
    path('registro/', views.registro, name="registro"),
    path('logout/', views.logout_request, name="logout"),
    path('login/', views.login_request, name="login"),
    path('sessiones/editar_session/<str:pk>', views.editar_session, name="editar_session"),
    path('grabaciones/editar_grabacion/<str:pk>', views.editar_grabacion, name="editar_grabacion")
]

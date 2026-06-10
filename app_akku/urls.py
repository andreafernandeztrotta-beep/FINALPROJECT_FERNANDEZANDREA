from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.inicio, name='index'),
    path('buscar/', views.buscar_solucion, name='buscar_solucion'),
    path('contacto/', views.contacto_cliente, name='contacto_cliente'),
    path('about/', views.about, name='about'),

    path('pages/', views.PostList.as_view(), name='pages'),
    path('pages/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('pages/nuevo/', views.PostCreate.as_view(), name='post_create'),
    path('pages/editar/<int:pk>/', views.PostUpdate.as_view(), name='post_update'),
    path('pages/borrar/<int:pk>/', views.PostDelete.as_view(), name='post_delete'),

    path('login/', LoginView.as_view(template_name='app_akku/app_akku/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='app_akku/app_akku/logout.html'), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('cambiar-password/', views.CambiarPassword.as_view(), name='cambiar_password'),

    path('mensajes/', views.MensajeList.as_view(), name='mensajes'),
    path('enviar-mensaje/', views.MensajeCreate.as_view(), name='enviar_mensaje'),

    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
]

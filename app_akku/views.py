from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .models import Post, Mensaje, Perfil
from .forms import ClienteForm, RegistroForm, UserEditForm, PerfilForm

# --- Vistas de Navegación Akkü Studio Lab ---
def inicio(request):
    return render(request, 'app_akku/app_akku/index.html')

def buscar_solucion(request):
    query = request.GET.get('q', '').strip().lower()
    catalogo = [
        {'nombre': 'Cyber Security', 'descripcion': 'Auditorías de vulnerabilidad y blindaje de activos digitales críticos.'},
        {'nombre': 'Agentic AI', 'descripcion': 'Diseño de agentes autónomos y arquitecturas de IA para automatización compleja.'},
        {'nombre': 'Growth Strategy', 'descripcion': 'Optimización de conversión mediante arquitectura de datos y funnels dinámicos.'}
    ]
    resultados = [item for item in catalogo if query in item['nombre'].lower() or query in item['descripcion'].lower()] if query else []
    return render(request, 'app_akku/app_akku/buscar.html', {'resultados': resultados, 'query': query})

def contacto_cliente(request):
    enviado = False
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            enviado = True
            form = ClienteForm()
    else:
        form = ClienteForm()
    return render(request, 'app_akku/app_akku/prospecto_form.html', {'form': form, 'enviado': enviado})

def about(request):
    return render(request, 'app_akku/app_akku/about.html')

# --- Registro de Usuarios ---
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            Perfil.objects.create(user=user, nombre=user.first_name, apellido=user.last_name)
            login(request, user)
            return redirect('index')
    else:
        form = RegistroForm()
    return render(request, 'app_akku/app_akku/registro.html', {'form': form})

# --- Gestión de Posts (Portfolio) ---
class PostList(ListView):
    model = Post
    template_name = 'app_akku/app_akku/pages.html'
    context_object_name = 'posts'

class PostDetail(DetailView):
    model = Post
    template_name = 'app_akku/app_akku/post_detail.html'

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'app_akku/app_akku/post_form.html'
    fields = ['titulo', 'subtitulo', 'cuerpo', 'imagen', 'autor']
    success_url = reverse_lazy('pages')

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'app_akku/app_akku/post_form.html'
    fields = ['titulo', 'subtitulo', 'cuerpo', 'imagen']
    success_url = reverse_lazy('pages')

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'app_akku/app_akku/post_confirm_delete.html'
    success_url = reverse_lazy('pages')

# --- Sistema de Mensajería (Chat Requerido) ---
class MensajeList(LoginRequiredMixin, ListView):
    model = Mensaje
    template_name = 'app_akku/app_akku/mensajes.html'
    context_object_name = 'mensajes'

    def get_queryset(self):
        return Mensaje.objects.filter(receptor=self.request.user)

class MensajeCreate(LoginRequiredMixin, CreateView):
    model = Mensaje
    template_name = 'app_akku/app_akku/enviar_mensaje.html'
    fields = ['receptor', 'contenido']
    success_url = reverse_lazy('mensajes')

    def form_valid(self, form):
        form.instance.emisor = self.request.user
        return super().form_valid(form)

# --- Perfil de Usuario (usa el modelo Perfil) ---
@login_required
def perfil(request):
    perfil_usuario, _ = Perfil.objects.get_or_create(
        user=request.user,
        defaults={'nombre': request.user.first_name, 'apellido': request.user.last_name}
    )
    return render(request, 'app_akku/app_akku/perfil.html', {'perfil': perfil_usuario})

@login_required
def editar_perfil(request):
    perfil_usuario, _ = Perfil.objects.get_or_create(
        user=request.user,
        defaults={'nombre': request.user.first_name, 'apellido': request.user.last_name}
    )
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil_usuario)
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            return redirect('perfil')
    else:
        user_form = UserEditForm(instance=request.user)
        perfil_form = PerfilForm(instance=perfil_usuario)
    return render(request, 'app_akku/app_akku/editar_perfil.html', {
        'user_form': user_form,
        'perfil_form': perfil_form,
    })

# --- Cambio de Password ---
class CambiarPassword(LoginRequiredMixin, PasswordChangeView):
    template_name = 'app_akku/app_akku/cambiar_password.html'
    success_url = reverse_lazy('perfil')

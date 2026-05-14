from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post, Mensaje

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
    return render(request, 'app_akku/app_akku/prospecto_form.html')

def about(request):
    return render(request, 'app_akku/app_akku/about.html')

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
    template_name = 'app_akku/app_akku/mensajes.html' # Corregido a ruta doble
    context_object_name = 'mensajes'

    def get_queryset(self):
        return Mensaje.objects.filter(receptor=self.request.user)

class MensajeCreate(LoginRequiredMixin, CreateView):
    model = Mensaje
    template_name = 'app_akku/app_akku/enviar_mensaje.html' # Corregido a ruta doble
    fields = ['receptor', 'contenido']
    success_url = reverse_lazy('mensajes')

    def form_valid(self, form):
        form.instance.emisor = self.request.user
        return super().form_valid(form)
    
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def perfil(request):
    return render(request, 'app_akku/app_akku/perfil.html')

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        # Formulario estándar de Django para cambiar datos de usuario
        formulario = UserChangeForm(request.POST, instance=request.user)
        if formulario.is_valid():
            formulario.save()
            return redirect('perfil')
    else:
        formulario = UserChangeForm(instance=request.user)
    return render(request, 'app_akku/app_akku/editar_perfil.html', {'form': formulario})


    
    
    












    





    

    





    



    
    

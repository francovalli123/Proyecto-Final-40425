from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from TechZone.models import Product, Profile, Mensaje
from django.urls import reverse_lazy
from TechZone.forms import BuscarProductoForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def about(request):
    return(render(request, "TechZone/about.html"))

def index(request):
    context={
        "products": Product.objects.all()
    }
    return render(request, "TechZone/index.html", context)

class ProductList(ListView):
    model = Product

class ProductDetail(DetailView):
    model = Product

class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    success_url = reverse_lazy("product-list")
    fields = ['producto','precio','titulo', 'estado', 'descripcion', 'imagen', 'item1', 'item2', 'item3']

    def form_valid(self, form):
        form.instance.publisher = self.request.user
        return super().form_valid(form)

class ProductUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    success_url = reverse_lazy("product-list")
    fields = '__all__'

    def test_func(self):
        user_id = self.request.user.id
        product_id = self.kwargs.get('pk')
        return Product.objects.filter(publisher=user_id, id=product_id).exists()
    
    def handle_no_permission(self):
        return render(self.request, "TechZone/not_found.html")

class ProductDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("product-list")

    def test_func(self):
        user_id = self.request.user.id
        product_id = self.kwargs.get('pk')
        return Product.objects.filter(publisher=user_id, id=product_id).exists()

    def handle_no_permission(self):
        return render(self.request, "TechZone/not_found.html")

class BuscarProducto(ListView):
    model = Product
    context_object_name = "productos"

    def get_queryset(self):
        f = BuscarProductoForm(self.request.GET)
        if f.is_valid():
           return Product.objects.filter(producto__icontains=f.data["criterio_nombre"]).all()
        return Product.objects.none()

class SignUp(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')

class Login(LoginView):
    next_page = reverse_lazy("home")

class Logout(LogoutView):
    template_name = 'registration/logout.html'

class ProfileUpdate(UserPassesTestMixin, UpdateView):
    model = Profile
    success_url = reverse_lazy('home')
    fields = ['imagen', 'info']
    
    def test_func(self):
        profile_id = self.kwargs.get('pk')
        return Profile.objects.filter(user=self.request.user, id = profile_id).exists()
    
    def handle_no_permission(self):
        return render(self.request, "TechZone/not_found.html")

class ProfileCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Profile
    success_url = reverse_lazy("home")
    fields = ['imagen', 'info']

    def test_func(self):
        return Product.objects.filter().exists()
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        return render(self.request, "TechZone/not_found.html")

class ProfileDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Profile
    context_object_name = "profile"

    def test_func(self):
        profile_id = self.kwargs.get('pk')
        return Profile.objects.filter(user=self.request.user, id = profile_id).exists()
    
    def handle_no_permission(self):
        return render(self.request, "TechZone/not_found.html")

class MensajeCreate(CreateView):
    model = Mensaje
    fields = '__all__'
    success_url = reverse_lazy('home')

class MensajeList(LoginRequiredMixin, ListView):
    model = Mensaje
    context_object_name = "mensajes"

    def get_queryset(self):
        return Mensaje.objects.filter(destinatario=self.request.user.id).all()
    
class MensajeDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mensaje
    success_url = reverse_lazy("mensaje-list")

    def test_func(self):
        user_id = self.request.user.id
        mensaje_id = self.kwargs.get('pk')
        return Mensaje.objects.filter(destinatario=user_id, id=mensaje_id).exists()

    def handle_no_permission(self):
        return render(self.request, "TechZone/not_found.html")

from timeit import default_timer

from django.contrib.auth.models import Group, Permission, User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from .forms import GroupForm
from .models import Product, Order
from .forms_old import ProductForm, OrderForm

class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Decktop', 2999),
            ('Smertphone', 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
        }
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupListView(View):
    """Создание групп разрешений"""
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)

class ProductDetailsView(DetailView):
    """Подробнее о продуктах"""
    template_name = "shopapp/products-details.html"
    model = Product
    context_object_name = "product"

class ProductListView(ListView):
    """Список продуктов"""

    template_name = "shopapp/products-list.html"
    # model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)

# def products_list(request: HttpRequest):
#     context = {
#         'products': Product.objects.all(),
#     }
#     return render(request, 'shopapp/products-list.html', context=context)

# def create_product(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             # name = form.cleaned_data["name"]
#             # price = form.cleaned_data["price"]
#             # Product.objects.create(**form.cleaned_data)
#             form.save()
#             url = reverse("shopapp:products_list")
#             return redirect(url)
#     else:
#         form = ProductForm()
#     context = {
#         "form": form,
#     }
#     return render(request, 'shopapp/create-product.html', context=context)

class ProductCreateView(PermissionRequiredMixin, CreateView):
    """Создание продуктов"""
    permission_required = "shopapp.add_product"
    # def test_func(self):
        # return self.request.user.groups.filter(name="qwerty") or self.request.user.is_superuser
        # return self.request.user

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    model = Product
    fields = "name", "price", "description", "discount"
    success_url = reverse_lazy("shopapp:products_list")

class ProductUpdateView(UserPassesTestMixin, UpdateView):
    """Изменение описания продуктов"""

    def test_func(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.created_by == self.request.user or self.request.user.is_superuser:
            return self.request.user.is_superuser or \
                self.request.user.has_perm("shopapp.change_product")
                # self.request.user.groups.filter(name="qwerty")
        else:
            raise PermissionDenied("403 Forbidden")


    # def get_object(self, queryset=None):
    #     obj = super().get_object(queryset=queryset)
    #     if obj.created_by == self.request.user or self.request.user.is_superuser:
    #         return obj
    #     else:
    #         raise PermissionDenied("403 Forbidden")

    model = Product
    fields = "name", "price", "description", "discount"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk":self.object.pk},
        )

class ProductDeleteView(DeleteView):
    """Удаление продуктов"""
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


""" 
Order section 
"""

class OrderListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects.select_related("user").prefetch_related("products")
    )

class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects.select_related("user").prefetch_related("products")
    )

class OrderCreateView(CreateView):
    model = Order
    fields = "user", "products", "delivery_address", "pomocode"
    success_url = reverse_lazy("shopapp:orders_list")

# def create_order(request: HttpRequest) -> HttpResponse:
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             url = reverse("shopapp:orders_list")
#             return redirect(url)
#     else:
#         form = OrderForm()
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'shopapp/create-order.html', context=context)


class OrderUpdateView(UpdateView):
    model = Order
    fields = "user", "products", "delivery_address", "pomocode"
    # template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk":self.object.pk},
        )

class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")

class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by("pk").all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived
            }
            for product in products
        ]
        return JsonResponse({"products": products_data})

"""
В этом модуле лежат различные наборы представлений.

Разные view интернет-магазина: по товарам, заказам и т.д.
"""

import logging
from timeit import default_timer

import json
from django.contrib.auth.models import Group, Permission, User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .forms import ProductForm
from .forms_old_1 import GroupForm
from .models import Product, Order, ProductImage
from .serializers import ProductSerializer, OrderSerializer
# from .forms_old import ProductForm, OrderForm

log = logging.getLogger(__name__)

@extend_schema(description="Product Views CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    Полный CRUD для сущностей товара
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]

    @extend_schema(
        summary="Get one product by ID",
        description="Retrieves **product**, returns 404 if not found",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description="Empty response, product by id not found"),
        },
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

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
            "items": 1,
        }
        log.debug("Product for shop index: %s", products)
        log.info("Rendering shop index")
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
    # model = Product
    queryset = Product.objects.prefetch_related("images")
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
    fields = "name", "price", "description", "discount", "preview"
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
    # fields = "name", "price", "description", "discount", "preview"
    template_name_suffix = "_update_form"
    form_class = ProductForm

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk":self.object.pk},
        )
    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response

class ProductDeleteView(DeleteView):
    """Удаление продуктов"""
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)

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

""" 
Order section 
"""

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["delivery_address"]
    filterset_fields = [
        "id",
        "delivery_address",
        "user_id",
        "created_at",
    ]
    ordering_fields = [
        "id",
        "delivery_address",
        "user_id",
    ]

class OrderListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )

class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
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

class OrdersExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by("pk").all()
        orders_data = [
            {
                "id": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.pomocode,
                "user_id": order.user_id,
                "products": [product.pk for product in order.products.all()]
            }
            for order in orders
        ]
        return JsonResponse({"orders": orders_data})
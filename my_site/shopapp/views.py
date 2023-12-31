"""
В этом модуле лежат различные наборы представлений.

Разные view интернет-магазина: по товарам, заказам и т.д.
"""

import logging
from timeit import default_timer
from csv import DictWriter

import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission, User
from django.contrib.syndication.views import Feed
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .common import save_csv_products
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

    @method_decorator(cache_page(60*2))
    def list(self, *args, **kwargs):
        # print("hello products list")
        return super().list(*args, **kwargs)

    @action(methods=['get'], detail=False)
    def download_csv(self, requests: Request):

        response = HttpResponse(content_type="text/csv")
        filename = "products-export.csv"
        response["Content-Disposition"] = f"attachment; filename={filename}"
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "name",
            "description",
            "price",
            "discount",
            "created_by_id",
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })
        return response

    @action(
        detail=False,
        methods=["post"],
        parser_classes=[MultiPartParser]
    )
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES["file"].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

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
    # @method_decorator(cache_page(60*2))
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
        print("shop index context", context)
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
        cache_key = "products_data_export"
        products_data = cache.get(cache_key)
        if products_data is None:
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
            cache.set(cache_key, products_data, 300)
        # elem = products_data[0]
        # name = elem["name"]
        # print('name:', name)
        return JsonResponse({"products": products_data})

class LatestProductsFeed(Feed):
    title = "Products (new)"
    description = "Update on changes and additions products list"
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return (
            Product.objects
            .filter(created_at__isnull=False)
            .order_by("-created_at")[:5]
        )

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:100]

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

""" User Orders """

class UserOrdersListView(ListView):
    template_name = "shopapp/user_orders.html"

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        if not self.request.user.id:
            raise Http404("Просмотр недоступен")
        self.owner = User.objects.get(pk=user_id)
        return Order.objects.filter(user_id=user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context

class UserOrderExport(View):

    def get(self, request: HttpRequest, user_id) -> JsonResponse:
        cache_key = f"user_orders_data_export {user_id}"
        user_data = cache.get(cache_key)

        user_orders = Order.objects.filter(user_id=user_id).order_by("pk").all()
        if not user_orders:
            raise Http404("Пользователь с заказами не найден!")

        if user_data is None:
            user_orders_data = [
                {
                    'order_id': order.id,
                    'delivery_address': order.delivery_address,
                    'products': [product.name for product in order.products.all()],
                }
                for order in user_orders
            ]
            cache.set = (cache_key, user_data, 300)

        return JsonResponse({"user_id": user_id, 'orders': user_orders_data})

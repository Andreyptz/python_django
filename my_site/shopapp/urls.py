from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    ShopIndexView,
    GroupListView,
    ProductDetailsView,
    ProductListView,
    ProductsDataExportView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    OrdersExportView,
    ProductViewSet,
    OrderViewSet,
    LatestProductsFeed,
    UserOrdersListView,
)
from django.views.decorators.cache import cache_page

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    # path('', cache_page(60*3)(ShopIndexView.as_view()), name="index"),
    path('', ShopIndexView.as_view(), name="index"),
    path('api/', include(routers.urls)),
    path('groups/', GroupListView.as_view(), name='groups_list'),
    path('products/export/', ProductsDataExportView.as_view(), name='products-export'),
    path('products/', ProductListView.as_view(), name='products_list'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
    path('products/create/', ProductCreateView.as_view(), name="product_create"),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name="product_update"),
    path('products/<int:pk>/archive/', ProductDeleteView.as_view(), name="product_delete"),
    path('products/latest/feed/', LatestProductsFeed(), name="product-feed"),
    path('orders/', OrderListView.as_view(), name="orders_list"),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name="order_details"),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/update/', OrderUpdateView.as_view(), name="order_update"),
    path('order/<int:pk>/archive/', OrderDeleteView.as_view(), name="order_delete"),
    path('order/export/', OrdersExportView.as_view(), name='orders-export'),
    path('users/<int:user_id>/orders/', UserOrdersListView.as_view(), name='users_order'),
]
from django.urls import path

from .views import ShopIndexView, \
    GroupListView, \
    ProductDetailsView, \
    ProductListView, \
    ProductsDataExportView, \
    ProductCreateView, \
    ProductUpdateView, \
    ProductDeleteView,\
    OrderListView, \
    OrderDetailView, \
    OrderCreateView, \
    OrderUpdateView, \
    OrderDeleteView, \
    OrdersDataExportView

app_name = "shopapp"

urlpatterns = [
    path('', ShopIndexView.as_view(), name="index"),
    path('groups/', GroupListView.as_view(), name='groups_list'),
    path('products/export/', ProductsDataExportView.as_view(), name='products-export'),
    path('products/', ProductListView.as_view(), name='products_list'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
    path('products/create/', ProductCreateView.as_view(), name="product_create"),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name="product_update"),
    path('products/<int:pk>/archive/', ProductDeleteView.as_view(), name="product_delete"),
    path('orders/', OrderListView.as_view(), name="orders_list"),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name="order_details"),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/update/', OrderUpdateView.as_view(), name="order_update"),
    path('order/<int:pk>/archive/', OrderDeleteView.as_view(), name="order_delete"),
    path('order/export/', OrdersDataExportView.as_view(), name='orders-export'),
]
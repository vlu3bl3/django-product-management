from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("products/", views.products, name="products"),
    path("products/<int:product_id>/", views.product_detail, name="product_detail"),
    path("test-404/", views.test_404, name="test_404"),
    path("products/create",views.product_create,name="product_create"),
    path("products/<int:product_id>/edit",views.product_update,name="product_update"),
    path("products/<int:product_id>/delete",views.product_delete,name="product_delete"),
    path("categories/<int:category_id>/",views.category_products,name="category_products"),
    path("register/",views.register_view,name="register"),
    path(
    "login/",
    auth_views.LoginView.as_view(
        template_name="products/login.html",
        next_page="products"
    ),
    name="login",
),path(
    "logout/",
    auth_views.LogoutView.as_view(next_page="products"),
    name="logout",
),
    path("products/<int:product_id>/buy",views.product_buy,name="product_buy"),
    path("my-orders",views.my_orders,name="my_orders"),
    path("manage-orders",views.manage_orders,name="manage_orders"),
    path("manage-orders/<int:order_id>",views.update_order_status,name="update_order_status")
]
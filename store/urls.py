from django.urls import path
from . import views

urlpatterns = [
    path("", views.store_list, name="store_list"),
    path(
        "store/<int:store_id>/",
        views.product_list,
        name="product_list",
    ),
    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart",
    ),
    path("cart/", views.view_cart, name="view_cart"),
    path(
        "cart/remove/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("checkout/", views.checkout, name="checkout"),
    path(
        "review/<int:product_id>/",
        views.leave_review,
        name="leave_review",
    ),
    path(
        "vendor/dashboard/",
        views.vendor_dashboard,
        name="vendor_dashboard",
    ),
    path(
        "vendor/store/create/",
        views.create_store,
        name="create_store",
    ),
    path(
        "vendor/store/<int:store_id>/edit/",
        views.edit_store,
        name="edit_store",
    ),
    path(
        "vendor/store/<int:store_id>/delete/",
        views.delete_store,
        name="delete_store",
    ),
    path(
        "vendor/store/<int:store_id>/product/add/",
        views.add_product,
        name="add_product",
    ),
    path(
        "vendor/product/<int:product_id>/edit/",
        views.edit_product,
        name="edit_product",
    ),
    path(
        "vendor/product/<int:product_id>/delete/",
        views.delete_product,
        name="delete_product",
    ),
    path(
        "vendor/store/<int:store_id>/",
        views.vendor_store_detail,
        name="vendor_store_detail",
    ),
    path(
        "product/<int:product_id>/",
        views.product_detail,
        name="product_detail",
    ),
]

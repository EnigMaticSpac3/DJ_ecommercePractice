from django.urls import path
# viewpages
from .views import (
    CheckoutView, HomeView,
    ItemDetailView, add_to_cart, remove_from_cart
)
app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path('product/<slug>', ItemDetailView.as_view(), name="product"),
    path('add-to-cart/<slug>', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>', remove_from_cart, name="remove-from-cart"),
]





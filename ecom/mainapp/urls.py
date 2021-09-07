from django.urls import path, base
from django.contrib.auth import views as authViews

from .views import *

urlpatterns = [
    path('', base, name='base'),
    path('products/<str:ct_model>/<str:slug>/', ProductPageView.as_view(), name='product_page'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('sign_out/', authViews.LogoutView.as_view(next_page='base'), name='sign_out'),
]
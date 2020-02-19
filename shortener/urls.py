from django.urls import path
from . import views


app_name = "shortener"

urlpatterns = [
    path('', views.shorten_url, name="shorten_url"),
    path('show/<slug:shortcut_value>/', views.show_shortcut, name="show_shortcut"),
    path('<slug:shortcut>', views.redirect_to_url, name="redirect_to_url"),
]
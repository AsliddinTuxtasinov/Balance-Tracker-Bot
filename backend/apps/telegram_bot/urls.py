from django.urls import path

from apps.telegram_bot import views

urlpatterns = [
    path("/", views.HomeView.as_view(), name="index"),
]

from django.urls import path
from api import views

app_name = "api"
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("login", views.Login.as_view(), name="login"),
    path("refresh-token", views.RefreshToken.as_view(), name="refresh_token"),
    path("search", views.SearchEntry.as_view(), name="search"),
    path("create-entry", views.CreateEntry.as_view(), name="create_entry"),
    path("delete-entry/<int:pk>", views.DeleteEntry.as_view(), name="delete_entry"),
]

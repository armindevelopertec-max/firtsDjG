from django.urls import path
from .views import suma

urlpatterns = [
    path('suma/', suma)
]
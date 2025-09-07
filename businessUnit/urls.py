from django.urls import path,include
from . import views

from .views import (
    BusinessUnit_view
)

urlpatterns = [
    path('api/',include([
        path('BusinessUnit_view/', BusinessUnit_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('BusinessUnit_view/<int:pk>/', BusinessUnit_view.as_view({
            'put': 'update',
            'delete': 'destroy',
        })),
    ])),
]
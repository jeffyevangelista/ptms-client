from django.urls import path,include
from . import views

from .views import (
    Fund_view
)

urlpatterns = [
    path('',include([
        path('', Fund_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('<int:pk>/', Fund_view.as_view({
            'put': 'update',
            'delete': 'destroy',
        })),
    ])),
]
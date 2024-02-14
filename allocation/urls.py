from django.urls import path,include
from . import views

from .views import (
    Allocation_view
)

urlpatterns = [
    path('',include([
        path('', Allocation_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('<int:pk>/', Allocation_view.as_view({
            'put': 'update',
            'delete': 'destroy',
        })),
    ])),
]
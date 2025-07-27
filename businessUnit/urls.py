from django.urls import path,include
from . import views

from .views import (
    BusinessUnit_view
)

urlpatterns = [
    path('',include([
        path('', BusinessUnit_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('<int:pk>/', BusinessUnit_view.as_view({
            'put': 'update',
            'delete': 'destroy',
        })),
    ])),
]
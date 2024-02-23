from django.urls import path,include
from . import views

from .views import (
    Allocation_view,create_fund_allocation
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

    path('api/create_fund_allocation/', create_fund_allocation, name='create_fund_allocation'),
]
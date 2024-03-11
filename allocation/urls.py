from django.urls import path,include
from . import views

from .views import (
    Allocation_view,create_fund_allocation,AllocationListView,Allocation_List_Per_BU_View,edit_fund_allocation
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
    path('api/edit_fund_allocation/<int:fund_allocation_id>/', edit_fund_allocation, name='edit_fund_allocation'),
    path('api/AllocationListView/', AllocationListView.as_view(), name='AllocationListView'),
    path('api/Allocation_List_Per_BU_View/', Allocation_List_Per_BU_View.as_view(), name='Allocation_List_Per_BU_View'),
]
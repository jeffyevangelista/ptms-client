from django.urls import path,include
from . import views

from .views import (
    Allocation_view,AllocationListView,Allocation_List_Per_BU_View,AllocationLog_view,Allocation_Log_Per_BU_View
)

urlpatterns = [
    path('api/',include([
        path('Allocation_view/', Allocation_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('Allocation_view/<int:pk>/', Allocation_view.as_view({
            'put': 'update',
            'delete': 'destroy',
        })),

          path('AllocationLog/', AllocationLog_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('AllocationLog/<int:pk>/', AllocationLog_view.as_view({
            'put': 'update',
            'delete': 'destroy',
        })),
    ])),
    
    path('api/AllocationListView/', AllocationListView.as_view(), name='AllocationListView'),
    path('api/Allocation_List_Per_BU_View/', Allocation_List_Per_BU_View.as_view(), name='Allocation_List_Per_BU_View'),
    path('api/Allocation_Log_Per_BU_View/', Allocation_Log_Per_BU_View.as_view(), name='Allocation_Log_Per_BU_View'),
]
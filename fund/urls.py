from django.urls import path,include

from .views import (
    Fund_view,FundListView
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

    path('api/FundListView/', FundListView.as_view(), name='FundListView'),
]
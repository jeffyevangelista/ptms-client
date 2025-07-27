from django.urls import path,include

from .views import (
    Fund_view,FundListView,BusinessUnitInFund_view,Fund_Comapny_View,FundLog_view
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

        path('BusinessToFund/', BusinessUnitInFund_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('BusinessToFund/<int:pk>/', BusinessUnitInFund_view.as_view({
            'put': 'update',
            'delete': 'destroy',
        })),

        path('FundLog_view/', FundLog_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('FundLog_view/<int:pk>/', FundLog_view.as_view({
            'put': 'update',
            'delete': 'destroy',
        })),
    ])),

    path('api/FundListView/', FundListView.as_view(), name='FundListView'),
    path('api/Fund_Comapny_View/', Fund_Comapny_View.as_view(), name='Fund_Comapny_View'),
]
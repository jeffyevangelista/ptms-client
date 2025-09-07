from django.urls import path,include

from .views import *
urlpatterns = [
    path('api/',include([
        path('Fund_view/', Fund_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('Fund_view/<int:pk>/', Fund_view.as_view({
            'put': 'update',
            'delete': 'destroy',
        })),

        path('FundCluster_view/', BusinessUnitInFund_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('FundCluster_view/<int:pk>/', BusinessUnitInFund_view.as_view({
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

    path('api/Fund_per_user/', FundListView.as_view(), name='Fund_per_user'),
    path('api/Fund_per_company/', Fund_Company_View.as_view(), name='Fund_per_company'),
]
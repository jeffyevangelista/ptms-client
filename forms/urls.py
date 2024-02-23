from django.urls import path,include
from . import views
from .views import LatestVoucherView
from .views import (
    RequestForm_view
)

urlpatterns = [
    path('',include([
        path('', RequestForm_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('<int:pk>/', RequestForm_view.as_view({
            'put': 'update',
            'delete': 'destroy',
        })),
    ])),
  path('api/latest_voucher/', LatestVoucherView.as_view(), name='latest_voucher'),
 
]
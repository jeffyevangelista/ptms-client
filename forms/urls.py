from django.urls import path,include
from . import views
from .views import LatestVoucherView
from .views import (
    RequestForm_view,FormListAPIView
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
  path('api/create_request_form/', views.create_request_form, name='create_request_form'),
  path('api/form_filtered_list/', FormListAPIView.as_view(), name='FormListAPIView'),
 
]
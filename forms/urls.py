from django.urls import path,include
from . import views
from .views import LatestVoucherView
from .views import (
    RequestForm_view , PurchaseRequestListView,PurchaseRequest_Reviewer_List_View,PurchaseRequest_GeneralManager_List_View, Cost_Controller_Release_View,Cost_Controller_To_Be_Release_View
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
  path('api/PurchaseRequestListView/', PurchaseRequestListView.as_view(), name='PurchaseRequestListView'),
  path('api/PurchaseRequest_Reviewer_List_View/', PurchaseRequest_Reviewer_List_View.as_view(), name='PurchaseRequest_Reviewer_List_View'),
  path('api/PurchaseRequest_GeneralManager_List_View/', PurchaseRequest_GeneralManager_List_View.as_view(), name='PurchaseRequest_GeneralManager_List_View'),
  path('api/Cost_Controller_Release_View/', Cost_Controller_Release_View.as_view(), name='Cost_Controller_Release_View'),
  path('api/Cost_Controller_To_Be_Release_View/', Cost_Controller_To_Be_Release_View.as_view(), name='Cost_Controller_To_Be_Release_View'),
 
]
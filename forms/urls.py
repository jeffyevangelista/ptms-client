from django.urls import path,include
from . import views
from .views import LatestVoucherView,create_request_form
from .views import (
    RequestForm_view , PurchaseRequestListView,PurchaseRequest_Reviewer_List_View,PurchaseRequest_GeneralManager_List_View,Item_view,
     Cost_Controller_Release_View,Cost_Controller_To_Be_Release_View,Refund_view,Excess_view, Cost_Controller_Liquidated_View,PurchaseRequest_Decline_List_View,
     PurchaseRequest_Approved_List_View,Fund_Custodian_Replenish_View,PurchaseRequestApprovedListView,
     edit_request_form,refund_function,excess_function,replenish_function,decline_return_fund_function,Fund_Custodian_Release_Amount,admin_released,
     admin_liquidated, admin_replenish
    
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

        path('Refund/', Refund_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('Refund/<int:pk>/', Refund_view.as_view({
            'put': 'update',
            'delete': 'destroy',
        })),

         path('Excess/', Excess_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('Excess/<int:pk>/', Excess_view.as_view({
            'put': 'update',
            'delete': 'destroy',
        })),

         path('Item/', Item_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('Item/<int:pk>/', Item_view.as_view({
            'put': 'update',
            'delete': 'destroy',
        })),
    ])),
#Encoder
  path('api/create_request_form/', create_request_form, name='create_request_form'),
  path('api/edit_request_form/<int:pk>/', edit_request_form, name='edit_request_form'),
  path('api/latest_voucher/', LatestVoucherView.as_view(), name='latest_voucher'),
  path('api/PurchaseRequestListView/', PurchaseRequestListView.as_view(), name='PurchaseRequestListView'),
  path('api/PurchaseRequestApprovedListView/', PurchaseRequestApprovedListView.as_view(), name='PurchaseRequestApprovedListView'),
#Cost Controller
  path('api/PurchaseRequest_Reviewer_List_View/', PurchaseRequest_Reviewer_List_View.as_view(), name='PurchaseRequest_Reviewer_List_View'),
#General Manager
  path('api/PurchaseRequest_GeneralManager_List_View/', PurchaseRequest_GeneralManager_List_View.as_view(), name='PurchaseRequest_GeneralManager_List_View'),
#Fund Custodian Fund_Custodian_Release_Amount
  path('api/Fund_Custodian_Release_Amount/<int:pk>/', Fund_Custodian_Release_Amount, name='Fund_Custodian_Release_Amount'),
  path('api/Cost_Controller_Release_View/', Cost_Controller_Release_View.as_view(), name='Cost_Controller_Release_View'),
  path('api/Cost_Controller_To_Be_Release_View/', Cost_Controller_To_Be_Release_View.as_view(), name='Cost_Controller_To_Be_Release_View'),
  path('api/Cost_Controller_Liquidated_View/', Cost_Controller_Liquidated_View.as_view(), name='Cost_Controller_Liquidated_View'),
  path('api/Fund_Custodian_Replenish_View/',  Fund_Custodian_Replenish_View.as_view(), name='Fund_Custodian_Replenish_View'),

  path('api/refund_function/', refund_function , name='refund_function'),
  path('api/excess_function/', excess_function , name='excess_function'),
  path('api/replenish_function/<int:pk>/', replenish_function , name='replenish_function'),
  
  #Encoder Decline List
  path('api/PurchaseRequest_Decline_List_View/',  PurchaseRequest_Decline_List_View.as_view(), name='PurchaseRequest_Decline_List_View'),
  #Encoder Approved List
  path('api/PurchaseRequest_Approved_List_View/',  PurchaseRequest_Approved_List_View.as_view(), name='PurchaseRequest_Approved_List_View'),
  
  
  #Cost Controller/General Manager 
  path('api/decline_return_fund_function/<int:pk>/',  decline_return_fund_function, name='decline_return_fund_function'),

  #admin
  path('api/admin_released/',  admin_released, name='admin_released'),
  path('api/admin_liquidated/',  admin_liquidated, name='admin_liquidated'),
  path('api/admin_replenish/',  admin_replenish, name='admin_replenish'),
 
]
from django.urls import path,include
from .views import LatestVoucherView,create_request_form
from .views import *

urlpatterns = [
    path('api/',include([
        path('RequestForm_view/', RequestForm_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('RequestForm_view/<int:pk>/', RequestForm_view.as_view({
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
  path('api/Cost_Controller_Replenish_View/', Cost_Controller_Replenish_View.as_view(), name='Cost_Controller_Replenish_View'),
  path('api/Fund_Custodian_Pie_Chart/',  Fund_Custodian_Pie_Chart.as_view(), name='Fund_Custodian_Pie_Chart'),
  path('api/Fund_Manager_Reports_View/',  Fund_Manager_Reports_View.as_view(), name='Fund_Manager_Reports_View'), 
  path('api/Fund_Manager_Daily_Reports_View/',  Fund_Manager_Daily_Reports_View.as_view(), name='Fund_Manager_Daily_Reports_View'), 
 #return liquidated amount to allocated amount
  path('api/replenish_function/<int:pk>/', replenish_function , name='replenish_function'),
  #excess or refund
  path('api/excess_or_refund_function/<int:pk>/', excess_or_refund_function , name='excess_or_refund_function'),
  
  #Encoder Decline List
  path('api/PurchaseRequest_Decline_List_View/',  PurchaseRequest_Decline_List_View.as_view(), name='PurchaseRequest_Decline_List_View'),
  #Encoder Approved List
  path('api/PurchaseRequest_Approved_List_View/',  PurchaseRequest_Approved_List_View.as_view(), name='PurchaseRequest_Approved_List_View'),
  #Encoder Released List
  path('api/PurchaseRequestReleasedListView/',  PurchaseRequestReleasedListView.as_view(), name='PurchaseRequestReleasedListView'),
  #Encoder Liquidated List
  path('api/Encoder_Liquidated_List_View/',  Encoder_Liquidated_List_View.as_view(), name='Encoder_Liquidated_List_View'),
  
  
  #Cost Controller/General Manager 
  path('api/decline_return_fund_function/<int:pk>/',  decline_return_fund_function, name='decline_return_fund_function'),

  #admin
  path('api/admin_released/',  admin_released, name='admin_released'),
  path('api/admin_liquidated/',  admin_liquidated, name='admin_liquidated'),
 
]

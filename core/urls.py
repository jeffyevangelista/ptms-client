"""
URL configuration for pettycash project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings  
from django.conf.urls.static import static 
from django.urls import path,include
from user.views import LoginAPIView,current_user,custodian_users, check_business_unit_based_on_email, logout_view
from forms.views import (
    LatestVoucherView,
    PurchaseRequestListView,
    PurchaseRequest_Reviewer_List_View,
    PurchaseRequest_GeneralManager_List_View,
    Cost_Controller_Release_View,
    Cost_Controller_To_Be_Release_View,
    Cost_Controller_Liquidated_View,
    edit_request_form,
    create_request_form,
    replenish_function,
    decline_return_fund_function,
    PurchaseRequest_Decline_List_View,
    PurchaseRequest_Approved_List_View,
    Fund_Custodian_Release_Amount,
    admin_released,
    admin_liquidated,
    PurchaseRequestApprovedListView,
    Fund_Custodian_Pie_Chart,
    Encoder_Liquidated_List_View,
    excess_or_refund_function,
    PurchaseRequestReleasedListView,
    Fund_Manager_Reports_View,
    Fund_Manager_Daily_Reports_View,
    Cost_Controller_Replenish_View
)
from fund.views import FundListView,Fund_Comapny_View
from allocation.views import create_fund_allocation, AllocationListView,Allocation_List_Per_BU_View, edit_fund_allocation,Allocation_Log_Per_BU_View
urlpatterns = [
    path('admin/', admin.site.urls),
     path('api/', include([
        path('user_list/', include('user.urls')),
        path('fund_list/', include('fund.urls')),
        path('businessUnit_list/', include('businessUnit.urls')),
        path('allocation_list/', include('allocation.urls')),
        path('forms_list/', include('forms.urls')),
    ])),

#User
        path('api/login/', LoginAPIView.as_view(), name='login'),
        path('api/current_user/', current_user, name='current_user'),
        path('api/custodian_users/',custodian_users, name='custodian_users'),
        path('api/check_business_unit_based_on_email/', check_business_unit_based_on_email, name='check_business_unit_based_on_email'),
        path('logout/', logout_view, name='logout'),

#Purchase Request
        #Encoder
        path('api/create_request_form/', create_request_form, name='create_request_form'),
        path('api/edit_request_form/<int:pk>/', edit_request_form, name='edit_request_form'),
        path('api/latest_voucher/', LatestVoucherView.as_view(), name='latest_voucher'),
        path('api/PurchaseRequestListView/', PurchaseRequestListView.as_view(), name='PurchaseRequestListView'),
        path('api/PurchaseRequestApprovedListView/', PurchaseRequestApprovedListView.as_view(), name='PurchaseRequestApprovedListView'),
        path('api/PurchaseRequestReleasedListView/',  PurchaseRequestReleasedListView.as_view(), name='PurchaseRequestReleasedListView'),

        #Cost Controller
        path('api/PurchaseRequest_Reviewer_List_View/', PurchaseRequest_Reviewer_List_View.as_view(), name='PurchaseRequest_Reviewer_List_View'),

        #General Manager
        path('api/PurchaseRequest_GeneralManager_List_View/', PurchaseRequest_GeneralManager_List_View.as_view(), name='PurchaseRequest_GeneralManager_List_View'),
       
        #Fund Custodian
        path('api/Fund_Custodian_Release_Amount/<int:pk>/', Fund_Custodian_Release_Amount, name='Fund_Custodian_Release_Amount'),
        path('api/Cost_Controller_Release_View/', Cost_Controller_Release_View.as_view(), name='Cost_Controller_Release_View'),
        path('api/Cost_Controller_To_Be_Release_View/', Cost_Controller_To_Be_Release_View.as_view(), name='Cost_Controller_To_Be_Release_View'),
        path('api/Cost_Controller_Liquidated_View/', Cost_Controller_Liquidated_View.as_view(), name='Cost_Controller_Liquidated_View'),
        path('api/Cost_Controller_Replenish_View/', Cost_Controller_Replenish_View.as_view(), name='Cost_Controller_Replenish_View'),
        path('api/Fund_Custodian_Pie_Chart/',  Fund_Custodian_Pie_Chart.as_view(), name='Fund_Custodian_Pie_Chart'),
        path('api/Fund_Manager_Reports_View/',  Fund_Manager_Reports_View.as_view(), name='Fund_Manager_Reports_View'),
        path('api/Fund_Manager_Daily_Reports_View/',  Fund_Manager_Daily_Reports_View.as_view(), name='Fund_Manager_Daily_Reports_View'), 



        #Encoder List
        path('api/PurchaseRequest_Decline_List_View/',  PurchaseRequest_Decline_List_View.as_view(), name='PurchaseRequest_Decline_List_View'),
        #Encoder Approved List
        path('api/PurchaseRequest_Approved_List_View/',  PurchaseRequest_Approved_List_View.as_view(), name='PurchaseRequest_Approved_List_View'),
        #Encoder Liquidated List
        path('api/Encoder_Liquidated_List_View/',  Encoder_Liquidated_List_View.as_view(), name='Encoder_Liquidated_List_View'),

        path('api/replenish_function/<int:pk>/', replenish_function , name='replenish_function'),
        #excess or refund
        path('api/excess_or_refund_function/<int:pk>/', excess_or_refund_function , name='excess_or_refund_function'),

        #Cost Controller/General Manager 
       path('api/decline_return_fund_function/<int:pk>/',  decline_return_fund_function, name='decline_return_fund_function'),

#Fund
        path('api/FundListView/', FundListView.as_view(), name='FundListView'),
        path('api/Fund_Comapny_View/', Fund_Comapny_View.as_view(), name='Fund_Comapny_View'),

#Allocation
        path('api/AllocationListView/', AllocationListView.as_view(), name='AllocationListView'),
        path('api/create_fund_allocation/', create_fund_allocation, name='create_fund_allocation'),
        path('api/Allocation_List_Per_BU_View/', Allocation_List_Per_BU_View.as_view(), name='Allocation_List_Per_BU_View'),
        path('api/Allocation_Log_Per_BU_View/', Allocation_Log_Per_BU_View.as_view(), name='Allocation_Log_Per_BU_View'),
        path('api/edit_fund_allocation/<int:fund_allocation_id>/', edit_fund_allocation, name='edit_fund_allocation'),

#admin
        path('api/admin_released/',  admin_released, name='admin_released'),
        path('api/admin_liquidated/',  admin_liquidated, name='admin_liquidated'),
    
]

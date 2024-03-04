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
from user.views import LoginAPIView,current_user
from forms.views import create_request_form,LatestVoucherView, PurchaseRequestListView,PurchaseRequest_Reviewer_List_View, PurchaseRequest_GeneralManager_List_View, Cost_Controller_Release_View,Cost_Controller_To_Be_Release_View,Cost_Controller_Liquidated_View,edit_request_form,refund_function,excess_function,replenish_function
from fund.views import FundListView,Fund_Comapny_View
from allocation.views import create_fund_allocation, AllocationListView,Allocation_List_Per_BU_View, edit_fund_allocation
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

        #Purchase Request
        path('api/create_request_form/', create_request_form, name='create_request_form'),
         path('api/edit_request_form/<int:purchase_request_id>/', edit_request_form, name='edit_request_form'),
        path('api/latest_voucher/', LatestVoucherView.as_view(), name='latest_voucher'),
        path('api/PurchaseRequestListView/', PurchaseRequestListView.as_view(), name='PurchaseRequestListView'),
        path('api/PurchaseRequest_Reviewer_List_View/', PurchaseRequest_Reviewer_List_View.as_view(), name='PurchaseRequest_Reviewer_List_View'),
        path('api/PurchaseRequest_GeneralManager_List_View/', PurchaseRequest_GeneralManager_List_View.as_view(), name='PurchaseRequest_GeneralManager_List_View'),
        path('api/Cost_Controller_Release_View/', Cost_Controller_Release_View.as_view(), name='Cost_Controller_Release_View'),
        path('api/Cost_Controller_To_Be_Release_View/', Cost_Controller_To_Be_Release_View.as_view(), name='Cost_Controller_To_Be_Release_View'),
        path('api/Cost_Controller_Liquidated_View/', Cost_Controller_Liquidated_View.as_view(), name='Cost_Controller_Liquidated_View'),

        path('api/refund_function/', refund_function , name='refund_function'),
        path('api/excess_function/', excess_function , name='excess_function'),
        path('api/replenish_function/<int:pk>/', replenish_function , name='replenish_function'),

        #Fund
        path('api/FundListView/', FundListView.as_view(), name='FundListView'),
        path('api/Fund_Comapny_View/', Fund_Comapny_View.as_view(), name='Fund_Comapny_View'),

        #Allocation
        path('api/AllocationListView/', AllocationListView.as_view(), name='AllocationListView'),
        path('api/create_fund_allocation/', create_fund_allocation, name='create_fund_allocation'),
        path('api/Allocation_List_Per_BU_View/', Allocation_List_Per_BU_View.as_view(), name='Allocation_List_Per_BU_View'),
        path('api/edit_fund_allocation/<int:fund_allocation_id>/', edit_fund_allocation, name='edit_fund_allocation'),

        
    
]
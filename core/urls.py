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
from forms.views import LatestVoucherView
from fund.views import FundListView,Fund_Comapny_View
from allocation.views import create_fund_allocation, AllocationListView,Allocation_List_Per_BU_View
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
        path('api/latest_voucher/', LatestVoucherView.as_view(), name='latest_voucher'),

        #Fund
        path('api/FundListView/', FundListView.as_view(), name='FundListView'),
        path('api/Fund_Comapny_View/', Fund_Comapny_View.as_view(), name='Fund_Comapny_View'),

        #Allocation
        path('api/AllocationListView/', AllocationListView.as_view(), name='AllocationListView'),
        path('api/create_fund_allocation/', create_fund_allocation, name='create_fund_allocation'),
        path('api/Allocation_List_Per_BU_View/', Allocation_List_Per_BU_View.as_view(), name='Allocation_List_Per_BU_View'),

        
    
]
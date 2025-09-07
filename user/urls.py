from django.urls import path,include
from . import views
from .views_auth import (
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    CookieLogoutView,
)
from rest_framework_simplejwt import views as jwt_views
from .views import *

urlpatterns = [
    path('api/',include([
        path('User_view/', User_view.as_view({
            'get': 'list',
            'post': 'create',
        })),
        path('User_view/<int:pk>/', User_view.as_view({
            'put': 'update',
            'delete': 'destroy',
        })),
    ])),

    #Session Based 
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/custodian_users/', custodian_users, name='custodian_users'),
    path('api/check_business_unit_based_on_email/', check_business_unit_based_on_email, name='check_business_unit_based_on_email'),
    path('logout/', logout_view, name='logout'),
    
    #JWT
    path("api/auth/login/",   CookieTokenObtainPairView.as_view(), name="jwt_login"),
    path("api/auth/refresh/", CookieTokenRefreshView.as_view(),    name="jwt_refresh"),
    path("api/auth/logout/",  CookieLogoutView.as_view(),          name="jwt_logout"),
    path("api/auth/me/",      current_user,                        name="jwt_me"),
    
    path('api/token/',
         jwt_views.TokenObtainPairView.as_view(),
         name ='token_obtain_pair'),
    path('api/token/refresh/',
         jwt_views.TokenRefreshView.as_view(),
         name ='token_refresh'),

]

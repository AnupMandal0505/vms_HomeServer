# src/urls.py
app_name="frontent"
from django.contrib import admin
from django.urls import path

from frontent.views import index,AuthView,LogoutView,Dashboard,GmAddUser,PaAddUser,GmList,PaList,UpdateUser,Passkey,SECRETARYAddUser,SECRETARYList
# from demo.views import index1

urlpatterns = [
    path('',index, name='index_urls'),
    path('auth',AuthView.as_view(), name='auth_urls'),
    path('logout', LogoutView.as_view(), name='logout_urls'),  # Logout URL
    path('dashboard',Dashboard.as_view(), name='dashboard_urls'),
    path('api/passkey', Passkey.as_view(), name='passkey_urls'),


    # General Manager.......................................
    path('add_gm_user',GmAddUser.as_view(), name='add_gm_user_urls'),
    path('user_gm_list',GmList.as_view(), name='user_gm_list_urls'),
    path('update_gm_user',UpdateUser.as_view(), name='update_user_urls'),

    
    # Secretary.......................................
    path('add_secretary_user',SECRETARYAddUser.as_view(), name='add_secretary_user_urls'),
    path('user_secretary_list',SECRETARYList.as_view(), name='user_secretary_list_urls'),
    path('update_secretary_user',UpdateUser.as_view(), name='update_user_urls'),

    # Personal Assistent.......................................
    path('add_pa_user',PaAddUser.as_view(), name='add_pa_user_urls'),
    path('user_pa_list',PaList.as_view(), name='user_pa_list_urls'),
    path('update_pa_user',UpdateUser.as_view(), name='update_pa_user_urls'),
]
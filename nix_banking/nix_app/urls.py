from . import views
from django.urls import path

urlpatterns = [
    path('api/v1/user/new', views.create_user, name='create_user'),
    path('api/v1/user/all', views.get_all_users, name='get_all_users'),
    path('api/v1/user/<int:user_id>/', views.get_delete_update_user, name='get_delete_update_user'),
    path('api/v1/transfer/new', views.create_transfer, name='create_transfer'),
    path('api/v1/transfer/all', views.get_all_transfers, name='get_all_transfers'),
    path('api/v1/transfer/<int:transfer_id>/', views.get_delete_update_transfer, name='get_delete_update_transfer'),
    path('api/v1/transfer/filter/<str:filter_type>/<str:filter>/', views.filter_transfers, name='filter_transfers'),
    path('api/v1/transfer/total', views.get_transfer_total, name='get_transfer_total'),
]

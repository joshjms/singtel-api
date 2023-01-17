from django.urls import path

from . import views

urlpatterns = [
    path('sales/', views.sale_list),
    path('sales/create/', views.sale_create),

    path('device/', views.device_list),
    path('device/train/', views.device_train),
    path('device/sales/', views.device_detail),

    path('prediction/run/', views.run_prediction_model),

    path('transactions/', views.transaction_list),
]